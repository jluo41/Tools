# Legacy Page-Type compatibility registry · phase owners included

This table keeps runtime `page-type:` keys resolvable while families migrate
to phase-owned `folder-kind:` contracts. Its fields still parameterize Page
phases. For a migrated key, `law:` points to the domain workflow phase that
owns the Folder kind and both faces; for an unmigrated key it points to the
remaining Page-Type contract.

```text
field       consumed by       what it answers
──────────────────────────────────────────────────────────────
outline     SHAPE             what shape may the plan take
evidence    SURVEY · LAND     what this kind of page owes exactly
                              (the item rows its survey must produce)
prose       WRITE             division vocabulary and budgets
closing     CHECK             when this kind of page may close
```

**One home per fact.** A key whose `standing:` is `contract` keeps its
`outline:` shape in the owning phase or compatibility contract's frontmatter
(the Page phases read the
file's first 20 lines; this registry carries only the mode and the pointer).
A key whose standing is `record-only` or `key-only` has no file, so its row
here IS the authority. `closing:` lines quoted from a contract are verbatim;
a line this registry authored is marked `(provisional)` until the owner
confirms it. Live page counts are never stored here: `cli/pagetypes.py`
prints them.

**The tooth** (`cli/pagetypes.py`): every engine key has a row here (drift
both ways is reported); a key with live pages whose standing is `key-only` is
a `registry-gap` — usage without law. Gaps print under `--check`;
`--strict-registry` exits 1 on them.

```yaml
# ── paper ──────────────────────────────────────────────────────────────
ideation:
  owner: paper            # standing: contract
  standing: contract
  token: SD
  mode: grammar
  evidence: "one source bullet per idea naming its IDEA_REPORT; novelty per claim from discovery QA"
  closing: "G0: novelty per claim + pilot + human PROCEED; the winning idea's went-to names the Seed"
  law: paper/workflow-phases/haipipe-paper-ideation
seed:
  owner: paper
  standing: contract
  token: SD
  mode: fixed
  evidence: "source pages bound via pagex; Establishment Board E-rows carry the novelty column"
  closing: "G4: ticked outline, novelty column filled, pitch sells only ✅ rows"
  law: paper/workflow-phases/haipipe-paper-seed
roadmap:
  owner: paper
  standing: contract
  token: SD
  mode: grammar
  evidence: "BLOCK rows each serve a Seed E-row with executor, done-when, budget; dispatch receipts land on lap divisions"
  closing: "G2+G3: every 🔨/⬜ E-row has a ▶️ row or waiver; done-when holds and the settle is written on the Seed"
  law: paper/workflow-phases/haipipe-paper-roadmap
narrative:
  owner: paper
  standing: contract
  token: NA
  mode: grammar
  evidence: "the venue bank page bound at §1; claims parented to Seed E-rows; map rows budgeted"
  closing: "G5: bank page bound, claims parented, map rows budgeted"
  law: paper/workflow-phases/haipipe-paper-narrative
section:
  owner: paper
  standing: contract
  token: "S<D> | SA"
  mode: resolved
  evidence: "a bibex key per claim; every number a PP<NN>.v<n> with its > Value: lane; a display unit per shown finding; a probe card per owed fact"
  closing: "per-unit CHECK ✅ against the resolved QBv division and the current Narrative row"
  law: paper/workflow-phases/haipipe-paper-section
round:
  owner: paper
  standing: contract
  token: RD
  mode: fixed
  evidence: "every intake feedback row served (Routed:) or declined with reason"
  closing: "G7, through CHECK: every concern ledgered and routed exactly once; a person approves the response receipt"
  law: paper/workflow-phases/haipipe-paper-round
venue:
  owner: paper
  standing: contract
  token: QBv
  mode: fixed
  evidence: "materials/ captures of the desk's own pages, CONTENT class only"
  closing: "V1-V4 derivable from the page for its desk (provisional)"
  law: paper/haipipe-paper-venue
# ── task ───────────────────────────────────────────────────────────────
task:
  owner: task
  standing: contract
  token: "folder-kind: task"
  mode: grammar
  evidence: "every shown number names the run that produced it; a rerun reopens the page"
  closing: "a person has read the result against the folder's own kind; a rerun reopens"
  law: task/page-types/haipipe-page-for-task
insight:
  owner: task
  standing: contract
  token: DIKW
  mode: fixed
  evidence: "QA files and Task Pages cited by path; the D → I → K → W trace"
  closing: "the trace is complete and Reusable Findings stand alone (provisional)"
  law: task/page-types/haipipe-page-for-insight
# ── board ──────────────────────────────────────────────────────────────
stage:
  owner: board
  standing: contract
  token: "S-<Family>-<unit>"
  mode: resolved
  evidence: "Required Inputs and Product declared on the live stage contract the page resolves"
  closing: "closes only when its human gate passes"
  law: board/page-types/haipipe-page-for-stage
# ── application ────────────────────────────────────────────────────────
brief:
  owner: application
  standing: contract
  mode: fixed
  evidence: "core PageX inputs named; insight needs raised as questions"
  closing: "the promise and Design roster stand alone for a Design page (provisional)"
  law: application/workflow-phases/haipipe-design-brief
data:
  owner: application
  standing: contract          # 0 live pages: dormant
  token: D
  mode: fixed
  evidence: "run-resolvable D rows"
  closing: "every D row names a resolvable run and a person has read the numbers against the origin's own question"
  law: application/workflow-phases/haipipe-insight-data
design:
  owner: application
  standing: contract
  mode: grammar
  evidence: "insight handoffs and venue-pack rails; units carry accepted: on their owning divisions"
  closing: "every unit accepted on its owning division (provisional)"
  law: application/workflow-phases/haipipe-design-division
information:
  owner: application
  standing: contract          # 0 live pages: dormant
  token: I
  mode: fixed
  evidence: "every I row derives from named D rows"
  closing: "every I row derives from named D rows and the nulls are visible"
  law: application/workflow-phases/haipipe-insight-information
knowledge:
  owner: application
  standing: contract          # 0 live pages: dormant
  token: K
  mode: fixed
  evidence: "propositions name their Information parents"
  closing: "the proposition names its Information parents, its strength, its uneliminated rivals and its boundary"
  law: application/workflow-phases/haipipe-insight-knowledge
meta:
  owner: application
  standing: contract
  token: MT
  mode: fixed
  evidence: "the source inventory with unit, grain, population, window, freshness"
  closing: "inventory and shared thresholds pinned (provisional)"
  law: application/workflow-phases/haipipe-insight-meta
question:
  owner: application
  standing: contract          # 0 live pages: dormant
  token: MT
  mode: grammar
  evidence: "each Queue cell names its answering page once one exists"
  closing: "every Queue cell terminal: ✅ answered or 🚫 closed-without-answer"
  law: application/workflow-phases/haipipe-insight-question
wisdom:
  owner: application
  standing: contract          # 0 live pages: dormant
  token: W
  mode: fixed
  evidence: "every counsel names a K parent; the forbidden clause is written"
  closing: "every counsel names a K parent, the forbidden clause is written, and the handoff reads standalone"
  law: application/workflow-phases/haipipe-insight-wisdom
# ── key-only: the engine accepts them, no contract and no record ───────
collection:
  owner: none
  standing: key-only          # live pages exist -> registry-gap until owned
labeling:
  owner: none
  standing: key-only          # live pages exist -> registry-gap until owned
view:
  owner: none
  standing: key-only          # live pages exist -> registry-gap until owned
dash:
  owner: none
  standing: key-only          # engine-accepted, unused
display:
  owner: none
  standing: key-only          # engine-accepted, unused
opening:
  owner: none
  standing: key-only          # engine-accepted, unused
slide:
  owner: none
  standing: key-only          # engine-accepted, unused
```
