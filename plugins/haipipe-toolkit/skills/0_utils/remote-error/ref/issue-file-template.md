# The issue-00N story file

One file per failure, at
`_WorkSpace/0-CMS-Store/Issue-From-CMS-Server/<YYMMDD>/issue-00N-<slug>.md`.

The counter `00N` restarts inside each day folder. The `<slug>` is 3 to 6 words,
lowercase, hyphenated, and names the MECHANISM, not the file it happened in:
`forvalues-brace-r198`, not `step-01-broke`.

Six headings, in this order. Do not add a seventh; the register and the day's
`FINDINGS.md` carry everything else.

---

```markdown
# issue-00N — <one line, the mechanism, no more than 12 words>

- **Recorded:** 2026-MM-DD
- **Severity:** 🔴 blocks the run at step NN, before any data is read
- **Found by:** running on the CMS server (<person>)
- **Session:** <the session name, verbatim: C-LBP, D-CABG, C01-R01-13>
- **Status:** FIXED in the repo YYMMDD, NOT yet re-run on the server

## Symptom

The pasted text, verbatim, in a fenced block. Never a paraphrase, because the
next person greps for this string.

Then one or two sentences on what is CONFUSING about it: what looked fine, what
a person would check first and find correct.

## Cause

The mechanism. Quote the line of code with its file:line. If an outside source
settles it (StataCorp, a manual page, a statalist thread), link it.

## Fix

```stata
// wrong
<the line as it was>

// right
<the line as it is now>
```

One sentence on the rule this generalizes to, and one on where the rule does
NOT apply, so a later sweep does not over-apply it.

## Scope of the repair, YYMMDD

How many lines, in which files, across which pipelines. A reader who wants to
audit the sweep uses this section as the list.

## Not affected

The code that carries a similar-looking pattern and is fine, with the reason.
This section is what stops the next reader re-fixing working code.
```

---

## Three rules the template cannot enforce

0. **The Session line is the only trace back to the reasoning.** The files here
   say WHAT changed; the chat that produced them says why every other candidate
   was rejected. One session per remote step is what keeps that findable.

1. **The Symptom block is verbatim.** Retyping it from memory loses the exact
   token that a future grep needs.
2. **Status stays 🟠 FIXED until a server run proves it.** The laptop has no
   Stata and no CMS data, so nothing written from the laptop is ✅ CLOSED.
