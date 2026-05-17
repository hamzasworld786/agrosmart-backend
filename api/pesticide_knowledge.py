# Pesticide Knowledge Base

PESTICIDE_KNOWLEDGE = {
    # Rice/Paddy crops
    ("rice", "blast"): {
        "pesticide": "Tricyclazole 75% WP",
        "dosage": "0.6g per liter water",
        "method": "Foliar spray",
        "frequency": "Every 10-14 days"
    },
    ("rice", "brown spot"): {
        "pesticide": "Mancozeb 75% WP",
        "dosage": "2g per liter water",
        "method": "Foliar spray",
        "frequency": "Every 7-10 days"
    },
    ("rice", "stem borer"): {
        "pesticide": "Chlorantraniliprole 18.5% SC",
        "dosage": "0.4ml per liter water",
        "method": "Foliar spray",
        "frequency": "At tillering and flowering stage"
    },
    ("rice", "leaf folder"): {
        "pesticide": "Cartap Hydrochloride 50% SP",
        "dosage": "1g per liter water",
        "method": "Foliar spray",
        "frequency": "When infestation is observed"
    },
    
    # Wheat crops
    ("wheat", "rust"): {
        "pesticide": "Tebuconazole 25.9% EC",
        "dosage": "1ml per liter water",
        "method": "Foliar spray",
        "frequency": "Every 10-15 days"
    },
    ("wheat", "powdery mildew"): {
        "pesticide": "Sulfur 80% WP",
        "dosage": "2g per liter water",
        "method": "Foliar spray",
        "frequency": "Every 7-10 days"
    },
    ("wheat", "aphids"): {
        "pesticide": "Imidacloprid 17.8% SL",
        "dosage": "0.5ml per liter water",
        "method": "Foliar spray",
        "frequency": "When colonies appear"
    },
    
    # Maize/Corn crops
    ("maize", "fall armyworm"): {
        "pesticide": "Emamectin Benzoate 5% SG",
        "dosage": "0.4g per liter water",
        "method": "Foliar spray",
        "frequency": "Early morning or evening"
    },
    ("maize", "stalk borer"): {
        "pesticide": "Quinalphos 25% EC",
        "dosage": "2ml per liter water",
        "method": "Foliar spray",
        "frequency": "At vegetative stage"
    },
    
    # Cotton crops
    ("cotton", "bollworm"): {
        "pesticide": "Spinosad 45% SC",
        "dosage": "0.5ml per liter water",
        "method": "Foliar spray",
        "frequency": "Weekly during flowering"
    },
    ("cotton", "whitefly"): {
        "pesticide": "Diafenthiuron 50% WP",
        "dosage": "1g per liter water",
        "method": "Foliar spray",
        "frequency": "Cover lower leaf surfaces"
    },
    
    # Vegetable crops
    ("vegetable", "downy mildew"): {
        "pesticide": "Metalaxyl + Mancozeb 72% WP",
        "dosage": "2g per liter water",
        "method": "Foliar spray",
        "frequency": "Preventive or at first sign"
    },
    ("vegetable", "fruit borer"): {
        "pesticide": "Cypermethrin 10% EC",
        "dosage": "1.5ml per liter water",
        "method": "Foliar spray",
        "frequency": "When fruiting begins"
    },
    ("vegetable", "leaf miner"): {
        "pesticide": "Cyromazine 75% WP",
        "dosage": "0.5g per liter water",
        "method": "Foliar spray",
        "frequency": "Repeat after 7 days"
    }
}

# Keywords for matching problem descriptions
PROBLEM_KEYWORDS = {
    "blast": "blast",
    "brown spot": "brown spot",
    "stem borer": "stem borer",
    "borer": "stem borer",
    "leaf folder": "leaf folder",
    "rust": "rust",
    "mildew": "powdery mildew",
    "armyworm": "fall armyworm",
    "bollworm": "bollworm",
    "whitefly": "whitefly",
    "aphid": "aphids",
    "leaf miner": "leaf miner",
    "fruit borer": "fruit borer"
}

def find_pesticide(crop_name, problem_description):
    """
    Find pesticide recommendation based on crop and problem
    """
    crop_name = crop_name.lower().strip()
    problem_desc = problem_description.lower().strip()
    
    # Try to match problem using keywords
    matched_problem = None
    for keyword, problem_key in PROBLEM_KEYWORDS.items():
        if keyword in problem_desc:
            matched_problem = problem_key
            break
    
    # If no keyword match, use the first few words of the problem
    if matched_problem is None:
        words = problem_desc.split()[:3]
        matched_problem = " ".join(words)
    
    # Look for exact crop + problem match
    for (crop, problem), solution in PESTICIDE_KNOWLEDGE.items():
        if crop == crop_name and problem == matched_problem:
            return solution
    
    # Try generic crop types
    if crop_name in ["tomato", "potato", "brinjal", "chili", "onion", "garlic"]:
        crop_name = "vegetable"
        
    for (crop, problem), solution in PESTICIDE_KNOWLEDGE.items():
        if crop == crop_name and problem == matched_problem:
            return solution
    
    # Default recommendation
    return {
        "pesticide": "Neem Oil (Organic)",
        "dosage": "5ml per liter water",
        "method": "Foliar spray (cover all plant parts)",
        "frequency": "Every 7 days until problem resolves",
        "note": "For specific diagnosis, consult local agricultural extension officer"
    }