---
name: apply-email-edits
description: "Applies user edits to generated emails. Scans all Generated emails for unresolved inline comments, applies the requested changes, and replies 'Applied.' to each thread. Status stays Generated throughout."
argument-hint: ""
---

# /apply-email-edits

Apply pending edits to generated emails. Scans all `Generated` emails for unresolved comment threads, applies the changes, and replies "Applied." to each thread. No status change needed from you.

## Notion Database IDs
See `AGENTS.md` for database IDs and schema details.

---

## Workflow

### Step 1: Find Emails With Unresolved Comments

1. Search the Emails DB to retrieve every email page. Do not rely on IDs from session memory. For each email returned, fetch its page to read the `Status` property. Collect only emails where `Status = Generated`.
2. For each Generated email, fetch comments using `get_comments` with `include_all_blocks: true`
3. An email has **unresolved comments** if it has at least one comment thread where none of the replies contain "Applied."
4. Collect only emails with unresolved comments

If none found, tell the user: "No Generated emails have unresolved comments." and stop.

List the emails found:
```
Found N email(s) with unresolved comments:
- [Email Title] (N unresolved thread(s))
...
```

---

### Step 2: For Each Email — Apply Edits

For each email with unresolved comments:

1. Fetch the full email page from Notion (to get current Subject Line, Preview Text, Email Body, CTA Text)
2. Read through all unresolved comment threads — these are the edit instructions
3. Skip any thread that already has an "Applied." reply

**Applying edits:**
- Treat each unresolved comment as a specific instruction to change something in the email
- Apply every comment's requested change to the appropriate field (Subject Line, Preview Text, Email Body, or CTA Text)
- If a comment is ambiguous, use judgment to make the most reasonable interpretation — do not ask for clarification mid-run
- Preserve everything not mentioned in the comments
- After applying edits, read `email-instructions.txt` fresh and verify the email complies with all its rules — word count, tone, banned words, and everything else specified there. Do not hardcode checks here; `email-instructions.txt` is the single source of truth

4. Update the email's fields in Notion with the revised text
5. Reply to each unresolved comment thread with: `Applied.`
6. Status remains `Generated` — do not change it

---

### Step 3: Extract Patterns to email-edit-log.md

After applying all edits, review every comment that was addressed in this run and extract generalizable writing patterns from them.

For each pattern:
- State it as a rule that applies to future emails, not as a description of what was fixed
- Check `email-edit-log.md` first — if the same underlying pattern is already captured, skip it or update the existing entry rather than adding a duplicate

If no new patterns are extractable (all comments were content-specific with no generalizable lesson), skip this step silently.

---

### Step 4: Report to User

After processing all emails:

```
Edits applied — N email(s) updated

[Email Title]
  Comments addressed: N

Note: Comments remain open in Notion — resolve them manually once you've reviewed the changes.
```

---

## Important Rules

- Only act on threads with no "Applied." reply — skip already-handled threads
- Never change content that wasn't mentioned in a comment
- Apply edits faithfully — do not rewrite the email beyond what the comment requests
- If an edit would violate `email-instructions.txt` rules, fix the violation while honoring the spirit of the edit
- Do not change the email's status — it stays `Generated`
- Process emails one at a time, sequentially
