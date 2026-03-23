---
name: generate-email
description: "Generates marketing emails for Spike guides. Fetches unprocessed guides from Notion, generates one email per guide, and writes them to the Emails DB in Notion."
argument-hint: "[guide-title or leave blank for auto-detect]"
---

# /generate-email

Generate marketing emails for Spike.sh guides. Fetches guides where Email Generated is unchecked, generates one email per guide, and writes them to the Emails DB in Notion. Each email's job is to drive clicks to the guide link.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Fetch Unprocessed Guides

Query the Guides DB for pages where:
- `Email Generated = unchecked`

If no guides are found, tell the user and stop.

If `[guide-title]` was passed as an argument, process only that guide. Otherwise process all unprocessed guides sequentially.

---

### Step 2: For Each Guide — Gather Context

For each guide:

1. Fetch the full guide page content from Notion, including the `URL` field (the public spike.sh guide URL — used as the CTA link)
2. **Check that the URL field is not empty and starts with `http://` or `https://`.** If it is empty or does not start with a valid scheme, stop processing this guide and tell the user:
   ```
   Guide "[title]" has no valid URL set in the Guides DB. Email would have a broken CTA link.
   Add the URL to the Guides DB and re-run to process this guide.
   ```
   Do not mark it as Email Generated. Move to the next guide if there are others.
3. Read `email-instructions.txt` — the full email writing brief. Follow it exactly.
4. Read `opinions.md` — opinions extracted from processed guides. Note which opinions are most relevant to this guide's topic; use them when writing the email.
5. Read `email-edit-log.md` — patterns extracted from past user edits on emails. Apply every pattern to the email generated. These represent real corrections and take precedence when they conflict with a first instinct.

If the guide body is empty, skip it and move to the next one.

---

### Step 3: Generate Email

Using the guide content, `email-instructions.txt`, and relevant opinions from `opinions.md`:

- Read the full guide and identify the single most compelling idea — the one with the strongest bait potential
- Write one email built around that idea
- Generate: subject line, preview text, email body, CTA text
- Follow all rules in `email-instructions.txt` strictly

---

### Step 4: Write to Notion

1. Search the Emails DB for any existing email whose title starts with `{Guide Title}`. If any exist, stop and warn the user:
   ```
   An email for "[Guide Title]" already exists in Notion. Skipping to avoid duplicates.
   If you want to regenerate, manually delete the existing email and uncheck Email Generated in the Guides DB.
   ```
2. Write the email to the Emails DB in Notion:
   - Title: `{Guide Title}`
   - Subject Line: the generated subject line
   - Preview Text: the generated preview text
   - Email Body: the full email body text
   - CTA Text: the generated CTA text
   - Guide URL: the guide's public URL
   - Status: `Generated`
   - Linked Guide: `["https://www.notion.so/{guide-page-id-no-dashes}"]`

   If the write fails, stop immediately. Do NOT mark the guide as Email Generated. Tell the user what failed.
3. Only after the email is written successfully: Mark the guide `Email Generated = true` in Notion
4. Tell the user:

```
Email generated — [Guide Title]

Subject: [subject line]
Preview: [preview text]

Next: Review in Notion → add inline comments if needed → run /apply-email-edits to apply → change to Approved → send via SendGrid.
```

---

## Important Rules

- Never write to Notion until the duplicate check passes
- Never mark a guide as Email Generated = true unless the email was successfully written to Notion
- Skip guides with empty content and move to the next one
- Read `email-instructions.txt` and `opinions.md` fresh on every run — never rely on cached memory
- Linked Guide relation format: JSON array of page URLs — `["https://www.notion.so/{page-id-no-dashes}"]`
- One email per guide — pick the single strongest idea, not multiple
- Process one guide at a time when multiple are unprocessed — do not batch them in parallel
