import requests
import time
import random
from config import GEMINI_API_KEY

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def analyze_post_with_gemini(post, hashtags=None, max_retries=3):
	hashtags = hashtags or []
	hashtags_text = ", ".join(f"#{h}" for h in hashtags[:8])  # cap to 8 to keep prompt short
	extra = f"\nHashtags: {hashtags_text}\n" if hashtags_text else "\n"
	prompt = f"""
	You are an expert in disaster monitoring. Analyze the social post and output ONLY a single-line valid JSON object (no markdown, no comments) with this schema and rules:
	{{
	  "ocean_hazard": true|false,  // true if the post relates to ocean/coastal hazards (e.g., tsunami, storm surge, high waves/swell, rip current, coastal erosion, tropical cyclones at/near coast, marine pollution/algal bloom). false otherwise.
	  "event_type": "tsunami|high waves|flooding|storm surge|cyclone|hurricane|typhoon|swell|rip current|coastal erosion|algal bloom|pollution|other",
	  "location": "short human place name (city/region/country). If unknown, put the most plausible concise place name; do not leave empty.",
	  "urgency": "immediate|moderate|low|rumor|unknown",
	  "sentiment": "panic|calm|confusion|neutral|unknown"
	}}

	Guidance:
	- Infer location from explicit location-like hashtags (e.g., #Manila, #Kochi) or text.
	- Prefer concise place names (ideally city). Avoid long descriptions.
	- Use lowercase for event_type values exactly as listed above.
	
	Post: "{post}"{extra}
	"""
	headers = {"Content-Type": "application/json"}
	data = {
		"contents": [{"parts": [{"text": prompt}]}]
	}
	
	for attempt in range(max_retries):
		try:
			response = requests.post(GEMINI_API_URL, headers=headers, json=data, timeout=45)
			
			# Handle rate limiting and transient server errors
			if response.status_code in (429, 500, 502, 503, 504):
				wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff with jitter
				msg = "Rate limited" if response.status_code == 429 else f"Server {response.status_code}"
				print(f"{msg}. Waiting {wait_time:.1f} seconds before retry {attempt + 1}/{max_retries}")
				time.sleep(wait_time)
				continue
			
			response.raise_for_status()
			
			# Gemini returns the text in a nested structure
			result = response.json()
			
			try:
				text_response = result["candidates"][0]["content"]["parts"][0]["text"]
				
				# Clean up the response - remove markdown code blocks if present
				if text_response.startswith("```json"):
					# Remove ```json from start and ``` from end
					text_response = text_response.replace("```json", "").replace("```", "").strip()
				elif text_response.startswith("```"):
					# Remove ``` from start and end
					text_response = text_response.replace("```", "").strip()
				
				return text_response
			except (KeyError, IndexError) as e:
				print(f"Error parsing Gemini response: {e}")
				return "{}"  # fallback empty JSON
				
		except requests.exceptions.RequestException as e:
			if attempt < max_retries - 1:
				wait_time = (2 ** attempt) + random.uniform(0, 1)
				print(f"Request failed: {e}. Retrying in {wait_time:.1f} seconds...")
				time.sleep(wait_time)
			else:
				print(f"Max retries reached. Error: {e}")
				return "{}"  # fallback empty JSON
	
	return "{}"  # fallback empty JSON
