# ai/worker.py
import pika
import json
import time
import requests
import os
import sys
from config import settings  # Use the new local config
from huggingface_hub import InferenceClient # Import the Hugging Face client

# Initialize the Hugging Face client
hf_client = InferenceClient(token=settings.HUGGING_FACE_TOKEN)

def analyze_description_with_huggingface(description: str, max_retries: int = 3):
    """
    Uses the Hugging Face model to analyze the user's description.
    Includes retry logic for API errors.
    """
    for attempt in range(max_retries):
        try:
            # Call the Hugging Face model
            response = hf_client.text_classification(
                model="prathamesh788/pravaah",
                inputs=description
            )
            # Assuming the model returns a list of dictionaries with 'label' and 'score'
            if response and isinstance(response, list) and all('label' in res and 'score' in res for res in response):
                # You might want to process the response further, but for now, we'll return it as is
                return response
            else:
                return {"error": "Invalid response from NLP model"}
        except requests.exceptions.RequestException as e:
            print(f"Error analyzing with Hugging Face (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt)
                print(f"API request failed. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                return {"error": f"Failed to analyze description after {max_retries} retries."}
        except Exception as e:
            # For other errors, don't retry
            return {"error": f"Failed to analyze description: {str(e)}"}

    return {"error": "Failed to analyze description after all retries."}

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
    analysis_results = analyze_description_with_huggingface(description)

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
    start_worker()