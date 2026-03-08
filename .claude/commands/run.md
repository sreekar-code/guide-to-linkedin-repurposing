---
name: run
description: "Master pipeline command. Scans the full queue — Generated posts with unresolved comments, image prompts, and unprocessed guides — and handles everything in one run. Processes in order: apply edits → generate image prompts → generate posts for new guides."
argument-hint: ""
---

# /run

Scan everything pending and handle it all in one run. No need to run individual commands separately.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Step 1: Scan the Queue

Query the Notion DBs in parallel and collect what's pending:

1. **Posts with unresolved comments** — LinkedIn Posts DB, `Status = Generated`. For each, fetch comments and check for threads with no "Applied." reply. Count only posts that have at least one unresolved thread.
2. **Posts approved for image prompts** — LinkedIn Posts DB, `Status = Approved`
3. **Unprocessed guides** — Guides DB, `Posts Generated = unchecked`

Report the queue to the user:

```
Queue scan complete

Posts with unresolved comments:  N post(s)
Approved (image prompts to gen): N post(s)
New guides to process:           N guide(s)
```

If everything is empty, tell the user: "Nothing pending. Queue is clear." and stop.

---

## Step 2: Apply Edits

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
Edits applied — N post(s) updated
```

---

## Step 3: Generate Image Prompts

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

## Step 4: Generate Posts for New Guides

If there are unprocessed guides, process them now — one at a time, sequentially.

Follow the full logic in `.claude/commands/generate-posts.md` exactly:
- Gather context (guide content, URL, Published posts, instructions.txt, opinions.md)
- Generate draft posts
- Run the 5-persona review board
- Apply rewrites if needed (max 2 rounds)
- Write passing posts to Notion, mark guide done, append opinions to opinions.md

---

## Final Summary

After all steps complete:

```
Run complete

Edits applied:        N post(s)
Image prompts gen'd:  N post(s)  → Ready to publish
New posts written:    N post(s) across N guide(s)

Nothing pending.
```

If any step produced a PAUSE (e.g. generate-posts failed after 2 rounds), surface that to the user and wait for their response before continuing to the next step.

---

## Important Rules

- Always scan the full queue first before doing any work
- Process in order: edits → image prompts → new guides. Do not reorder.
- If a step has nothing to process, skip it silently and move to the next
- If generate-posts hits a PAUSE state (2 failed rounds), stop and ask the user before continuing with remaining guides
- Individual commands (`/apply-edits`, `/generate-image-prompts`, `/generate-posts`) remain available for targeted runs
