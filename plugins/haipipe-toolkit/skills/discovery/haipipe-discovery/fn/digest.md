---
name: haipipe-discovery-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument (run from a fresh session) -- scanning its transcript for tool/skill feedback (gripes + preferences), distilling discrete items, deduping (merge-or-create), and after a MANDATORY confirm gate routing each through the feedback router into bucket-unit inboxes. The bulk harvester for /haipipe-discovery feedback. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense the session into routed feedback)

Most feedback is given conversationally and never filed. `digest` is the bulk
harvester: it reads a session's transcript, distills the discrete pieces of
TOOL/SKILL feedback you gave, dedups them, and (after you confirm) routes each
into the right bucket-unit inbox. A digest is, by definition, deduped and
condensed -- the same discipline as the merge-or-create capture.

Typical usage: from a FRESH session (clean context), name the PAST session to
harvest -- `/haipipe-discovery digest "Display-for-Opioid-MISQ"`. With no argument
it digests the CURRENT session instead. Running from a fresh session is what keeps
the digest's judgment uncontaminated by the work it is reviewing.

Relation to `feedback`. `digest` HARVESTS; `feedback` ROUTES + MERGES. digest
REUSES `fn/feedback.md` for everything downstream of distillation: the
keyword->unit map, the cross-cutting guard, and the merge-or-create capture. No
routing or merge logic is duplicated here. digest's only new job is turning a
session into a clean candidate list and gating it.

## Run: `/haipipe-discovery digest ["<session-name|id>"] [--dry-run]`

```
0. RESOLVE which session to digest (see "Resolving the target session" below):
     - NO arg   -> the CURRENT session: reason over this live conversation.
     - "<id>"   -> that transcript .jsonl in this repo's ~/.claude/projects dir.
     - "<name>" -> the session /rename'd to that name: find the matching .jsonl.
   For a named/id session, EXTRACT its human turns first; that extract is the
   "transcript" the steps below scan. (Run from a fresh session for clean context.)
1. SCAN the target session's transcript for TOOL/SKILL feedback signals:
     KEEP  - explicit gripes ("this is clunky", "why did you...", "don't do X")
           - corrections you made to my behavior this session
           - stated preferences about how a stage/bucket SHOULD work
           - repeated friction (you had to ask twice, re-route, re-explain)
     DROP  - discovery-finding discussion (about the SOURCES/VERDICT/LANDSCAPE/
             IDEAS, not the TOOL)
           - one-off task instructions ("now search arxiv", "fix this slug")
           - my own narration / anything you did not actually push back on
2. DISTILL into discrete candidate items, ONE concern each, in YOUR words
   (quote where possible; do not invent feedback you cannot point to).
   COMPOUND TURNS are the norm, not the exception: a single turn often bundles
   feedback + a one-off task instruction + a file path (e.g. "the landscape.md
   should group by method not by year ... go ahead and run the review, and my
   notes go in notes.md"). Extract ONLY the feedback clause(s); DROP the task
   clause ("go run it", "search X now"); a path is a location, not feedback.
   One turn may yield TWO feedback items (split them) or ZERO.
3. DEDUP each candidate, and infer its target via the feedback router. ROUTING
   ORDER MATTERS: the cross-cutting GUARD runs BEFORE the keyword map
   (fn/feedback.md resolve step 0), so a layer-wide habit like "always show the
   type field as a plain word" is caught by the guard / the Scope rule below and
   is NEVER keyword-routed to a bucket. Route by the complaint's SUBJECT, not by
   a bucket-name or path it MENTIONS: "add feedback to 1_search that the verdict
   ignored counter-evidence" is about REVIEW (the subject), not 1_search (a
   mis-named destination).
     a. within-batch:  collapse candidates that are the same topic this run.
        The survivor is the batch-master; the rest are tagged [DUP-IN-BATCH]
        and FOLD INTO the master -- they are not routed on their own.
     b. against inbox: run the "Same-topic test" vs the resolved inbox's files.
   Tag each candidate:  [NEW]  |  [MERGE -> <file>]  |  [DUP-IN-BATCH]
   and assign  target-unit.
4. PRESENT the candidate list for the MANDATORY confirm gate. Group by target
   unit; one line per item:
     <tag> · <target-unit> · "<your words>"   (src L<nn>; for MERGE show the
     file, and if a plausible SIBLING exists in the same inbox add
     "also considered <file>")
   Showing the source line + the runner-up merge target lets you catch a wrong
   MERGE into a look-alike sibling that the same-topic test cannot disambiguate
   on its own (e.g. two 1_search files both about "sources.md wide table").
   You: approve / edit text / re-route / drop each item. NOTHING is written
   before you confirm. (This is the same illuminate->confirm gate the lifecycle
   stages use; a session sweep WILL mis-read, so the gate is non-negotiable.)
5. ROUTE each APPROVED item through the feedback capture (fn/feedback.md
   merge-or-create): same-topic -> append a dated recurrence to the existing
   file (prior wording preserved verbatim; reopen if it was fixed); else create.
   [DUP-IN-BATCH] items were already folded into their master in step 3a -- do
   NOT route them separately. Capture runs in BATCH mode: the confirm gate
   (step 4) already approved everything, so capture does NOT re-confirm per item.
6. REPORT what landed where: "N new, M merged, K dropped" (dup-in-batch items
   counted under their master, not separately), grouped by unit. Suggest
   `/haipipe-discovery feedback list` to review the result.
```

## Resolving the target session (the argument)

The transcript store for THIS repo is the matching dir under `~/.claude/projects/`
(slug = the launch cwd with every `/` replaced by `-`); inside it, one
`<uuid>.jsonl` per session.

```
STORE="$HOME/.claude/projects/$(pwd | sed 's#/#-#g')"   # this repo's transcript dir

# id mode   : arg looks like a uuid ->  FILE="$STORE/<id>.jsonl"
# name mode : the /rename name is written into the transcript, so grep for it ->
#             FILE=$(grep -l '"<session-name>"' "$STORE"/*.jsonl | head -1)
#             0 hits -> ask for the id; >1 -> list candidates by mtime, ask which.

# Extract that session's HUMAN turns (the only thing digest needs); drop the
# noise: assistant text, tool_results, injected slash-command skill bodies,
# system reminders. Surface what the USER actually typed.
jq -r 'select(.type=="user") | .message.content | select(type=="string")' "$FILE" \
  | grep -viE 'Base directory for this skill|<command-(name|message)>|<system-reminder>|^Skill: ' \
  | sed -E 's#<command-args>(.*)</command-args>#[CMD] \1#'
```

This is the extraction PATTERN (adapt to the transcript format); the goal is a
short list of the user's actual utterances, which becomes step 1's input. For a
very large session, run the extraction inline (it shrinks MBs to a few KB) and
digest the result; no subagent is needed because the fresh session is already
clean context.

## Scope: skill feedback only (flag, don't file, global prefs)

```
digest files ONLY skill-feedback into bucket-unit inboxes. Some session remarks
are GLOBAL BEHAVIORAL preferences (how the agent should act across ALL sessions,
not a discovery-skill defect). Do NOT file those -- FLAG them in the report and
suggest you `/remember` them. One job per verb.
  skill defect    "the landscape.md synthesis ignored counter-evidence"  -> inbox
  global behavior "always show me a diagram instead of prose"   -> flag -> memory
```

## `--dry-run`

```
Scan + distill + dedup + present the candidate list, then STOP -- do not file
even if confirmed. For previewing what a session would digest.
```

## Safeguards (why this is safe to run often)

```
- confirm-gated:  never auto-files; you approve every item.
- merge-or-create: same-topic items update an existing file instead of spawning
  duplicates, so inboxes stay SELF-LIMITING. (see fn/feedback.md merge-or-create)
- evidence-bound:  only files feedback you can point to in the transcript; no
  invented or inferred-too-far items.
- drop transient:  one-off instructions and discovery-finding talk are excluded.
- fresh-context:   digesting a PAST session from a NEW session keeps the digest's
  judgment uncontaminated by the work it is reviewing (the intended usage).
```
