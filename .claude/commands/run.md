---
name: run
description: "Master pipeline command. Scans the full queue — posts/emails with unresolved comments, image prompts, unprocessed guides — and handles everything in one run. Processes in order: apply post edits → apply email edits → generate image prompts → generate posts → generate emails."
argument-hint: ""
---

# /run

Scan everything pending and handle it all in one run. No need to run individual commands separately.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Step 1: Scan the Queue

Query the Notion DBs in parallel and collect what's pending:

1. **All posts in the LinkedIn Posts DB** — Search the LinkedIn Posts DB to retrieve every post page. Do not rely on post IDs from session memory. If the search returns `has_more: true`, continue fetching with `next_cursor` until all pages are retrieved. For each post returned, fetch its page to read the `Status` property, then:
   - `Status = Generated`: fetch its comments using `get_comments` with `include_all_blocks: true`, and check for threads with no "Applied." reply. If at least one unresolved thread exists, add to the "post unresolved comments" list.
   - `Status = Approved`: add to the "approved for image prompts" list.
   - Any other status (`Ready to publish`, `Published`, etc.): skip.
2. **All emails in the Emails DB** — Search the Emails DB to retrieve every email page. For each email returned, fetch its page to read the `Status` property, then:
   - `Status = Generated`: fetch its comments using `get_comments` with `include_all_blocks: true`, and check for threads with no "Applied." reply. If at least one unresolved thread exists, add to the "email unresolved comments" list.
   - Any other status: skip.
3. **Unprocessed guides (posts)** — Guides DB, `Posts Generated = unchecked`
4. **Unprocessed guides (emails)** — Guides DB, `Email Generated = unchecked`

Report the queue to the user:

```
Queue scan complete

Posts with unresolved comments:  N post(s)
Emails with unresolved comments: N email(s)
Approved (image prompts to gen): N post(s)
New guides (posts to gen):       N guide(s)
New guides (emails to gen):      N guide(s)
```

If everything is empty, tell the user: "Nothing pending. Queue is clear." and stop.

---

## Step 2: Apply Post Edits

If there are `Generated` posts with unresolved comment threads, process them now.

Follow the full logic in `.claude/commands/apply-edits.md` exactly:
- For each post, read all comment threads — skip any with an "Applied." reply
- Apply every unresolved comment's requested change to the post content
- Verify the edited post still complies with `instructions.txt` rules
- Update `Post Content` in Notion
- Reply "Applied." to each unresolved comment thread
- Status stays `Generated` — do not change it

When done, report:
```
Post edits applied — N post(s) updated
```

---

## Step 3: Apply Email Edits

If there are `Generated` emails with unresolved comment threads, process them now.

Follow the full logic in `.claude/commands/apply-email-edits.md` exactly:
- For each email, read all comment threads — skip any with an "Applied." reply
- Apply every unresolved comment's requested change to the email fields
- Verify the edited email still complies with `email-instructions.txt` rules
- Update the email fields in Notion
- Reply "Applied." to each unresolved comment thread
- Status stays `Generated` — do not change it

When done, report:
```
Email edits applied — N email(s) updated
```

---

## Step 4: Generate Image Prompts

If there are posts with `Status = Approved`, process them now.

Follow the full logic in `.claude/commands/generate-image-prompts.md` exactly:
- Read `image-guide.md` in full
- For each post, read the Post Content and generate a tailored image prompt
- Write the prompt to the `Image Prompt` column
- Set status to `Ready to publish`

When done, report:
```
Image prompts generated — N post(s) updated
```

---

## Step 5: Generate Posts for New Guides

If there are guides with `Posts Generated = unchecked`, process them now — one at a time, sequentially.

Follow the full logic in `.claude/commands/generate-posts.md` exactly:
- Gather context (guide content, URL, Published posts, instructions.txt, opinions.md, edit-log.md)
- Generate posts
- Write directly to Notion, mark guide done, append opinions to opinions.md

---

## Step 6: Generate Emails for New Guides

If there are guides with `Email Generated = unchecked`, process them now — one at a time, sequentially.

Follow the full logic in `.claude/commands/generate-email.md` exactly:
- Gather context (guide content, URL, email-instructions.txt, opinions.md, email-edit-log.md)
- Generate one email per guide
- Write to Notion, mark guide done

---

## Final Summary

After all steps complete:

```
Run complete

Post edits applied:   N post(s)
Email edits applied:  N email(s)
Image prompts gen'd:  N post(s)  → Ready to publish
New posts written:    N post(s) across N guide(s)
New emails written:   N email(s) across N guide(s)

Nothing pending.
```

---

## Important Rules

- Always scan the full queue first before doing any work
- Process in order: post edits → email edits → image prompts → new posts → new emails. Do not reorder.
- If a step has nothing to process, skip it silently and move to the next
- Individual commands (`/apply-edits`, `/apply-email-edits`, `/generate-image-prompts`, `/generate-posts`, `/generate-email`) remain available for targeted runs
