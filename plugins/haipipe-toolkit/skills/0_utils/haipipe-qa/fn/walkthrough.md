fn/walkthrough -- One-issue-at-a-time resolution loop
=====================================================

Prerequisite: QA_ISSUES.md exists (from fn/discover.md or a previous session).

Procedure
---------

### Step 0 -- Load state

Read `<target>/QA_ISSUES.md`. Parse all issues. Identify which are OPEN.
If none are OPEN, report "all issues resolved" and exit.

### Step 1 -- Present the next OPEN issue

Find the first issue with status OPEN. Present it using this exact format:

```
## Q{N} of {TOTAL}: {title}  [{severity}]

**Where:** `{file}:{line}`

**Problem:** {1-2 sentences, no jargon}

**Evidence:**
```
{the actual code or data snippet -- 3-10 lines max}
```

**Impact:** {what breaks if not fixed, in concrete terms}

**Suggested fix:** {the specific edit}

What do you want to do?
```

Then STOP. Do not present the next issue. Do not fix anything yet.
Wait for the user's response.

### Step 2 -- Act on user response

| User says | Action |
|-----------|--------|
| "fix" / "yes" / "go ahead" | Apply the suggested fix. Show the diff. Mark FIXED in QA_ISSUES.md. |
| "skip" / "no" / "leave it" | Mark SKIPPED in QA_ISSUES.md. Note the user's reason if given. |
| "discuss" / "why?" / "explain" | Give deeper explanation. Re-present with more context. Stay on same issue. |
| "fix all" / "just do them all" | Batch-apply all remaining OPEN issues. Show summary of changes. |
| a specific alternative fix | Apply what the user said instead. Mark FIXED with note. |

### Step 3 -- Confirm and advance

After fixing or skipping:
- Show one-line confirmation: "Q{N}: {FIXED|SKIPPED}. {remaining} issues left."
- Go back to Step 1 with the next OPEN issue.

### Step 4 -- Final summary

When all issues are resolved (no OPEN remaining):

```
QA Complete: <target>
  Fixed:     N
  Skipped:   N
  Discussed: N (resolved as fixed or skipped)
  Total:     N

Files changed:
  {list of files modified during this walkthrough}
```

Update QA_ISSUES.md with final status for each issue.


Rules
-----

1. ONE issue per turn. Never present two issues in the same message.
2. Always show evidence (the actual code). Never describe a bug abstractly.
3. The suggested fix must be concrete enough to apply immediately.
4. If the user gives context that changes the assessment, update the issue.
5. Keep the conversation focused. If the user asks an unrelated question,
   answer it, then say "Back to Q{N}:" and re-present.
6. If a fix for Q{N} also resolves Q{M}, note it: "This also fixes Q{M}."
   Mark both as FIXED.
