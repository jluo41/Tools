---
name: haipipe-insight-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the insight SKILL itself, ROUTED at capture time to the specific sub-skill it concerns (else the orchestrator fallback). `feedback list` aggregates across all inboxes; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list [skill] | move <file> <skill>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the insight SKILL (confusing dashboard, clunky verb,
missing routing, bad card-review gate, hard-to-read output) and FILES IT NEXT TO
THE CODE THAT NEEDS FIXING. Does NOT fix anything; fixing is a separate revision
pass. Distinguish from insight content: feedback is about the TOOL, not the D/I/K/W
cards it produces.

Capture-time routing: each complaint is inferred to a specific sub-skill and
written into THAT sub-skill's `feedback/` folder. When no sub-skill matches
(cross-cutting DIKW concern, or genuinely unclassifiable), it lands in the
orchestrator fallback `feedback/`. The folder a file lives in IS the record of
which skill it concerns; there is no separate `skill:` field.

## Capture: `/haipipe-insight feedback "<text>"`

```
1. Read the active context from .insight-console.yaml if present (active layer /
   project — the SECONDARY routing signal). insight may have no console; that's fine.
2. INFER the target skill (see "Routing the capture" below).
3. Resolve the skill -> its feedback/ folder PATH (see "Inbox paths").
   If that folder is missing, create it + a one-line README (template below).
4. MERGE-OR-CREATE (an inbox must NOT grow without bound):
   a. Read the OPEN (and fixed) items already in the resolved inbox.
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
   "filed -> haipipe-insight-knowledge/feedback/ NEW (matched keyword 'K card').
    wrong target? /haipipe-insight feedback move <file> <skill>"
   (When invoked in BATCH by digest, SKIP this per-item confirm: digest's gate
   already approved and its step-6 report is the single confirmation.)
   Do NOT attempt a fix now.
```

### Same-topic test (for merge-or-create)

```
SAME TOPIC = complains about the SAME behavior, or wishes for the SAME change,
even if phrased differently. Same skill alone is NOT enough.
  same topic   "the K card overclaimed beyond its evidence scope"  +  "the K
               writer let the claim cover groups the cited evidence never
               touched"   -> both = K card boundary overclaim  -> MERGE
  diff topic   "the K card overclaims its scope"  +  "the K card is missing a
               citation to its source probe"   -> distinct concerns, same skill
               (knowledge)                       -> SEPARATE
When unsure, prefer ASK (manual) / the confirm gate (digest) over a silent
guess: a wrong MERGE buries a distinct concern, a wrong SPLIT regrows the inbox.
```

### Routing the capture (cross-cutting guard first, then keyword, then context)

```
signal A (primary):   a routing keyword appears in the feedback TEXT
signal B (secondary): the active layer in .insight-console.yaml (if any)
resolve:
  0. CROSS-CUTTING GUARD (runs BEFORE keyword match). The TEST is SEMANTIC:
     does the complaint assert a rule that holds ACROSS ALL DIKW LAYERS
     (something true at D, I, K, AND W alike, however phrased) OR name a known
     cross-cutting concern -- rather than report a bug in ONE layer's behavior
     or output? If yes -> orchestrator FALLBACK, STOP. This overrides any
     keyword it contains.
       Signals that it is layer-wide (non-exhaustive examples, NOT a checklist):
         - quantifies over layers: "every/each/all layers", "D, I, K and W",
           "across the lifecycle", "throughout", "any card", "always ... before
           filing", or the same idea with no trigger word at all
           (e.g. "the INDEX never rebuilds after I file a card" = a rule for
           every layer -> fallback, NOT -data even mid-data-filing).
         - names a known cross-cutting concern: the DIKW boundary cut
           (in-sample vs generalization), the insight-md card schema, INDEX.md,
           the id<->layer graph, sources<->ref_by symmetry, the review/apply
           funnel as a whole, card granularity / lifecycle / change-log policy.
       Rule of thumb: "would this complaint be equally true about a D card, a K
       card, AND a W card?" If yes, it is cross-cutting.
       Contrast: "the INDEX should rebuild for every card I file" -> fallback
       (layer-wide rule); "the K writer left out the confidence field" -> a
       single-layer bug -> haipipe-insight-knowledge.
  1. else keyword match in TEXT -> that skill (most specific wins)
  2. else active-layer skill (from .insight-console.yaml, if any)
  3. else orchestrator fallback
```

Keyword -> skill map (first/most-specific match wins):

```
data, D card, dataset profile, observation        -> haipipe-insight-data
information, I card, in-sample pattern             -> haipipe-insight-information
knowledge, K card, generalization claim, scope     -> haipipe-insight-knowledge
wisdom, W card, recommendation, actionable         -> haipipe-insight-wisdom
review, card review, gate, accuracy, boundary      -> haipipe-insight-review
explore, browse KB, card browse                    -> haipipe-insight-explore
creator agent, reviewer agent, index audit,
  ref_by symmetry, dispatch                        -> agents
--------------------------------------------------------------------------
NO MATCH  (cross-cutting: DIKW boundaries, insight-md schema, INDEX.md,
          id<->layer graph, anything true across all layers)
          ............................. -> orchestrator fallback (this folder)
```

When more than one keyword matches, prefer the MOST SPECIFIC. When the only
signal is the active layer and the complaint is plainly cross-cutting, prefer
the fallback over the layer skill (do not bury a layer-wide rule inside one
layer).

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD        # = created until the first merge
occurrences: 1            # bumped on each same-topic merge
context: <layer/project, or "general">
fixed_in: ""
regressed: ""             # set to a date if a fixed item resurfaces
---
<the feedback, in the reporter's words>

## Recurrences            # added on the FIRST merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

### Inbox paths (relative to the INSIGHT LAYER ROOT)

The insight layer root is the `skills/insight/` directory, NOT
`skills/insight/haipipe-insight` (the orchestrator is a sibling of the six DIKW
skills, not their parent — avoid the symlink trap: this skill may be reached via
`.claude/skills/haipipe-insight` -> `…/skills/insight/haipipe-insight`, so the
layer root is one level ABOVE the orchestrator folder, i.e. `…/skills/insight`).
Inboxes are created LAZILY on first capture, so a mapped folder not existing yet
is expected, not an error.

```
haipipe-insight-data         haipipe-insight-data/feedback/
haipipe-insight-information   haipipe-insight-information/feedback/
haipipe-insight-knowledge     haipipe-insight-knowledge/feedback/
haipipe-insight-wisdom        haipipe-insight-wisdom/feedback/
haipipe-insight-review        haipipe-insight-review/feedback/
haipipe-insight-explore       haipipe-insight-explore/feedback/
agents (creators/reviewers)   agents/feedback/
ORCHESTRATOR FALLBACK         haipipe-insight/feedback/   (this skill's own folder)
```

New-inbox README template (write only if the folder lacks a README.md):

```
# <skill-name> — Feedback Inbox

Feedback about THIS skill, captured by `/haipipe-insight feedback "<text>"` when
the text (or the active layer) points here (capture-time routing), or moved here
via `/haipipe-insight feedback move <file> <skill-name>`.

One file per item: `<YYYY-MM-DD>_<slug>.md` (`status: open|fixed`). Fix in a
later revision pass; keep files as history (never delete). Shared convention:
the orchestrator inbox `insight/haipipe-insight/feedback/README.md`.
```

## List: `/haipipe-insight feedback list [skill]`

```
AGGREGATE across every feedback/ inbox under the insight layer root, not just
this folder. Grep all */feedback/*.md (and this folder) for `status: open` and
print them newest-first, GROUPED BY inbox (skill), each line showing the slug +
context. If [skill] is given, restrict to that one inbox.

  find <insight-layer-root> -type d -name feedback   # enumerate inboxes
  then grep each for `status: open`

The folder each file sits in tells you which skill it concerns.
```

## Move (re-route a mis-filed item): `/haipipe-insight feedback move <file> <skill>`

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
