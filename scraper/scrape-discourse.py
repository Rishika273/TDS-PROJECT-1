import requests
import json
import os
import time

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"

def get_topics_from_category(category_id, max_pages=5):
    all_topics = []

    for page in range(max_pages):
        print(f"Fetching page {page}...")
        url = f"{BASE_URL}/latest.json?category={category_id}&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            continue

        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])
        all_topics.extend(topics)

        time.sleep(0.5)

    return all_topics


def fetch_full_posts(topic_ids):
    full_posts = []

    for topic in topic_ids:
        topic_id = topic['id']
        topic_url = f"{BASE_URL}/t/{topic_id}.json"
        response = requests.get(topic_url, headers=HEADERS)

        if response.status_code == 200:
            full_posts.append(response.json())
        else:
            print(f"Failed to fetch topic {topic_id}")

        time.sleep(0.5)

    return full_posts


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    category_id = 34  # TDS Knowledge Base
    topics = get_topics_from_category(category_id, max_pages=5)

    full_data = fetch_full_posts(topics)

    with open("data/discourse.json", "w", encoding="utf-8") as f:
        json.dump(full_data, f, indent=2)

    print("✅ Scraping completed and saved to data/discourse.json")
