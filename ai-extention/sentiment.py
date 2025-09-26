from transformers import pipeline

_emotion_classifier = None

def get_emotion_classifier():
    """
    Load (lazily) and return a text-classification pipeline for emotions.
    Using GoEmotions for strong multilingual-ish coverage via RoBERTa base.
    """
    global _emotion_classifier
    if _emotion_classifier is not None:
        return _emotion_classifier
    model_name = "SamLowe/roberta-base-go_emotions"
    _emotion_classifier = pipeline("text-classification", model=model_name, framework="pt")
    return _emotion_classifier

def classify_emotion_text(text):
    """
    Classify a single text into one of: panic | calm | confusion | neutral | unknown
    Returns dict: {label, score}
    """
    if not text or not text.strip():
        return {"label": "unknown", "score": 0.0}

    emotion_to_category = {
        'fear': 'panic', 'nervousness': 'panic', 'remorse': 'panic',
        'joy': 'calm', 'love': 'calm', 'admiration': 'calm', 'approval': 'calm',
        'caring': 'calm', 'excitement': 'calm', 'gratitude': 'calm', 'optimism': 'calm',
        'relief': 'calm', 'pride': 'calm',
        'confusion': 'confusion', 'curiosity': 'confusion', 'realization': 'confusion',
        'neutral': 'neutral',
        'anger': 'unknown', 'annoyance': 'unknown', 'disappointment': 'unknown',
        'disapproval': 'unknown', 'disgust': 'unknown', 'embarrassment': 'unknown',
        'grief': 'unknown', 'sadness': 'unknown', 'surprise': 'unknown', 'desire': 'unknown'
    }

    classifier = get_emotion_classifier()
    try:
        result = classifier(text)
        top_label = result[0]['label']
        top_score = float(result[0]['score'])
    except Exception:
        return {"label": "unknown", "score": 0.0}

    mapped = emotion_to_category.get(top_label, 'unknown')
    return {"label": mapped, "score": top_score}

if __name__ == "__main__":
    # Simple demo
    examples = [
        "Cyclone warning issued; please evacuate immediately.",
        "Beautiful calm sea today.",
        "Why is the alert not clear?",
        "Meeting at 3 PM.",
    ]
    clf = get_emotion_classifier()
    for ex in examples:
        print(ex, "->", classify_emotion_text(ex))

