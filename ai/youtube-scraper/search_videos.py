import os
import datetime
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
# Load the .env file
load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Define the keywords we are interested in.
# The '|' acts as an 'OR' operator in the search query.
SEARCH_KEYWORDS = "tsunami | storm surge | coastal flood | cyclone | rogue wave"

# How far back do we want to search? (in hours)
SEARCH_TIMEFRAME_HOURS = 48
# --- END CONFIGURATION ---


def search_for_videos(api_key, query, search_hours):
    """
    Searches for YouTube videos uploaded within a specified timeframe.
    """
    if not api_key:
        print("Error: YouTube API key not found.")
        return

    try:
        # Create a YouTube service object
        youtube = build('youtube', 'v3', developerKey=api_key)

        # We need to calculate the time to search from.
        # The API requires time in RFC 3339 format (e.g., 1970-01-01T00:00:00Z)
        from_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=search_hours)
        published_after_time = from_time.isoformat()

        print(f"Searching for videos with keywords: '{query}'")
        print(f"Looking for videos published after: {published_after_time}\n")

        # Make the API call
        search_request = youtube.search().list(
            q=query,
            part='snippet', # 'snippet' contains title, description, channel, etc.
            type='video',
            order='date',   # Order by upload date to get the newest first
            publishedAfter=published_after_time,
            maxResults=25  # Get up to 25 results
        )
        response = search_request.execute()
        print("[DEBUG] Raw YouTube API response:", response)  # Debug print

        # Process the results
        videos = []
        if 'items' in response:
            for item in response['items']:
                video_info = {
                    'title': item['snippet']['title'],
                    'video_id': item['id']['videoId'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_info)
        
        return videos

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None


# --- Main execution block ---
if __name__ == "__main__":
    found_videos = search_for_videos(API_KEY, SEARCH_KEYWORDS, SEARCH_TIMEFRAME_HOURS)

    if found_videos:
        print(f"--- Found {len(found_videos)} relevant videos in the last {SEARCH_TIMEFRAME_HOURS} hour(s) ---\n")
        for video in found_videos:
            print(f"Title: {video['title']}")
            print(f"Video ID: {video['video_id']}")
            print(f"Published: {video['published_at']}")
            print(f"Link: https://www.youtube.com/watch?v={video['video_id']}\n")
    elif found_videos is None:
         print("--- An error occurred during the search. ---")
    else:
        print(f"--- No relevant videos found in the last {SEARCH_TIMEFRAME_HOURS} hour(s). ---")