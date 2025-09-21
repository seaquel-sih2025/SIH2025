import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import the search function from our previous script
from search_videos import search_for_videos, SEARCH_KEYWORDS, SEARCH_TIMEFRAME_HOURS

# --- CONFIGURATION ---
from config import YOUTUBE_API_KEY as API_KEY
# --- END CONFIGURATION ---


def get_video_details(api_key, video_id):
    """
    Fetches details (description, tags) and comments for a specific video ID.
    """
    if not api_key:
        print("Error: YouTube API key not found.")
        return None

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        full_text_data = {
            'description': '',
            'tags': [],
            'comments': []
        }

        # 1. Get Video Description and Tags
        video_request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        video_response = video_request.execute()
        
        if video_response['items']:
            snippet = video_response['items'][0]['snippet']
            full_text_data['description'] = snippet.get('description', '')
            full_text_data['tags'] = snippet.get('tags', [])

        # 2. Get Video Comments
        # This can fail if comments are disabled, so we wrap it in a try/except
        try:
            comment_request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=20,  # Get up to 20 top-level comments
                order="relevance" # relevance is often better for finding descriptive comments
            )
            comment_response = comment_request.execute()
            
            for item in comment_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                full_text_data['comments'].append(comment)
        except HttpError as e:
            # If e.resp.status is 403, it's likely that comments are disabled.
            if e.resp.status == 403:
                full_text_data['comments'].append("Comments are disabled for this video.")
            else:
                # For other errors, we can re-raise or handle them as needed.
                print(f"An unexpected HTTP error occurred while fetching comments: {e}")


        return full_text_data

    except HttpError as e:
        print(f"An HTTP error {e.resp.status} occurred: {e.content}")
        return None


# --- Main execution block ---
if __name__ == "__main__":
    print("--- Step 2: Searching for relevant videos ---")
    found_videos = search_for_videos(API_KEY, SEARCH_KEYWORDS, SEARCH_TIMEFRAME_HOURS)

    if found_videos:
        print(f"\n--- Found {len(found_videos)} videos. Now fetching text data for each. ---\n")
        
        all_videos_data = []
        for video in found_videos:
            print(f"Fetching data for video: '{video['title']}' (ID: {video['video_id']})")
            
            # This is our new function from Step 3
            details = get_video_details(API_KEY, video['video_id'])
            
            if details:
                # Combine the initial info with the new details
                combined_data = {**video, **details}
                all_videos_data.append(combined_data)
                
                # Print a summary of what we found
                print(f"  > Description Length: {len(details['description'])} characters")
                print(f"  > Tags: {details['tags']}")
                print(f"  > Found {len(details['comments'])} comments.\n")
        
        # You could now save `all_videos_data` to a file or database
        # For now, we just print the title of the first video's data as an example
        if all_videos_data:
            print("\n--- Example of final combined data for one video ---")
            print(all_videos_data[0])

    else:
        print("\n--- No videos found, so no data to fetch. ---")