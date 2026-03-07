"""
setup_notion.py

Creates the 2 Notion databases for the Spike.sh LinkedIn engine.
Run this once. It prints all database IDs at the end — paste them into .env.

Requires in .env:
  NOTION_API_KEY=secret_...
  NOTION_PARENT_PAGE_ID=<ID of the Notion page where databases will be created>
"""

import os
import sys
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
PARENT_PAGE_ID = os.getenv("NOTION_PARENT_PAGE_ID")

if not NOTION_API_KEY:
    print("Error: NOTION_API_KEY is not set in .env")
    sys.exit(1)

if not PARENT_PAGE_ID:
    print("Error: NOTION_PARENT_PAGE_ID is not set in .env")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def notion_post(endpoint: str, payload: dict) -> dict:
    url = f"https://api.notion.com/v1/{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"\nNotion API error {e.code} on {endpoint}:")
        print(body)
        sys.exit(1)


def create_db(title: str, properties: dict) -> str:
    print(f"  Creating '{title}'...")
    result = notion_post("databases", {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": title}}],
        "properties": properties,
    })
    db_id = result["id"]
    print(f"  Done. ID: {db_id}")
    return db_id


# ---------------------------------------------------------------------------
# Step 1: Guides
# ---------------------------------------------------------------------------

print("\n[1/2] Creating Guides database...")
guides_id = create_db("Guides", {
    "Title": {"title": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Draft", "color": "gray"},
                {"name": "Published", "color": "green"},
            ]
        }
    },
    "Date Published": {"date": {}},
    "Posts Generated": {"checkbox": {}},
})

# ---------------------------------------------------------------------------
# Step 2: LinkedIn Posts
# ---------------------------------------------------------------------------

print("\n[2/2] Creating LinkedIn Posts database...")
linkedin_posts_id = create_db("LinkedIn Posts", {
    "Title": {"title": {}},
    "Post Content": {"rich_text": {}},
    "Status": {
        "select": {
            "options": [
                {"name": "Generated", "color": "yellow"},
                {"name": "Finalized", "color": "blue"},
                {"name": "Published", "color": "green"},
            ]
        }
    },
    "Linked Guide": {
        "relation": {
            "database_id": guides_id,
            "single_property": {},
        }
    },
    "Impressions":        {"number": {"format": "number"}},
    "Engagements":        {"number": {"format": "number"}},
    "Engagement Rate":    {"number": {"format": "percent"}},
    "Clicks":             {"number": {"format": "number"}},
    "Click-through Rate": {"number": {"format": "percent"}},
    "Reactions":          {"number": {"format": "number"}},
    "Comments":           {"number": {"format": "number"}},
    "Reposts":            {"number": {"format": "number"}},
    "Notes":              {"rich_text": {}},
    "Screenshot":         {"files": {}},
})

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("All databases created successfully!")
print("=" * 60)
print("\nCopy these into your .env file:\n")
print(f"NOTION_GUIDES_DB_ID={guides_id}")
print(f"NOTION_LINKEDIN_POSTS_DB_ID={linkedin_posts_id}")
print()
