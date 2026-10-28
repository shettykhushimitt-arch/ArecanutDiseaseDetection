"""EigenCAM visualisation for the trained YOLOv8 disease detector.

This module performs PCA/SVD on the final convolutional feature activations.
Unlike the previous bounding-box overlay, the resulting map represents the
image regions that are most prominent in the model's learned feature space.
"""

from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as functional
from PIL import Image


MODEL_IMAGE_SIZE = 640


def _eigen_projection(activation):
    """Project a feature tensor onto its first principal component."""
    if activation.ndim != 4:
        raise ValueError("EigenCAM requires a 4D convolutional activation tensor.")

    # Convert [batch, channels, height, width] to [height * width, channels].
    feature_map = activation[0]
    channels, height, width = feature_map.shape
    feature_matrix = feature_map.permute(1, 2, 0).reshape(height * width, channels)
    feature_matrix = feature_matrix - feature_matrix.mean(dim=0, keepdim=True)

    # EigenCAM uses the first PCA direction of the activation matrix. SVD gives
    # the same principal component without computing a full covariance matrix.
    left_singular_vectors, _, _ = torch.linalg.svd(feature_matrix, full_matrices=False)
    return left_singular_vectors[:, 0].reshape(height, width)


def _normalise(cam):
    cam = cam - cam.min()
    maximum = cam.max()
    if maximum > 0:
        cam = cam / maximum
    return cam


def _jet_colormap(cam):
    """Create a JET-like RGB colour map with NumPy, without OpenCV."""
    red = np.clip(1.5 - np.abs(4.0 * cam - 3.0), 0.0, 1.0)
    green = np.clip(1.5 - np.abs(4.0 * cam - 2.0), 0.0, 1.0)
    blue = np.clip(1.5 - np.abs(4.0 * cam - 1.0), 0.0, 1.0)
    return np.stack((red, green, blue), axis=-1)


def generate_eigen_cam(image_path, detection_model, save_path):
    """Generate and save an EigenCAM overlay for one uploaded plant image.

    Args:
        image_path: Path to the original user-uploaded image.
        detection_model: The underlying PyTorch YOLOv8 detection model.
        save_path: Destination path for the EigenCAM image.
    """
    original_image = Image.open(image_path).convert("RGB")
    original_array = np.asarray(original_image, dtype=np.float32) / 255.0
    original_height, original_width = original_array.shape[:2]

    resized_image = original_image.resize(
        (MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE),
        Image.Resampling.BILINEAR,
    )
    input_array = np.asarray(resized_image, dtype=np.float32) / 255.0
    input_tensor = torch.from_numpy(input_array).permute(2, 0, 1).unsqueeze(0)

    try:
        parameter = next(detection_model.parameters())
        device = parameter.device
        dtype = parameter.dtype
    except StopIteration:
        device = torch.device("cpu")
        dtype = torch.float32

    input_tensor = input_tensor.to(device=device, dtype=dtype)
    target_layer = detection_model.model[-2]
    activations = []

    def save_activation(_, __, output):
        if isinstance(output, (tuple, list)):
            output = output[0]
        activations.append(output.detach())

    hook = target_layer.register_forward_hook(save_activation)
    was_training = detection_model.training

    try:
        detection_model.eval()
        with torch.inference_mode():
            detection_model(input_tensor)
    finally:
        hook.remove()
        detection_model.train(was_training)

    if not activations:
        raise RuntimeError("Unable to capture YOLOv8 feature activations for EigenCAM.")

    cam = _eigen_projection(activations[-1])
    cam = functional.interpolate(
        cam.unsqueeze(0).unsqueeze(0),
        size=(original_height, original_width),
        mode="bilinear",
        align_corners=False,
    )[0, 0]
    cam_array = _normalise(cam).detach().float().cpu().numpy()

    heatmap_array = _jet_colormap(cam_array)
    overlay = (0.60 * original_array) + (0.40 * heatmap_array)
    overlay = np.clip(overlay * 255.0, 0, 255).astype(np.uint8)

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(overlay).save(save_path)
    return save_path
