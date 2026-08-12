# The full walk: one paper board, birth to submission
state: 🟡 PARTIAL · written 260806 on JL's ask; awaiting his read
owner: JL
method: walk the ten groups in execution order; every stage states its page, phases, evidence, gate, and artifact

## Opening
What happens, in order and in full, when one paper walks its board from nothing to a submitted round?

JL 260806: "把 paper 这个 board 从头走到尾，方方面面、点点滴滴，都给我详细列一下." This page is that list. It is the WALK view; the wiring view (which unit calls which) is Skill-6 `[1/2]`, and the one-call zoom is Skill-0 `[2/2]`. Every stage below runs the same engine loop drawn in `§1`; what changes per stage is only its stage.md contract, its craft, and what its gate accepts.

## Diagram
```text
  🚪 enter (birth) ─▶ S01 Opening ─▶ S02 Work ─▶ S05 Display ─▶ S06 Main
       │                seed venue      resource     one page      sections,
       │                pitch           claims       per unit      per unit
       │                                narrative       │             │
       │                     ▲              │           ▼             ▼
       │                     │       S03 Literature · S04 Value   S07 Appendix
       │                     │       (the two probe POOLS: every       │
       │                     │        stage's questions land here)     ▼
       │                     └──────────── venue re-target ◀── S09 Build ─▶ pdf
       │                                                            │
       └──────────────────────────────────────────────▶ S08 Present · S10 Round
                                                          poster     submit ↔
                                                          slides     rebuttal
```

## Content
### §S The script: ten scenes, four lines each (JL 260806, "我们要不要一起过一过剧本")
Every scene reads the same way: YOU SAY one verb · THE SYSTEM does its part under the stage.md contract · YOU SEE pages appear · IN YOUR HANDS is a gate or a spend call. You do only three things all play long: type a verb, tick or bounce each CHECK gate, approve --depth spend.

```text
scene 0 · enter      you: /haipipe-paper enter papers/Paper-X (missing → asks once)
                     system: scaffolds README + 0-lifecycle/board.md + seed shell,
                     builds, pushes the board to your browser
                     yours: nothing yet, start writing

scene 1 · seed       you: /haipipe-paper seed
                     system: DRAFT writes question·motivation·landscape·H1-H3;
                     every shaky claim wears [Q-Seed-n] → collected into E0 queues
                     yours: the gate: is this seed worth a paper?

scene 2 · resource   you: /haipipe-paper resource
                     system: one row per asset (data·checkpoints·code) + evidence;
                     unknowns PROBE out at depth 0 (harvest, free)
                     yours: gate + the spend call: open --depth for what's missing?

scene 3 · claims     you: /haipipe-paper claims
                     system: H-slots become the ledger: status+confidence+needed
                     numbers; missing numbers PROBE to S04, return as value bindings
                     yours: gate (from now on, claim status changes ONLY here)

scene 4 · venue      you: /haipipe-paper venue "MISQ"
                     system: reads the QBv catalog ONCE, pins the venue CONTRACT
                     (no REVISE; retarget later = replay this scene only)
                     yours: gate: submit there?

scene 5 · pitch +    you: pitch, then narrative
        narrative    system: one-minute story against the pinned taste; then the
                     beat map: which section owes which claim and which display
                     yours: two gates (narrative is every later scene's work order)

interlude · S03/S04  not a scene: the evidence desk running through the whole play.
                     Every scene's question is COLLECTED into a topic's E0 queue;
                     PROBE promotes it to an E<n> division + its QA-probe, agents
                     cross the wall, the QA-bank answers, the record copies it in.
                     You drop by to watch consumer rows turn SUPPORTED / BOUND.

scene 6 · display    you: /haipipe-paper display "Table1 + main regression + concept"
                     system: one for-display page per unit, each climbing
                     ①requested→②sourced→③rendered→④ACCEPTED→⑤placed;
                     missing aggregates go to the bank, never inline
                     yours: ④ per unit, by eye; a re-render falls back to ③

scene 7 · sections   you: /haipipe-paper section-edit intro (one unit at a time)
                     system: template resolved per (venue × section_kind);
                     citation bindings land as \citep, values with their lanes,
                     accepted displays as \ref; an unlanded binding stays lit
                     yours: one gate per section; appendix same law

scene 8 · build      you: compile / diffpdf (door verbs, no gate)
                     system: board pages → LaTeX → main.pdf; diffpdf shows the delta
                     yours: read it

scene 9 · round      you: round (submit) … months later: rebuttal with the letters
                     system: each comment routes to the page it reopens; that page
                     replays ITS scene; reconcile→compile→review→submit, reused
                     every round; S08 poster/slides come from the accepted copy
                     yours: one gate per round, until ✅ accepted
```

### §0 Birth: from nothing to a board
- `/haipipe-paper enter <path>` on a missing path CONFIRMS, then creates: repo-backed inside a Project-* (org asked, never assumed) or a plain folder.
  `haipipe-paper-folder` scaffolds the minimum: README, .gitignore, `0-lifecycle/` with `board.md` and one S01 Opening page. Everything else is absent-until-allocated.
- The paper's `0-lifecycle/` IS a board: `build.py` renders it, `serve.py` makes it live, and every page below is a page ON it.
- The console (`enter`/`status`) derives the frontier from disk on every call; nothing is stored as status.

### §1 The loop every stage runs (stated once, referenced ten times)
```text
  door: verb → stages/index.yml → ONE stage.md → page exists (create-page.py)
  engine: haipipe-page · TYPE for-stage · PHASE by authority
    DRAFT   write Content per template.md; every unknown becomes an owned
            hole: a Q-consumer with its stake, an Aims row
    PROBE   only exit to evidence: Q-executor (stake stripped) → a QA-probe
            record under S03 or S04 → bank agents → QA-bank file; the record
            copies the answer in (A-executor), the owning E<n> division's
            consumers rows interpret it (A-consumer). Ceiling: probe_depth
            (0 = harvest only; --depth is the human spend lever)
    REVISE  weave landed answers in; discharge [Q-<Stage>-n] brackets
    CHECK   run the stage.md `checker:` → fresh judge → the HUMAN GATE:
            state ✅ is [CHECK-JL]'s alone
  finish: build.py rebuilds board/ · the Log gains its [PHASE-actor] line
  craft: files load last (citation-craft, values-craft, …): the LaTeX how-to
```

### §2 S01 Opening: three pages that fix what the paper IS
- seed (order 0, venue-FREE) · page S-Open-Seed
  The seed question, motivations, landscape, hedged H1/H2/H3. Its unknowns are collected into S03/S04's E0 queues.
- venue (order 2a) · page S-Open-Venue · phases [draft, probe, check], no REVISE
  Reads the QBv venue catalog ONCE (the one stage allowed to); pins the journal; produces a CONTRACT, not prose. Retarget = re-run venue; seed/resource/claims never change on retarget.
- pitch (order 2b, venue-ALIGNED) · page S-Open-Pitch
  The one-minute story against the pinned venue's taste.

### §3 S02 Work: what the paper has, and what it claims
- resource (order 1a, venue-FREE) · S-Work-R + unit pages
  What must EXIST for the paper to be testable: data, checkpoints, producing code; each resource one row with its evidence.
- claims (order 1b) · S-Work-C control page + C0..Cn unit pages
  The claim ledger: H-slots with status supported | refuted | inconclusive + confidence. THE only home of a claim's status; every number cited by a claim needs a value binding.
- narrative (order 3) · S-Work-N
  The arc: beats, section map, what each section owes the argument. Feeds display and the section blueprint.

### §4 S03 Literature · S04 Value: the two evidence POOLS
Not stages with their own runs: evidence pages (for-literature outward, for-value inward, keyed by the head `route:` line) that collect EVERY stage's questions into their E0 queue and organize Content BY EXECUTOR: one `### E<n>` division per Q-executor conversation.
- One hidden QA-probe record per conversation under `probes/L<n>-…/` or `probes/V<n>-…/` (1:1 with its E<n> division); dispatch crosses the wall to discovery (outward) or task (inward) orchestrator agents; many QA-probes may point at one QA-bank.
- Write-backs are typed, on the division's `#### consumers` rows: citation binding (real key + positioning + novelty verdict) or value binding (number + run/spec/QA paths + claim update). A consumer row closes SUPPORTED/BOUND · DEFERRED · WITHDRAWN; the page closes when every division's rows are terminal AND E0 is empty.

### §5 S05 Display: units a person accepts
- display (order 4) · one for-display page PER UNIT (figure, table, diagram)
  The acceptance ladder: ① requested → ② sourced (producing run named) → ③ rendered → ④ ACCEPTED by a person, dated → ⑤ placed (a sentence cites it). Re-render after ④ falls back to ③.
- The four renderers (table/figure/diagram/illustration) are commissioned workers; a missing display-ready aggregate goes to the bank via `haipipe-task-for-display`, never inline.

### §6 S06 Main · S07 Appendix: the prose, one section at a time
- section-edit (order 5, runs: per-unit) · one for-section page per reader-ordered unit (S-Main-1-introduction, … S-Appendix-A-…)
  Each carries its `### Venue contract` block: the blueprint line BINDS this unit's budget and shape (two-hop: only the venue stage read the catalog); section_kind joins division ↔ blueprint ↔ template.
  This is the landing surface: citation bindings become \citep on the owing sentence, value bindings become the number with its lane, display acceptances become \ref. A binding that never reached its sentence is this page's open work.

### §7 S08 Present · S09 Build: the artifact side
- S09 build tools (skills, not stages): compile (the pdf), diffpdf (what changed), to-overleaf, to-word, project (board pages → LaTeX candidates). `haipipe-paper-conform` audits the folder against the delete test.
- S08 present: poster and slides from the ACCEPTED paper (display family renderers; a slide deck can live as a for-slide page, divisions embedding the live deck).

### §8 S10 Round: the loop that repeats until acceptance
- round · dated work rounds: what came back, what was decided, what was applied.
- rebuttal · reviewer letters in; each comment routed to the page it reopens (a Work claim, a Display unit, a Main section), that page re-runs its loop, then reconcile → compile → review → submit again. The four submission steps are REUSED every round, never duplicated.

### §9 What is true the whole way
- One direction of control: door → stage data → engine → page; evidence only through PROBE; humans hold exactly two levers (every CHECK gate, and --depth spend).
- Every substantive act leaves a `[PHASE-actor]` Log line on its page; RUN leaves receipts under `_runs/`; git holds the bytes. Three ledgers, one story.
- The board is the paper's face: after every write, rebuild; what a colleague opens is never stale.

### §10 The stage table: template · draft · probe · revise/check, per stage
(shared by all eight stage.md stages, stated once: probes land in S03/S04's probes/L|V folders; CHECK = check-probe-cards.sh --stage <key> + fresh judge + [CHECK-JL]; DRAFT follows board draft contract + stage.md body + template.md)
```text
stage         template file                     DRAFT extra            REVISE/CHECK special
─────────────────────────────────────────────────────────────────────────────────────────
seed          S01-opening/seed/template.md      [Q-Seed-n] brackets    standard
venue        S01-opening/venue/template.md     reads QBv, only one    NO REVISE (d,p,c);
                                                                       outputs a contract
pitch         S01-opening/pitch/template.md     + readability.md       standard
resource      S02-work/resource/template.md     one row per resource   standard
claims        S02-work/claims/template.md       craft: citation +      status's ONLY home;
                                                values craft           numbers need bindings
narrative     S02-work/narrative/template.md    same 2 crafts          feeds display + blueprint
display       S05-display/display/template.md   + checklist ·          ladder ①→⑤; ④ human;
                                                figure-logic ·         re-render falls to ③
                                                draft-craft
section-edit  resolved per (venue×section_kind) 3 revise/check crafts  per-unit gate; binding
                                                                       must reach its sentence
S03/S04       none TODAY (template.md owed;     for-literature/-value  rows close SUPPORTED/
              being built 260806)               contracts              BOUND · DEFER · WITHDRAW
S08/S09/S10   no stage.md: present · build      —                      round reuses 4 submit
              tools · round/rebuttal skills                            steps every round
```

### §11 The type table: which for-xxx each stage touches
(resolution: S-filename → for-stage · head route: line → for-literature/-value · page-type: key → for-display/-slide/-section · QBv name → for-venue · Skill-/Agent-/Meeting- → for-skill/-meeting)
```text
stage           its S page     other typed pages it produces or reads
──────────────────────────────────────────────────────────────────────
seed·pitch·     for-stage      —
resource·
narrative
venue           for-stage      READS for-venue (QBv catalog, sole reader)
claims          for-stage      consumes S04's value bindings
S03 Literature  for-literature hidden QA-probe records (topic-entry contract)
S04 Value       for-value      hidden QA-probe records
display         for-stage hub  one for-display page per unit
section-edit    (per unit)     for-section, which LOADS for-stage + venue
                               contract block; the only two-layer type
S08 present     —              for-slide (division=beat, live deck embed)
S10 round       for-stage      for-meeting for spoken decisions
unused by paper —              for-skill (design boards) · for-design
                               (application's message A/B/C briefs)
```

## Aims
- A1 · The walk is complete and correct
  **Done when:** JL reads it and every stage's page/phases/gate/artifact statement survives his check; corrections land here, not in chat.

## States
- 🔨 A1 · Written 260806 from the shipped contracts (door 0.5.0, for-stage 0.5.0, the ten types, index.yml); awaiting JL's read.

## Files
- `../../../paper/haipipe-paper/SKILL.md`
  The door: every verb in §0-§8 enters here.
- `../../../paper/haipipe-paper/stages/index.yml`
  The execution order §2-§6 follow.
- `../QCskill-engine-skill/Skill-6-haipipe-board.md`
  The wiring view this walk complements.

## Log
- 260806 1000 · [REVISE-CC] §4 and the script interlude rewritten to JL's final evidence-page shape: questions are COLLECTED into E0, PROBE promotes each to an E<n> division + its QA-probe, write-backs land on `#### consumers` rows, and the type key is the head `route:` line (base 0.21.0, for-literature/for-value 0.4.0). Minimal edits; the walk's other divisions already read correctly.
- 260806 0700 · [REVISE-CC] the SCRIPT landed as §S on JL's placement ruling ("剧本放到哪里? QA11"): ten scenes, four lines each (you say · system does · you see · in your hands), the S03/S04 interlude, and the three-things-you-do rule; §0-§9 stay as the reference prose behind it, §10/§11 as the tables. Chat carried the Chinese telling; the page carries the English per the boards-are-English rule.
- 260806 0600 · [REVISE-CC] theory consolidated before the MISQ end-to-end rerun (JL: "在做之前,我想先把这个东西在理论上整清楚"): §10 the per-stage table (template · draft · probe home · revise/check), §11 the per-stage type table; S03/S04's missing template.md recorded as owed and its build dispatched the same hour, together with register-rows-as-evidence-cards (JL: literature/values are the first test bed for the card mechanism).
- 260806 0520 · [DRAFT-CC] page opened on JL's ask ("把 paper 这个 board 从头走到尾... 详细列一下"): the walk in nine divisions, the per-stage loop stated once in §1, pools not stages for S03/S04, the acceptance ladder, the venue two-hop, and the round loop; sources are the shipped 0.5.0 contracts, not memory.
