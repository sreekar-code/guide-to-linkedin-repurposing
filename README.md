# Spike.sh LinkedIn Post Generator

Reads published guides from Notion and uses Claude to generate LinkedIn posts from them.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Edit `.env` and fill in your keys:

```
ANTHROPIC_API_KEY=sk-ant-...
NOTION_API_KEY=secret_...
NOTION_GUIDES_DB_ID=<32-char Notion database ID>
NOTION_TRANSCRIPTS_DB_ID=<32-char Notion database ID>
NOTION_PERPLEXITY_DB_ID=<32-char Notion database ID>
NOTION_LINKEDIN_POSTS_DB_ID=<32-char Notion database ID>
NOTION_WEEKLY_ANALYTICS_DB_ID=<32-char Notion database ID>
```

**Where to find a Notion database ID:**
Open the database in Notion → copy the URL → the ID is the 32-character string after the workspace name and before the `?`. Example:
`https://notion.so/myworkspace/abc123...def456?v=...` → ID is `abc123...def456`

**Notion integration setup:**
1. Go to https://www.notion.so/my-integrations and create an integration.
2. Copy the "Internal Integration Secret" as your `NOTION_API_KEY`.
3. In each Notion database, click ··· → Connections → add your integration.

### 3. Add your writing instructions

Edit `instructions.txt` and replace the placeholder with your actual tone guidelines, post structure rules, and any reference posts.

### 4. Run

```bash
python generate.py
```

The script will:
1. Find all guides with Status = Published and Posts Generated = unchecked
2. Pull in linked transcripts and Perplexity threads (if they exist)
3. Pull in the last 10 finalized LinkedIn posts for style reference (if any exist)
4. Pull in the last 4 weeks of analytics (if any exist)
5. Call Claude and generate posts
6. Print the posts for your review
7. Ask for confirmation before writing anything to Notion

## Notes

- Re-run at any time — guides with Posts Generated already checked are skipped automatically.
- As you finalize posts and log weekly analytics in Notion, the script will start including them as context on future runs.
- The `NOTION_TRANSCRIPTS_DB_ID`, `NOTION_PERPLEXITY_DB_ID`, and `NOTION_WEEKLY_ANALYTICS_DB_ID` variables are optional — if left blank, those sections are skipped gracefully.
