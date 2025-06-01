import requests
import json
import os
import time

def scrape_discourse_category(category_id=34, start_page=0, end_page=5):
    base_url = "https://discourse.onlinedegree.iitm.ac.in"
    all_topics = []

    for page in range(start_page, end_page + 1):
        print(f"Fetching topics from category page {page}...")
        url = f"{base_url}/c/courses/tds-kb/{category_id}.json?page={page}"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            continue

        data = response.json()
        topics = data.get("topic_list", {}).get("topics", [])

        for topic in topics:
            topic_id = topic["id"]
            topic_url = f"{base_url}/t/{topic_id}.json"
            topic_response = requests.get(topic_url)

            if topic_response.status_code != 200:
                print(f"Skipping topic {topic_id}. Failed to fetch.")
                continue

            topic_data = topic_response.json()
            all_topics.append(topic_data)

            # polite scraping delay
            time.sleep(0.5)

    os.makedirs("data", exist_ok=True)
    with open("data/discourse.json", "w", encoding="utf-8") as f:
        json.dump(all_topics, f, indent=2)

    print("Scraping completed and saved to data/discourse.json")

if __name__ == "__main__":
    scrape_discourse_category(category_id=34, start_page=0, end_page=5)  
    
