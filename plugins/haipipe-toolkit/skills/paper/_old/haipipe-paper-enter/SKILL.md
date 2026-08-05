---
name: haipipe-paper-enter
description: "THE SINGLE DOOR into a paper. Use for `/haipipe-paper`, `/haipipe-paper enter PAPER_PATH`, `/haipipe-paper status [paper-path]`, or when starting work in an existing paper folder. Resolves the paper root, GET-OR-CREATEs a missing path (confirm-gated, repo-backed inside Project-* repos), then CALLS haipipe-board to build the paper`s 0-lifecycle/ into board.html and push its URL to the browser: the human ends up LOOKING at the board, and never types /haipipe-board for a paper. Derives the frontier from disk and from each S page`s state (nothing derived is stored), then prints only what a terminal is good at: the URL, one frontier line, open needs with routes, and the recommended next command. Records only the active paper identity in .paper-console.yaml and routes free-form input through the lifecycle in copilot mode."
allowed-tools: Bash, Read, Grep, Glob, Write, Skill
metadata:
  version: "0.6.6"
  last_updated: "2026-07-26"
  summary: "Paper Console: the single door that opens the Board, re-derives artifact, S-page state, and gate-receipt truth from disk before routing, and stores only an identity pointer for the active paper. History: ./CHANGELOG.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# haipipe-paper-enter (Paper Console)

Open a concrete paper folder as the **Paper Console**: a context-aware working session for one active paper.
It mirrors the Probe Console.

The console:

```text
1. resolves the paper root
2. derives current state from disk, not from stored status
3. builds and opens the Board, then prints its URL, frontier, and open needs
4. records only the active paper identity in .paper-console.yaml
5. routes later free-form user input through the lifecycle
```

## Missing path = get-or-create (the ONLY way papers are created)

There is no separate create verb.
When the given path does not exist, do NOT fail -- offer to create, but CONFIRM FIRST (repo creation is outward-facing; never create off a typo):

```text
1. CONFIRM: "<path> 不存在。要建这个 paper 吗？" -- and resolve --org (flag or ask,
   NEVER assume; the paper's owner may differ from the project's org).
2. Parent is a Project-* repo -> paper is REPO-BACKED: follow the papers-inside
   recipe in project/haipipe-project/fn/repo-project.md (gh repo create
   <org>/<Paper-Name> --private + git submodule add at the PROJECT's papers/).
   Plain projects: just the folder.
3. Scaffold contents via Skill("haipipe-paper-lifecycle", args="folder <path>").
4. Repo-backed: double-bump (paper push -> project pointer -> workspace pointer).
5. Continue straight into the console (steps 1-5 above) -- one command from
   nothing to dashboard.
```

The main job is to expose the paper's current debt board: open claim gaps, display/table gaps, section-edit phase gaps, round todo gaps, and evidence needs that may require probe/discover/task work.
The user often does not know the next stage in advance; the dashboard makes the next need visible.

Before every follow-up paper action, re-read `board.md` and the relevant S pages, then re-derive the frontier, open needs, and gates from disk before routing.
A fresh Claude/Codex session should run `enter` again.

Story ownership rule: this paper owns its own story, claim wording, narrative, displays, and section editing.
Shared evidence lives in project-level tasks and discoveries.
Do not look for or require a project-level narrative layer.

Read first:

```text
../../PHILOSOPHY.md
../../1-lifecycle/ref/04-lifecycle-map.md
```

The dashboard spec itself lives in this file (Dashboard Spec, below) — this skill owns it.

Then, when the task touches lifecycle shape or rounds:

```text
../../1-lifecycle/ref/03-paper-lifecycle.md
../haipipe-paper-round/SKILL.md          ("Rounds contract")
../../README.md                           (skill-tree layout, Router Rule, Maturity Rule)
```

When creating or interpreting explicit need records, use `../../haipipe-paper/SKILL.md` ("Delivery Need Routing").

## Input

Accept either:

```text
<paper-root>
```

or any path inside a paper root.
If no path is supplied, use the current directory.

## Resolve Paper Root

Look upward from the supplied path until one of these signatures is found:

- `0-lifecycle/board.md`   the only signature that matters: every paper is Board-first
- `0-lifecycle/`           a paper mid-migration, whose board index is not written yet
- `<paper>.tex` and `sections/`   a paper that reached the manuscript upgrade

`STATUS.md` is NOT a signature. It is retired (see CONTRACT.md); a folder that has only a
`STATUS.md` is not a paper, it is a leftover.

If no paper root is found, report `status: blocked` and suggest:

```text
/haipipe-paper seed "<paper-path>"
/haipipe-paper-lifecycle folder "<paper-path>"
```

## Open the Board (the FIRST thing enter does after resolving the root)

Ruled 2026-07-26 (design board `QA1`, `QA4`). **`/haipipe-paper` is the single
thing a human types.** For a board inside a paper, `haipipe-board` is CALLED,
never typed. Before this ruling the console read `board.md` as a data file and
rendered its own text panel, so a human who wanted to SEE the paper had to type
a second skill with the `0-lifecycle/` path by hand.

```text
   👤 types ONE command
        │
        ▼
   /haipipe-paper enter <paper-path>
        │
        ├─ resolve the paper root
        ├─ get-or-create when the path is new
        │     └ haipipe-paper-folder: board.md + ONE Seed page
        ├─ CALL ③ haipipe-board on <paper-root>/0-lifecycle/
        │     ├ build.py   the S pages → board.html
        │     └ serve.py   push the URL to the browser
        └─ print the URL, the frontier line, and the open needs
```

**Calling is not owning.** `③` owns the format, the build, the filename rule,
the html and the write-back; this console renders none of it and never will.

### The three moments ① calls ③

```text
1 ENTER                    here. The human is looking at ⑧ before work starts.
2 AFTER EVERY WRITE TO ⑧   a stage run, a phase worker, a CHECK gate: each ends
                           with a rebuild, or the human reads a paper that no
                           longer exists. Owned by haipipe-paper-stage.
3 BEFORE ① ACTS            a comment or a `>` lane arrived through serve.py, so
                           ⑧'s markdown changed underneath. Re-read; never cache.
```

### When the push fails

The URL reaches the human over the VS Code IPC socket on port 5599. After this
ruling that path is on the critical path of EVERY paper session, so it must
never fail silently:

```text
✅  say the push failed, print the URL, continue with the text lines
✗   report success when only the build succeeded
✗   fall back to file:// — it is not the same page and the live layer is dead
```

A silent success is indistinguishable from a dead port forward, which is exactly
how a session was lost on 2026-07-25. Note also that `open` on this machine acts
on the machine Claude runs on, which is not necessarily where the human is
sitting: hand over the URL, do not assume you can show it.

## Read Order

Read only files that exist, in this order:

1. `0-lifecycle/board.md` -- the spine. It names every page that exists and is the cheapest
   possible read of the paper's shape.
2. `0-lifecycle/2-venue/S-Venue-1-pitch.md` -- HIGH PRIORITY for the dashboard header.
Take its `## Question` lead and its one-line pitch. These become the 2-3 sentence "what this
paper is about" summary at the top of the dashboard.
If the page does not exist, the dashboard says "pitch not yet written".
3. The remaining S pages, by family folder. Each page's own `state:` line is the primary signal:
   - `0-lifecycle/0-seed/S-Seed-*.md`
   - `0-lifecycle/1-work/S-Work-0-resources.md` (venue-FREE prerequisite contract; absent on every pre-2026-07-14 paper -- see the resource exemption below)
   - `0-lifecycle/1-work/S-Work-1-claims.md`
   - `0-lifecycle/2-venue/S-Venue-0-venue.md` (the venue PIN is on its `state:` line, e.g. `state: ✅ PINNED · MISQ 2026`)
   - `0-lifecycle/2-venue/S-Venue-2-narrative.md`
   - `0-lifecycle/3-display/` display pages
4. Main and appendix sections: scan `0-lifecycle/4-main/` and `0-lifecycle/5-appendix/` for
   `S-Main-*.md` / `S-Appendix-*.md`. Derive per-section DPRC status from each page's `state:`
   and from what exists on disk.
4b. `S03-literature/probes/` and `S04-value/probes/`: the paper's open questions, one nested entry page per q-executor. Per entry read its bank-binding `**state**` and whether `#### a-executor` is filled — this is what the phase strip's `probe` glyph is derived from.
5. Explicit need records in lifecycle TeX comments or markdown tables.
   Search for `NEED`, `GAP`, `TODO`, `blocked`, `missing`, and `open`.
6. `displays/*/README.md` -- one per unit; there is no top-level index and no `figures/`.
7. `sections/README.md`
8. `sections/*.tex` and `appendices/*.tex` names and short headers/comments only; do not read full long sections unless needed to diagnose section drift.
9. `0-lifecycle/7-round/S-Round-*.md` -- the round pages themselves; there is no stored pointer to a current round.
11. Git state:
   - `git status --short --branch`
   - `git log --oneline --max-count=3`

## Dashboard Spec

THE single source of truth for the behavior of `/haipipe-paper` with no arguments inside a paper, and for the panel this Console renders.
The dashboard is a derive-from-disk preflight. It orients the session before the Console or any lifecycle stage acts.

### Golden Rule

```text
A stage is done only when its S page resolves on disk with real content
(not the scaffold stub), that page's own `state:` begins `✅`, and its
`## Log` contains the approval receipt for the declared gate.

There is no stored frontier to disagree with. STATUS.md is retired, which
retires DRIFT with it: DRIFT existed only to name the gap between a stored
current_layer and the disk, and there is no longer a stored current_layer.
A page's `state:` is not "stored status" in that sense -- it sits ON the
artifact it describes, so it cannot point at a paper it is not part of.
```

### Lifecycle frontier

The dashboard uses the paper lifecycle spine:

```text
0-seed -> 1-resource -> 1-claims -> venue -> 2-pitch -> 3-narrative -> 4-display
-> 5-section-edit -> review
```

(`1-resource` and `1-claims` share the number 1, deliberately, exactly as `2-venue` and `2-pitch` already do. The number is decoration; the spine key is the bare name `resource`, and a frontier predicate matches on that bare name.)

For every row below, `done` is a conjunction: the disk predicate passes, the
stage's S page has first state token `✅`, AND the page's `## Log` contains a
gate row with `Approved = yes`, an actor, and a date. For a stage represented
by several S pages, every required page must satisfy all three. Content with
`🔴`, `🟡`, or `⏸️`, or a green page with no gate receipt, is not done and may
not advance; it is the current gate.

The frontier is the first stage whose conjunction is not satisfied.

| Stage | Done when | Next action if frontier |
|---|---|---|
| `0-seed` | `0-lifecycle/0-seed/S-Seed-0-seed.md` has question / motivations / claim-shape content | `/haipipe-paper seed` |
| `1-resource` | `0-lifecycle/1-work/S-Work-0-resources.md` exists with real `Resource Description` and `Q-consumer` content; **`n/a` counts as a PASS** only under the resource exemption in Diagnosis Rules | `/haipipe-paper resource` |
| `1-claims` | `0-lifecycle/1-work/S-Work-1-claims.md` ledger non-empty, each row has a status (anchor `planned` still counts as a status; unmaterialized evidence is an open need, not a stage fail) | `/haipipe-paper claims` |
| `venue` | `0-lifecycle/2-venue/S-Venue-0-venue.md` exists and its `state:` line names the pinned outlet (`✅ PINNED · <venue> <year>`) | `/haipipe-paper venue` |
| `2-pitch` | `0-lifecycle/2-venue/S-Venue-1-pitch.md` has a one-line pitch | `/haipipe-paper pitch` |
| `3-narrative` | `0-lifecycle/2-venue/S-Venue-2-narrative.md` has an arc | `/haipipe-paper narrative` |
| `4-display` | the display pages map claim -> display and `displays/displayNN-<slug>/` units exist | `/haipipe-paper display` |
| `5-section-edit` | `0-lifecycle/4-main/S-Main-*.md` pages exist and `sections/*.tex` compile to PDF | `/haipipe-paper section-edit` |
| `review` | audits pass and venue checks pass | `/haipipe-paper review` |

Glyphs:

```text
OK       done on disk
ACTIVE   current frontier
TODO     not reached
STALE    the S page's own `state:` claims done but its disk predicate fails
         (the page over-claims about ITSELF; this is the only disagreement
         the retirement of STATUS.md left standing, and it is a real one)
BLOCKED  explicit blocker (open need / failed gate)
```

### Shallow check

For each paper:

```text
1. Read `0-lifecycle/board.md` for the page list, then each page's first `state:` emoji and `## Log`.
2. For each stage, test its disk predicate, its required S-page state, and its declared-gate receipt.
3. The frontier IS the first stage where either half fails. Nothing stores it.
4. Predicate fail + `✅`, or `✅` with no approval receipt, is STALE: the page over-claims completion.
5. Predicate pass + a non-`✅` gate (or missing receipt) is BLOCKED at that stage: recommend
   `/haipipe-paper <stage> check`, never the next stage.
6. Surface open needs from claims GAP rows, missing display units, open section checklist
   items, section TODOs, and the current S-Round page's open items.
```

### Render skeleton

RETIRED 2026-07-26. The console no longer renders a panel; `⑧` is the panel.
See Output Format below for the three lines the terminal still prints.

## Diagnosis Rules

Derive the current layer from disk, following the Dashboard Spec above.
A stage is done only when its S page resolves with real content and every
required S-page gate has first token `✅`.
The frontier is the first stage where the content predicate or gate predicate
fails, and it is derived on every run rather than stored.
If `state: ✅` claims more progress than disk shows, flag STALE and trust disk.
If disk content passes but the gate is not `✅`, stop at that stage and request
its CHECK approval; never infer permission to advance from content alone.

Per-stage inference when disk is the source of truth:

| Evidence | Current layer |
|---|---|
| only `README.md` / seed lifecycle | `0-seed` |
| seed exists but resource is absent/thin (and NOT exempt -- see below) | `0-seed -> 1-resource` |
| resource settled (or exempt) but claims are absent/thin | `1-resource -> 1-claims` |
| claims exist but S-Venue-0-venue.md's `state:` line is not pinned | `1-claims -> venue` |
| venue pinned but pitch is absent/thin | `venue -> 2-pitch` |
| pitch exists but narrative is absent/thin | `2-pitch -> 3-narrative` |
| narrative exists but display units are missing | `3-narrative -> 4-display` |
| display plan exists but display units/canonical PDFs are missing | `4-display` |
| display units exist and placed | ready for `5-section-edit` |

**Resource exemption -- `n/a` COUNTS AS PASS (binding).**
The resource stage shipped 2026-07-14; every paper already on disk predates it and none will get an `S-Work-0-resources.md` written retroactively.
So for the resource predicate, `n/a` is an ACCEPTED PASS: a paper whose seed gate closed BEFORE the stage existed passes by exemption and the frontier walks straight past it to claims.
Without this, every live paper's frontier REGRESSES to `resource` and the console reports DRIFT on seeds JL personally approved.
The exemption is per-paper and backwards-only -- a paper seeded after 2026-07-14 gets no exemption, and an absent `S-Work-0-resources.md` is a real frontier.

(The Board may still show an exempt Resource page as not started because it
renders the page itself, not the compatibility exemption. Do not call that
drift.)

Infer maturity separately from current layer -- read it from artifacts, never assumed:

| Evidence | Maturity |
|---|---|
| seed / pitch only | `seed` |
| 1-resource settled: every demand HAVE+FIT, COMMISSIONED, or SCOPE CUT | `resource` |
| demand is real but the resource is in flight / behind a DUA -- nothing to do but wait (resource's `park` exit) | `resource-blocked` |
| lifecycle + sections + compile script | `scaffold` |
| 1-claims has explicit claims | `claim-ledger` |
| 4-display maps claim -> display | `display-map` |
| section-edit scaffolds with DPRC in progress | `section-edit` |
| sections compile with prose | `draft` |
| checks/audits mostly pass | `submission-candidate` |
| frozen PDF + submission metadata | `submitted` |
| an S-Round page open after external/coauthor review | `revision` |
| final external state | `accepted/published` |

Need diagnosis is separate from lifecycle layer.
Extract open needs from:

| Surface | Typical need |
|---|---|
| `1-resource` unanswered `Q<n>` (no **A**), or a BUILD section whose `eta:` has passed | probe (the PROBE worker opens the SECTION and routes it -- the stage only ASKS) |
| `1-claims` GAP/weak/unsupported rows | probe, discovery, task |
| `4-display` missing display units | display or task |
| `5-section-edit` sections with incomplete DPRC phases | section-edit work |
| section comments/TODOs | paper edit or evidence need |
| round `todo.md` unresolved items | paper edit, probe, display, citation |

Classify each open item using the delivery-need interface:

```text
probe | discovery | task | display | paper-edit
```

Loopback diagnosis follows the paper lifecycle:

| Symptom | Return to |
|---|---|
| wording, citation, format, stale number | section-edit cycle |
| figure/table unclear or lacks source/caption/preview | `4-display` |
| unsupported or too-strong claim | `1-claims` / `3-narrative` |
| the claim's data/checkpoint/producing-code does not exist, or exists but cannot CARRY the claim | `1-resource` |
| story not compelling or abstract/intro disagree | `2-pitch` |
| every demand row is unobtainable -- the paper cannot be written as seeded | `0-seed` (resource's `reseed` exit) |
| paper no longer viable | `0-seed` |

## Output Format

**The BOARD is the panel. The terminal is the pointer to it.**

Ruled 2026-07-26. Before this, the console rendered a full text dashboard: a
paper-identity table, a two-line focus strip, a current-state block, a stable
block and an artifacts-read list. `⑧` renders every one of those, in a browser,
with comment lanes a terminal cannot have. Two renderers of one truth is one
too many, and the terminal was always the weaker one.

What a terminal is genuinely good at is three things. Print exactly these, in
this order, and stop:

```markdown
📋 <board URL>          ← FIRST. The human reads the paper THERE.
   (if the push failed, say so on this line and print the URL anyway)

<paper-folder-name> · <venue: from S-Venue-0-venue.md> · frontier: <stage>
<one sentence on what the paper is about, from S-Venue-1-pitch.md's lead.
 If no pitch page exists: "Pitch not yet written — run /haipipe-paper pitch.">

## Open Needs
  - <gap> -> <route>       one line each, route per Delivery Need Routing
  - <gap> -> <route>       in `../../haipipe-paper/SKILL.md`

## Recommended Next
  <the single highest-leverage command>
```

That is the whole panel. If a reader wants more, the URL is on the first line.

### What was RETIRED with the text dashboard

```text
Paper Identity table   ⑧'s board.md header carries it
Focus Strip 🔥/🚀      ⑧'s spine shows every page's state at once
the 9-stage strip      a worse copy of that spine; no second renderer remains
Current State / Stable ⑧'s per-page `state:` IS this
Artifacts Read         a log of the console's own work, useful to nobody
```

Loopback is no longer a rendered block either: with the frontier derived and
nothing stored, re-running an earlier stage is ordinary, not an anomaly to
diagnose. Say it in one clause on the frontier line if it is worth saying.

Per the Lifecycle TeX Quality Standard (full text sits with the retired deliver
router; debt tracked in `../_old/README.md`), a stale PDF is a defect: list any
stage whose `.tex` is newer than its `.pdf` under Open Needs.

Keep it concise. The goal is to orient the session and hand over the URL, not
to rewrite the paper.

## Free-form Routing

After the dashboard, route follow-up input through the lifecycle using the command map in `../haipipe-paper-stage/ref/04-lifecycle-map.md`:

```text
seed                       -> /haipipe-paper seed         (stage key: seed)
resource / prereq /        -> /haipipe-paper resource      (stage key: resource)
  do we have the data /
  does the checkpoint exist
claims / ledger            -> /haipipe-paper claims        (stage key: claims)
venue / journal            -> /haipipe-paper venue         (stage key: venue)
pitch / story / sell       -> /haipipe-paper pitch         (stage key: pitch)
narrative / arc            -> /haipipe-paper narrative     (stage key: narrative)
display / figure / table   -> /haipipe-paper display       (stage key: display)
section / edit / §N        -> /haipipe-paper section-edit  (stage key: section-edit)
check §N                   -> /haipipe-paper section-edit, CHECK gate (page logic: haipipe-board-page-check)
round / todo               -> round skills
rebuttal / respond         -> rebuttal skills
```

If the input does not name a stage, re-derive the current frontier from disk, then route to it.
If the input is ambiguous, ask before acting.

## Copilot Policy

Default mode is copilot.
The console may automatically read files, summarize the frontier, classify input, draft or revise a stage `.tex`, plan section work, and suggest routes.

It must ask before:

```text
calling costly task/PHI/full-data work
committing a claim verdict or downgrading a claim
editing prose across many sections at once
compiling-to-submit or packaging a submission
opening or closing a revision round destructively
landing a settled claim status in 0-lifecycle/1-work/S-Work-1-claims.md
```

## Session State

Record the console session at the paper/project root (the nearest directory containing the paper folder), not necessarily the repo root:

```text
.paper-console.yaml
```

Fields:

```yaml
paper_root: <path>
active_paper: <Paper-Name>
updated: <YYMMDD>
```

This file is an identity pointer, not a state cache.
Never store frontier, maturity, round, gate, or open-need values here; re-derive them from the Board, S pages, probe entries, and their targets on every action.

## Return Contract

Every reply from a paper specialist (and every enter dashboard) MUST end with the closing block defined in `../../haipipe-paper/SKILL.md` (Closing Block section, the single source of truth).
Omitting it is a protocol violation.
Do not copy or redefine its shape here; use the umbrella contract verbatim so the Board URL and phase line cannot drift.
