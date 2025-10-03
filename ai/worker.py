# ai/worker.py
import pika
import json
import time
import requests
import os
import sys
import google.generativeai as genai
from config import settings # Use the new local config

# Configure the Gemini API client
genai.configure(api_key=settings.GEMINI_API_KEY)

# --- Standalone NLP Analysis Logic ---
import time
import random

def analyze_description_with_gemini(description: str, max_retries: int = 3):
    """
    Uses the Gemini LLM to analyze the user's description and extract structured data.
    Includes retry logic for rate limiting and quota issues.
    """
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"""
    Analyze the following hazard report description and extract the following information in a structured JSON format:
    - "hazard_type": Classify the event into one of the following categories: Tsunami, Storm Surge, High Waves, Coastal Flooding, Unusual Sea Behavior, Other.
    - "urgency": Assess the urgency on a scale of Low, Medium, High, or Critical.
    - "sentiment": Determine the sentiment of the reporter (e.g., Worried, Panicked, Informative).
    - "summary": Provide a brief, one-sentence summary of the event.

    Description: "{description}"

    Return ONLY the JSON object.
    """
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            # Clean the response to get only the JSON part
            json_str = response.text.strip().replace('```json', '').replace('```', '').strip()
            return json.loads(json_str)
        except Exception as e:
            error_msg = str(e)
            print(f"Error analyzing with Gemini (attempt {attempt + 1}/{max_retries}): {e}")
            
            # Check if it's a quota/rate limit error
            if "quota" in error_msg.lower() or "rate" in error_msg.lower() or "429" in error_msg:
                if attempt < max_retries - 1:
                    # Exponential backoff with jitter
                    wait_time = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limit hit. Waiting {wait_time:.1f} seconds before retry...")
                    time.sleep(wait_time)
                    continue
                else:
                    print("Max retries reached for quota/rate limit. Using fallback analysis.")
                    return fallback_analysis(description)
            else:
                # For other errors, don't retry
                return {"error": f"Failed to analyze description: {error_msg}"}
    
    return {"error": "Failed to analyze description after all retries."}

def fallback_analysis(description: str):
    """
    Simple fallback analysis when Gemini API is unavailable.
    Provides basic keyword-based analysis.
    """
    description_lower = description.lower()
    
    # Simple keyword matching for hazard type
    hazard_keywords = {
        "tsunami": ["tsunami", "tidal wave", "giant wave"],
        "storm_surge": ["storm surge", "storm", "surge"],
        "high_waves": ["high waves", "big waves", "swell", "rough seas", "high surf", "surf advisory"],
        "coastal_flooding": ["coastal flooding", "flooding", "flood", "water level", "inundation"],
        "rip_current": ["rip current", "rip", "undertow"],
        "coastal_erosion": ["coastal erosion", "beach erosion", "shoreline erosion"],
        "other": []
    }
    
    detected_hazard = "other"
    for hazard, keywords in hazard_keywords.items():
        if any(keyword in description_lower for keyword in keywords):
            detected_hazard = hazard
            break
    
    # Simple urgency detection
    urgent_keywords = ["urgent", "emergency", "immediate", "dangerous", "critical"]
    urgency = "High" if any(keyword in description_lower for keyword in urgent_keywords) else "Medium"
    
    # Simple sentiment detection
    panic_keywords = ["panic", "scared", "frightened", "terrified"]
    calm_keywords = ["calm", "normal", "usual"]
    
    if any(keyword in description_lower for keyword in panic_keywords):
        sentiment = "Panicked"
    elif any(keyword in description_lower for keyword in calm_keywords):
        sentiment = "Calm"
    else:
        sentiment = "Informative"
    
    return {
        # Use backend enum style: lowercase with underscores
        "hazard_type": detected_hazard,
        "urgency": urgency,
        "sentiment": sentiment,
        "summary": f"Fallback analysis: {description[:100]}{'...' if len(description) > 100 else ''}",
        "analysis_method": "fallback_keywords"
    }

# --- Standalone RabbitMQ Callback ---
def on_message_received(ch, method, properties, body):
    """
    Callback function to process messages from the nlp_queue.
    """
    print(" [x] Received new message from nlp_queue")
    report_data = json.loads(body)
    report_id = report_data.get("report_id")
    description = report_data.get("user_description")

    if not report_id or not description:
        print(" [!] Invalid message format. Missing 'report_id' or 'user_description'.")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    print(f" [*] Analyzing description for report_id: {report_id}")
    analysis_results = analyze_description_with_gemini(description)

    # Normalize hazard_type to backend enum (lowercase with underscores)
    try:
        ht = analysis_results.get("hazard_type") if isinstance(analysis_results, dict) else None
        if isinstance(ht, str) and ht.strip():
            norm = ht.strip().lower().replace("-", "_").replace(" ", "_")
            synonyms = {
                "storm": "storm_surge",
                "stormsurge": "storm_surge",
                "high_surf": "high_waves",
                "high_wave": "high_waves",
                "coastal_flood": "coastal_flooding",
                "rip": "rip_current",
                "ripcurrents": "rip_current",
                "erosion": "coastal_erosion",
                "algae_bloom": "water_discoloration",
                "algal_bloom": "water_discoloration",
                "red_tide": "water_discoloration",
                "debris": "marine_debris",
            }
            analysis_results["hazard_type"] = synonyms.get(norm, norm)
    except Exception:
        pass

    # Prepare data for the fan-in endpoint
    verification_payload = {
        "report_id": report_id,
        "result_data": analysis_results
    }

    # Make a POST request to the backend's fan-in endpoint
    try:
        response = requests.post(
            f"{settings.BACKEND_URL}/api/verifications/nlp",
            json=verification_payload,
            timeout=30
        )
        response.raise_for_status() # Raise an exception for bad status codes
        print(f" [✔] Successfully submitted NLP verification for report_id: {report_id}")
    except requests.exceptions.RequestException as e:
        print(f" [!] Failed to submit NLP verification. Error: {e}")
        # Here you might want to implement a retry mechanism or log to a dead-letter queue

    ch.basic_ack(delivery_tag=method.delivery_tag)

# --- Standalone RabbitMQ Connection Logic ---
def start_worker():
    """
    Connects to RabbitMQ and starts consuming messages from the nlp_queue.
    """
    connection_params = pika.URLParameters(settings.RABBITMQ_URL)
    while True:
        try:
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()
            channel.queue_declare(queue='nlp_queue', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue='nlp_queue', on_message_callback=on_message_received)

            print(' [*] NLP Worker is waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Interrupted by user. Shutting down...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Restarting worker...")
            time.sleep(5)

if __name__ == '__main__':
    # Test the fallback analysis if run directly
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_description = "The waves are getting very high and the wind is strong. Water is reaching the shore line."
        print("Testing fallback analysis:")
        result = fallback_analysis(test_description)
        print(json.dumps(result, indent=2))
    else:
        start_worker()