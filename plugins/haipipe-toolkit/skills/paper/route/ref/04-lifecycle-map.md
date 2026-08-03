# Paper Lifecycle Map

The Paper Lifecycle Map connects each lifecycle stage to its skill procedure,
question, action, file ownership, external calls, human output, machine state,
and stop gate. The lifecycle is the stage spine from `paper-lifecycle.md`, not a
separate set of verbs.

## Map

Phase dimension: every stage skill below runs the ordered `phases:` declared by
its `stage.md` through the `2-phase/` workers
(`haipipe-paper-{draft,probe,revise,check}`). Most stages declare DRAFT ->
PROBE -> REVISE -> CHECK; Venue declares DRAFT -> PROBE -> CHECK. Users invoke
stage skills only; every current stage has one human gate, CHECK.

## Board Projection

The lifecycle board is the human-facing projection of this execution map. Its
S faces use stable ownership families:

```text
Seed       research possibility and literature position
Work       resources and claims
Venue      venue choice and pitch
Display    claim-to-display map, approved assets, captions, and placement
Main       narrative plus reader-facing manuscript sections
Appendix   appendix control plus appendix sections
Submission reconcile, compile, review, and submit
```

Family order is for navigation, not execution. The stage router still resolves
the executable sequence from `haipipe-paper-stage/stages/index.yml`:

```text
seed -> resource -> claims -> venue -> pitch -> narrative -> display -> section-edit
```

Each stage contract declares `board_family` and `board_unit`; Board tooling owns
and resolves the literal S-face filename. Those fields map stage progress to one
S face; they do not replace the stage's `artifact:` path and do not reorder the router. After a phase runs,
the mapped S face synchronizes only its `state`, `Items to Finish`, and
`Where we are`. Its Content remains the embedded or linked lifecycle artifact.

Display is an independent ownership family because Main and Appendix both consume
its evidence units; execution still places it after Narrative. Submission is downstream of the routed authoring stages. The same Submission
pages are reused for every submission or revision round. External review
reopens the affected Work, Display, Main, or Appendix pages, then the paper reruns
Reconcile -> Compile -> Final Review -> Submit.

| Step | Skill Procedure | Question | Action | Reads | Writes | External Calls | Human Output | Machine State | Stop / Gate |
|---|---|---|---|---|---|---|---|---|---|
| `enter` (console) | `haipipe-paper-enter` | Which paper is active, what stage is blocked, what open needs remain? | Resolve root, open Board, derive artifacts + S gates from disk, route input | 0-lifecycle/board.md + every S page's `state:`, displays/, sections/, git | `.paper-console.yaml` identity pointer only | `haipipe-board` | Board URL + frontier + open needs | the S pages and artifacts; no console state cache | no paper root, ambiguous paper |
| `0-seed` | `seed` | Why might this paper exist? | State possibility: question, motivations, claim shape | seed notes, project evidence | `0-lifecycle/0-seed/S-Seed-0-seed.md` (+ its `## Log` gate row) | none | seed contract | `S-Seed-0-seed.md` | not viable -> drop | venue: FREE |
| `1-resource` | `resource` | What must EXIST for this paper to be testable, does it exist, can it CARRY the claim? | Derive Demand (one `N<n>` per `H<n>`), ASK the Questions (`Q<n>`); the PROBE phase opens an entry per Q and routes it within the invocation's `--depth` ceiling | seed (Tentative Claim Shape), `S-Seed-0-seed.md` forward pointers | `0-lifecycle/1-work/S-Work-0-resources.md` (+ its `## Log` gate row) | the PROBE phase ONLY (never executes bank work inline) | Demand + Questions (with their **A**) | `S-Work-0-resources.md` | CHECK gate; `--depth` is the separate human spend authorization | venue: FREE |
| `1-claims` | `claims` | What must be true? What evidence do we have? | Maintain claim ledger (the ONLY home of a claim's status), mark needs | seed, `S-Work-0-resources.md`, the answering QA files a probe entry's `target:` names | `0-lifecycle/1-work/S-Work-1-claims.md` (+ its `## Log` gate row) | the stage's `haipipe-paper-probe` worker → isolated collector | claim ledger | `S-Work-1-claims.md` | claim unsupported/too strong, no route | venue: FREE |
| `venue` | `venue` | Which venue fits, and pin it | Recommend best-fit venue; PROBE records every lookup as an entry; CHECK pins the venue page's `state:` line | seed, claims, topic, `venue/playbook-*` packs | `S-Venue-0-venue.md` + its `## Log` gate row | the stage's `haipipe-paper-probe` worker → isolated collector | venue shortlist + recommendation | `S-Venue-0-venue.md` | no clear fit; missing entry/receipt; venue change re-runs pitch | venue: (the chooser) |
| `2-pitch` | `pitch` | What is the paper selling to THIS audience? = cover letter | Maintain one-minute story + cover letter: Editor's Chair Test, [primary] claim, RQ framing | seed, claims (venue-neutral H), `venue/playbook-<venue>` (framing) | `0-lifecycle/2-venue/S-Venue-1-pitch.md` (+ its `## Log` gate row) | none | pitch / cover letter | `S-Venue-1-pitch.md` | abstract/intro sells another story | venue: ALIGNED |
| `3-narrative` | `narrative` | How do claims structure into a paper for THIS venue? | Build section-mirrored arc | claims, pitch, `venue/playbook-<venue>` (structure) | `0-lifecycle/2-venue/S-Venue-2-narrative.md`, DR rows in `0-lifecycle/3-display/_DISPLAY_REQUEST.md` (+ its `## Log` gate row) | none | narrative | `S-Venue-2-narrative.md` | arc weak -> pitch / claims | venue: ALIGNED |
| `4-display` | `display` (+ render skills) | What figure/table carries each claim per THIS venue's limits? | Plan display map + units | claims, narrative, results, `venue/playbook-<venue>` (-> Display) | the display S pages, `displays/displayNN-<slug>/*` (+ the `## Log` gate row) | `/haipipe-task-for-display` | display map + units | `4-display.tex`, display units | display cannot support claim | venue: HEAVY |
| `5-section-edit` | `section-edit` | How is each section written for THIS venue? | Per-section DRAFT -> PROBE -> REVISE -> CHECK | 3-narrative, display units, `venue/playbook-<venue>` | `0-lifecycle/4-main/S-Main-*.md` (the section's S face), `sections/*.tex` | compile / overleaf | section outlines + draft PDF | section scaffolds, section files | writing exposes missing evidence -> 1-claims | venue: SPECIFIC |
| `review` | `haipipe-paper-{claim-audit,reviewer,optimizer}` | Which layer is broken, or ready? | Adversarial audits, route verdict | PDF, lifecycle files, sections | review notes, the current `S-Round` page | reviewer agents / Codex | review verdict + routing | the S pages' `state:` | overclaim, broken layer, venue check fails |
| `round` | `haipipe-paper-round` (enter/new/triage/apply/close) | Where does this round's discussion/decision/todo/applied go? | Open / triage / apply / close round | discussion, review, decisions | `0-lifecycle/7-round/S-Round-<n>-<vYYMMDD>.md`; received letters sit beside it | route each todo to a stage or evidence worker | round log | the S-Round page; no stored pointer | unresolved item with no target |
| `respond` | `haipipe-paper-rebuttal`, `4-respond/*` | How do reviews become revision + rebuttal? | Parse reviews, plan, draft, revise | reviews, submitted manuscript | the owning S-Round page, received letters, `sections/*.tex` | route new evidence through the affected stage's PROBE worker | rebuttal + revision | round files | reviewer needs new evidence, approval |
| `present` | `5-present/{paper-slides,paper-poster}` | How does the paper cash out? | Build slides / poster | final paper, pitch, displays | slides, poster | none | slides/poster | n/a | talk cannot explain in one minute -> pitch |

## Evidence Loop (back to probe)

The lifecycle loops out to probe whenever the problem is EVIDENCE, not wording.
The contract is `delivery-need.md` (paper-owned; no cross-skill shared file).

```text
1-claims GAP  ──out──▶  /haipipe-paper probe "<need>"   (a question ENTRY in 1-probes/)
                          PROBE phase: ORGANIZE → MATCH → DISPATCH → POINT → INTERPRET
                          the executor answers in <task-folder>/QA/<n>-<slug>.md
1-claims slot ◀─backfill─  the entry's `### a-executor` lands and each Q-consumer's
                           a-consumer interprets it; THE CLAIM'S STATUS IS WRITTEN IN
                           S-Work-1-claims.md; the executor never edits paper prose
```

Outbound points: `1-claims` (a claim's status is unsettled), `4-display` (display
needs a run), and `review`/`respond` when an evidence gap surfaces. All route
through `delivery-need.md`. The inbound backfill writes the claim's status in
`0-lifecycle/1-work/S-Work-1-claims.md` (supported | refuted | inconclusive), citing the
entry's `**target**:` QA file. Ownership split: the paper owns the NEED and the
JUDGMENT; the EXECUTOR owns the FACT (its `<task-folder>/QA/<n>-<slug>.md`, general
language, reusable by any paper). Anatomy: `probe/haipipe-probe/SKILL.md`.

## File Principles

The paper folder is fixed. Execution contracts and the board control plane are
related but distinct:

```text
0-lifecycle/board.md
0-lifecycle/**/S-<Family>-<unit>-<slug>.md         lifecycle board face AND execution artifact
0-lifecycle/{board.md,board.html}                  board index and generated view
sections/*.tex
displays/displayNN-<slug>/
0-lifecycle/7-round/vYYMMDD/S-Round-<n>-<vYYMMDD>.md
the S-Round pages themselves (no stored pointer)
.paper-console.yaml   (active paper identity only, at paper/project root)
```

The execution artifact path is defined by each `stage.md`, and it IS the S face:
`artifact:` resolves to `S-<board_family>-<board_unit>-<board_slug>.md` in the
stage's directory, with the filename owned by Board tooling (QB4@paper). `log:` was
retired on 2026-07-26: no live paper ever carried a `_LOG_*.md`, and the S face
already holds current state, remaining work, and history in one page.
Only `4-display` compiles its execution artifact (`4-display.tex` + PDF). A
stage is done only when its execution artifact resolves on disk with real
content and every required S face has first state token `✅`.

## Command Routing

```text
/haipipe-paper                  -> Console (active paper) or venue dashboard
/haipipe-paper enter|status     -> Console
/haipipe-paper seed             -> 0-seed
/haipipe-paper resource         -> 1-resource (prereq | prerequisite | need | demand |
                                   "do we have the data" | "does the checkpoint exist")
/haipipe-paper claims           -> 1-claims
/haipipe-paper venue            -> venue (pin target journal in S-Venue-0-venue.md)
/haipipe-paper pitch            -> 2-pitch
/haipipe-paper narrative        -> 3-narrative
/haipipe-paper display|figures  -> 4-display (display contract + units)
/haipipe-paper figure1|framework -> 4-display framework mode (Figure 1 candidate rounds)
/haipipe-paper section-edit     -> 5-section-edit

# 4-display render verbs (data-driven vs concept), dispatched via haipipe-paper-lifecycle:
/haipipe-paper table            -> haipipe-display-table        (data CSV -> LaTeX table)
/haipipe-paper figure           -> haipipe-display-figure       (data CSV -> plot; SINGULAR = plots)
/haipipe-paper diagram          -> haipipe-display-diagram      (concept -> deterministic vector SVG)
/haipipe-paper illustration     -> haipipe-display-illustration (concept -> AI raster, Codex bridge)
/haipipe-paper write|edit       -> 5-section-edit (per-section prose work)
/haipipe-paper review           -> review
/haipipe-paper round            -> round
/haipipe-paper rebuttal|respond -> respond
/haipipe-paper slides|poster    -> present
/haipipe-paper <venue>          -> apply venue profile (conference/journal/is)
/haipipe-paper enter (missing path) -> get-or-create, then console
/haipipe-paper "<free text>"    -> active Console router, else plan at the frontier
```

## Procedure Status

Every stage now has a dedicated procedure:

```text
0-seed         seed                       (stages/0-seed/)
1-resource     resource                   (stages/1a-resource/; venue-FREE)
1-claims       claims                     (stages/1b-claims/)
5-section-edit section-edit               (stages/5-section-edit/; per-unit)
round          haipipe-paper-round        (built; verbs enter/new/triage/apply/close)
```

Stage procedures own the execution paths declared in their `stage.md`.
Lifecycle S faces are the board projection of those contracts. Only
`4-display` owns a `.tex` + PDF execution artifact.
