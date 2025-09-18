import json
import time
import random
from twitter.fetch import fetch_tweets
from llm.analyze import analyze_post_with_gemini
from db.models import store_scraped_data

# QUERY = 'lang:en (tsunami OR flood OR flooding OR cyclone OR hurricane OR typhoon OR "high waves" OR "storm surge" OR swell) (warning OR alert OR advisory OR watch OR evacuate OR evacuation OR hazard OR inundation) -is:retweet -is:reply -is:quote -giveaway -meme -politics -election -vote'

QUERY = 'lang:en (tsunami OR flood OR flooding OR cyclone OR hurricane OR typhoon OR "high waves" OR "storm surge" OR swell) (warning OR alert OR advisory OR watch OR evacuate OR evacuation OR hazard OR inundation) -is:retweet -is:reply -is:quote -giveaway -meme -politics -election -vote'



def main():
	# Load last since_id to avoid duplicates
	try:
		with open("since_id.txt", "r") as f:
			since_id = f.read().strip()
			since_id = int(since_id) if since_id else None
	except FileNotFoundError:
		since_id = None

	tweets, places = fetch_tweets(QUERY, count=10, since_id=since_id)  # Twitter API requires min 10 tweets
	print(f"Fetched {len(tweets)} tweets.")

	max_id = None
	seen_text_signatures = set()

	def is_relevant_fast(text: str) -> bool:
		text_lower = text.lower()
		if text_lower.startswith("rt @"):
			return False
		blacklist = [
			"giveaway", "follow back", "followback", "politics", "election", "vote",
			"crypto", "nft", "airdrop", "promo", "advertisement", "ad:", "sponsored",
			"movie", "trailer", "music", "song", "game", "simulation"
		]
		if any(bad in text_lower for bad in blacklist):
			return False
		hazard_terms = [
			"tsunami", "flood", "flooding", "cyclone", "hurricane", "typhoon",
			"storm surge", "high waves", "swell", "inundation", "earthquake"
		]
		signal_terms = [
			"warning", "watch", "advisory", "alert", "evacuate", "evacuation",
			"red alert", "amber alert"
		]
		has_hazard = any(term in text_lower for term in hazard_terms)
		has_signal = any(term in text_lower for term in signal_terms)
		# Accept any hazard mention unless clearly entertainment/ads; prefer signal when present
		return has_hazard and not any(bad in text_lower for bad in ["movie", "trailer", "game", "music", "song"]) or has_signal

	for i, tweet in enumerate(tweets):
		text = tweet.text
		print(f"Processing tweet {i+1}/{len(tweets)}: {text[:80]}...")

		# In-run deduplication by lightweight signature
		sig = (text[:120].lower()).strip()
		if sig in seen_text_signatures:
			print("Duplicate content in this batch. Skipping.")
			continue
		seen_text_signatures.add(sig)

		# Compose tweet metadata
		tweet_id = tweet.id
		tweet_url = f"https://twitter.com/i/web/status/{tweet_id}"
		tweet_created_at = getattr(tweet, "created_at", None)
		# Resolve place name from includes mapping
		geo = getattr(tweet, "geo", None) or {}
		place_id = None
		if isinstance(geo, dict):
			place_id = geo.get("place_id")
		place_name = places.get(place_id) if place_id else None
		# Extract hashtags list
		entities = getattr(tweet, "entities", None) or {}
		hashtags = []
		if isinstance(entities, dict):
			for tag in entities.get("hashtags", []) or []:
				text_tag = tag.get("tag") if isinstance(tag, dict) else None
				if text_tag:
					hashtags.append(text_tag)

		# Fast prefilter to avoid LLM calls on irrelevant tweets
		if not is_relevant_fast(text):
			print("Prefilter: irrelevant. Skipping LLM.")
			continue

		try:
			llm_result = analyze_post_with_gemini(text, hashtags=hashtags)
			llm_json = json.loads(llm_result)

			def is_hazard_from_llm(payload):
				if not isinstance(payload, dict):
					return False
				# Support both schemas: hazard_related "yes" or ocean_hazard boolean/string
				hazard_related = str(payload.get("hazard_related", "")).lower().strip()
				if hazard_related == "yes":
					return True
				ocean_hazard = payload.get("ocean_hazard")
				if isinstance(ocean_hazard, bool) and ocean_hazard:
					return True
				if isinstance(ocean_hazard, str) and ocean_hazard.lower() in ("yes", "true", "1"):
					return True
				# Fallback: treat known ocean/coastal event types as hazards
				event_type = str(payload.get("event_type", "")).lower().strip()
				coastal_types = {
					"tsunami", "high waves", "storm surge", "swell", "rip current",
					"coastal erosion", "algal bloom", "pollution", "cyclone", "hurricane", "typhoon"
				}
				if event_type in coastal_types:
					return True
				return False

			if is_hazard_from_llm(llm_json):
				# If model didn't extract a location, use place name if available
				if place_name and not (llm_json.get("location") or "").strip():
					llm_json["location"] = place_name
				llm_json["tweet_url"] = tweet_url
				llm_json["tweet_created_at"] = tweet_created_at
				store_scraped_data(llm_json)
				print("Stored in DB.")
			else:
				print("Not a hazard, not stored.")
		except Exception as e:
			print("LLM or DB Error:", e)
		
		# Exponential backoff with jitter to avoid rate limits
		if i < len(tweets) - 1:  # Don't sleep after the last tweet
			base_delay = 2  # Base delay of 2 seconds
			jitter = random.uniform(0.5, 1.5)  # Add randomness
			delay = base_delay + jitter
			print(f"Waiting {delay:.1f} seconds before next request...")
			time.sleep(delay)
		
		if max_id is None or tweet.id > max_id:
			max_id = tweet.id

	# Save the newest tweet id for next run
	if max_id:
		with open("since_id.txt", "w") as f:
			f.write(str(max_id))

if __name__ == "__main__":
	main()
