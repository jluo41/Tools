# Paper Lifecycle Map

The Paper Lifecycle Map connects each lifecycle stage to its skill procedure,
question, action, file ownership, external calls, human output, machine state,
and stop gate. The lifecycle is the stage spine from `paper-lifecycle.md`, not a
separate set of verbs.

## Map

Phase dimension: every stage skill below internally runs DRAFT -> PROBE ->
REVISE -> CHECK via the `2-phase/` workers
(`haipipe-paper-{draft,probe,revise,check}`). Users invoke stage skills
only; CHECK is the only human-involved phase.

| Step | Skill Procedure | Question | Action | Reads | Writes | External Calls | Human Output | Machine State | Stop / Gate |
|---|---|---|---|---|---|---|---|---|---|
| `enter` (console) | `haipipe-paper-enter` | Which paper is active, what layer, what open needs? | Resolve root, derive-from-disk dashboard, route input | STATUS.md, 0-lifecycle, 1-rounds, 0-displays, 0-sections, git | `.paper-console.yaml`, STATUS.md | none | dashboard panel | `.paper-console.yaml` | no paper root, ambiguous paper |
| `0-seed` | `haipipe-paper-seed` | Why might this paper exist? | State possibility: question, motivations, claim shape | seed notes, project evidence | `0-lifecycle/0-seed/0-seed.md` + `_LOG`, STATUS.md | none | seed contract | `0-seed.md` | not viable -> drop | venue: FREE |
| `1-claims` | `haipipe-paper-claims` | What must be true? What evidence do we have? | Maintain claim ledger, mark needs | seed, evidence refs, probe verdicts | `0-lifecycle/1-claims/1-claims.md` + `_LOG` + `_EVIDENCE_`, STATUS.md | `/haipipe-probe`, `/haipipe-discovery`, `/haipipe-task`, `/haipipe-insight` | claim ledger | `1-claims.md` | claim unsupported/too strong, no route | venue: FREE |
| `venue` | `haipipe-paper-venue` | Which venue fits, and pin it | Recommend best-fit venue, pin STATUS venue | seed, claims, topic, `_venue/playbook-*` packs | `STATUS.md` `venue:` | none | venue shortlist + recommendation | `STATUS.md` `venue:` | no clear fit; venue change re-runs pitch | venue: (the chooser) |
| `2-pitch` | `haipipe-paper-pitch` | What is the paper selling to THIS audience? = cover letter | Maintain one-minute story + cover letter: Editor's Chair Test, [primary] claim, RQ framing | seed, claims (venue-neutral H), `_venue/playbook-<venue>` (framing) | `0-lifecycle/2-pitch/2-pitch.md` + `_LOG`, STATUS.md | none | pitch / cover letter | `2-pitch.md` | abstract/intro sells another story | venue: ALIGNED |
| `3-narrative` | `haipipe-paper-narrative` | How do claims structure into a paper for THIS venue? | Build section-mirrored arc | claims, pitch, `_venue/playbook-<venue>` (structure) | `0-lifecycle/3-narrative/3-narrative.md` + `_LOG` + `_DISPLAY_`, STATUS.md | none | narrative | `3-narrative.md` | arc weak -> pitch / claims | venue: ALIGNED |
| `4-display` | `haipipe-paper-display` (+ render skills) | What figure/table carries each claim per THIS venue's limits? | Plan display map + units | claims, narrative, results, `_venue/playbook-<venue>` (-> Display) | `0-lifecycle/4-display/4-display.tex`, `0-displays/README.md`, `0-displays/displayNN-<slug>/*`, STATUS.md | `/haipipe-task-for-display` | display map + units | `4-display.tex`, display units | display cannot support claim | venue: HEAVY |
| `5-section-edit` | `haipipe-paper-section-edit` | How is each section written for THIS venue? | Per-section DRAFT -> PROBE -> REVISE -> CHECK | 3-narrative, display units, `_venue/playbook-<venue>` | `0-lifecycle/5-section-edit/<section>/` (outline `.md`, `_LOG`, `_CITATION_`, `_VALUES_`), `0-sections/*.tex` | compile / overleaf | section outlines + draft PDF | section scaffolds, section files | writing exposes missing evidence -> 1-claims | venue: SPECIFIC |
| `review` | `haipipe-paper-edit-{claim-audit,reviewer,proof-checker,submission-audit}`, citation components | Which layer is broken, or ready? | Adversarial audits, route verdict | PDF, lifecycle files, sections | review notes, `1-rounds/<round>/todo.md`, STATUS.md | reviewer agents / Codex | review verdict + routing | STATUS.md maturity | overclaim, broken layer, venue check fails |
| `round` | `haipipe-paper-round` (enter/new/triage/apply/close) | Where does this round's discussion/decision/todo/applied go? | Open / triage / apply / close round | discussion, review, decisions | `1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md`, `1-rounds/latest.md` | route each todo to a stage or evidence worker | round log | round files | unresolved item with no target |
| `respond` | `haipipe-paper-rebuttal`, `4-respond/*` | How do reviews become revision + rebuttal? | Parse reviews, plan, draft, revise | reviews, submitted manuscript | `1-rounds/vYYMMDD/` rebuttal/submission subtree, `0-sections/*.tex` | `/haipipe-task`, `/haipipe-probe` for new experiments | rebuttal + revision | round files | reviewer needs new evidence, approval |
| `present` | `5-present/{paper-slides,paper-poster}` | How does the paper cash out? | Build slides / poster | final paper, pitch, displays | slides, poster | none | slides/poster | n/a | talk cannot explain in one minute -> pitch |

## Evidence Loop (back to probe)

The lifecycle loops out to probe whenever the problem is EVIDENCE, not wording.
The contract is `delivery-need.md` (paper-owned; no cross-skill shared file).

```text
1-claims GAP  ──out──▶  /haipipe-probe plan from-need <need>
                          probe: Plan → Gather → Read → Judge → Return
1-claims slot ◀─backfill─  probe Return writes the verdict; the paper re-words,
                           the probe never edits paper prose
```

Outbound points: `1-claims` (claim needs a verdict), `4-display` (display
needs a run), and `review`/`respond` when an evidence gap surfaces. All route
through `delivery-need.md`. The inbound backfill updates the `1-claims` slot
(have | weak | GAP) citing the probe verdict. Ownership split: the paper owns the
NEED (loose), the probe owns the VERDICT (strict, in
`probe/.../ref/probe-yaml-schema.md`).

## File Principles

The paper folder is fixed. Stage contracts are markdown:

```text
STATUS.md
0-lifecycle/<stage>/<stage>.md + _LOG_<stage>.md   (4-display only: 4-display.tex + PDF)
0-sections/*.tex
0-displays/displayNN-<slug>/
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md
1-rounds/latest.md
.paper-console.yaml   (console session state, at paper/project root)
```

Each stage contract is markdown (`<stage>.md` + `_LOG_<stage>.md`); ONLY
`4-display` compiles (`4-display.tex` + PDF). A stage is done only when its
file resolves on disk with real content (see `paper-dashboard.md`).

## Command Routing

```text
/haipipe-paper                  -> Console (active paper) or venue dashboard
/haipipe-paper enter|status     -> Console
/haipipe-paper seed             -> 0-seed
/haipipe-paper claims           -> 1-claims
/haipipe-paper venue            -> venue (pin target journal in STATUS.md)
/haipipe-paper pitch            -> 2-pitch
/haipipe-paper narrative        -> 3-narrative
/haipipe-paper display|figures  -> 4-display (display contract + units)
/haipipe-paper figure1|framework -> 4-display framework mode (Figure 1 candidate rounds)
/haipipe-paper section-edit     -> 5-section-edit

# 4-display render verbs (data-driven vs concept), dispatched via haipipe-paper-lifecycle:
/haipipe-paper table            -> haipipe-paper-display-table        (data CSV -> LaTeX table)
/haipipe-paper figure           -> haipipe-paper-display-figure       (data CSV -> plot; SINGULAR = plots)
/haipipe-paper diagram          -> haipipe-paper-display-diagram      (concept -> deterministic vector SVG)
/haipipe-paper illustration     -> haipipe-paper-display-illustration (concept -> AI raster, DEFAULT Codex bridge)
/haipipe-paper illustration-gemini -> haipipe-paper-display-illustration-gemini (Gemini fallback)
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
0-seed         haipipe-paper-seed         (built)
1-claims       haipipe-paper-claims       (built)
5-section-edit haipipe-paper-section-edit (built; per-section DRAFT/PROBE/REVISE/CHECK)
round          haipipe-paper-round        (built; verbs enter/new/triage/apply/close)
```

Stage procedures own markdown contracts: `0-lifecycle/<stage>/<stage>.md` +
`_LOG_<stage>.md`. Only `4-display` owns a `.tex` + PDF.
