import requests
import json
from datetime import date, timedelta

from dotenv import load_dotenv
import os

# Load values from .env into environment
load_dotenv()

# Access the API key
API_KEY = os.getenv("TWITTER_API_KEY")


def search_tweets(query, query_type="Latest", limit=20):
    """
    Searches for tweets using the twitterapi.io advanced search endpoint.
    """
    url = "https://api.twitterapi.io/twitter/tweet/advanced_search"
    headers = {"X-API-Key": API_KEY}
    params = {"query": query, "queryType": query_type, "limit": limit}
    
    print(f"🔍 Executing search with query: {query}")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def extract_tweets(result_json):
    """
    Extracts a normalized list of tweets from the API result.
    Returns a list of dicts with keys: tweet_url, location, created_at, text, hashtags
    """
    if not result_json or 'tweets' not in result_json:
        return []
    tweets = result_json.get('tweets', [])
    extracted_data = []
    for tweet in tweets:
        tweet_url = tweet.get('url')
        text = tweet.get('text')
        created_at = tweet.get('createdAt')
        location = tweet.get('author', {}).get('location', None)
        hashtags = [tag['text'] for tag in tweet.get('entities', {}).get('hashtags', [])]
        extracted_data.append({
            'tweet_url': tweet_url,
            'location': location,
            'created_at': created_at,
            'text': text,
            'hashtags': hashtags
        })
    return extracted_data

def build_default_query(hazard_keywords=None, location=None):
    """
    Builds the default hazard + India coastal locations + language + date query.
    
    Args:
        hazard_keywords (str, optional): Custom hazard keywords. If None, uses default.
        location (str, optional): Custom location keywords. If None, uses default.
    
    Returns:
        str: Complete query string for Twitter search
    """
    # Default hazard keywords
    if hazard_keywords is None:
        hazard_keywords = (
            "(flood OR tsunami OR cyclone OR \"storm surge\" OR \"high tide\" OR \"high waves\" OR swell OR "
            "\"coastal flooding\" OR \"rip current\" OR \"coastal erosion\" OR \"water discoloration\" OR "
            "\"algal bloom\" OR \"marine debris\" OR pollution)"
        )
    
    # Default location keywords
    if location is None:
        location = (
            "(Mumbai OR Chennai OR Kolkata OR Odisha OR Kerala OR Gujarat OR Goa OR \"Andhra Pradesh\" "
            "OR \"West Bengal\" OR Vizag OR Puri OR \"Bay of Bengal\" OR \"Arabian Sea\")"
        )
    
    allowed_languages = [
        "as", "bn", "brx", "doi", "gu", "hi", "kn", "ks", "kok", "ml", "mni", 
        "mr", "ne", "or", "pa", "sa", "sat", "sd", "ta", "te", "ur", "en", "bh", "en"
    ]
    lang_query = "(" + " OR ".join([f"lang:{lang}" for lang in allowed_languages]) + ")"
    yesterday = date.today() - timedelta(days=1)
    date_filter = f"since:{yesterday.strftime('%Y-%m-%d')}"
    full_query = f"{hazard_keywords} {location} {lang_query} {date_filter}"
    return full_query

def fetch_hazard_tweets(limit=20, hazard_keywords=None, location=None):
    """
    Fetches tweets matching the hazard query and returns extracted list.
    
    Args:
        limit (int): Maximum number of tweets to fetch
        hazard_keywords (str, optional): Custom hazard keywords. If None, uses default.
        location (str, optional): Custom location keywords. If None, uses default.
    
    Returns:
        list: List of extracted tweet dictionaries
    """
    query = build_default_query(hazard_keywords=hazard_keywords, location=location)
    result = search_tweets(query=query, query_type="Latest", limit=limit)
    return extract_tweets(result)

if __name__ == "__main__":
    tweets = fetch_hazard_tweets(limit=20)
    if tweets:
        print("\nExtracted tweets:")
        print(json.dumps(tweets, indent=2, ensure_ascii=False))
