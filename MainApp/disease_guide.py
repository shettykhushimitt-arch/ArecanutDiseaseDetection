"""Reliable care guidance for every class produced by the detection model."""

DISEASE_GUIDE = {
    'No_Detection': {
        'symptoms': 'No supported healthy or disease condition was detected with sufficient confidence.',
        'causes': 'The image may be blurred, too dark, too distant, obstructed, or may show a condition not included in the trained classes.',
        'prevention': 'Take a close, well-lit photograph of one leaf, nut, bud, trunk, or stem-base area. Keep the target in focus and avoid people or busy backgrounds.',
        'treatment': 'Upload a clearer image. If visible symptoms persist, consult a local agricultural officer or crop specialist.',
    },
    'Healthy_Leaf': {
        'symptoms': 'Fresh green leaves with normal appearance. No yellowing or spots.',
        'causes': 'The palm is healthy and receiving suitable nutrition and care.',
        'prevention': 'Maintain balanced fertilisation, irrigation, field hygiene and regular monitoring.',
        'treatment': 'No treatment is required. Continue good agricultural practices.',
    },
    'Healthy_Foot': {
        'symptoms': 'A healthy stem base without cracks, rot or signs of infection.',
        'causes': 'The palm is healthy.',
        'prevention': 'Maintain proper drainage and keep the plantation clean.',
        'treatment': 'No treatment is required.',
    },
    'Healthy_Nut': {
        'symptoms': 'Healthy green nuts with no holes, rot or discolouration.',
        'causes': 'The crop is growing normally.',
        'prevention': 'Continue regular nutrient management and pest monitoring.',
        'treatment': 'No treatment is required.',
    },
    'Healthy_Trunk': {
        'symptoms': 'A smooth trunk without bleeding, cracking or damaged bark.',
        'causes': 'The palm is healthy.',
        'prevention': 'Provide proper irrigation and avoid mechanical injuries to the trunk.',
        'treatment': 'No treatment is required.',
    },
    'Bud_Borer': {
        'symptoms': 'Holes in spindle leaves, damaged buds, a drying central shoot and reduced growth.',
        'causes': 'Bud borer larvae feeding inside the developing bud and spindle leaves.',
        'prevention': 'Inspect palms regularly, remove affected shoots and keep the field clean.',
        'treatment': 'Seek local agricultural advice on the recommended insecticide and remove heavily infested plant parts.',
    },
    'Mahali_Koleroga': {
        'symptoms': 'Black lesions, fruit rot, flower drop and rapid infection in wet weather.',
        'causes': 'Fungal infection caused by Phytophthora arecae, commonly encouraged by persistent rain and poor drainage.',
        'prevention': 'Improve drainage, reduce excess moisture and promptly remove infected nuts or flower parts.',
        'treatment': 'Apply an approved fungicide or Bordeaux mixture before and during the monsoon as advised locally.',
    },
    'Stem_Bleeding': {
        'symptoms': 'Dark brown fluid oozing from the trunk, bark cracking and a weakened stem.',
        'causes': 'A fungal infection, often worsened by trunk injuries and waterlogged conditions.',
        'prevention': 'Avoid trunk injuries, improve drainage and inspect the plantation regularly.',
        'treatment': 'Remove the infected bark carefully and apply an appropriate fungicidal paste as recommended by an agricultural officer.',
    },
    'Stem_Cracking': {
        'symptoms': 'Long cracks in the stem, dry bark and a weak-looking trunk.',
        'causes': 'Environmental stress, nutrient deficiency, uneven irrigation or physical injury.',
        'prevention': 'Maintain balanced fertilisation, consistent irrigation and protect trunks from mechanical damage.',
        'treatment': 'Improve soil nutrition and irrigation management, then monitor the plant’s recovery.',
    },
    'Yellow_Leaf_Disease': {
        'symptoms': 'Yellowing leaves, reduced leaf size, slow growth, drying foliage and reduced yield.',
        'causes': 'Phytoplasma infection, sometimes compounded by nutrient imbalance and poor soil health.',
        'prevention': 'Use healthy seedlings, maintain nutrition and remove severely affected palms where advised.',
        'treatment': 'There is no complete cure for severe cases. Improve nutrient management and consult an agricultural officer for local control measures.',
    },
}


def get_disease_guidance(disease_name):
    """Return a safe fallback if the model returns an unknown class name."""
    return DISEASE_GUIDE.get(disease_name, {
        'symptoms': 'The image contains a condition that needs closer inspection.',
        'causes': 'The precise cause could not be confirmed from this image alone.',
        'prevention': 'Keep the area clean, improve drainage and monitor the palm closely.',
        'treatment': 'Consult a local agricultural officer or crop specialist for a field assessment.',
    })
