document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.querySelector('.site-nav');
  if (toggle && nav) toggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });
  const input = document.querySelector('#image-upload');
  const preview = document.querySelector('#image-preview');
  const zone = document.querySelector('.drop-zone');
  if (input && preview && zone) input.addEventListener('change', () => {
    const file = input.files && input.files[0];
    if (!file) return;
    preview.src = URL.createObjectURL(file); preview.hidden = false; zone.classList.add('has-preview');
  });

  const liveForm = document.querySelector('#live-scan-form');
  if (!liveForm) return;

  const video = document.querySelector('#live-video');
  const canvas = document.querySelector('#live-canvas');
  const annotation = document.querySelector('#live-annotation');
  const placeholder = document.querySelector('#camera-placeholder');
  const startButton = document.querySelector('#start-camera');
  const stopButton = document.querySelector('#stop-camera');
  const status = document.querySelector('#live-status');
  const emptyState = document.querySelector('#live-empty');
  const resultPanel = document.querySelector('#live-result');
  let stream = null;
  let timer = null;
  let requestInProgress = false;

  const setStatus = (message, active = false) => {
    status.textContent = message;
    status.parentElement.classList.toggle('active', active);
  };

  const showResult = (data) => {
    emptyState.hidden = true;
    resultPanel.hidden = false;
    annotation.src = `data:image/jpeg;base64,${data.annotated_image}`;
    annotation.hidden = false;
    video.hidden = true;
    document.querySelector('#live-icon').textContent = data.is_healthy ? 'OK' : '!';
    document.querySelector('#live-disease').textContent = data.disease_display;
    document.querySelector('#live-confidence').textContent = data.confidence === null ? '--' : `${Number(data.confidence).toFixed(1)}%`;
    document.querySelector('#live-symptoms').textContent = data.guidance.symptoms;
    document.querySelector('#live-causes').textContent = data.guidance.causes;
    document.querySelector('#live-care-title').textContent = data.is_no_detection ? 'Next step' : (data.is_healthy ? 'Ongoing care' : 'Prevention');
    document.querySelector('#live-prevention').textContent = data.guidance.prevention;
    document.querySelector('#live-treatment').textContent = data.guidance.treatment;
  };

  const analyzeFrame = async () => {
    if (!stream || requestInProgress || video.readyState < HTMLMediaElement.HAVE_CURRENT_DATA) return;
    requestInProgress = true;
    setStatus('Analyzing latest frame', true);
    const maxWidth = 640;
    const scale = Math.min(1, maxWidth / video.videoWidth);
    canvas.width = Math.max(1, Math.round(video.videoWidth * scale));
    canvas.height = Math.max(1, Math.round(video.videoHeight * scale));
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

    try {
      const blob = await new Promise((resolve) => canvas.toBlob(resolve, 'image/jpeg', 0.85));
      if (!blob) throw new Error('Could not capture a camera frame.');
      const data = new FormData();
      data.append('image', blob, 'live-frame.jpg');
      const response = await fetch(liveForm.dataset.endpoint, {
        method: 'POST',
        headers: { 'X-CSRFToken': liveForm.querySelector('[name=csrfmiddlewaretoken]').value },
        body: data,
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || 'Live analysis failed.');
      showResult(result);
      setStatus('Camera is analyzing', true);
    } catch (error) {
      setStatus(error.message || 'Live analysis failed');
    } finally {
      requestInProgress = false;
    }
  };

  const startCamera = async () => {
    if (!navigator.mediaDevices?.getUserMedia) {
      setStatus('This browser does not support camera access.');
      return;
    }
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment', width: { ideal: 1280 }, height: { ideal: 720 } }, audio: false });
      video.srcObject = stream;
      video.hidden = false;
      annotation.hidden = true;
      placeholder.hidden = true;
      startButton.disabled = true;
      stopButton.disabled = false;
      setStatus('Camera started', true);
      await video.play();
      analyzeFrame();
      timer = window.setInterval(analyzeFrame, 2000);
    } catch (error) {
      setStatus('Camera permission was not granted.');
    }
  };

  const stopCamera = () => {
    window.clearInterval(timer);
    timer = null;
    if (stream) stream.getTracks().forEach((track) => track.stop());
    stream = null;
    video.srcObject = null;
    video.hidden = true;
    annotation.hidden = true;
    placeholder.hidden = false;
    startButton.disabled = false;
    stopButton.disabled = true;
    setStatus('Camera stopped');
  };

  startButton.addEventListener('click', startCamera);
  stopButton.addEventListener('click', stopCamera);
  window.addEventListener('beforeunload', stopCamera);
});
