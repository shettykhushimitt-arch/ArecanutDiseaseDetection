"""
Centralized disease knowledge base and normalization layer for ArecaCare.
Provides symptoms, likely causes, prevention measures, and targeted treatment
information for all supported arecanut conditions.
"""

DISEASE_INFO = {
    "Bud Borer": {
        "symptoms": [
            "Small bore holes on spindle leaves and inner bud core.",
            "Chewed fibrous frass, feeding marks, and decayed patches around affected buds.",
            "Drying, withering, and rotting of the central shoot / spindle.",
            "Stunted palm crown development and damage to developing inflorescence.",
        ],
        "cause": [
            "Larval infestation by bud borer insects feeding inside the tender bud and spindle leaves.",
            "Dense palm crowns and prolonged high humidity favoring pest multiplication.",
            "Unsanitary field conditions allowing borer larvae to pupate and spread.",
            "Delayed detection during early shoot emergence.",
        ],
        "prevention": [
            "Inspect spindle leaves and unopened buds regularly for early signs of borer holes or frass.",
            "Promptly cut and safely dispose of or destroy heavily infested spindle shoots.",
            "Maintain plantation hygiene and remove decaying or dried crown matter.",
            "Encourage natural insect predators and monitor closely during seasonal pest peaks.",
        ],
        "treatment": {
            "problem": "Bud Borer",
            "what_to_apply": "Indoxacarb 14.5 SC",
            "dose": "0.75 ml/L water",
            "how_to_apply": (
                "Spray on tender foliage/inflorescence when eggs or early infestation appears. "
                "Collection/removal of mature larvae also helps."
            ),
        },
    },

    "Mahali / Koleroga": {
        "symptoms": [
            "Water-soaked dark lesions appearing at the base of green nuts.",
            "Heavy premature shedding and rotting of immature nuts (fruit drop).",
            "Blackened patches and rot spreading along bunches, fruit stalks, and inflorescence.",
            "White felty fungal growth visible on fallen infected nuts under wet conditions.",
        ],
        "cause": [
            "Fungal infection caused by Phytophthora arecae (or Phytophthora meadii).",
            "Continuous heavy monsoon rains coupled with persistent high relative humidity.",
            "Poor crown aeration, lack of sunlight penetration, and water stagnation in the plantation.",
            "Rain splash transmitting fungal spores from infected ground debris to upper bunches.",
        ],
        "prevention": [
            "Collect and burn or deeply bury all fallen, rotting nuts to eliminate spore reservoirs.",
            "Cover bunches with polythene covers or protective bags prior to monsoon onset where feasible.",
            "Ensure proper plantation drainage to prevent waterlogging around palm roots.",
            "Thin out dense canopies to improve aeration and sunlight throughout the plantation.",
        ],
        "treatment": {
            "problem": "Mahali / Koleroga",
            "what_to_apply": "1% Bordeaux mixture",
            "dose": "Approximately 10 g/L water",
            "how_to_apply": (
                "Spray thoroughly on bunches. First spray before or at the beginning of the monsoon. "
                "Repeat after 40–45 days. A third spray may be required if monsoon conditions continue."
            ),
        },
    },

    "Stem Bleeding": {
        "symptoms": [
            "Dark reddish-brown or black gummy liquid oozing from cracks on the trunk.",
            "Discoloration and rotting of internal fibrous stem tissue beneath the bark.",
            "Gradual yellowing and reduction in crown leaf size as the trunk weakens.",
            "Development of hollow internal cavities along the stem in advanced stages.",
        ],
        "cause": [
            "Fungal infection primarily caused by Thielaviopsis paradoxa (Ceratocystis paradoxa).",
            "Physical or mechanical bark wounds caused by tools, harvesting poles, or sun scorching.",
            "Waterlogged soil, fluctuating high water table, or severely unbalanced nutrition.",
            "Spread through infected plant sap or unsterilized agricultural tools.",
        ],
        "prevention": [
            "Avoid mechanical or tool injury to the trunk during intercultural and harvesting operations.",
            "Protect young and exposed trunks from direct afternoon sun scorch using whitewash or intercropping.",
            "Provide effective drainage channels to avoid water stagnation around palm bases.",
            "Disinfect pruning, cutting, and scraping tools between palms.",
            "Maintain balanced palm nutrition based on soil test results.",
        ],
        "treatment": {
            "problem": "Stem Bleeding",
            "what_to_apply": "Hexaconazole 5 EC",
            "dose": "1 ml/L water",
            "how_to_apply": (
                "Scrape/remove diseased tissue first and treat the affected wound appropriately. "
                "Bordeaux paste may be used as recommended for wound treatment. "
                "Soil drenching may also be used according to the product label/local agricultural recommendation."
            ),
        },
    },

    "Stem Cracking": {
        "symptoms": [
            "Long cracks on the stem.",
            "Dry or damaged bark.",
            "Weak trunk/stem.",
            "Cracks may become more visible under environmental stress.",
        ],
        "cause": [
            "Environmental stress.",
            "Nutrient deficiency.",
            "Physical/mechanical injury.",
            "Irrigation/moisture stress can contribute.",
        ],
        "prevention": [
            "Apply balanced fertilizers.",
            "Maintain proper irrigation.",
            "Avoid mechanical damage to the stem.",
            "Maintain proper soil moisture and drainage.",
            "Monitor the palm regularly.",
        ],
        "treatment": {
            "problem": "Stem Cracking",
            "what_to_apply": "Do not automatically spray pesticide",
            "dose": "—",
            "how_to_apply": (
                "Stem cracking can be associated with environmental stress, physical injury, "
                "nutrient problems, or stem bleeding. If brown/red gummy liquid is coming from the crack, "
                "treat it as a possible stem-bleeding symptom and follow the appropriate stem-bleeding treatment."
            ),
        },
    },

    "Yellow Leaf Disease (YLD)": {
        "symptoms": [
            "Characteristic bright yellowing of leaves starting from inner whorls and margins.",
            "Gradual reduction in leaf size, leading to a stunted crown (bunchy top appearance).",
            "Black necrosis on leaf tips and premature drying of fronds.",
            "Kernel darkening, softening, and premature dropping of nuts.",
        ],
        "cause": [
            "Phytoplasma pathogen transmitted by sap-sucking insect vectors (plant hoppers / leaf hoppers).",
            "Root decay and impaired vascular nutrient transportation.",
            "Exacerbated by poor drainage, acidic soil conditions, and micronutrient imbalances.",
        ],
        "prevention": [
            "Source planting seedlings exclusively from certified disease-free nurseries.",
            "Manage insect vector populations through recommended agronomic practices.",
            "Provide proper drainage channels to prevent water stagnation in root zones.",
            "Maintain optimal soil health with balanced fertilization and regular soil testing.",
        ],
        "treatment": {
            "problem": "Yellow Leaf Disease (YLD)",
            "what_to_apply": "No curative pesticide/fungicide for the phytoplasma itself",
            "dose": "—",
            "how_to_apply": (
                "Focus on improving nutrition, soil condition and drainage.\n\n"
                "Recommended nutrition:\n"
                "220 g urea + 200 g superphosphate + 230 g MOP per palm per year in two split doses.\n\n"
                "For affected gardens:\n"
                "1 kg superphosphate per palm.\n\n"
                "Organic matter:\n"
                "12 kg compost + 12 kg green leaves per palm per year."
            ),
        },
    },

    "Healthy Palm": {
        "symptoms": [
            "Fresh, vibrant green leaves with no chlorosis, spots, or yellowing.",
            "Smooth, solid trunk free of cracks, dark bleeding, or fungal lesions.",
            "Healthy green nut bunches with normal fruit setting.",
            "Vigorous overall crown growth and robust canopy.",
        ],
        "cause": [
            "The palm is receiving optimal nutrition, consistent irrigation, and good grove management.",
            "No active pest infestation or fungal disease present.",
        ],
        "prevention": [
            "Continue scheduled balanced organic and mineral fertilization.",
            "Maintain steady irrigation intervals throughout dry periods.",
            "Maintain field hygiene and regular plant health inspections.",
        ],
        "treatment": {
            "problem": "Healthy Palm",
            "what_to_apply": "No chemical treatment required",
            "dose": "—",
            "how_to_apply": (
                "Continue balanced fertilization, proper irrigation, regular mulching, "
                "and routine plantation care to maintain palm vigor."
            ),
        },
    },

    "No Detection": {
        "symptoms": [
            "No definitive plant disease symptoms detected in this image.",
            "The visual cues in the scan did not match any trained disease patterns.",
        ],
        "cause": [
            "The image may be blurred, dimly lit, taken from too far, or obstructed.",
            "The target area may not show recognizable disease characteristics.",
        ],
        "prevention": [
            "Take a close, well-lit photograph in bright daylight.",
            "Focus directly on a single leaf, nut bunch, or stem area.",
            "Ensure the camera is steady and the subject is clearly in focus.",
        ],
        "treatment": {
            "problem": "Unidentified Condition",
            "what_to_apply": "Upload a clearer photograph",
            "dose": "—",
            "how_to_apply": (
                "Retake a clear, high-resolution photo of the specific affected palm area "
                "and run a new scan. If visible distress continues, consult a local agricultural officer."
            ),
        },
    },
}


def normalize_disease_name(raw_name: str) -> str:
    """
    Robust normalization mapping layer.
    Maps various raw labels produced by the YOLO model (such as 'bud_borer',
    'mahali_koleroga', 'stem_bleeding', 'stem_cracking', 'yellow_leaf_disease',
    'YLD', 'Healthy_Leaf', etc.) into one of the canonical disease keys:
      1. Bud Borer
      2. Mahali / Koleroga
      3. Stem Bleeding
      4. Stem Cracking
      5. Yellow Leaf Disease (YLD)
      6. Healthy Palm
      7. No Detection
    """
    if not raw_name:
        return "No Detection"

    clean = str(raw_name).strip()
    lowered = clean.lower().replace("-", " ").replace("_", " ").replace("/", " ")
    tokens = set(lowered.split())

    # 1. Bud Borer
    if "borer" in tokens or "bud borer" in lowered:
        return "Bud Borer"

    # 2. Mahali / Koleroga
    if "mahali" in tokens or "koleroga" in tokens or "fruit rot" in lowered:
        return "Mahali / Koleroga"

    # 3. Stem Bleeding
    if "bleeding" in tokens or "stem bleeding" in lowered:
        return "Stem Bleeding"

    # 4. Stem Cracking
    if "cracking" in tokens or "stem cracking" in lowered:
        return "Stem Cracking"

    # 5. Yellow Leaf Disease (YLD)
    if "yld" in tokens or ("yellow" in tokens and "leaf" in tokens):
        return "Yellow Leaf Disease (YLD)"

    # Healthy categories
    if "healthy" in tokens:
        return "Healthy Palm"

    # No detection categories
    if "no detection" in lowered or ("no" in tokens and "detection" in tokens):
        return "No Detection"

    # Direct case-insensitive match against canonical dictionary
    for canonical in DISEASE_INFO.keys():
        can_norm = canonical.lower().replace("-", " ").replace("_", " ").replace("/", " ")
        if lowered == can_norm:
            return canonical

    # If unrecognized, format cleanly as title case
    return clean.replace("_", " ").title()


def get_disease_info(raw_name: str) -> dict:
    """
    Retrieve centralized disease information for any raw or normalized disease name.
    Always returns a dictionary with 'canonical_name', 'symptoms', 'cause',
    'prevention', and 'treatment'.
    """
    canonical = normalize_disease_name(raw_name)

    if canonical in DISEASE_INFO:
        info = dict(DISEASE_INFO[canonical])
        info["canonical_name"] = canonical
        return info

    # Graceful fallback for unexpected classes
    return {
        "canonical_name": canonical,
        "symptoms": [
            "Detailed symptoms are being updated for this condition.",
            "Inspect the palm closely for abnormalities, discoloration, or lesions.",
        ],
        "cause": [
            "Environmental factors, localized injury, or an unclassified pathogen.",
        ],
        "prevention": [
            "Maintain good agricultural practices, balanced fertilization, and grove sanitation.",
            "Monitor the palm regularly and isolate affected sections.",
        ],
        "treatment": {
            "problem": canonical,
            "what_to_apply": "Consult a local agricultural extension officer",
            "dose": "As advised by crop specialist",
            "how_to_apply": (
                "Collect an affected sample and consult your local agricultural office "
                "or plantation extension service for precise field diagnosis."
            ),
        },
    }
