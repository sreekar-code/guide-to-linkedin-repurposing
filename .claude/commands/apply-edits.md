---
name: apply-edits
description: "Applies user edits to LinkedIn posts. Scans all Generated posts for unresolved inline comments (threads with no 'Applied.' reply), applies the requested changes, and replies 'Applied.' to each thread. Status stays Generated throughout."
argument-hint: ""
---

# /apply-edits

Apply pending edits to LinkedIn posts. Scans all `Generated` posts for unresolved comment threads, applies the changes, and replies "Applied." to each thread. No status change needed from you.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Find Posts With Unresolved Comments

1. Search the LinkedIn Posts DB to retrieve every post page. Do not rely on post IDs from session memory. If the search returns `has_more: true`, continue fetching with `next_cursor` until all pages are retrieved. For each post returned, fetch its page to read the `Status` property. Collect only posts where `Status = Generated`.
2. For each Generated post, fetch comments using `get_comments` with `include_all_blocks: true`
3. A post has **unresolved comments** if it has at least one comment thread where none of the replies contain "Applied."
4. Collect only posts with unresolved comments

If none found, tell the user: "No Generated posts have unresolved comments." and stop.

List the posts found:
```
Found N post(s) with unresolved comments:
- [Post Title] (N unresolved thread(s))
- [Post Title] (N unresolved thread(s))
...
```

---

### Step 2: For Each Post — Apply Edits

For each post with unresolved comments:

1. Fetch the full post page content from Notion (to get the current Post Content)
2. Read through all unresolved comment threads — these are the edit instructions
3. Skip any thread that already has an "Applied." reply (already handled in a previous run)

**Applying edits:**
- Treat each unresolved comment as a specific instruction to change something in the post
- Apply every comment's requested change to the post content
- If a comment is ambiguous, use judgment to make the most reasonable interpretation — do not ask for clarification mid-run
- Preserve everything not mentioned in the comments (structure, tone, word count, all rules from `instructions.txt`)
- After applying edits, read `instructions.txt` fresh and verify the post complies with all its rules — word count, tone, banned words, format, hashtags, and everything else specified there. Do not hardcode checks here; `instructions.txt` is the single source of truth

4. Update the post's `Post Content` field in Notion with the revised text
5. Reply to each unresolved comment thread with: `Applied.`
6. Status remains `Generated` — do not change it

---

### Step 3: Extract Patterns to edit-log.md

After applying all edits, review every comment that was addressed in this run and extract generalizable writing patterns from them.

For each pattern:
- State it as a rule that applies to future posts, not as a description of what was fixed
- Check `edit-log.md` first — if the same underlying pattern is already captured, skip it or update the existing entry rather than adding a duplicate
- Add new patterns under the `## Writing patterns` section

If no new patterns are extractable (all comments were content-specific with no generalizable lesson), skip this step silently.

---

### Step 4: Report to User

After processing all posts:

```
Edits applied — N post(s) updated

[Post Title]
  Comments addressed: N

[Post Title]
  Comments addressed: N

Note: Comments remain open in Notion — resolve them manually once you've reviewed the changes.
```

---

## Important Rules

- Only act on threads with no "Applied." reply — skip already-handled threads
- Never change content that wasn't mentioned in a comment
- Apply edits faithfully — do not rewrite the post beyond what the comment requests
- If an edit would violate `instructions.txt` rules, fix the violation while honoring the spirit of the edit
- Do not change the post's status — it stays `Generated`
- Process posts one at a time, sequentially
