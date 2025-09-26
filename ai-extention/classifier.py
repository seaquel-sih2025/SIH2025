from transformers import pipeline
from scraper import fetch_hazard_tweets
from translate import translate_to_english
from sentiment import classify_emotion_text
from ner import extract_hazard_and_locations
import json

model_name = "joeddav/xlm-roberta-large-xnli"

classifier = pipeline("zero-shot-classification", model=model_name,framework="pt")

def classify_with_model(tweet_text):
    """
    Classifies a tweet using a MULTILINGUAL zero-shot learning model.
    Returns 1 if hazardous, else 0.
    """
    if not tweet_text or not tweet_text.strip():
        return 0
    candidate_labels = ["report of an ocean hazard", "not an ocean hazard"]
    result = classifier(tweet_text, candidate_labels)
    top_label = result['labels'][0]
    top_score = result['scores'][0]
    if top_label == "report of an ocean hazard" and top_score > 0.75:
        return 1
    return 0

def classify_tweets(tweets):
    """
    Accepts list of tweet dicts with 'text' field.
    Pipeline: classify hazard -> if hazardous, translate -> sentiment -> NER.
    Returns enriched dicts.
    """
    classified = []
    for t in tweets:
        text = t.get('text', '')
        hazardous = classify_with_model(text)
        item = dict(t)
        item['hazardous'] = hazardous
        translated = translate_to_english(text)
        item['translated_text'] = translated
        if hazardous == 1:
            sentiment = classify_emotion_text(translated)
            item['sentiment'] = sentiment
            ner_info = extract_hazard_and_locations(translated)
            item['ner'] = ner_info
        classified.append(item)
    return classified

if __name__ == "__main__":
    tweets = fetch_hazard_tweets(limit=20)
    classified = classify_tweets(tweets)
    print(json.dumps(classified, indent=2, ensure_ascii=False))