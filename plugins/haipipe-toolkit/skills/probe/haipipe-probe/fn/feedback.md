---
name: haipipe-probe-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the probe SKILL itself, ROUTED at capture time to the unit it concerns: the AGENTS (agent behavior) or the orchestrator+lifecycle (everything else, the fallback). `feedback list` aggregates across both inboxes; `feedback move` re-routes a mis-filed item. Not a probe verdict."
argument-hint: "[\"<text>\" | list [unit] | move <file> <unit>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the probe SKILL (confusing dashboard, clunky lifecycle
step, missing verb, bad routing, hard-to-read output, an agent that misbehaves)
and FILES IT NEXT TO THE CODE THAT NEEDS FIXING. Does NOT fix anything; fixing is
a separate revision pass. Distinguish from a probe verdict: feedback is about the
TOOL, not a claim.

Capture-time routing: probe is the FLAT case. There are only TWO physical code
locations to route between, so each complaint is inferred to one of them and
written into THAT unit's `feedback/` folder:

```
(a) AGENTS            agents/                — feedback about agent BEHAVIOR
(b) ORCHESTRATOR      haipipe-probe/         — everything else (the fallback)
```

The whole lifecycle (Plan/Gather/Read/Judge/Deposit) lives as `fn/*.md` PROCEDURE
files inside the orchestrator folder; the procedure a non-agent item concerns
stays encoded in its filename slug (existing convention), NOT in a sub-folder.
There are no per-procedure feedback inboxes. The folder a file lives in IS the
record of which unit it concerns; there is no separate `skill:` field.

## Capture: `/haipipe-probe feedback "<text>"`

```
1. Read the active probe + step from .probe-console.yaml if present
   (the active step is the SECONDARY routing signal).
2. INFER the target unit -- agents or orchestrator (see "Routing the capture").
3. Resolve the unit -> its feedback/ folder PATH (see "Inbox paths").
   If that folder is missing, create it + a one-line README (template below).
   (agents/feedback/ is created LAZILY on the first agent-behavior item.)
4. MERGE-OR-CREATE (an inbox must NOT grow without bound):
   a. Read the OPEN (and fixed) items already in the resolved inbox.
   b. SAME-TOPIC test: is the new item the same underlying concern as an
      existing file -- not merely the same unit? (see "Same-topic test").
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
   "filed -> agents/feedback/ NEW (matched 'orchestrator dispatch').
    wrong unit? /haipipe-probe feedback move <file> orchestrator"
   (When invoked in BATCH by digest, SKIP this per-item confirm: digest's gate
   already approved and its step-6 report is the single confirmation.)
   Do NOT attempt a fix now.
```

### Same-topic test (for merge-or-create)

```
SAME TOPIC = complains about the SAME behavior, or wishes for the SAME change,
even if phrased differently. Same unit alone is NOT enough.
  same topic   "orchestrator did all the work itself"  +  "orchestrator never
               dispatched creator/reviewer"   -> both = monolithic collapse  -> MERGE
  diff topic   "orchestrator collapses to monolithic"  +  "the reviewer's
               verdict enum is missing 'revise'"   -> distinct concerns, same
               unit (agents)                    -> SEPARATE
When unsure, prefer ASK (manual) / the confirm gate (digest) over a silent
guess: a wrong MERGE buries a distinct concern, a wrong SPLIT regrows the inbox.
```

### Routing the capture (cross-cutting guard first, then agent keyword, then context)

```
signal A (primary):   an agent-behavior keyword appears in the feedback TEXT
signal B (secondary): the active lifecycle step in .probe-console.yaml
resolve:
  0. CROSS-CUTTING GUARD (runs BEFORE keyword match). The TEST is SEMANTIC:
     does the complaint assert a rule that holds across the WHOLE probe
     lifecycle (something true at Plan AND Gather AND Read AND Judge AND
     Deposit, however phrased) OR name a known cross-cutting concern -- rather
     than report a misbehavior of the AGENTS? If yes -> ORCHESTRATOR FALLBACK,
     STOP. This overrides any agent keyword it contains.
       Signals that it is lifecycle-wide / cross-cutting (non-exhaustive
       examples, NOT a checklist):
         - quantifies over steps: "every/each step", "across the lifecycle",
           "throughout", "always ... before done", or the same idea with no
           trigger word at all (e.g. "the stage strip never reflects what
           actually ran" = a strip rule across steps -> fallback).
         - names a known cross-cutting concern: stage strip, the return tail /
           status tail, probe id/naming/granularity (atomic vs comparison),
           the console/dashboard render, venue editor-chair test, compile-tex,
           one-probe-many-discoveries fan-out, the Read/Judge/Deposit boundary
           as a CONCEPT (vs an agent that crossed it).
       Rule of thumb: "would this complaint be equally true if a HUMAN ran the
       lifecycle by hand, with no agents at all?" If yes, it is orchestrator/
       lifecycle, not agents -> fallback.
       Contrast: "the orchestrator agent hung before dispatching" -> agents
       (an agent misbehaved); "Read must not contain verdict language" ->
       fallback (a lifecycle-procedure rule, true with or without agents).
  1. else an AGENT keyword in TEXT -> agents/feedback/
  2. else the active context points at an agent run -> agents/feedback/
  3. else ORCHESTRATOR FALLBACK (haipipe-probe/feedback/)
```

Keyword -> unit map (use EXACTLY this):

```
orchestrator agent, creator agent, reviewer agent, dispatch,
nested agent, monolithic collapse, creator/reviewer loop,
agent failure, expected-vs-actual dispatch         -> agents/feedback/
------------------------------------------------------------------------------
NO MATCH  (lifecycle procedures plan/gather/read/judge/deposit, console/
          dashboard, stage strip, return tail, probe id/naming, granularity,
          venue editor-chair test, compile-tex, anything true across the
          lifecycle) ............................. -> orchestrator fallback
                                                      (haipipe-probe/feedback/)
```

When the only signal is the active context and the complaint is plainly a
lifecycle/cross-cutting rule, prefer the fallback over agents (do not bury a
lifecycle-wide rule in the agents inbox just because an agent happened to be
running when it surfaced).

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD        # = created until the first merge
occurrences: 1            # bumped on each same-topic merge
context: <probe/step, or "general">
fixed_in: ""
regressed: ""             # set to a date if a fixed item resurfaces
---
<the feedback, in the reporter's words>

## Recurrences            # added on the FIRST merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

(Existing items predate this schema and use a leaner front-matter, e.g.
`date:`/`source:`/`scope:` instead of `created:`/`context:`. That is fine -- do
not mass-rewrite them; bring a file up to schema only when you next merge into
it.)

### Inbox paths (relative to the PROBE SKILL ROOT)

The probe skill root is the `skills/probe/` directory (resolve symlinks: this
skill is reached via `.claude/skills/haipipe-probe` -> `…/skills/probe/haipipe-probe`,
so the root is one level ABOVE the orchestrator folder, i.e. `…/skills/probe`,
NOT `…/skills/probe/haipipe-probe`). Inboxes are created LAZILY on first capture,
so a mapped folder not existing yet is expected, not an error.

```
AGENTS (agent behavior)        agents/feedback/
ORCHESTRATOR FALLBACK          haipipe-probe/feedback/   (this skill's own folder)
                               (lifecycle + console + cross-cutting + unclassifiable)
```

New-inbox README template (write only if the folder lacks a README.md):

```
# probe <unit> — Feedback Inbox

Feedback about THIS unit, captured by `/haipipe-probe feedback "<text>"` when the
text or the active context points here (capture-time routing), or moved here via
`/haipipe-probe feedback move <file> <unit>`.

One file per item: `<YYYY-MM-DD>_<slug>.md` (`status: open|fixed`). Fix in a
later revision pass; keep files as history (never delete). Shared convention:
the orchestrator inbox `probe/haipipe-probe/feedback/README.md`.
```

## List: `/haipipe-probe feedback list [unit]`

```
AGGREGATE across BOTH feedback/ inboxes under the probe skill root, not just this
folder. Find every feedback/ dir, grep each for `status: open`, and print them
newest-first, GROUPED BY unit (agents | orchestrator), each line showing the
slug + context. If [unit] is given (agents | orchestrator), restrict to that one
inbox.

  find <probe-skill-root> -type d -name feedback   # enumerate inboxes
  then grep each for `status: open`

The folder each file sits in tells you which unit it concerns.
```

## Move (re-route a mis-filed item): `/haipipe-probe feedback move <file> <unit>`

```
<unit> is `agents` or `orchestrator`. Move <file> from its current inbox to the
target unit's feedback/ folder (resolve via "Inbox paths"; create the target +
README if missing -- e.g. agents/feedback/ on the first agent item). Use after a
wrong capture-time guess. This is a pure file move; no content edit.
```

## Resolve (during a revision pass, not via this verb)

```
Set status: fixed + fixed_in: <skill version> + a one-line Fix note.
Keep the file as history; never delete it.
```

## Where it lives

There is no single inbox and no per-procedure sub-folders. Probe is the FLAT
case: feedback routes to exactly two units -- the AGENTS (`agents/feedback/`,
for agent behavior) or the ORCHESTRATOR (`haipipe-probe/feedback/`, the fallback
for the lifecycle procedures, the console, and every cross-cutting concern). The
report sits next to the code that needs fixing. There is no cross-skill shared
feedback. Both inboxes travel with the skill in the submodule.
