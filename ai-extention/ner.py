from transformers import pipeline

_ner_pipeline = None

def get_ner_pipeline():
    """
    Lazily load and return NER pipeline for multilingual location extraction.
    """
    global _ner_pipeline
    if _ner_pipeline is not None:
        return _ner_pipeline
    # Use a lighter multilingual model to avoid OOM on constrained machines
    ner_model_name = "Davlan/bert-base-multilingual-cased-ner-hrl"
    try:
        _ner_pipeline = pipeline("ner", model=ner_model_name, aggregation_strategy="simple")
    except Exception:
        # Return None to allow regex/location keyword fallback downstream
        _ner_pipeline = None
    return _ner_pipeline

def extract_hazard_and_locations(text):
    """
    Extract hazard keywords and locations from a single text.
    Returns dict: {hazards: [..], locations: [..]}
    """
    if not text or not text.strip():
        return {"hazards": [], "locations": []}

    hazard_keywords = [
        'Tsunami', 'High Waves', 'Coastal Flooding', 'Storm Surge', 
        'Rip Current', 'Coastal Erosion', 'Algal Bloom', 
        'Marine Pollution', 'Cyclone', 'flood'
    ]
    detected_hazards = []
    text_lower = text.lower()
    for hazard in hazard_keywords:
        if hazard.lower() in text_lower:
            detected_hazards.append(hazard)

    ner = get_ner_pipeline()
    locations = []
    if ner is not None:
        try:
            ner_results = ner(text)
            locations = [entity['word'] for entity in ner_results if entity.get('entity_group') == 'LOC']
        except Exception:
            locations = []
    # Fallback: simple keyword-based location spotting if NER unavailable
    if not locations:
        location_keywords = [
            "Mumbai","Chennai","Kolkata","Odisha","Kerala","Gujarat","Goa",
            "Andhra Pradesh","West Bengal","Vizag","Visakhapatnam","Puri",
            "Bay of Bengal","Arabian Sea","Tamil Nadu","Maharashtra","Karnataka",
            "Andaman","Nicobar","Lakshadweep","Kochi","Cochin","Mangaluru","Mangalore",
            "Chandipur","Paradip","Digha","Gopalpur"
        ]
        text_lower = text.lower()
        for name in location_keywords:
            if name.lower() in text_lower:
                locations.append(name)

    return {"hazards": detected_hazards, "locations": locations}

# Removed hard-coded demo runner; this module now only provides reusable functions.
    """
    Loads a Named Entity Recognition (NER) model to find locations and then
    searches the text for specific hazard-related keywords.
    """
    # --- 1. Load the NER Model for Location Extraction ---
    # UPDATED: Using the large, high-accuracy model as requested.
    ner_model_name = "Davlan/xlm-roberta-large-ner-hrl"
    print(f"Loading NER model: '{ner_model_name}'...")
    try:
        ner_pipeline = pipeline("ner", model=ner_model_name, aggregation_strategy="simple")
        print("NER model loaded successfully!")
    except Exception as e:
        print(f"Failed to load NER model. Error: {e}")
        return

    # --- 2. Define the Hazard Keywords to search for ---
    # These are the exact phrases we will look for in the text.
    hazard_keywords = [
        'Tsunami', 'High Waves', 'Coastal Flooding', 'Storm Surge', 
        'Rip Current', 'Coastal Erosion', 'Algal Bloom', 
        'Marine Pollution', 'Cyclone', 'flood' # Added "flood" as a common variation
    ]

    # --- 3. Prepare Example Tweets for Analysis ---
    tweets_to_analyze = [
        "Major coastal flooding reported in Chennai due to the storm surge. All residents advised to stay indoors.",
        "Authorities have issued a tsunami warning for the entire Odisha coastline after the earthquake.",
        "The recent cyclone has caused severe coastal erosion near Puri beach.",
        "मुंबई में ऊंची लहरों की चेतावनी है, कृपया समुद्र तट से दूर रहें।", # Hindi: "Warning of high waves in Mumbai, please stay away from the beach."
        "Not a hazard: The sunset over the calm sea in Goa was beautiful today."
    ]

    print("\n--- Analyzing Tweets for Hazards and Locations ---")

    for tweet in tweets_to_analyze:
        try:
            # --- Step 1: Extract Locations using the NER model ---
            ner_results = ner_pipeline(tweet)
            # Filter the results to get only the words identified as locations ('LOC').
            locations = [entity['word'] for entity in ner_results if entity['entity_group'] == 'LOC']

            # --- Step 2: Extract Hazard Keywords directly from the text ---
            detected_hazards = []
            tweet_lower = tweet.lower()
            for hazard in hazard_keywords:
                # Check if the hazard keyword exists in the tweet (case-insensitive)
                if hazard.lower() in tweet_lower:
                    detected_hazards.append(hazard)

            # --- Print the structured results ---
            print(f"Text: '{tweet}'")
            print(f"  -> Location(s): {locations if locations else 'None Detected'}")
            print(f"  -> Detected Hazard(s): {detected_hazards if detected_hazards else 'None Detected'}")
            print("-" * 25)

        except Exception as e:
            print(f"Could not process tweet: '{tweet}'. Error: {e}")

if __name__ == "__main__":
    extract_hazard_info()

