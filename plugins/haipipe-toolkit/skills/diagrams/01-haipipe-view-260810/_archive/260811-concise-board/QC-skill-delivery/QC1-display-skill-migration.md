# From specimen to haipipe-view: detailed implementation and migration plan
state: 🟡 ACTIVE · View-owned Displays are becoming native renderer units; Paper/Application migration remains gated
owner: JL
method: extract only contracts proven by QBt1, keep existing renderers intact, and place a validation gate before each consumer migration

## Opening
How should the accepted View specimen become a reusable skill without breaking the existing Display renderers or the Paper work already in progress?
The View skill must own the semantic hub and its deterministic file operations.
The existing table, figure, diagram, and illustration skills should remain renderers that receive one selected Display brief.

Paper and application consumers should migrate only after a fresh agent can create, validate, build review projections, and stop at the human gate using the new View skill.

**Authority update**: JL authorized proceeding from the updated specimen into a detailed plan and first skill implementation.
This supersedes the earlier blanket hold, while human acceptance still controls whether the new route replaces existing Paper routes.

**Dirty-worktree boundary**: existing Paper Page Type files already carry unrelated work.
This implementation creates the View contracts and minimal Board resolver support first; it does not rewrite or retire those Paper files in the same round.

## Diagram

**The target ownership**: View owns organization and relationships; renderer skills own format craft; consumers own placement.

```text
TASK / QA-BANK
      │ answered Probes
      ▼
HAIPIPE-VIEW
├── <ViewPageStem>.md                  canonical Page
├── input/QA-probes + input/sources
├── inline Cards
├── output/<PageID>-Display1..n-<slug>     native renderer units
│   ├── output.md + README.md
│   ├── intake/ + recipe/
│   ├── candidates/ + assets/ + versions/
│   └── float.tex + preview.tex + preview.{png,pdf}
├── source code
├── validation
└── build contract ─────────────────────┐
                                        ▼
_fixture/
├── views/<ViewPageStem>/{<ViewPageStem>.tex,<ViewPageStem>.pdf,<ViewPageStem>.docx,manifest.json}
├── displays/<DisplayFolder>/{manifest.json,float.tex,assets/,preview.png,preview.pdf}
└── references.bib
      │
      ├── <PageID>-Display1 brief ─▶ table renderer
      ├── <PageID>-Display2 brief ─▶ figure / diagram / illustration renderer
      │
      └── accepted View/Display binding
                    ▼
             Paper · Appendix · Application
```

**The delivery gates**:

```text
G0 specimen clean
   ▼
G1 Page Type + View door validate
   ▼
G2 fresh agent creates and checks a realistic View
   ▼
G3 renderer adapter consumes one View Display
   ▼
G4 Paper/Application consumer migration
   ▼
G5 old public routes may be folded
```

## Content

### 1 · Responsibility map
**KEEP unchanged in the first implementation**:

```text
display/ref/display-unit-output-contract.md
display/skills/haipipe-display-table/
display/skills/haipipe-display-figure/
display/skills/haipipe-display-diagram/
display/skills/haipipe-display-illustration/
```

These units already own rendering craft and artifact-specific review.
They become producers selected by a View Display; they do not become the View semantic hub.

**ADD**:

```text
view/page-types/haipipe-page-for-view/
├── SKILL.md
├── agents/openai.yaml
└── assets/view-page-template.md

view/haipipe-view/
├── SKILL.md
├── agents/openai.yaml
├── scripts/view.py
└── assets/view-template/
    └── manifest.json
```

**MINIMAL BOARD INTEGRATION**:

```text
board/haipipe-board/cli/check.py
└── admit page-type: view
```

No new Card renderer is planned.
`haipipe-view` reuses the exact-span Card grammar from `haipipe-sentence` and the existing citation, value/Q-reference, and Display resolvers.

**CURRENT renderer integration**:

```text
display/ref/display-intake-contract.md                 View-owned Display uses it directly
display/ref/display-unit-output-contract.md            View output folder conforms directly
view/haipipe-view/scripts/view.py                         validates and distributes the unit
```

**DEFER until the renderer-complete specimen passes**:

```text
paper/page-types/haipipe-page-for-value/               consumer migration
paper/page-types/haipipe-page-for-literature/          consumer migration
paper/page-types/haipipe-page-for-display/             formal Display placement migration
application/.../haipipe-application-display/           application migration
task/7_display/haipipe-task-for-display/                task-side adapter
```

Nothing is retired merely because the new skill exists.

### 2 · haipipe-page-for-view contract
**Purpose**: extend the shared Page frame for one View Page.

Required Page head:

```text
page-type: view
view-unit: views/<ViewPageStem>
```

Required Content divisions:

```text
1  QA inputs
2  View body
3  Displays
4  Consumers
```

Required behavior:

```text
Opening      identity, purpose, reader
Diagram      QA inputs → body/Cards/Displays → consumers
Content 1    answered Probe bindings; plural collections
Content 2    topic-specific readable subsections with inline Cards
Content 3    one or several Displays and selected body/Card bindings
Content 4    zero or several consumers and placement/gate state
Aims/States  evidence freshness, Display acceptance, consumer handoff separately
Files        canonical Page, input/, source/, output/, manifest, review build
```

Close condition:

```text
mechanical bindings current
+ promised Displays inspectable
+ consumer relations explicit
+ person accepts the current View version
```

A machine may build and validate, but it may not write human acceptance.

### 3 · haipipe-view door and deterministic script
**Verbs**:

```text
create   scaffold the View Page's same-named stem from the asset template
check    validate required files, manifest, Card bindings, and output roster
build    generate TeX/PDF/Word review projections from the canonical Page
status   print inputs/body/Displays/consumers and independent gate states
```

**`scripts/view.py create`**:

1. Validate the View id and destination.
2. Create `<ViewPageStem>.md`, `manifest.json`, `input/QA-probes/`, `input/sources/`, `source/`, and `output/`; generated files belong only in `_fixture/`.
3. Never create mandatory fake outputs; the initial `output/` may be empty until the user names `<PageID>-Display1`.
4. Refuse to overwrite an existing View.

**`scripts/view.py check`**:

1. Parse `manifest.json`.
2. Verify the canonical Page, every declared Probe/source binding, every renderer-complete Display folder, and every consumer target.
3. Verify that Display ids are unique and use `<PageID>-Display<n>`.
4. Verify that the review build remains a projection and never becomes a second semantic source.
5. Report evidence freshness, Display acceptance, and consumer handoff separately.
6. Never mark a human gate accepted.

**`scripts/view.py build`**:

1. Extract `## Content` from the canonical Page.
2. Embed declared Display previews and resolve local citation labels.
3. Generate `.tex`, `.pdf`, and `.docx`, safe View/Display consumer manifests, a merged bibliography, and build receipts.
4. Hash the canonical Page and every declared resource.
5. Support `--check` for stale-build detection.

### 4 · Specimen-to-skill extraction sequence
**Extraction sequence**: implementation advances only after each preceding gate is inspectable.

```text
specimen check ─▶ skill contract ─▶ script tests ─▶ fresh-context test
```

#### Phase A · specimen gate

1. Rebuild the `QBt1-for-view` TeX/PDF/Word review projections.
2. Rebuild the Board.
3. Run Board check.
4. Run real-browser checks for QA input, Citation, Value, Probe, Display, and Consumer Cards.
5. Update Page States from those receipts.

#### Phase B · initialize skills

1. Initialize `haipipe-page-for-view` under `view/page-types/`.
2. Initialize `haipipe-view` under `view/`.
3. Generate `agents/openai.yaml` from the final View skill metadata.
4. Keep each SKILL.md concise; place scaffold files under assets and deterministic behavior in `scripts/view.py`.

#### Phase C · implement and validate

1. Write the Page Type contract from Content 2.
2. Implement the four View verbs from Content 3.
3. Add `view` to the Board checker’s admitted Page Type values.
4. Run `quick_validate.py` on both skills.
5. Run script tests in a temporary directory for create/check/build/check-current and overwrite refusal.

#### Phase D · fresh-context forward test

Dispatch a fresh agent with only the installed skill and this realistic request.

**Forward-test prompt**: the task must reveal whether the agent finds the unified structure and stops at the human gate.
```text
Create the View for Page QZ1-for-view from two answered Probe files,
write a readable body containing one checked value and one citation,
declare a table Display QZ1-Display1 and a Results-section consumer,
validate and build its review projections, and stop before human acceptance.
```

**Forward-test pass conditions**: every row must hold without access to this design conversation.
```text
skill triggers without this design conversation
correct unified folders are created
Cards remain annotations/bindings, not copied evidence files
QZ1-Display1 is declared without inventing values
private inputs do not ship
consumer remains blocked on human acceptance
all deterministic checks pass
```

If any condition fails, revise the skill and repeat with a fresh context.

#### Phase E · preview-first regression test

After the first browser review exposed metadata-only Display Cards, run a second fresh-context test that requires two rendered Displays. Each must carry and embed `preview.png`, expose `preview.pdf`, and remain blocked on human acceptance.

### 5 · Later renderer and consumer migration
**The migration path**: first adapt one renderer, then one consumer, and retire nothing until both pass.

```text
accepted View-owned Display ─▶ existing renderer ─▶ accepted artifact ─▶ pilot consumer
```

#### Native renderer unit, after G2

1. Make `View/output/<PageID>-Display<n>-<slug>/` conform directly to the generic Display intake/output contracts.
2. Keep `output.md` as the View-owned semantic brief and preserve View-body/Card bindings in the manifest.
3. Dispatch exactly one renderer based on Display kind into the same folder; do not create an adapter copy.
4. Publish only safe consumer metadata, float, winning assets, and previews into `_fixture/`.
5. Keep View and Display acceptance independently human-gated.

#### Paper/Application migration, after one real renderer adapter passes

1. Add View/Display binding to Section and Application consumers.
2. Teach consumer Cards to expose placement and current gate state.
3. Migrate one real Paper section as a pilot.
4. Compare the pilot against direct Value/Literature/Display routes.
5. Fold old routes only when no live consumer depends on them.

### 6 · Non-goals and stop rules
**Stop rules**: unresolved inputs, outputs, consumers, and human gates return control instead of broadening authority.

```text
missing binding · stale output · unresolved consumer · human gate
                              └──────── STOP ────────┘
```

The first skill does not recompute Task values, search literature, render figures itself, decide Paper narrative, or accept Displays.
It does not move existing Paper Page Types.
It stops when an input binding is missing, a declared output is stale, a consumer target is unresolved, or a human acceptance is required.

## Aims

### A1 · Responsibility map
- A1.1 · Assign one owner to View semantics, rendering craft, and consumer placement.
  **Done when:** no responsibility is duplicated between `haipipe-view`, renderer skills, and Paper/Application consumers.
- A1.2 · Protect existing dirty Paper work.
  **Done when:** the first implementation creates new View units and touches only the minimum Board checker line outside them.

### A2 · haipipe-page-for-view contract
- A2.1 · Implement `haipipe-page-for-view` from the unified specimen.
  **Done when:** the Page Type fixes QA inputs, body, Displays, and consumers without fixing topic-specific subsections.

### A3 · haipipe-view door and deterministic script
- A3.1 · Implement deterministic View create/check/build/status verbs.
  **Done when:** a temporary View can be scaffolded, validated, packaged, and checked current without copying private inputs.

### A4 · Specimen-to-skill extraction sequence
- A4.1 · Pass the specimen’s mechanical and browser gates.
  **Done when:** every promised Card kind opens and the package is current.
- A4.2 · Pass skill-creator validation and script tests.
  **Done when:** both skill folders pass `quick_validate.py` and the script’s success/failure paths are tested.
- A4.3 · Pass a fresh-context forward test.
  **Done when:** a new agent independently follows the intended workflow and stops at human acceptance.
- A4.4 · Pass a fresh-context preview-first regression test after revising the skill.
  **Done when:** a new agent creates two rendered Displays with PNG/PDF inspection surfaces, embeds both PNGs, packages them, and stops before acceptance.

### A5 · Later renderer and consumer migration
- A5.1 · Make View Displays native generic renderer units.
  **Done when:** QBt1 D1 and D2 pass the unit contract, rebuild their own assets/previews, and distribute safe consumer manifests with preserved bindings.
- A5.2 · Pilot one real downstream consumer before folding old routes.
  **Done when:** one Section/Application uses an accepted View output and no old route is retired prematurely.

### A6 · Non-goals and stop rules
- A6.1 · Keep the first skill inside its declared boundary.
  **Done when:** it stops on missing bindings, stale output, unresolved consumers, and human gates without taking renderer or Paper authority.

## States

### A1 · Responsibility map
- ✅ A1.1 · Content 1 assigns View semantics, renderer craft, and consumer placement to separate owners.
- ✅ A1.2 · The plan explicitly defers edits to the already-dirty Paper Page Type family.

### A2 · haipipe-page-for-view contract
- ✅ A2.1 · `view/page-types/haipipe-page-for-view/` implements the four fixed Content divisions, flexible View-body subsections, three independent state dimensions, and the human close gate.

### A3 · haipipe-view door and deterministic script
- ✅ A3.1 · `view/haipipe-view/scripts/view.py` implements canonical create/check/build/status, complete Display/Consumer schema checks, atomic review replacement, stale-review detection, overwrite refusal, and valid TeX/PDF/DOCX generation.

### A4 · Specimen-to-skill extraction sequence
- ✅ A4.1 · The review build is current, all 8 Board Pages are clean, and the adapter-free browser suite passes 45 of 45 including C1-to-S-Main-4 navigation.
- ✅ A4.2 · Both skill folders pass skill-creator validation; the script passes create, check, status, build, build-current, overwrite-refusal, and stale-output tests.
- 🧠 A4.3 · Earlier QY3/QV9 fresh runs passed the pre-native-unit workflow. The current revision passes local multi-View regressions, but a new independent Agent run remains required; the internal thread endpoint did not respond and the external Claude API run was denied because repository data export was not explicitly authorized.
- ✅ A4.4 · Fresh QY3 also proved a Card can carry one evidence Binding plus several real Files paths without false binding failures; TeX/PDF/DOCX remained current and every human gate stayed waiting.

### A5 · Later renderer and consumer migration
- ✅ A5.1 · QBt1 D1 and D2 directly satisfy the generic intake/output contracts, rebuild their winning assets and previews, and distribute safe manifests with preserved EC1–EC4 bindings.
- ❄️ A5.2 · Consumer migration remains held until an accepted View output is compiled through one real Paper/Application pilot.

### A6 · Non-goals and stop rules
- ✅ A6.1 · Content 6 fixes the stop conditions and excludes renderer, Task, Paper, and human-acceptance authority.

## Files

- `../QBt-page-types/QBt1-for-view.md`
  The unified specimen from which the skill contract is extracted.
- `../QA-view-model/QA1-view-boundary.md`
  The fixed relation grammar.
- `../QA-view-model/QA2-evidence-card-contract.md`
  The Card source, binding, and interface contract.
- `../../display/ref/display-unit-output-contract.md`
  Existing renderer artifact contract to keep.
- `../../display/ref/display-intake-contract.md`
  Caller-owned provenance contract used directly by each View Display unit.
- `../../view/page-types/haipipe-page-for-view/SKILL.md`
  The shipping View Page Type contract extracted from QBt1.
- `../../view/haipipe-view/SKILL.md`
  The shipping View door and workflow.
- `../../view/haipipe-view/scripts/view.py`
  The deterministic create/check/build/status implementation.
- `../../view/haipipe-view/scripts/test_view.py`
  Regression coverage for native Display scaffolding, shared fixture ownership, safe distribution, cleanup isolation, and BibTeX collision refusal.
- `../../board/haipipe-board/cli/check.py`
  The minimal Board integration point admitting `page-type: view`.
- `../_runs/skill-forward/QV7/report.md`
  The durable fresh-context forward-test receipt and parent-side verification.
- `../_runs/skill-forward/QV9/report.md`
  The no-intervention preview-first regression receipt and parent-side verification.
- `../_runs/skill-forward/QZ1/report.md`
  The fresh owner-index naming regression and parent-side verification.
- `../_runs/skill-forward/QY3/report.md`
  The final canonical-Page, complete-schema, review-build, and Card-parser regression.

## Log

- 260810 2036 · [CHECK-CC] Native-unit Board rebuild passes 8 pages with 0 error, 0 warning, and 0 gap; the real-browser Card suite passes 45/45 after restoring View-owned takeaway and EC-binding text in Display Cards.
- 260810 2034 · [CHECK-CC] Both revised skills pass quick validation; `test_view.py` passes 3/3 including two Views sharing one fixture and conflicting BibTeX refusal.
- 260810 2034 · [BUILD-CC] QBt1 D1/D2 now directly satisfy the generic renderer unit contract and publish source-free View/Display consumer manifests with explicit handoff blockers.
- 260810 2034 · [BLOCKED-CC] A fresh independent run could not be completed: the internal Agent endpoint was unavailable, and the escalated Claude API run was rejected because explicit permission to export repository skill content was absent. Mechanical completion is not being misreported as fresh-agent acceptance.
- 260810 · [CHECK-SONNET] QY3 is the final clean-context regression: canonical Page only, complete schema, one rendered Display, one local Consumer, valid review formats, Binding plus Files Card, and all human gates waiting.
- 260810 · [LESSON-SONNET] QY1 exposed missing kind/reader-job/placement enforcement; QY2 exposed an over-broad Card path parser; both contracts were corrected before QY3 passed.
- 260810 · [CHECK-SONNET] Fresh owner-index regression created QZ1-for-view with QZ1-Display1, a real consumer target, rendered PNG/PDF surfaces, a current six-file public package, and all human gates waiting.
- 260810 · [CHECK-CC] Parent re-ran QZ1 check, status, and build-current; both skill folders also pass skill-creator quick validation.
- 260810 · [CHECK-CC] Added the first live Consumer-Page route inside the specimen: C1 opens S-Main-4, while production Paper/Application migration remains separately gated.
- 260810 · [CORRECTION-JL] The first skill version allowed Display metadata to pass while its inspection artifact remained below the Card fold; rendered visual/table Displays now require and embed PNG/PDF previews.
- 260810 · [CHECK-CC] Expanded QBt1 browser acceptance passes 43 of 43 and confirms both inline PNGs plus preview-first display01/display02 Cards; fresh-context skill regression remains in progress.
- 260810 · [LESSON-CC] Euler eventually passed QV8 only after an explicit SVG conversion hint; this exposed a skill gap, so the exact local `rsvg-convert` PNG/PDF fallback was added before the final fresh run.
- 260810 · [CHECK-BERNOULLI] No-intervention QV9 passed with 2 Probes, 2 rendered Displays, 1 consumer, 10 packaged files, private inputs excluded, both previews embedded, and all human gates waiting.
- 260810 · [CHECK-CC] Parent re-ran QV9 check/status/build-current, byte-compared both Probe snapshots, and visually inspected both generated PNGs; all passed without invented interpretation.
- 260810 · [RULING-JL] Authorized updating the specimen, writing a detailed specimen-to-skill plan, and beginning the View skill implementation.
- 260810 · [REVISE-CC] Replaced the earlier broad migration sketch with file-level ownership, four deterministic verbs, explicit gates, a fresh-agent task, and stop rules.
- 260810 · [BOUNDARY-CC] Existing dirty Paper Page Type files are excluded from the first implementation; their migration remains a later gated phase.
- 260810 · [BUILD-CC] Added `haipipe-page-for-view`, `haipipe-view`, their OpenAI metadata, templates, and the deterministic View script; added only the View key and roster entries to the shared Board/Page contracts.
- 260810 · [CHECK-AMPERE] Fresh-context QV7 forward test passed: 2 Probes, 1 Display, 1 consumer, private inputs excluded, package current, human acceptance still waiting.
- 260810 · [CHECK-CC] Parent re-ran View check, status, package-current check, byte-compared both copied Probes, and enumerated a three-file public package containing only view.md, D1 output, and generated manifest.
