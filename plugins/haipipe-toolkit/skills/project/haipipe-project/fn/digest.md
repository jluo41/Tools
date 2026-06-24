---
name: haipipe-project-digest
description: "Utility verb. Digests a session -- the CURRENT one, or a PAST session named/id'd as an argument (run from a fresh session) -- scanning its transcript for tool/skill feedback (gripes + preferences), distilling discrete items, deduping (merge-or-create), and after a MANDATORY confirm gate routing each through the feedback router into sub-skill inboxes. The bulk harvester for /haipipe-project feedback. Never auto-files."
argument-hint: "[\"<session-name|id>\"] [--dry-run]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Digest (condense the session into routed feedback)

Most feedback is given conversationally and never filed. `digest` is the bulk
harvester: it reads a session's transcript, distills the discrete pieces of
TOOL/SKILL feedback you gave, dedups them, and (after you confirm) routes each
into the right sub-skill inbox. A digest is, by definition, deduped and condensed
-- the same discipline as the merge-or-create capture.

Typical usage: from a FRESH session (clean context), name the PAST session to
harvest -- `/haipipe-project digest "Display-for-Opioid-MISQ"`. With no argument it
digests the CURRENT session instead. Running from a fresh session is what keeps
the digest's judgment uncontaminated by the work it is reviewing.

The project orchestrator keeps no console yaml (it dispatches inline), so digest
relies on the TRANSCRIPT only -- there is no active-context state to consult.
That is expected, not a gap (the same way paper's digest works from its transcript).

Relation to `feedback`. `digest` HARVESTS; `feedback` ROUTES + MERGES. digest
REUSES `fn/feedback.md` for everything downstream of distillation: the
keyword->skill map, the cross-cutting guard, and the merge-or-create capture. No
routing or merge logic is duplicated here. digest's only new job is turning a
session into a clean candidate list and gating it.

## Run: `/haipipe-project digest ["<session-name|id>"] [--dry-run]`

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
           - stated preferences about how a specialist/skill SHOULD work
           - repeated friction (you had to ask twice, re-route, re-explain)
     DROP  - project-content discussion (about the PROJECT / tasks, not the TOOL)
           - one-off scaffold/review instructions ("now scaffold the C01 task",
             "review ProjB")
           - my own narration / anything you did not actually push back on
2. DISTILL into discrete candidate items, ONE concern each, in YOUR words
   (quote where possible; do not invent feedback you cannot point to).
   COMPOUND TURNS are the norm, not the exception: a single turn often bundles
   feedback + a one-off task instruction + a file path (e.g. "the overview
   should group by task-group not dump every file ... go ahead and scaffold the
   new C01 group, and the project lives under examples/ProjB"). Extract ONLY the
   feedback clause(s); DROP the task clause ("go scaffold it", "review X now");
   a path is a location, not feedback. One turn may yield TWO feedback items
   (split them) or ZERO.
3. DEDUP each candidate, and infer its target via the feedback router. ROUTING
   ORDER MATTERS: the cross-cutting GUARD runs BEFORE the keyword map
   (fn/feedback.md resolve step 0), so a project-wide rule like "every new task
   folder should get a diagram stub" is caught by the guard and is NEVER
   keyword-routed to a specialist. Route by the complaint's SUBJECT, not by a
   skill-name or path it MENTIONS: "add feedback to /haipipe-organize that the
   overview must group by task-group" is about the OVERVIEW (the subject, ->
   -inspect), not -organize (a mis-named destination).
     a. within-batch:  collapse candidates that are the same topic this run.
        The survivor is the batch-master; the rest are tagged [DUP-IN-BATCH]
        and FOLD INTO the master -- they are not routed on their own.
     b. against inbox: run the "Same-topic test" vs the resolved inbox's files.
   Tag each candidate:  [NEW]  |  [MERGE -> <file>]  |  [DUP-IN-BATCH]
   and assign  target-skill.
4. PRESENT the candidate list for the MANDATORY confirm gate. Group by target
   skill; one line per item:
     <tag> · <target-skill> · "<your words>"   (src L<nn>; for MERGE show the
     file, and if a plausible SIBLING exists in the same inbox add
     "also considered <file>")
   Showing the source line + the runner-up merge target lets you catch a wrong
   MERGE into a look-alike sibling that the same-topic test cannot disambiguate
   on its own (e.g. two inspect files both about "overview readability").
   You: approve / edit text / re-route / drop each item. NOTHING is written
   before you confirm. (A session sweep WILL mis-read, so the gate is
   non-negotiable.)
5. ROUTE each APPROVED item through the feedback capture (fn/feedback.md
   merge-or-create): same-topic -> append a dated recurrence to the existing
   file (prior wording preserved verbatim; reopen if it was fixed); else create.
   [DUP-IN-BATCH] items were already folded into their master in step 3a -- do
   NOT route them separately. Capture runs in BATCH mode: the confirm gate
   (step 4) already approved everything, so capture does NOT re-confirm per item.
6. REPORT what landed where: "N new, M merged, K dropped" (dup-in-batch items
   counted under their master, not separately), grouped by skill. Suggest
   `/haipipe-project feedback list` to review the result.
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
digest files ONLY skill-feedback into sub-skill inboxes. Some session remarks
are GLOBAL BEHAVIORAL preferences (how the agent should act across ALL sessions,
not a project-skill defect). Do NOT file those -- FLAG them in the report and
suggest you `/remember` them. One job per verb.
  skill defect    "project inventory miscounted task-folders"   -> inbox
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
- drop transient:  one-off instructions and project-content talk are excluded.
- fresh-context:   digesting a PAST session from a NEW session keeps the digest's
  judgment uncontaminated by the work it is reviewing (the intended usage).
```
