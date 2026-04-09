import json
import os
import time
import requests
from datetime import datetime

URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology":    ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":     ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":        ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":       ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

def find_category(title):
    t = title.lower()
    for cat, keywords in CATEGORIES.items():
        for word in keywords:
            if word in t:
                return cat
    return None

def fetch_ids():
    try:
        r = requests.get(f"{URL}/topstories.json", headers=HEADERS, timeout=10)
        ids = r.json()
        return ids[:500]
    except Exception as e:
        print(f"something went wrong while fetching ids: {e}")
        return []

def load_story(sid):
    try:
        r = requests.get(f"{URL}/item/{sid}.json", headers=HEADERS, timeout=10)
        return r.json()
    except Exception as e:
        print(f"something went wrong with {sid}, skipping")
        return None

print("starting script...")

story_ids = fetch_ids()
print(f"got {len(story_ids)} story ids")

all_stories = []
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for category in CATEGORIES:
    count = 0
    print(f"\nlooking for {category} stories...")

    for sid in story_ids:
        if count >= 25:
            break

        story = load_story(sid)

        if not story or story.get("type") != "story":
            continue

        title = story.get("title", "")
        if not title:
            continue

        if find_category(title) != category:
            continue

        all_stories.append({
            "post_id":      story.get("id"),
            "title":        title,
            "category":     category,
            "score":        story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author":       story.get("by", ""),
            "collected_at": now
        })

        count += 1
        print(f"  {count}/25 - {title[:60]}")

    time.sleep(2)

os.makedirs("data", exist_ok=True)
filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

with open(filename, "w") as f:
    json.dump(all_stories, f, indent=2)

if len(all_stories) < 100:
    print("warning: less than 100 stories collected")
else:
    print("looks good!")

print(f"\nCollected {len(all_stories)} stories. Saved to {filename}")
