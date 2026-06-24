---
name: haipipe-application-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the application SKILL itself, ROUTED at capture time to the specific sub-skill it concerns (else the orchestrator fallback). `feedback list` aggregates across all inboxes; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list [skill] | move <file> <skill>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the application SKILL (confusing dashboard, clunky
stage, missing verb, bad routing, hard-to-read output) and FILES IT NEXT TO THE
CODE THAT NEEDS FIXING. Does NOT fix anything; fixing is a separate revision
pass. Distinguish from intervention content: feedback is about the TOOL, not the
intervention it produces.

Capture-time routing: each complaint is inferred to a specific sub-skill and
written into THAT sub-skill's `feedback/` folder. When no sub-skill matches
(cross-cutting discipline, or genuinely unclassifiable), it lands in the
orchestrator fallback `feedback/`. The folder a file lives in IS the record of
which skill it concerns; there is no separate `skill:` field.

## Capture: `/haipipe-application feedback "<text>"`

```
1. Read the active intervention + frontier from .intervention-console.yaml if
   present (the active stage is the SECONDARY routing signal).
2. INFER the target skill (see "Routing the capture" below).
3. Resolve the skill -> its feedback/ folder PATH (see "Inbox paths").
   If that folder is missing, create it + a one-line README (template below).
4. MERGE-OR-CREATE (an inbox must NOT grow without bound):
   a. Read the OPEN (and fixed) items already in the resolved inbox
      (small set: one skill's folder).
   b. SAME-TOPIC test: is the new item the same underlying concern as an
      existing file -- not merely the same skill? (see "Same-topic test").
   c. SAME TOPIC -> UPDATE that file in place:
        - append a dated line under "## Recurrences" in the reporter's NEW
          words. NEVER edit, compress, or translate the prior text -- earlier
          wording is preserved verbatim.
        - bump frontmatter: updated: <today>; occurrences: +1.
        - if status was `fixed`, REOPEN: status: open + regressed: <today>.
          A fixed concern resurfacing is a REGRESSION signal, not a dup.
        - sharpen the title only if the new instance genuinely clarifies it.
   d. NEW TOPIC -> CREATE one file: <inbox>/<YYYY-MM-DD>_<short-slug>.md
      (frontmatter + body per "One file per item" below).
   e. AMBIGUOUS near-match (manual capture) -> ASK "looks like <file> -- merge
      or new?" rather than guess. (Under digest, the confirm gate decides.)
5. CONFIRM where it landed, whether it was MERGED (into <file>) or NEW, and how
   it matched; offer the one-line correction:
   "filed -> haipipe-application-pitch/feedback/ NEW (matched keyword 'pitch').
    wrong target? /haipipe-application feedback move <file> <skill>"
   (When invoked in BATCH by digest, SKIP this per-item confirm: digest's gate
   already approved and its step-6 report is the single confirmation.)
   Do NOT attempt a fix now.
```

### Same-topic test (for merge-or-create)

```
SAME TOPIC = complains about the SAME behavior, or wishes for the SAME change,
even if phrased differently. Same skill alone is NOT enough.
  same topic   "the SMS draft blew past the venue character limit"  +  "the
               draft came back too long for the channel"   -> both = draft
               ignores the length constraint            -> MERGE
  diff topic   "the SMS draft blew past the venue character limit"  +  "the
               draft used the wrong audience tone (too clinical for a patient)"
               -> distinct concerns, same skill (draft)   -> SEPARATE
When unsure, prefer ASK (manual) / the confirm gate (digest) over a silent
guess: a wrong MERGE buries a distinct concern, a wrong SPLIT regrows the inbox.
```

### Routing the capture (cross-cutting guard first, then keyword, then stage)

```
signal A (primary):   a routing keyword appears in the feedback TEXT
signal B (secondary): the active lifecycle stage in .intervention-console.yaml
resolve:
  0. CROSS-CUTTING GUARD (runs BEFORE keyword match). The TEST is SEMANTIC:
     does the complaint assert a rule about the lifecycle/spine AS A WHOLE
     (something that should hold at EVERY stage, however phrased) OR name a
     known cross-cutting concern -- rather than report a bug in ONE stage's
     behavior or output? If yes -> orchestrator FALLBACK, STOP. This overrides
     any keyword it contains.
       Signals that it is spine-wide (non-exhaustive examples, NOT a checklist):
         - quantifies over stages: "every/each/all stages", "at every step",
           "across the lifecycle", "throughout", "spine-wide", "always ...
           before done", or the same idea with no trigger word at all
           (e.g. "the venue depth isn't respected at any stage" = a spine-wide
           depth rule -> fallback, NOT -venue even mid-venue-stage).
         - names a known cross-cutting concern: stage strip, stage gate /
           user-confirm, status tail, illuminate-every-stage, depth-by-venue,
           diagram-ascii habit, interrogate-every-unit.
       Rule of thumb: "would this complaint be equally true at the seed stage,
       the claims stage, AND the display stage?" If yes, it is cross-cutting.
       Contrast: "every stage must respect the venue depth" -> fallback (spine
       rule); "the display stage skipped the panel widget I asked for" -> one
       bug in -display.
  1. else keyword match in TEXT -> that skill (most specific wins)
  2. else active-stage skill
  3. else orchestrator fallback
```

Keyword -> skill map (first/most-specific match wins):

```
seed                                    -> haipipe-application-seed
pitch                                   -> haipipe-application-pitch
venue, journal, profile                 -> haipipe-application-venue
claims, claim, K/W select               -> haipipe-application-claims
narrative                               -> haipipe-application-narrative
display, panel, widget, content elem    -> haipipe-application-display
minimap                                 -> haipipe-application-minimap
lifecycle orchestration                 -> haipipe-application-lifecycle
draft, write, generate SMS, the message -> haipipe-application-draft
review                                  -> haipipe-application-review
deploy, ship, send, go live             -> haipipe-application-deploy
claim-audit, evidence check             -> haipipe-application-claim-audit
iterate                                 -> haipipe-application-iterate
round, rounds                           -> haipipe-application-round
enter, console, dashboard, status       -> haipipe-application-enter
ask, research question                  -> haipipe-application-ask
gate, stage gate                        -> haipipe-application-gate
--------------------------------------------------------------------------
NO MATCH  (cross-cutting: stage strip, illuminate-every-stage, gate
          discipline, status tail, depth-by-venue, anything true across all
          stages) ............................ -> orchestrator fallback (this folder)
```

When more than one keyword matches, prefer the MOST SPECIFIC. When the only
signal is the active stage and the complaint is plainly cross-cutting, prefer
the fallback over the stage skill (do not bury a spine-wide rule inside one
stage).

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD        # = created until the first merge
occurrences: 1            # bumped on each same-topic merge
context: <stage/intervention, or "general">
fixed_in: ""
regressed: ""             # set to a date if a fixed item resurfaces
---
<the feedback, in the reporter's words>

## Recurrences            # added on the FIRST merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

### Inbox paths (relative to the APPLICATION SKILL ROOT)

The application skill root is the `skills/application/` directory (resolve
symlinks: this skill is reached via `.claude/skills/haipipe-application` ->
`…/skills/application/haipipe-application`, so the root is one level ABOVE the
orchestrator folder, i.e. `…/skills/application`, NOT
`…/skills/application/haipipe-application`). Inboxes are created LAZILY on first
capture, so a mapped folder not existing yet is expected, not an error.

```
haipipe-application-seed         1-lifecycle/haipipe-application-seed/feedback/
haipipe-application-pitch        1-lifecycle/haipipe-application-pitch/feedback/
haipipe-application-venue        1-lifecycle/haipipe-application-venue/feedback/
haipipe-application-claims       1-lifecycle/haipipe-application-claims/feedback/
haipipe-application-narrative    1-lifecycle/haipipe-application-narrative/feedback/
haipipe-application-display      1-lifecycle/haipipe-application-display/feedback/
haipipe-application-minimap      1-lifecycle/haipipe-application-minimap/feedback/
haipipe-application-lifecycle    1-lifecycle/haipipe-application-lifecycle/feedback/
haipipe-application-draft        3-draft/haipipe-application-draft/feedback/
haipipe-application-review       4-review-deploy/haipipe-application-review/feedback/
haipipe-application-deploy       4-review-deploy/haipipe-application-deploy/feedback/
haipipe-application-claim-audit  4-review-deploy/haipipe-application-claim-audit/feedback/
haipipe-application-iterate      5-iterate/haipipe-application-iterate/feedback/
haipipe-application-round        2-rounds/haipipe-application-round/feedback/
haipipe-application-enter        0-enter/haipipe-application-enter/feedback/
haipipe-application-ask          shared/haipipe-application-ask/feedback/
haipipe-application-gate         shared/haipipe-application-gate/feedback/
ORCHESTRATOR FALLBACK            haipipe-application/feedback/   (this skill's own folder)
```

New-inbox README template (write only if the folder lacks a README.md):

```
# <skill-name> — Feedback Inbox

Feedback about THIS skill, captured by `/haipipe-application feedback "<text>"`
when the text or the active stage points here (capture-time routing), or moved
here via `/haipipe-application feedback move <file> <skill-name>`.

One file per item: `<YYYY-MM-DD>_<slug>.md` (`status: open|fixed`). Fix in a
later revision pass; keep files as history (never delete). Shared convention:
the orchestrator inbox `application/haipipe-application/feedback/README.md`.
```

## List: `/haipipe-application feedback list [skill]`

```
AGGREGATE across every feedback/ inbox under the application skill root, not
just this folder. Grep all */feedback/*.md (and this folder) for `status: open`
and print them newest-first, GROUPED BY inbox (skill), each line showing the
slug + context. If [skill] is given, restrict to that one inbox.

  find <application-skill-root> -type d -name feedback   # enumerate inboxes
  then grep each for `status: open`

The folder each file sits in tells you which skill it concerns.
```

## Move (re-route a mis-filed item): `/haipipe-application feedback move <file> <skill>`

```
Move <file> from its current inbox to <skill>'s feedback/ folder (resolve via
"Inbox paths"; create the target + README if missing). Use after a wrong
capture-time guess. This is a pure file move; no content edit.
```

## Resolve (during a revision pass, not via this verb)

```
Set status: fixed + fixed_in: <skill version> + a one-line Fix note.
Keep the file as history; never delete it.
```

## Where it lives

There is no single inbox. Each skill keeps its OWN `feedback/` folder so the
report sits right next to the code that needs fixing; the orchestrator's
`feedback/` is the fallback for cross-cutting and unclassifiable items. There is
no cross-skill shared feedback. All inboxes travel with the skills in the
submodule.
