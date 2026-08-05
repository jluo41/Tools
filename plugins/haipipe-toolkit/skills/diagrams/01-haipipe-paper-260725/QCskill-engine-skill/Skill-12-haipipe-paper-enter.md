# haipipe-paper-enter · v0.6.6
state: 🔴 OPEN
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
REPLACE THIS PARAGRAPH. Load `haipipe-board-page-for-skill` and write the three slots it names, in its order, in plain words: ❶ what `haipipe-paper-enter` is and what it is FOR, ❷ when you reach for it rather than the ONE sibling you would otherwise pick, named, ❸ where it stands, meaning the one thing to know before trusting it.

NEVER open a skill page with a question. This stub used to seed `{name} is a shipped unit: what does it still owe, and is it healthy?`, and on 260802 five pages generated from it all opened with the same rhetorical question in the same four-slot shape, because a skill page DECIDES NOTHING and so has nothing to ask.
Delete these instructions once the paragraph is written; the FIRST BLANK LINE above is the split, and everything below it is the `More details` drawer, written as labelled parts.
`Opening` is the lead section's ONE name on every page kind (JL 260731: "just one single Opening"); `Question` survives only as a legacy alias for pages written before the rename.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start d78d1928a1c81d9e paper/haipipe-paper-enter -->

**What `haipipe-paper-enter` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-paper-enter/
  feedback/
    2026-06-22_console-too-dense-want-stage-progress.md    15 ln  我感觉第一次出来的东西太多了，我可能其实就像知道这个论文是什么，什么story之类的，你这给我整的不知道去哪看啥了。然后我觉得有个stage process挺好的。有个lifecycle之类的，从左到右，一个stage
    2026-06-22_enter-should-show-what-paper-is-about.md    14 ln  When entering a paper, the dashboard should tell the user what this paper is about — not just the structural s
    README.md                            9 ln  haipipe-paper-enter — Feedback Inbox
  CHANGELOG.md                         161 ln  haipipe-paper-enter — Changelog
  SKILL.md                             467 ln  haipipe-paper-enter (Paper Console)
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-paper-enter` is used**: REPLACE THIS CAPTION with what your figure below actually shows.

```
WORKFLOW  (authored: a folder can be read off disk, an intent cannot)
Draw how this skill is actually used: the entry point, what it reads,
what it writes, and where it hands off. Delete this fence AND the
caption line above it if the tree is the whole story.
```

## Content
<!-- haipipe:skill:body:start d78d1928a1c81d9e paper/haipipe-paper-enter -->

**haipipe-paper-enter** · `0.6.6` · last shipped 2026-07-26

- folder   `paper/haipipe-paper-enter/`
- tools    Bash, Read, Grep, Glob, Write, Skill
- summary  Paper Console: the single door that opens the Board, re-derives artifact, S-page state, and gate-receipt truth from disk before routing, and stores only an identity pointer for the active paper. History: ./CHANGELOG.md.

### SKILL.md




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


- 1 · Missing path = get-or-create (the ONLY way papers are created)
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

- 2 · Input
      Accept either:
      ```text
      <paper-root>
      ```
      or any path inside a paper root.
      If no path is supplied, use the current directory.

- 3 · Resolve Paper Root
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

- 4 · Open the Board (the FIRST thing enter does after resolving the root)
      Ruled 2026-07-26 (design board `QA1`, `QA4`). **`/haipipe-paper` is the single thing a human types.** For a board inside a paper, `haipipe-board` is CALLED,
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

- 4.1 · The three moments ① calls ③
      ```text
      1 ENTER                    here. The human is looking at ⑧ before work starts.
      2 AFTER EVERY WRITE TO ⑧   a stage run, a phase worker, a CHECK gate: each ends
                                 with a rebuild, or the human reads a paper that no
                                 longer exists. Owned by haipipe-paper-stage.
      3 BEFORE ① ACTS            a comment or a `>` lane arrived through serve.py, so
                                 ⑧'s markdown changed underneath. Re-read; never cache.
      ```

- 4.2 · When the push fails
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

- 5 · Read Order
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

- 6 · Dashboard Spec
      THE single source of truth for the behavior of `/haipipe-paper` with no arguments inside a paper, and for the panel this Console renders.
      The dashboard is a derive-from-disk preflight. It orients the session before the Console or any lifecycle stage acts.

- 6.1 · Golden Rule
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

- 6.2 · Lifecycle frontier
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

- 6.3 · Shallow check
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

- 6.4 · Render skeleton
      RETIRED 2026-07-26. The console no longer renders a panel; `⑧` is the panel.
      See Output Format below for the three lines the terminal still prints.

- 7 · Diagnosis Rules
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

- 8 · Output Format
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

- 8.1 · What was RETIRED with the text dashboard
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

- 9 · Free-form Routing
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

- 10 · Copilot Policy
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

- 11 · Session State
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

- 12 · Return Contract
      Every reply from a paper specialist (and every enter dashboard) MUST end with the closing block defined in `../../haipipe-paper/SKILL.md` (Closing Block section, the single source of truth).
      Omitting it is a protocol violation.
      Do not copy or redefine its shape here; use the umbrella contract verbatim so the Board URL and phase line cannot drift.
### The other files

3 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
feedback/2026-06-22_console-too-dense-want-stage-progress.md    15 ln  我感觉第一次出来的东西太多了，我可能其实就像知道这个论文是什么，什么story之类的，你这给我整的不知道去哪看啥了。然后我觉得有个stage process挺好的。有个lifecycle之类的，从左到右，一个stage
feedback/2026-06-22_enter-should-show-what-paper-is-about.md    14 ln  When entering a paper, the dashboard should tell the user what this paper is about — not just the structural s
feedback/README.md                   9 ln  haipipe-paper-enter — Feedback Inbox
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.

## States
### P · Page-level health ruling
- ⬜ P1 · Page generated 260804 1627; nothing ruled yet.

## Log
260804 1627 · page generated from `paper/haipipe-paper-enter/` by `skillpage.py new`

<!-- haipipe:skill:log:start d78d1928a1c81d9e paper/haipipe-paper-enter -->

Converted from the skill's own `CHANGELOG.md`: 24 releases.

260726 · `0.6.6` · Resource frontier uses the live schema
      - Resource completion now requires real `Resource Description` and
        `Q-consumer` content, matching its stage contract and template.
260726 · `0.6.5` · a green state needs its receipt
      - Frontier completion now requires the disk predicate, first `state:` token
        `✅`, and an approved gate row with actor/date in the S page's `## Log`.
      - A green page missing that receipt is STALE and reopens CHECK rather than
        advancing.
      - Corrected the console scan to the current probe anatomy,
        `1-probes/PP*/*.md` (one q-executor file inside each topic folder).
      - Removed the unsupported `argument-hint` frontmatter key.
260726 · `0.6.4` · no retired strip vocabulary
      - The compatibility exemption now explains the Board projection directly.
      - Venue pin detection names the actual S-page `state:` line.
260726 · `0.6.3` · content and gate form one frontier predicate
      - Made frontier selection test both the disk artifact predicate and the
        required S-page `✅` gate.
      - Content that exists under `🔴`, `🟡`, or `⏸️` now stops at the current stage
        and recommends its CHECK action instead of silently advancing.
      - Kept `✅` plus missing content as the narrower STALE over-claim case.
260726 · `0.6.2` · session pointer, not a second state store
      - Reduced `.paper-console.yaml` to paper identity fields only: `paper_root`, `active_paper`, and `updated`.
      - Every follow-up action now re-reads the Board and relevant S pages and derives frontier, gates, maturity, round, and open needs from disk before routing.
      - Removed the local closing-block example; the enter skill now consumes the umbrella's canonical block verbatim.
260726 · `0.6.1` · the venue pin reads the `state:` line, not an invented frontmatter key
      Found by running the skill against `Paper-Personality2Opioid-MISQ2026` rather than by reading it.
      Yesterday's `STATUS.md` retirement moved the venue pin to "`S-Venue-0-venue.md` frontmatter, `venue:`". That field does not parse. `haipipe-board`'s face grammar is a CLOSED whitelist (`src/parse.py:145`): `state|owner|method|session|requires|style-from|provides|contract-source-hash`. A `venue:` key is invisible to the board, so the frontier predicate failed on the only real paper, and the fix was never going to be "add the key" — the whitelist is `haipipe-board`'s, ruled on its own board.
      The pin needed no new field. It was already on the page's own `state:` line: `state: ✅ PINNED · MISQ 2026`. Corrected in 12 places across the stage contract, the console, the router, the two refs, the anatomy spec and `restructure`.
      Recorded on design-board face `QA4` as the third cross-package gap of the day, with the rule it produced: **`haipipe-paper` may not invent a face-grammar key.** It uses a key that already parses, or it goes to the board's own board and asks.
260726 · `0.6.0` · enter OPENS the board, and stops being a second renderer
      Implements the single-door ruling (design board `skills/diagrams/01-haipipe-paper-260725`, faces `QA1` + `QA4`, JL 2026-07-26): **`/haipipe-paper` is the single thing a human types**, and it CALLS `haipipe-board` to build and open the paper's `0-lifecycle/`. `haipipe-board` remains its own door for boards that are not inside a paper. Calling is not owning: `haipipe-board` still owns the format, the build, the filename rule, the html and the write-back.
      - **New `## Open the Board`, the first thing `enter` does after resolving the root.** Before this, the console read `board.md` as a data file and never called `haipipe-board` at all: a human who wanted to SEE the paper typed a second skill, with the `0-lifecycle/` path, by hand. Now `enter` resolves the root, get-or-creates when the path is new, calls `build.py` + `serve.py`, and hands over the URL.
      - **The 152-line text dashboard is gone.** The paper-identity table, the two-line focus strip, the current-state block, the stable block and the artifacts-read list were a second renderer of the same S pages. The board renders every one of them, in a browser, with comment lanes a terminal cannot have. `SKILL.md` 570 to 421 lines.
      - **What the terminal still prints, and why**: the board URL first, one frontier line, one sentence on what the paper is about, Open Needs with routes, Recommended Next. That is what a terminal is genuinely good at, and it is also the fallback when the push fails.
      - **The push may never fail silently.** The URL travels over the VS Code IPC socket on 5599, and after this ruling that path is on the critical path of every paper session. Say it failed, print the URL anyway, never fall back to `file://`. A silent success is indistinguishable from a dead port forward, which is how a session was lost on 2026-07-25.
      - **Loopback diagnosis retired as a rendered block.** With the frontier derived and nothing stored, re-running an earlier stage is ordinary rather than an anomaly worth a section.
260726 · `0.5.0` · derives the frontier for real, and DRIFT is retired with STATUS.md
      Aligned with the paper-folder layout ruled 2026-07-26 on the design board (`skills/diagrams/01-haipipe-paper-260725`, face QA6): `0-sections/` to `sections/`, `0-displays/` to `displays/` (one folder per unit, the only home of an asset, no top-level `figures/`), `1-compile.sh` to `2-src/compile.sh`, and `STATUS.md` retired.
      - **DRIFT is gone, replaced by STALE.** DRIFT named the gap between a stored `current_layer` and the disk. With nothing stored there is no such gap. What survives is a real disagreement: an S page whose own `state:` claims done while its disk predicate fails. That is now `STALE`, and it is narrower and more useful, because the page sits ON the artifact it describes and cannot over-claim about a paper it is not part of.
      - **The Golden Rule rewritten** around the S page rather than around distrusting a status file.
      - **Paper-root signatures rewritten**: `0-lifecycle/board.md` first, because every paper is Board-first. `STATUS.md` is explicitly NOT a signature; a folder carrying only one is a leftover, not a paper.
      - **Read Order rewritten to the eight family folders.** It was still reading `0-lifecycle/0-seed/0-seed.tex`, `1a-resource/`, `1b-claims/`, `2b-pitch/`, `3-narrative/`, `4-display/`, none of which exist after the one-family-one-folder migration.
      - **The frontier predicate table** now tests S pages, and the venue predicate reads `S-Venue-0-venue.md` frontmatter.
      - **The stage strip** reads the derived frontier. It was specified in the 260622 feedback as reading `STATUS.md current_layer`, with the stated precondition that a stale value would make it lie; the console had already stopped honoring that design, and this makes the file match the behavior.
260724 · `0.4.1`
      Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 4.1.1; older entries below keep their original numbers).
260719 · `4.1.1` · vocabulary: a probe question is an ENTRY, not a SECTION
      ### Changed
      The probe file's unit of one question was renamed `## Q-<Stage>-<n>` SECTION (flat `serves:` /
      `target:` / `a-consumer:` fields) -> `## QX<n>` ENTRY (four `###` subsections) when the probe model
      changed. This file still said SECTION, so an agent reading it wrote the OLD flat structure, which
      `check-probe-cards.sh` FAILs as `stale-old-format` -- that stage's PROBE phase could then never go
      green. Mechanical rename, no design change. (JL ruling 2026-07-19, board 260719-04-SEED-2PHASE D5:
      "如果这样的话，那还是叫entry 吧". Swept 31 lines across 15 files; phrase-level, because "section"
      also legitimately means a MANUSCRIPT section in these docs.)
260719 · `4.1.0`
      Changed (JL 2026-07-19, paper/2-phase refactor — the sidecar model is retired: `1-probes/` is the only consumer-side source of truth)
      - **The console no longer SCORES a document nobody writes.** The phase-derivation rules read `cite ✅ if _CITATION_ all placed and density >= venue norm` and `val ✅ if _VALUES_ all verified` — a metric the Console could not compute, over files that are not created. Re-rooted onto what exists on disk: `draft` now checks that every hole is FILLED or OWNED (each `\cite{TOADD}` / `{VAL:?` carries a `[Q-<Stage>-<n>]` id; `🕳️ N` counts unowned holes), and `probe` reads the paper's `1-probes/` entries (`**state**` + whether `### a-executor` is filled; `📨 N` counts entries still open).
      - **The phase strip is FOUR glyphs, one per phase, at every stage** — `draft │ probe │ revise │ check`. The `probe: cite X val X disp X` sub-track split is gone from the Line-2 spec and from both rendered examples; it mirrored three lane workers that no longer exist, and it made section-edit render a different strip shape than every other stage.
      - **Read Order step 4** re-rooted: scan `5-section-edit/` for section `.md` + `_LOG_*` files (was: + `_CITATION_*`, `_VALUES_*`). New step **4b** reads `1-probes/PP*.md` — named as the source the `probe` glyph derives from, so the Console reads the questions before it reports on them.
260719 · `4.0.2`
      - WIKI RETIREMENT — the retired wiki folder's `05-paper-dashboard.md` absorbed here as the **Dashboard Spec** section (inserted between Read Order and Diagnosis Rules, where the console actually uses it). It IS this skill's dashboard spec, so this skill is its ONE home.
        - Carried intact: the Golden Rule (never report a stage done because STATUS.md says so; disk wins, the gap is DRIFT), the lifecycle-frontier spine + per-stage done-predicate table + next-action commands, the note that `1-resource`/`1-claims` share the number 1 on purpose (`stage-strip.sh` strips the digit), the OK/ACTIVE/TODO/DRIFT/BLOCKED glyphs, the 5-step shallow check, the render skeleton (paper header → Story line → 进度 spine) with its per-stage glyph legend and the worked MedJournal example, the field-source table, and the Open needs block.
        - Deduped rather than duplicated, since this file already restated parts of the spec: the resource exemption keeps its single full statement in Diagnosis Rules (the spec's frontier table points there), and the maturity ladder is MERGED into the existing evidence→maturity table, which gains the rungs the wiki carried and this file lacked (`scaffold`, `display-map`, `submitted`, `accepted/published`) plus the fuller `resource` / `resource-blocked` definitions.
      - Reference rewiring after the wiki retirement: `Read first:` drops the dashboard entry (the spec is in this file now) and repoints rounds -> `../haipipe-paper-round/SKILL.md`, skill structure -> `../../README.md`, delivery need -> `../../haipipe-paper/SKILL.md`; the stale-deliverable flag now cites the Lifecycle TeX Quality Standard in `../../3-deliver/haipipe-paper-deliver/SKILL.md`.
260714 · `4.0.1`
      - Need-diagnosis table: "a BUILD card whose eta: has passed" -> "a BUILD section"; "the gateway mints the PP and picks the type" -> "the PROBE worker opens the SECTION and routes it".
260714 · `3.3.0`
260714 · `4.0.0`
      - PROBE REDESIGN (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL 2026-07-14 — R1-R18). 1-probe-plans/ -> 1-probes/ (PPNN_<topic>.md, one file per TOPIC, one SECTION per question: serves/target/state/commission/reading + ONE `## Why` per file holding the stake). Binding is by PATH: a section's `target:` points at the answering `<leaf>/QA/<n>-<slug>.md` in the bank. DELETED: `## Verdict`, the `verdicted` and `dispatched` states, `_ASK/`/`_ANS/` stubs, `answers:`, and Agent(haipipe-probe-orchestrator-agent) (the GATEWAY — archived + de-registered). A claim's STATUS now lives ONLY in 0-lifecycle/1b-claims/1b-claims.md. Dispatch is now DIRECT: the section's `commission:` block, VERBATIM, to Agent(haipipe-task-orchestrator-agent) / Agent(haipipe-discovery-orchestrator-agent).
      - 'landing a settled verdict in a 1-probe-plans/PPNN card' -> 'landing a settled claim status in 0-lifecycle/1b-claims/1b-claims.md'.
      Fixed
      - **The console shipped the 7-stage spine and contradicted its own script.** `stage-strip.sh` had rendered 9 stages since the resource ruling landed, while this SKILL.md mentioned `resource` zero times — every strip example, the frontier table, the maturity table and the routing table were all pre-resource. Repaired throughout.
      - Frontier-diagnosis table: `seed exists but claims are absent/thin -> 0-seed -> 1-claims` (seed handing straight to claims) SPLIT into `0-seed -> 1-resource` and `1-resource -> 1-claims`.
      - **Resource exemption carried into the console (`n/a` COUNTS AS PASS).** Every live paper predates the stage (shipped 2026-07-14); without the exemption every one of their frontiers REGRESSES to `resource` and the console reports DRIFT on seeds JL personally approved. Backwards-only and per-paper: a paper seeded after 2026-07-14 gets no exemption. Also states that `resource ⬜` in the strip is the strip's artifact test, not drift.
      - Maturity table: added the `resource` and `resource-blocked` rungs (the latter from the stage's `park` exit).
      - Free-form routing table: added the `resource` verb (+ prereq / "do we have the data" / "does the checkpoint exist").
      - Open-needs table: added the `1-resource` surface (unanswered `Q<n>`, or a BUILD card whose `eta:` has passed).
      - Loopback table: added `1-resource` (resource cannot carry the claim) and `0-seed` via resource's `reseed` exit (every demand row unobtainable).
      - Read Order: added `0-lifecycle/1a-resource/1a-resource.md`.
      - All six stage-strip examples regenerated to the real 9-stage output of `stage-strip.sh` (verified against live papers Paper-ScalingGlucose-NatSeries2026 and Paper-PersonalizedGlucoseModel), including a new resource-stage example.
260703 · `3.2.2`
      Fixed
      - Focus Strip: added the exactly-one-🔥-one-🚀-never-zero rule with the virgin-paper collapse case (`draft 🔥🚀`); examples reordered so the frontier/default case leads and a fresh-paper-at-seed example added (loopback examples kept, labeled as such).
260703 · `3.2.1`
      Fixed
      - Return Contract still carried the retired 4-field tail (status / paper_root / current_layer / next); the live test session rendered it. Replaced with the umbrella Closing Block shape (status merged with active stage, no paper_root/current_layer) and pointed to haipipe-paper/SKILL.md as the single source of truth.
260703 · `3.2.0`
      - GET-OR-CREATE absorbed (JL: 直接去掉create，enter的时候没有就call create): a missing path now offers to create the paper -- confirm-gated (repo creation is outward-facing), org resolved per invocation, repo-backed inside Project-* repos per the papers-inside recipe, contents scaffolded via haipipe-paper-lifecycle folder, double-bump, then straight into the console. The umbrella's create verb is retired (haipipe-paper 2.4.0).
260703 · `3.1.1`
      - phase spine renamed DGPC -> DPRC (GATHER -> PROBE, POLISH -> REVISE); phase strip line now 'draft │ probe: cite val disp │ revise │ check' (stages without sub-tracks show just 'probe').
260703 · `3.1.0`
      - focus strip dual markers -- 🔥 (active now) + 🚀 (frontier reached); both appear on stage and phase lines, collapse to 🔥🚀 when coincident; convention codified in 01-focus-strip-markers.md; added a shared-reference folder parallel to feedback/.
260702 · `3.0.0`
      - lifecycle reorder (seed -> claims -> venue -> pitch -> narrative -> display -> section-edit); claims is stage 1 (venue-free), pitch is stage 2 (venue-aligned); minimap removed; section-edit replaces write/edit with per-section DGPC status grid (DRAFT/GATHER/POLISH auto, CHECK human); updated file paths, stage strip, diagnosis rules, free-form routing, and dashboard format.
260622 · `2.1.0`
      - dashboard leads with pitch summary + stage strip before operational details; read order prioritizes 1-pitch.tex; return contract enforces structured tail + failed status; stale-deliverable flag from 13-tex-quality.md.
260622 · `2.0.0`
      - reframed as the Paper Console; added derive-from-disk frontier, free-form routing, copilot policy, and .paper-console.yaml session state.
260621 · `1.2.0`
      - open-needs paper session loader.

<!-- haipipe:skill:log:end -->
