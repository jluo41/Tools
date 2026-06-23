# Paper Lifecycle Map

The Paper Lifecycle Map connects each lifecycle stage to its skill procedure,
question, action, file ownership, external calls, human output, machine state,
and stop gate. The lifecycle is the stage spine from `paper-lifecycle.md`, not a
separate set of verbs.

## Map

| Step | Skill Procedure | Question | Action | Reads | Writes | External Calls | Human Output | Machine State | Stop / Gate |
|---|---|---|---|---|---|---|---|---|---|
| `enter` (console) | `haipipe-paper-enter` | Which paper is active, what layer, what open needs? | Resolve root, derive-from-disk dashboard, route input | STATUS.md, 0-lifecycle, 1-rounds, 0-displays, 0-sections, git | `.paper-console.yaml`, STATUS.md | none | dashboard panel | `.paper-console.yaml` | no paper root, ambiguous paper |
| `0-seed` | `haipipe-paper-seed` | Why might this paper exist? | State possibility, evidence, kill criteria | seed notes, project evidence | `0-lifecycle/0-seed/0-seed.tex`, STATUS.md | none | seed contract | `0-seed.tex` | not viable -> drop |
| `1-pitch` | `haipipe-paper-pitch` | What is the paper selling? | Maintain one-minute story + provenance | seed, review, decisions, `_venue/playbook-<venue>` (framing) | `0-lifecycle/1-pitch/1-pitch.tex`, STATUS.md | none | pitch | `1-pitch.tex` | abstract/intro sells another story |
| `venue` | `haipipe-paper-venue` | Which venue fits, and pin it | Recommend best-fit venue, pin STATUS venue | seed, pitch, topic, `_venue/playbook-*` packs | `STATUS.md` `venue:` | none | venue shortlist + recommendation | `STATUS.md` `venue:` | no clear fit; venue change re-runs `2-claims` |
| `2-claims` | `haipipe-paper-claims` | Which claims are supported, weak, or GAP? | Maintain claim ledger, mark needs | pitch, evidence refs, probe verdicts, `_venue/playbook-<venue>` (rewards + references/) | `0-lifecycle/2-claims/2-claims.tex`, STATUS.md | `/haipipe-probe`, `/haipipe-discover`, `/haipipe-task`, `/haipipe-insight` | claim ledger | `2-claims.tex` | claim unsupported/too strong, no route |
| `3-narrative` | `haipipe-paper-narrative` | How do claims become a manuscript arc? | Build evidence-backed arc | 2-claims, results | `0-lifecycle/3-narrative/3-narrative.tex`, STATUS.md | none | narrative | `3-narrative.tex` | arc weak -> 1-pitch / 2-claims |
| `4-display` | `haipipe-paper-display` (+ render skills: -display-table, -display-figure, -display-diagram, -display-illustration[-gemini]; figure-logic ref) | What figure/table carries each claim? | Plan display map + units | 2-claims, results, probe verdicts, `_venue/playbook-<venue>` (-> Display) | `0-lifecycle/4-display/4-display.tex`, `0-displays/README.md`, `0-displays/displayNN-<slug>/*`, STATUS.md | `/haipipe-task-for-display` | display map + units | `4-display.tex`, display units | display cannot support claim |
| `5-minimap` | `haipipe-paper-minimap` (folds in architecture-blueprint + plan-outline refs) | What job does each paragraph do, and what anchors it? | Map paragraph jobs + evidence anchors | narrative, display map, `_venue/playbook-<venue>` (-> Minimap) | `0-lifecycle/5-minimap/5-minimap.tex`, STATUS.md | none | minimap | `5-minimap.tex` | paragraph has no job / anchor |
| `write/edit` | `haipipe-paper-build-*`, `haipipe-paper-edit*` (write drafts, weaving polishes), `sections/*` | Realize the spine as TeX prose | Scaffold, write, polish | 5-minimap, display units, `_venue/playbook-<venue>` | `0-sections/*.tex`, `0-displays/*/float.tex`, `0-*.bib`, PDF | compile / overleaf | draft PDF | section files | writing exposes missing evidence -> 2-claims |
| `review` | `haipipe-paper-edit-{claim-audit,reviewer,proof-checker,submission-audit}`, citation components | Which layer is broken, or ready? | Adversarial audits, route verdict | PDF, lifecycle files, sections | review notes, `1-rounds/<round>/todo.md`, STATUS.md | reviewer agents / Codex | review verdict + routing | STATUS.md maturity | overclaim, broken layer, venue check fails |
| `round` | `haipipe-paper-round` (enter/new/triage/apply/close) | Where does this round's discussion/decision/todo/applied go? | Open / triage / apply / close round | discussion, review, decisions | `1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md`, `1-rounds/latest.md` | route each todo to a stage or evidence worker | round log | round files | unresolved item with no target |
| `respond` | `haipipe-paper-rebuttal`, `5-respond/*` | How do reviews become revision + rebuttal? | Parse reviews, plan, draft, revise | reviews, submitted manuscript | `1-rounds/vYYMMDD/` rebuttal/submission subtree, `0-sections/*.tex` | `/haipipe-task`, `/haipipe-probe` for new experiments | rebuttal + revision | round files | reviewer needs new evidence, approval |
| `present` | `6-present/{paper-slides,paper-poster}` | How does the paper cash out? | Build slides / poster | final paper, pitch, displays | slides, poster | none | slides/poster | n/a | talk cannot explain in one minute -> pitch |

## Evidence Loop (back to probe)

The lifecycle loops out to probe whenever the problem is EVIDENCE, not wording.
The contract is `delivery-need.md` (paper-owned; no cross-skill shared file).

```text
2-claims GAP  ──out──▶  /haipipe-probe plan from-need <need>
                          probe: Plan → Gather → Read → Judge → Return
2-claims slot ◀─backfill─  probe Return writes the verdict; the paper re-words,
                           the probe never edits paper prose
```

Outbound points: `2-claims` (claim needs a verdict), `4-display` (display
needs a run), and `review`/`respond` when an evidence gap surfaces. All route
through `delivery-need.md`. The inbound backfill updates the `2-claims` slot
(have | weak | GAP) citing the probe verdict. Ownership split: the paper owns the
NEED (loose), the probe owns the VERDICT (strict, in
`probe/.../ref/probe-yaml-schema.md`).

## File Principles

The paper folder is fixed and TeX-first:

```text
STATUS.md
0-lifecycle/<stage>/<stage>.tex
0-sections/*.tex
0-displays/displayNN-<slug>/
1-rounds/vYYMMDD/{README,discussion,decisions,todo,applied}.md
1-rounds/latest.md
.paper-console.yaml   (console session state, at paper/project root)
```

Each `0-lifecycle/<stage>/<stage>.tex` is a stage contract and should compile
standalone. A stage is done only when its file resolves on disk with real
content (see `paper-dashboard.md`).

## Command Routing

```text
/haipipe-paper                  -> Console (active paper) or venue dashboard
/haipipe-paper enter|status     -> Console
/haipipe-paper seed             -> 0-seed
/haipipe-paper pitch            -> 1-pitch
/haipipe-paper claims           -> 2-claims
/haipipe-paper narrative        -> 3-narrative
/haipipe-paper display|figures  -> 4-display (display contract + units)
/haipipe-paper figure1|framework -> 4-display framework mode (Figure 1 candidate rounds)
/haipipe-paper minimap          -> 5-minimap

# 4-display render verbs (data-driven vs concept), dispatched via haipipe-paper-lifecycle:
/haipipe-paper table            -> haipipe-paper-display-table        (data CSV -> LaTeX table)
/haipipe-paper figure           -> haipipe-paper-display-figure       (data CSV -> plot; SINGULAR = plots)
/haipipe-paper diagram          -> haipipe-paper-display-diagram      (concept -> deterministic vector SVG)
/haipipe-paper illustration     -> haipipe-paper-display-illustration (concept -> AI raster, DEFAULT Codex bridge)
/haipipe-paper illustration-gemini -> haipipe-paper-display-illustration-gemini (Gemini fallback)
/haipipe-paper write|edit       -> write/edit
/haipipe-paper review           -> review
/haipipe-paper round            -> round
/haipipe-paper rebuttal|respond -> respond
/haipipe-paper slides|poster    -> present
/haipipe-paper <venue>          -> apply venue profile (conference/journal/is)
/haipipe-paper create|revise    -> composite route over the lifecycle
/haipipe-paper "<free text>"    -> active Console router, else plan at the frontier
```

## Procedure Status

Every stage now has a dedicated procedure:

```text
0-seed    haipipe-paper-seed      (built)
2-claims  haipipe-paper-claims    (built)
5-minimap haipipe-paper-minimap   (built; wraps -architecture + -plan)
round     haipipe-paper-round               (built; verbs enter/new/triage/apply/close)
```

All stage procedures are TeX-first: each owns `0-lifecycle/<stage>/<stage>.tex`.
