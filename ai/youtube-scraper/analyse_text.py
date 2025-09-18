import os
import json
import datetime
import time
from dotenv import load_dotenv
# from google.generativeai import GenerativeModel  # replaced by LangChain wrapper
import psycopg2
from psycopg2 import sql
from search_videos import search_for_videos, SEARCH_KEYWORDS, SEARCH_TIMEFRAME_HOURS
from get_text_data import get_video_details

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

# DB utilities
from db_utils import ensure_schema, store_alert

# --- CONFIGURATION ---
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

ALERT_THRESHOLD = 2

# --- Configure LangChain Google AI Client ---
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",  # faster, higher limits
        google_api_key=GOOGLE_API_KEY,
        temperature=0.2,
        convert_system_message_to_human=True,
    )
    print("Google AI client (LangChain) configured successfully.")
except Exception as e:
    print(f"Error configuring Google AI client: {e}")
    llm = None


def analyze_video_text_with_llm(video_data):
    if not llm:
        print("Google AI model not initialized.")
        return None

    prompt_instructions = (
        "You are a disaster intelligence analyst. Analyze the following YouTube video text "
        "(title, description, comments) to determine if it describes a real-time ocean hazard. "
        "Respond ONLY with a valid JSON object with this exact structure:\n"
        "{\n"
        "  \"is_potential_event\": boolean,\n"
        "  \"event_type\": \"string (e.g., 'Tsunami', 'Storm Surge', 'News Report', 'General Discussion', 'False Alarm', 'Old Footage')\",\n"
        "  \"locations_mentioned\": [\"string\"],\n"
        "  \"confidence_score\": integer (0-100, likelihood it's a real, current event),\n"
        "  \"reasoning\": \"string (a brief explanation for your analysis)\"\n"
        "}\n"
        "Return only JSON."
    )

    title = video_data.get('title', '')
    description = video_data.get('description', '')
    comments_text = " ".join(video_data.get('comments', []))

    # Trim to stay within quotas
    if len(description) > 4000:
        description = description[:4000]
    if len(comments_text) > 6000:
        comments_text = comments_text[:6000]

    combined_text = (
        f"Analyze this text:\n\nTitle: {title}\n\nDescription: {description}\n\nComments: {comments_text}"
    )

    try:
        messages = [HumanMessage(content=f"{prompt_instructions}\n\n{combined_text}")]
        response = llm.invoke(messages)
        response_text = response.content if hasattr(response, 'content') else str(response)
        json_str = response_text.strip().lstrip('```json').rstrip('```')
        analysis_result = json.loads(json_str)
        return analysis_result
    except Exception as e:
        print(f"An error occurred during Gemini analysis: {e}")
        return None


if __name__ == "__main__":
    print("--- Starting Ocean Hazard Monitoring Run ---")

    # Ensure DB schema exists
    ensure_schema()

    found_videos = search_for_videos(YOUTUBE_API_KEY, SEARCH_KEYWORDS, SEARCH_TIMEFRAME_HOURS)
    high_priority_alerts = []

    if found_videos:
        print(f"\nFound {len(found_videos)} videos. Fetching and analyzing text data...\n")

        for video in found_videos:
            print(f"-> Analyzing '{video['title']}'...")
            details = get_video_details(YOUTUBE_API_KEY, video['video_id'])

            if details:
                combined_data = {**video, **details}
                analysis = analyze_video_text_with_llm(combined_data)

                if analysis:
                    is_event = analysis.get('is_potential_event', False)
                    confidence = analysis.get('confidence_score', 0)

                    if is_event and confidence >= ALERT_THRESHOLD:
                        alert_message = (
                            f"** HIGH-PRIORITY ALERT (Confidence: {confidence}%) **\n"
                            f"Event Type: {analysis.get('event_type', 'N/A')}\n"
                            f"Video Title: {video['title']}\n"
                            f"Locations: {', '.join(analysis.get('locations_mentioned', [])) or 'N/A'}\n"
                            f"Reasoning: {analysis.get('reasoning', 'N/A')}\n"
                            f"Link: https://www.youtube.com/watch?v={video['video_id']}\n"
                        )
                        high_priority_alerts.append(alert_message)

                        data_to_store = {
                            "event_type": analysis.get('event_type', 'N/A'),
                            "location": ", ".join(analysis.get('locations_mentioned', [])) or 'N/A',
                            "urgency": (
                                'High' if confidence >= 80 else 'Medium' if confidence >= 50 else 'Low'
                            ),
                            "sentiment": 'Neutral',
                            "video_url": f"https://www.youtube.com/watch?v={video['video_id']}",
                            "video_created_at": video.get('published_at'),
                            "video_date": (video.get('published_at') or '')[:10] if video.get('published_at') else None,
                            "video_time": (video.get('published_at') or '')[11:19] if video.get('published_at') else None,
                        }
                        store_alert(data_to_store)

                time.sleep(2)  # be gentle with rate limits
    else:
        print("\nNo new videos found in the specified timeframe.")

    print("\n-------------------------------------------")
    print("--- MONITORING RUN COMPLETE ---")
    print(f"Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if high_priority_alerts:
        print(f"\nGenerated {len(high_priority_alerts)} High-Priority Alert(s):")
        for alert in high_priority_alerts:
            print(alert)
    else:
        print("\nNo high-priority events detected.")
    print("-------------------------------------------\n")