---
name: haipipe-task-feedback
description: "Utility verb. Captures a complaint/confusion/wish about the task SKILL itself, ROUTED at capture time to the specific domain folder it concerns (else the orchestrator fallback). `feedback list` aggregates across all inboxes; `feedback move` re-routes a mis-filed item."
argument-hint: "[\"<text>\" | list [unit] | move <file> <unit>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Feedback (capture skill feedback, route at capture, fix later)

Captures feedback about the task SKILL (confusing dashboard, clunky stage,
missing verb, bad routing, hard-to-read output) and FILES IT NEXT TO THE CODE
THAT NEEDS FIXING. Does NOT fix anything; fixing is a separate revision pass.
Distinguish from task work: feedback is about the TOOL, not the task-folder it
builds.

Capture-time routing: each complaint is inferred to a specific DOMAIN FOLDER
(the routable unit — `task/` groups its ~40 specialist skills into 9 domain
folders, too granular to route to 40 individual skills, plus a shared `agents/`
folder) and written into THAT unit's `feedback/` folder. When no unit matches
(cross-cutting discipline, or genuinely unclassifiable), it lands in the
orchestrator fallback `feedback/`. The folder a file lives in IS the record of
which unit it concerns; there is no separate `skill:` field.

## Capture: `/haipipe-task feedback "<text>"`

```
1. Read the active task-folder + task-type from any session/console state if
   present (the active task-type is the SECONDARY routing signal).
2. INFER the target unit (see "Routing the capture" below).
3. Resolve the unit -> its feedback/ folder PATH (see "Inbox paths").
   If that folder is missing, create it + a one-line README (template below).
4. MERGE-OR-CREATE (an inbox must NOT grow without bound):
   a. Read the OPEN (and fixed) items already in the resolved inbox
      (small set: one unit's folder).
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
      or new?" rather than guess. (Under digest's BATCH, the confirm gate decides.)
5. CONFIRM where it landed, whether it was MERGED (into <file>) or NEW, and how
   it matched; offer the one-line correction:
   "filed -> 2_nn/feedback/ NEW (matched keyword 'model').
    wrong target? /haipipe-task feedback move <file> <unit>"
   Do NOT attempt a fix now.
   (When invoked in BATCH by digest, SKIP this per-item confirm: digest's gate
   already approved.)
```

### Same-topic test (for merge-or-create)

```
SAME TOPIC = complains about the SAME behavior, or wishes for the SAME change,
even if phrased differently. Same unit alone is NOT enough.
  same topic   "the figure renderer emitted a broken .tex"  +  "display task
               keeps producing .tex that won't compile"   -> both = renderer
               output is broken                            -> MERGE
  diff topic   "the figure renderer emitted a broken .tex"  +  "the display
               task has no way to pin the source CSV"   -> distinct concerns
               (renderer bug vs missing config), same unit (7_display) -> SEPARATE
When unsure, prefer ASK (manual) / the confirm gate (digest) over a silent
guess: a wrong MERGE buries a distinct concern, a wrong SPLIT regrows the inbox.
```

### Routing the capture (cross-cutting guard first, then keyword, then context)

```
signal A (primary):   a routing keyword appears in the feedback TEXT
signal B (secondary): the active task-type / domain in session state
resolve:
  0. CROSS-CUTTING GUARD (runs BEFORE keyword match). The TEST is SEMANTIC:
     does the complaint assert a rule about the task lifecycle/spine AS A WHOLE
     (something that should hold across EVERY domain or at EVERY stage, however
     phrased) OR name a known cross-cutting concern -- rather than report a bug
     in ONE domain's behavior or output? If yes -> orchestrator FALLBACK, STOP.
     This overrides any keyword it contains.
       Signals that it is spine-wide (non-exhaustive examples, NOT a checklist):
         - quantifies over domains/stages: "every/each/all domains", "every
           task-type", "at every stage", "across the lifecycle", "throughout",
           "spine-wide", "always ... before done", or the same idea with no
           trigger word at all (e.g. "the report.yaml never mirrors plan.yaml
           shape" = a lifecycle contract rule -> fallback, NOT -2_nn even mid-nn-task).
         - names a known cross-cutting concern: the 4-stage lifecycle
           (Plan/Build/Execute/Report), the IPO contract, the task-folder
           scaffold, run conventions (runs/*.sh, papermill, configs/), the
           creator-reviewer loop discipline, stage file-ownership, anything
           true across all domains.
       Rule of thumb: "would this complaint be equally true for a data task,
       an nn task, AND a display task?" If yes, it is cross-cutting.
       Contrast: "every stage must mirror IPO shape" -> fallback (spine rule);
       "the figure renderer emitted a broken .tex" -> 7_display (one bug).
  1. else keyword match in TEXT -> that unit (most specific wins)
  2. else active-domain unit (from task-type / session state)
  3. else orchestrator fallback
```

Keyword -> unit map (first/most-specific match wins; the unit is the DOMAIN FOLDER):

```
data, source, record, case, aidata, raw, remote, external     -> 1_data
nn, model, algo, tuner, instance, modelset                    -> 2_nn
end, endpoint, deploy, develop, meta/trig/post fn, src2input   -> 3_end
individual, inference                                         -> 4_individual
fit, training                                                 -> 5_fit
eval, evaluation                                              -> 6_eval
display, figure, table (task-for-display)                     -> 7_display
stata, do-file, dialect                                       -> 8_stata
agent task (task-for-agent)                                   -> 9_agent
creator/orchestrator/reviewer agent, dispatch, gate 1,
gate 2, code review, run audit                                -> agents
--------------------------------------------------------------------------
NO MATCH  (cross-cutting: the 4-stage lifecycle Plan/Build/Execute/Report,
          IPO contract, task-folder scaffold, run conventions, anything true
          across all domains) ................. -> orchestrator fallback (this folder)
```

When more than one keyword matches, prefer the MOST SPECIFIC. When the only
signal is the active task-type and the complaint is plainly cross-cutting,
prefer the fallback over the domain unit (do not bury a spine-wide rule inside
one domain).

### One file per item (schema)

```
---
status: open | fixed
created: YYYY-MM-DD
updated: YYYY-MM-DD        # = created until the first merge
occurrences: 1            # bumped on each same-topic merge
context: <task-folder/type, or "general">
fixed_in: ""
regressed: ""             # set to a date if a fixed item resurfaces
---
<the feedback, in the reporter's words>

## Recurrences            # added on the FIRST merge; one dated line per re-surfacing
- YYYY-MM-DD: <the new phrasing, verbatim from the reporter>

Fix: <added when resolved>
```

(Existing items predate this schema and use a leaner front-matter, e.g.
`status:`/`created:`/`context:`/`fixed_in:` with no `updated:`/`occurrences:`/
`regressed:`. That is fine -- do not mass-rewrite them; bring a file up to schema
only when you next merge into it.)

### Inbox paths (relative to the TASK SKILL ROOT)

The task skill root is the `skills/task/` directory (resolve symlinks: this
skill is reached via `.claude/skills/haipipe-task` -> `…/skills/task/haipipe-task`,
so the root is one level ABOVE the orchestrator folder, i.e. `…/skills/task`, NOT
`…/skills/task/haipipe-task`). Inboxes are created LAZILY on first capture, so a
mapped folder not existing yet is expected, not an error -- do NOT pre-create
empty inboxes.

```
1_data        1_data/feedback/
2_nn          2_nn/feedback/
3_end         3_end/feedback/
4_individual  4_individual/feedback/
5_fit         5_fit/feedback/
6_eval        6_eval/feedback/
7_display     7_display/feedback/
8_stata       8_stata/feedback/
9_agent       9_agent/feedback/
agents        agents/feedback/
ORCHESTRATOR FALLBACK               haipipe-task/feedback/   (this skill's own folder)
```

New-inbox README template (write only if the folder lacks a README.md):

```
# <unit-name> — Feedback Inbox

Feedback about THIS domain's task skills, captured by
`/haipipe-task feedback "<text>"` when the text or the active task-type points
here (capture-time routing), or moved here via
`/haipipe-task feedback move <file> <unit-name>`.

One file per item: `<YYYY-MM-DD>_<slug>.md` (`status: open|fixed`). Fix in a
later revision pass; keep files as history (never delete). Shared convention:
the orchestrator inbox `haipipe-task/feedback/README.md`.
```

## List: `/haipipe-task feedback list [unit]`

```
AGGREGATE across every feedback/ inbox under the task skill root, not just this
folder. Grep all */feedback/*.md (and this folder) for `status: open` and print
them newest-first, GROUPED BY unit (domain folder), each line showing the slug +
context. If [unit] is given, restrict to that one inbox.

  find <task-skill-root> -type d -name feedback   # enumerate inboxes
  then grep each for `status: open`

The folder each file sits in tells you which unit it concerns.
```

## Move (re-route a mis-filed item): `/haipipe-task feedback move <file> <unit>`

```
Move <file> from its current inbox to <unit>'s feedback/ folder (resolve via
"Inbox paths"; create the target + README if missing). Use after a wrong
capture-time guess. This is a pure file move; no content edit.
```

## Resolve (during a revision pass, not via this verb)

```
Set status: fixed + fixed_in: <skill version> + a one-line Fix note.
Keep the file as history; never delete it.
```

## Where it lives

There is no single inbox. Each domain folder keeps its OWN `feedback/` folder so
the report sits right next to the code that needs fixing; the orchestrator's
`feedback/` is the fallback for cross-cutting and unclassifiable items. There is
no cross-unit shared feedback. All inboxes travel with the skills in the
submodule.
