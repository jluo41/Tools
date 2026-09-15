## 0.32.0 · 2026-09-15

- Add the human-first `Scratch` lane under Page Writing.
- Present `rp-scratch-NN_<target>` Runs and their Summary-based close state in
  the same read-only Run Space presenter.

## 0.30.0 · 2026-09-15

- Present Run Workflow Runtime, Run Spec, Gate, and Route state as read-only
  Run Space projections without minting Runs for internal Steps or decisions.

## 0.29.0 · 2026-09-14

- Present SHAPE and SURVEY as cycles of one shared Structure card and expose
  participants/contributors in its collapsed collaboration details.

## 0.28.0 · 2026-09-14

- Redesign Run Space as minimal result-first cards: Page Writing is grouped
  into Structure/Section/Paragraph, Page Evidence into Value/Display/Citation,
  and Supporting Runs into Task/Discovery columns with Task-level grouping.
- Keep review inside the Paragraph Run, keep metadata and technical paths
  collapsed, and show actual Result content first when a card opens.
- Present typed RP and RE identities, including the generic `DISPLAY` kind;
  keep inline Evidence Labels as zero-to-many bindings on a Result/Card rather
  than child Runs.

## 0.26.0 · 2026-09-13

- Move the presenter from a top-level Runs plugin into Outline's Run Workspace.
- Replace Page Runs / Task Runs with Run P / Run E / Supporting Runs and keep
  external Results inspectable by reference without copying them.

## 0.25.0 · 2026-09-13

- Separate the Labeling native family from physical origin: a page-local
  `rlNN` row shows its operation as Kind and `Local` as Where.

## 0.24.0 · 2026-09-13

- Present direct `labeling/runs/` + `labeling/results/` envelopes as ordinary
  Task Runs with their native `rlNN` identity and Labeling origin.

## 0.23.0 · 2026-09-12

- Suppress Track Changes cards whose Before/After is missing or unchanged.
- Use the card heading as the one classification record and keep non-wording
  Steps in Changes; only the current Step is expanded by default.

## 0.22.0 · 2026-09-12

- Render saved Before/After text as granular inline Track Changes with red
  deletion, green insertion, and plain surviving context.
- Show feedback classification, rationale, inferred preference, and its
  provisional status in the read-only Page Run detail.

## 0.21.0 · 2026-09-12

- Delete the legacy Page Run label and resolver fallback.
- Show noncanonical interactive-writing identities as Held contract errors and
  never let them unlock paragraph Runs.

## 0.20.0 · 2026-09-12

- Add `run=<exact-run-id>` deep links that render the requested Page or Task
  Run expanded at load while preserving the reader-first history view.

## 0.19.0 · 2026-09-12

- Present the reserved structure Run as `rp00 · Mermaid Structure` and begin
  paragraph Run labels at `rp01`.
- Read the former `rp01_mermaid-structure` identity as legacy input without
  allocating it on new Pages.

## 0.18.0 · 2026-09-12

- Keep all normal `rNN` work in the Task Run lane and label its physical origin
  as Local, Task Job, or Linked instead of inventing a third lane.
- Preserve the exact `rNN` identity for standalone Page-local Runs rather than
  applying the Paper-only `P` prefix.
- Put a truthful “What happened” digest in the overview, preferring a declared
  outcome and otherwise deriving the bounded Page setup report or current
  state plus target.
- Translate a setup receipt's mode into an action so create and resume runs do
  not collapse into identical-looking coverage rows.
- Omit empty Evidence boilerplate from ordinary Task Run detail.
- Put a nonempty Task lane before an empty Page lane so standalone setup work is
  visible without scrolling past an empty state.

## 0.17.0 · 2026-09-12

- Replace raw Page Run ticket, working-state, and Version-journal dumps with a
  reader-first Goal/Scope/Status summary plus rendered latest feedback, saved
  result, and Next action.
- Keep earlier Steps and repository paths available in collapsed History and
  Technical details regions instead of occupying the default reading path.
- Stack the five-column Runs overview into readable cards on narrow screens;
  remove zero-count status noise and replace the long preface with one action
  hint.
- Reuse the shared deterministic Mermaid renderer in `rp01` detail, and scope
  mobile overview selectors so nested saved-result tables retain their headers.
- Project the same Mermaid source as a large-text relationship sequence on
  phones, add a visible row expander, remove the repeated mobile detail title,
  and translate the structure Run's Scope into reader-facing language.
- Wrap code blocks and long content inside collapsed historical Steps so opening
  old feedback cannot widen or clip the phone viewport.

## 0.16.0 · 2026-09-12

- Present only the current `rpNN` Run-of-Page namespace and remove the old
  interactive-name compatibility branch from the live classifier.
- Keep Page and Task counters independent and require a closed
  `rp01_mermaid-structure` before paragraph Runs.

## 0.15.0 · 2026-09-12

- Present the mandatory first Page Run as `pr01 · Mermaid Structure`.
- Present numbered paragraph Runs as `pr02 · P01`, `pr03 · P02-P03`, and so on.
- Treat numbered `prNN` Runs before a closed `pr01_mermaid-structure` as Held;
  retain old `rpNN` records as readable history.

## 0.14.0 · 2026-09-12

- Present the mandatory first Page Run as `rp01 · Outline`.
- Present paragraph Page Runs with concise labels such as `rp02 · P01` and
  `rp03 · P02-P03`, while retaining the full canonical identity in detail.
- Treat paragraph Runs before a closed `rp01_outline` as Held.

## 0.13.0 · 2026-09-12

- Present new interactive Page Runs with a separate Page-local `rpNN` identity
  sequence while preserving owner-native `rNN` and global identities for Task
  Runs, including Discovery.
- Move delegated, output-only Paragraph Writing to the Task Run lane; reserve
  Page Run for interactive writing with human-feedback Versions and Steps.
- Keep historical interactive `rNN_page-writing_*` records readable without
  minting new Page Runs in the old namespace.

## 0.12.0 · 2026-09-12

- Split the Page-facing projection into Page Runs for interactive writing and
  output-only Task Runs for delegated work, including Discovery.
- Read each writing Version from one `vNNN.md` journal and project `Waiting`
  only when its current Step contains both Human feedback and Saved result.
- Keep allocated but unresolved Task identities visible as `Held`.
- Hold stale complete Task records whose Result is absent, and surface orphan
  Results, duplicate identities, and Page Run receipt mismatches as audit findings.

## 0.11.0 · 2026-09-11

- Document one-row interactive Run history and truthful waiting semantics. Explicitly distinguish the new skill protocol from the existing renderer, which has no Version/Step browser yet.

## 0.10.0 · 2026-09-08

- Present Paragraph Writing targets and inline, escaped Markdown instructions, paragraph and trace beneath the compact Run row.
- Keep missing writing outputs Held and preserve existing evidence navigation and Folder/Job result ownership.

# Changelog · haipipe-plugin-runs

## 0.9.7 — 2026-09-04

- Resolve canonical Task Tickets from `<task>/runs/` against Job-owned
  `<job>/results/<task>/<run>/` without copying Results into the Task Folder.
- Derive a missing Task receipt id from the Block/Job/Task path plus local rNN,
  and show the full b/j/t/r identity instead of a Paper `P` route.

## 0.9.6 — 2026-09-04

- Distinguish the cross-Folder neutral classification schema from the current
  Board Page adapter, which truthfully presents Page-local pairs only; external
  Supporting Runs remain in Outline and open at their owning Folder.

## 0.9.5 — 2026-09-04

- Clarify that Runs is an optional presenter beneath the Task Face and treat
  PageX only as historical migration input.

## 0.9.4 — 2026-09-03

- Distinguish Outline's evidence-grouped source/Run inventory from this
  top-level presenter of physically allocated page-local Runs.

## 0.9.3 — 2026-09-03

- Clarify that Outline evidence-side Run details show Purpose/Plan,
  Availability, and Next action as separate facts while raw paths remain
  non-downloading text.

## 0.9.1 — 2026-09-03

- Keep Runs visible on source-backed Board Pages even when no local Run is
  allocated, using one truthful empty state without creating empty folders.

## 0.9.0 — 2026-09-03

- Point evidence lineage to the Outline plugin's Evidence Workspace and name
  its generated folder `outline/evidence/supporting-runs/`.
- Keep Runs limited to physical page-local `runs/` and `results/` pairs.

## 0.8.4 — 2026-09-03

- Use Run/Result as the only reader-facing object names and show their exact,
  wrapping repository-relative paths.
- Route Outline lineage to the unified Evidence Items panel; keep Runs limited
  to real page-local Run–Result pairs.

## 0.8.3 — 2026-09-02

- Clarify navigation ownership: Outline Run tokens open Evidence → Run links;
  only physical page-local Ticket–Result pairs belong in this Runs overview.

## 0.8.1 — 2026-09-02
- Evidence Item detail rows show PageX source count and accepted authorities
  beside Supporting Runs and the local Run. PageX remains a source binding,
  never an extra Run or Result row.

## 0.8.0 — 2026-09-01
- Add `Page · Evidence Item` to the Page group. Its compact row shows typed
  item target, support count, local Run, status, and ready Result; detailed
  Supporting Runs and frozen input remain behind the row.

## 0.7.0 — 2026-09-01
- Present each independently closable Labeling operation as one Run row and
  group by P0-P5 episode without adding Round/Test/Scan/Audit umbrella rows.
- Resolve Labeling Tickets and safe Result envelopes from root `runs/` and
  `results/`, while canonical protected artifacts stay in their domain paths.

## 0.6.0 — 2026-09-01
- Add Labeling as a fourth Run family with Calibration Round, Qualification
  Test, Production Scan, and Final Audit operations.
- Resolve Labeling through its authority-owned domain folders and keep the Runs
  view read-only, protected-data-safe, and control-free.

## 0.5.1 — 2026-09-01
- Load the neutral `haipipe-run` contract before presenting Run identities,
  paired Results, receipts, and normalized statuses.

## 0.5.0 — 2026-09-01
- Replace the independent Runs, Results, Notebook, and Scripts segments with
  two regions: one compact Run overview and one collapsible Scripts tree.
- Group complete Run identities as Execution, Discovery, or Page; Page shows
  Division Writing and Display. Keep Ticket and Result together in one row and
  expose commands, receipts, logs, outputs, and script links only on click.
- Fix the overview to five statuses (`Ready`, `Running`, `Done`, `Failed`,
  `Held`) derived from the owning Run contract. Make Scripts freestyle: no
  manifest, internal grammar, one-to-one binding, or unbound-file finding.

## 0.4.0 — 2026-09-01
- Rename the presenter from Execution to Runs. Execute remains a workflow
  action; the plugin presents a plural collection of durable Run identities.
- Add the two physical dialects behind one logical pair: Folder-local
  `runs/<run>.sh <-> results/<run>/` and Job-backed Task
  `<task>/runs/<run>.sh <-> <job>/results/<task>/<run>/`.
- Treat config, scripts, and runtime notebooks as conditional projections;
  never copy job-owned Results into a Task Page to fake Folder-local storage.

## 0.3.0 — 2026-09-01
- Rename the presenter from Code to Execution. Its stable unit is the exact
  `runs/<RUNNAME>.sh <-> results/<RUNNAME>/` pair; `scripts/` and config are
  optional supporting material.
- Make no-code execution explicit: a Run may dispatch a skill, CLI, API, or
  external worker. Discovery Paper Runs are the first concrete case.
- Preserve the lifecycle boundary: Execution presents attempts and receipts;
  the owning workflow phase still decides run permission and Folder closure.

## 0.2.0 — 2026-08-31
- Under the former Code name, execution was treated as universal Task-Face
  behavior and the presenter was limited to Folders with code. Version 0.3.0
  supersedes that name and narrows the distinction correctly: the Task Face is
  universal, while materialized Run/Result execution remains optional.
- The presenter gained no lifecycle authority and exposed no run button.

## 0.1.0 — 2026-08-31
- Born contract-only as the presenter owed to scripts/ · runs/ · results/;
  segments fixed as Runs, Results, and Scripts.
## 0.12.0 — 2026-09-12

- Replace the peer family overview with two Page-facing lanes: Page Runs for
  interactive writing feedback history, and Task Runs for delegated Results,
  including Discovery while preserving each native family underneath.
- Implement read-only Version/Step history and the normal Waiting state for
  Page Runs. Hide Task Ticket, command, log, actor, and runtime internals at the
  Page boundary; show only target, Result/output, status, and Evidence use.
- Surface broken current-Step pointers and unresolved allocated Task identities
  as Held findings, sort newer same-status Runs first, and expose Page-owned
  supporting code only in a collapsed read-only Scripts inventory.
## 0.27.0 · 2026-09-14

- Present RP scope bands and distinguish Section-level Steps from later
  independently commissioned Section Runs.
