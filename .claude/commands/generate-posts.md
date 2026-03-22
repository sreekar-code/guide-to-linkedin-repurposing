---
name: generate-posts
description: "Full LinkedIn post pipeline. Fetches unprocessed Spike guides from Notion, generates posts, and writes them directly to Notion. No review round."
argument-hint: "[guide-title or leave blank for auto-detect]"
---

# /generate-posts

Run the full LinkedIn post generation pipeline for Spike.sh. Fetches unprocessed guides from Notion, generates click-driven posts designed to lure readers into clicking the guide link, and writes them directly to Notion. The posts do not need to educate — the guide does that. Each post's job is to grab attention, build curiosity, and drive the click.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Fetch Unprocessed Guides

Query the Guides DB for pages where:
- `Posts Generated = unchecked`

If no guides are found, tell the user and stop.

If `[guide-title]` was passed as an argument, process only that guide. Otherwise process all unprocessed guides sequentially.

---

### Step 2: For Each Guide — Gather Context

For each guide:

1. Fetch the full guide page content from Notion, including the `URL` field (the public spike.sh guide URL — used in the P.S. of each post)
2. **Check that the URL field is not empty and starts with `http://` or `https://`.** If it is empty or does not start with a valid scheme, stop processing this guide and tell the user:
   ```
   Guide "[title]" has no valid URL set in the Guides DB. Posts would have a broken P.S. link.
   Add the URL to the Guides DB and re-run to process this guide.
   ```
   Do not mark it as Posts Generated. Move to the next guide if there are others.
3. Fetch the last 10 **Published** posts from the LinkedIn Posts DB — use as style reference. Skip if none.
4. Read `instructions.txt` — the full writing brief. Follow it exactly.
5. Read `opinions.md` — a growing list of opinions extracted from previously processed guides. Note which opinions are most relevant to this guide's topic; use them when writing posts.
6. Read `edit-log.md` — patterns extracted from past user edits. Apply every pattern in this file to every post generated. These represent real corrections and take precedence when they conflict with a first instinct.

If the guide body is empty, skip it and move to the next one.

---

### Step 3: Generate Posts

Using the guide content, style references, `instructions.txt`, and relevant opinions from `opinions.md`:

- Extract every idea from the guide that can be turned into compelling bait — something surprising, counterintuitive, or tension-creating
- Write one LinkedIn post per idea. Each post should tease the idea, build curiosity, and leave the reader wanting the full answer from the guide
- Stop when there are no more ideas that would make a reader want to click
- Follow all rules in `instructions.txt` strictly

Label each post: `Post 1`, `Post 2`, etc.

---

### Step 4: Write to Notion

1. Search the LinkedIn Posts DB for any existing posts whose title starts with `{Guide Title} — Post`. If any exist, stop and warn the user:
   ```
   Posts for "[Guide Title]" already exist in Notion. Skipping to avoid duplicates.
   If you want to regenerate, manually delete the existing posts and uncheck Posts Generated in the Guides DB.
   ```
2. Write all posts to the LinkedIn Posts DB in Notion, one at a time:
   - Title: `{Guide Title} — Post {N}`
   - Post Content: the full post text
   - Status: `Generated`
   - Linked Guide: `["https://www.notion.so/{guide-page-id-no-dashes}"]`

   If any individual post write fails, stop immediately. Do NOT mark the guide as Posts Generated. Tell the user which posts were written successfully and which failed, so they can clean up manually before re-running.
3. Only after all posts are written successfully: Mark the guide `Posts Generated = true` in Notion
4. Extract 2-4 sharp opinions from this guide and append them to `opinions.md`:
   - Each opinion is one plain sentence stating a belief the guide supports — not a summary, but a point of view
   - Add a heading with the guide title, then list the opinions as bullets
   - Do not duplicate opinions already in the file. An opinion is a duplicate if it makes the same underlying claim, even in different words — paraphrases count as duplicates
5. Tell the user:

```
Pipeline complete — [Guide Title]

Posts written to Notion: {N}

Next: Review in Notion → add inline comments if needed → run /run to apply edits → change to Approved.
```

---

## Important Rules

- Never write to Notion until the duplicate check passes
- Never mark a guide as Posts Generated = true unless posts were successfully written to Notion
- Skip guides with empty content and move to the next one
- Read `instructions.txt` and `opinions.md` fresh on every run — never rely on cached memory
- Linked Guide relation format: JSON array of page URLs — `["https://www.notion.so/{page-id-no-dashes}"]`
- Process one guide at a time when multiple are unprocessed — do not batch them in parallel
