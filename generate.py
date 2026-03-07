import os
import sys
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
from notion_client import Client as NotionClient
import anthropic

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
GUIDES_DB = os.getenv("NOTION_GUIDES_DB_ID")
LINKEDIN_POSTS_DB = os.getenv("NOTION_LINKEDIN_POSTS_DB_ID")

notion = NotionClient(auth=NOTION_API_KEY)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def db_query(database_id: str, payload: dict) -> dict:
    """POST to /v1/databases/{id}/query — notion-client v3 dropped this method."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=NOTION_HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise Exception(f"Notion query error {e.code}: {e.read().decode()}")


# ---------------------------------------------------------------------------
# Notion helpers
# ---------------------------------------------------------------------------

def get_page_text(page_id: str) -> str:
    """Concatenate all block text from a page body."""
    text_parts = []
    cursor = None

    while True:
        kwargs = {"block_id": page_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor

        response = notion.blocks.children.list(**kwargs)

        for block in response.get("results", []):
            block_type = block.get("type", "")
            rich_text_block = block.get(block_type, {}).get("rich_text", [])
            if rich_text_block:
                text_parts.append("".join(rt.get("plain_text", "") for rt in rich_text_block))

        if not response.get("has_more"):
            break
        cursor = response.get("next_cursor")

    return "\n".join(text_parts).strip()


def get_rich_text_value(prop: dict) -> str:
    parts = prop.get("rich_text", [])
    return "".join(p.get("plain_text", "") for p in parts)


def get_number_value(prop: dict):
    return prop.get("number")


def get_title_value(prop: dict) -> str:
    parts = prop.get("title", [])
    return "".join(p.get("plain_text", "") for p in parts)


# ---------------------------------------------------------------------------
# Fetch data from Notion
# ---------------------------------------------------------------------------

def fetch_unprocessed_guides() -> list:
    """Return guides with Status=Published and Posts Generated=False."""
    print("Fetching guides with Status=Published and Posts Generated=unchecked...")
    response = db_query(GUIDES_DB, {
        "filter": {
            "and": [
                {"property": "Status", "select": {"equals": "Published"}},
                {"property": "Posts Generated", "checkbox": {"equals": False}},
            ]
        }
    })
    guides = response.get("results", [])
    print(f"  Found {len(guides)} guide(s) to process.")
    return guides


def fetch_finalized_posts(limit: int = 10) -> list:
    """Return the post content of the last N finalized LinkedIn posts (style reference)."""
    try:
        response = db_query(LINKEDIN_POSTS_DB, {
            "filter": {"property": "Status", "select": {"equals": "Finalized"}},
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
            "page_size": limit,
        })
        posts = []
        for page in response.get("results", []):
            props = page.get("properties", {})
            content = get_rich_text_value(props.get("Post Content", {}))
            if content:
                posts.append(content)
        return posts
    except Exception:
        return []


def fetch_post_analytics(limit: int = 10) -> list:
    """Return analytics from the last N published posts that have impressions data."""
    try:
        response = db_query(LINKEDIN_POSTS_DB, {
            "filter": {
                "and": [
                    {"property": "Status", "select": {"equals": "Published"}},
                    {"property": "Impressions", "number": {"is_not_empty": True}},
                ]
            },
            "sorts": [{"timestamp": "last_edited_time", "direction": "descending"}],
            "page_size": limit,
        })
        analytics = []
        for page in response.get("results", []):
            props = page.get("properties", {})
            analytics.append({
                "title":           get_title_value(props.get("Title", {})),
                "impressions":     get_number_value(props.get("Impressions", {})),
                "engagements":     get_number_value(props.get("Engagements", {})),
                "engagement_rate": get_number_value(props.get("Engagement Rate", {})),
                "clicks":          get_number_value(props.get("Clicks", {})),
                "ctr":             get_number_value(props.get("Click-through Rate", {})),
                "reactions":       get_number_value(props.get("Reactions", {})),
                "comments":        get_number_value(props.get("Comments", {})),
                "reposts":         get_number_value(props.get("Reposts", {})),
                "notes":           get_rich_text_value(props.get("Notes", {})),
            })
        return analytics
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Build the Claude prompt
# ---------------------------------------------------------------------------

def load_instructions() -> str:
    instructions_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
    with open(instructions_path, "r") as f:
        return f.read().strip()


def fmt(value, suffix: str = ""):
    if value is None:
        return None
    return f"{value}{suffix}"


def build_prompt(guide_content: str, finalized_posts: list, post_analytics: list) -> str:
    instructions = load_instructions()

    sections = []
    sections.append("You are writing LinkedIn posts for Spike.sh, an incident management platform.\n")

    sections.append("[INSTRUCTIONS]")
    sections.append(instructions)

    if finalized_posts:
        sections.append("\n[STYLE REFERENCES - Last 10 finalized posts]")
        for i, post in enumerate(finalized_posts, 1):
            sections.append(f"\n--- Post {i} ---\n{post}")

    if post_analytics:
        sections.append("\n[ANALYTICS CONTEXT - Recent published post performance]")
        for a in post_analytics:
            parts = [f'"{a["title"]}"']
            for label, val, suffix in [
                ("Impressions",     a["impressions"],     ""),
                ("Engagements",     a["engagements"],     ""),
                ("Engagement rate", a["engagement_rate"], "%"),
                ("Clicks",          a["clicks"],          ""),
                ("CTR",             a["ctr"],             "%"),
                ("Reactions",       a["reactions"],       ""),
                ("Comments",        a["comments"],        ""),
                ("Reposts",         a["reposts"],         ""),
            ]:
                formatted = fmt(val, suffix)
                if formatted is not None:
                    parts.append(f"{label}: {formatted}")
            if a["notes"]:
                parts.append(f"Note: {a['notes']}")
            sections.append(" | ".join(parts))

    sections.append("\n[SOURCE MATERIAL]")
    sections.append(f"Guide:\n{guide_content}")

    sections.append(
        "\nNow extract all the sharp, distinct ideas from this guide and write one LinkedIn post per idea. "
        "Extract as many posts as the guide genuinely supports. Stop when there are no more sharp ideas worth a standalone post.\n\n"
        "For each post, output:\n"
        "POST 1:\n[post content]\n---\n"
        "POST 2:\n[post content]\n---\n"
        "...and so on."
    )

    return "\n\n".join(sections)


# ---------------------------------------------------------------------------
# Parse Claude response
# ---------------------------------------------------------------------------

def parse_posts(response_text: str) -> list:
    """Extract individual posts from Claude's formatted response."""
    posts = []
    for chunk in response_text.split("---"):
        chunk = chunk.strip()
        if not chunk:
            continue
        lines = chunk.splitlines()
        if lines and lines[0].strip().upper().startswith("POST "):
            lines = lines[1:]
        content = "\n".join(lines).strip()
        if content:
            posts.append(content)
    return posts


# ---------------------------------------------------------------------------
# Hook alternatives (Feature 4)
# ---------------------------------------------------------------------------

def generate_hook_alternatives(post_content: str) -> list:
    """Ask Claude to rewrite the opening hook 3 ways. Returns list of 3 strings."""
    first_line = post_content.splitlines()[0].strip()
    prompt = (
        f"Here is a LinkedIn post:\n\n{post_content}\n\n"
        "Rewrite only the opening hook (the very first line) in 3 different ways. "
        "Each hook should be counter-intuitive, specific, or thought-provoking — "
        "and make the reader want to continue reading. Keep the same topic and idea. "
        "Do not rewrite the rest of the post.\n\n"
        "Output exactly this format:\n"
        "HOOK 1: [hook]\n"
        "HOOK 2: [hook]\n"
        "HOOK 3: [hook]"
    )
    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    hooks = []
    for line in raw.splitlines():
        line = line.strip()
        if line.upper().startswith("HOOK 1:"):
            hooks.append(line[7:].strip())
        elif line.upper().startswith("HOOK 2:"):
            hooks.append(line[7:].strip())
        elif line.upper().startswith("HOOK 3:"):
            hooks.append(line[7:].strip())
    # Fall back to original if parsing fails
    while len(hooks) < 3:
        hooks.append(first_line)
    return hooks


def pick_hook(post_content: str, post_number: int) -> str:
    """Show hook options for a post and return the post with the chosen hook."""
    first_line = post_content.splitlines()[0].strip()
    rest = "\n".join(post_content.splitlines()[1:])

    print(f"\n  Generating hook alternatives for Post {post_number}...")
    hooks = generate_hook_alternatives(post_content)

    print(f"\n  POST {post_number} — current hook:")
    print(f"    0. {first_line}")
    print(f"  Alternatives:")
    for i, hook in enumerate(hooks, 1):
        print(f"    {i}. {hook}")

    while True:
        choice = input(f"  Pick a hook for Post {post_number} (0=original, 1/2/3): ").strip()
        if choice == "0":
            return post_content
        elif choice in ("1", "2", "3"):
            chosen_hook = hooks[int(choice) - 1]
            return (chosen_hook + "\n" + rest).strip()
        else:
            print("  Enter 0, 1, 2, or 3.")


# ---------------------------------------------------------------------------
# Write posts back to Notion
# ---------------------------------------------------------------------------

def write_posts_to_notion(posts: list, guide_page_id: str, guide_title: str):
    print(f"\nWriting {len(posts)} post(s) to Notion LinkedIn Posts database...")
    for i, post_content in enumerate(posts, 1):
        title = f"{guide_title} — Post {i}"
        notion.pages.create(
            parent={"database_id": LINKEDIN_POSTS_DB},
            properties={
                "Title": {"title": [{"text": {"content": title}}]},
                "Post Content": {"rich_text": [{"text": {"content": post_content}}]},
                "Status": {"select": {"name": "Generated"}},
                "Linked Guide": {"relation": [{"id": guide_page_id}]},
            },
        )
        print(f"  Created: {title}")


def mark_posts_generated(guide_page_id: str):
    notion.pages.update(
        page_id=guide_page_id,
        properties={"Posts Generated": {"checkbox": True}},
    )
    print("  Marked guide 'Posts Generated' = checked.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_guide(guide: dict):
    props = guide.get("properties", {})
    guide_id = guide["id"]
    guide_title = get_title_value(props.get("Title", {})) or "Untitled"

    print(f"\n{'='*60}")
    print(f"Processing guide: {guide_title}")
    print(f"{'='*60}")

    print("  Fetching guide content...")
    guide_content = get_page_text(guide_id)
    if not guide_content:
        print("  Warning: guide body is empty. Skipping.")
        return
    print(f"  Guide fetched ({len(guide_content)} chars).")

    print("  Fetching finalized posts for style reference...")
    finalized_posts = fetch_finalized_posts(limit=10)
    if finalized_posts:
        print(f"  Found {len(finalized_posts)} finalized post(s) for style context.")
    else:
        print("  No finalized posts yet, skipping style reference.")

    print("  Fetching published post analytics...")
    post_analytics = fetch_post_analytics(limit=10)
    if post_analytics:
        print(f"  Found {len(post_analytics)} post(s) with analytics.")
    else:
        print("  No post analytics yet, skipping.")

    print("\n  Building prompt and calling Claude API...")
    prompt = build_prompt(guide_content, finalized_posts, post_analytics)

    message = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = message.content[0].text
    print("  Claude response received.")

    posts = parse_posts(response_text)
    print(f"\n  Extracted {len(posts)} post(s).")

    # Show all posts first
    print("\n" + "-" * 60)
    print("GENERATED POSTS:")
    print("-" * 60)
    for i, post in enumerate(posts, 1):
        print(f"\nPOST {i}:\n{post}\n---")

    # Hook selection pass
    print("\n" + "-" * 60)
    print("HOOK SELECTION:")
    print("For each post, pick the opening hook you want (or keep the original).")
    print("-" * 60)
    final_posts = []
    for i, post in enumerate(posts, 1):
        final_post = pick_hook(post, i)
        final_posts.append(final_post)

    # Final confirmation
    print("\n" + "-" * 60)
    print("FINAL POSTS (with chosen hooks):")
    print("-" * 60)
    for i, post in enumerate(final_posts, 1):
        print(f"\nPOST {i}:\n{post}\n---")

    print()
    answer = input("Write these to Notion? (y/n): ").strip().lower()
    if answer != "y":
        print("  Skipped. Nothing written to Notion.")
        return

    write_posts_to_notion(final_posts, guide_id, guide_title)
    mark_posts_generated(guide_id)
    print(f"  Done with: {guide_title}")


def main():
    print("Spike.sh LinkedIn Post Generator")
    print("=" * 60)

    missing = [v for v in ["ANTHROPIC_API_KEY", "NOTION_API_KEY", "NOTION_GUIDES_DB_ID",
                            "NOTION_LINKEDIN_POSTS_DB_ID"] if not os.getenv(v)]
    if missing:
        print(f"Error: missing required environment variables: {', '.join(missing)}")
        sys.exit(1)

    guides = fetch_unprocessed_guides()

    if not guides:
        print("Nothing to process. All published guides already have posts generated.")
        return

    for guide in guides:
        try:
            process_guide(guide)
        except KeyboardInterrupt:
            print("\nInterrupted.")
            sys.exit(0)
        except Exception as e:
            title = get_title_value(guide.get("properties", {}).get("Title", {})) or guide["id"]
            print(f"\nError processing guide '{title}': {e}")
            print("Continuing to next guide...\n")

    print("\nAll guides processed.")


if __name__ == "__main__":
    main()
