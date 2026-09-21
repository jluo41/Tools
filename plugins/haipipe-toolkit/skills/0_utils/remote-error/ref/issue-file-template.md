# Remote error report template

This is an engine-neutral report shape. The selected profile supplies the
register path, issue ID grammar, status vocabulary, and any required headings.
When no profile matches, use a user-provided register path and identify any
profile-specific fields that are unavailable; do not invent them.

---

````markdown
# <issue ID or `unassigned`> — <mechanism, no more than 12 words>

- **Recorded:** YYYY-MM-DD
- **Environment:** <remote environment or profile name>
- **Impact:** <what the failure blocks or changes>
- **Found by:** <person or process>
- **Session:** <debugging-round name, verbatim>
- **Remote Run ID:** <actual Run ID, or `N/A` when none is known>
- **Status:** <what changed and what verification remains>

## Symptom

The pasted text, verbatim, in a fenced block. Never paraphrase the error token
that a future reader may need to search for.

Then explain what appeared to work and what the person would check first.

## Cause

Name the mechanism and quote the relevant code with its file and line. Link any
outside source needed to establish the cause.

## Fix

```text
Before:
<the relevant old behavior>

After:
<the relevant corrected behavior>
```

State the rule the fix generalizes to and where it does not apply.

## Scope of the repair, YYYY-MM-DD

List affected files, lines, units, and copies so another reader can audit the
change.

## Not affected

Name similar-looking code that is safe and explain why it was not changed.
````

---

## Template rules

1. The **Session** field identifies the debugging conversation. It is not a
   Run ID and does not create a Run.
2. The **Remote Run ID** field refers only to an actual remote Run identity. If
   the error came from an untracked command or no ID is available, write `N/A`.
3. A profile may define a concrete path, issue ID format, status terms, and
   static gate. Never copy CMS/Stata conventions into an unrelated profile.
4. Status records what has been verified. A local code change cannot claim a
   successful re-run on an inaccessible remote machine.
