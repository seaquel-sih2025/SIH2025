import asyncio
import httpx
import json
from aio_pika.abc import AbstractIncomingMessage
from app.core.config import settings
from app.services.rabbitmq_service import rabbitmq_service

PRAVAAH_API_URL = "http://127.0.0.1:8000"

async def send_peer_notification(notification_data: dict):
    """Sends peer notification data to the main FastAPI backend endpoint."""
    endpoint_url = f"{PRAVAAH_API_URL}/api/notifications/peer"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(endpoint_url, json=notification_data)
            response.raise_for_status()
            print(f"  - Successfully sent peer notification for report {notification_data['report_id']}")
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"Error sending peer notification: HTTP {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while sending notification: {e}")
            return None

async def process_peer_notification_message(message: AbstractIncomingMessage):
    """Callback function to process a message from the peer_notification_queue."""
    async with message.process():
        try:
            body = json.loads(message.body.decode())
            
            report_id = body["report_id"]
            latitude = body["latitude"]
            longitude = body["longitude"]
            hazard_type = body["hazard_type"]

            print(f"[+] Received peer notification request for '{hazard_type}' report {report_id}")
            
            # Prepare notification data to send to the endpoint
            notification_data = {
                "report_id": report_id,
                "latitude": latitude,
                "longitude": longitude,
                "hazard_type": hazard_type,
                "notification_type": "new_report_alert",
                "message": f"New {hazard_type} report submitted in your area",
                "priority": "normal"
            }
            
            # Send the notification to the endpoint
            result = await send_peer_notification(notification_data)
            
            if result:
                print(f"[✔] Successfully processed peer notification for report {report_id}")
            else:
                print(f"[!] Failed to process peer notification for report {report_id}")

        except Exception as e:
            print(f"[!] Error processing peer notification message: {e}")

async def main():
    """Main function to connect to RabbitMQ and start the worker."""
    print("Starting Peer Notification Worker...")
    await rabbitmq_service.connect()
    await rabbitmq_service.consume_messages("peer_notification_queue", process_peer_notification_message)
    
    print("[*] Peer notification worker is running and waiting for jobs...")
    try:
        await asyncio.Future()
    finally:
        await rabbitmq_service.close()

if __name__ == "__main__":
    asyncio.run(main())