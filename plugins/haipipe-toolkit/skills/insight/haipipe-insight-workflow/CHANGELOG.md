# haipipe-insight-workflow · version history


## 2.3.0 · 2026-10-01 · Evidence needs in the gates (JL 261001)

- GI1 requires evidence needs with kinds legal at the rung; GI2, GI3 and GI4 require `haipipe-insight-check` to find every need bound, fit, cited and current (GI4: no compute need reasoned away); GI6 settles only without an overclaim. Contract: `haipipe-insight/ref/evidence-needs.md`.

## 2.2.0 · 2026-10-01 · Partition names, not letters (JL 261001)

- Partition-name grammar: `9-cross/`, `<L><NN>-<partition>-<slug>/` page folders, `QG-<partition>-<L>`, `🚫 full-only`; run-workflow and handoff examples use placeholder partitions.

## 2.1.0 · 2026-10-01 · Page tickets; the answering page is the report (JL 261001)

- No `RESULT_STORE=insights/<board>/_results` dispatch and no `reports/`: the runtime enumerates
  each answering page's `runs/` tickets (`RESULT_DIR` = the page's `results/<ticket>/`), the
  Report runs that write the page's `.md` from its own results, and Wisdom page Runs.
- GI2/GI3 read the page's own results; GI6 settles `✅ <page id>`; group mapping shows the
  partition folder as Job and the page as Task.
- `ref/run-workflow.md`: `support` runs a page's ticket; `report` writes/refreshes the answering
  page; worked example updated. `ref/partition-policy.md`: a new dataset is a new board whose
  pages call the same tasks.

## 2.0.0 · 2026-10-01 · Runs and reports answer questions (JL 261001)

- The runtime enumerates the DIKW Block's task runs (a config's `answers:` names the
  questions; dispatched with `RESULT_STORE=insights/<board>/_results`), the Report runs that
  write `reports/<partition>/<QID>.md`, and the Wisdom pages' writing/delivery Runs.
- GI0 names the board's one extract and the partition register's config stems; GI2/GI3 pass
  on a current `ok` run result (and a checked report); GI4 on a checked Knowledge report;
  GI6 settles `✅ report`.
- `ref/run-workflow.md`: `support.<target>` is the DIKW task run; new `report.<QID>.<partition>`
  Spec; `evidence/structure/write/deliver` scoped to Wisdom pages and legacy boards; new
  dependency graph and worked example.
- New computation is a task config authored through `haipipe-task`; legacy Page Evidence
  Items are read-only history.

## 1.3.4 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.
- Server `workbench-insight/insightboard.py`: the registration log resolves through `plan_dir` (`draft/records/`), not `<page>/outline`.

## 1.3.3 — 2026-09-28 · No content hashes (JL 260928)

- `ref/run-workflow.md`: `deliver.<page>.<target>` is the Page's fixed `run_delivery_<lane>`, current by file time (JL 260928).
- The handoff index, GI5/GI6 receipts, Runtime and control records name paths and versions only;
  no `sha256`, `definition_hash` or `result_hash`. The Insight viewer reports a handoff stale when the
  signed Page or a whole-file dependency is newer than the GI5 receipt (file time).

## 1.3.2 — 2026-09-20

- Require the pooling verdict to cite the predeclared shared threshold source
  and support `POOL`, `SPLIT`, or `UNDETERMINED` without forcing an incomplete
  comparison. Route `UNDETERMINED` to whole-extract-only counsel or a licensed
  partial-final W non-answer with Question-owned GI6 receipts.
- Migration: preserve existing Results, verdicts, and settled cells; use the
  new route on new or reopened partition-major work.

## 1.3.1 — 2026-09-20

- Align managed Writing and reused Evidence examples; specify canonical registration and exact GI5/GI6 handoff records. Permit governed static local input at GI2; update partition Task paths and move conditional policy to references.
- Migration: preserve existing records; see the scoped migration reference and current handoff contract.

1.3.0 · 260920
- Replace the six-label execution model with bounded Run Specs, dependencies,
  actual native inventory, frozen definitions, receipt indexing and completion.
- Distinguish registration-only completion from answering work; preserve
  human signature authority over exact signed payloads.
- Migration: `ref/migration.md`; no live Board rewrite.

1.2.3 · 260916
- Fix four bare `ref/partition.md` references to the umbrella's real path.

1.2.2 · 260915
- Replace phase authority language with Insight RunTypes and Workflow Runtime
  records while preserving legacy phase labels for compatibility.
- Make GI0-GI6 runtime control keys and keep Question Group as the derived
  `partition × DIKW target` view.

1.2.1 · 260913
- Require the task-side external-parent bridge to carry the exact `riNN`,
  base-R pointer, frozen dataset binding, version, Result hash, and RF id.

1.2.0 · 260913
- Define the derived Question Group frontier as `partition × DIKW target` while
  preserving the Queue CELL as the atomic transition.
- Nest every rung dispatch inside one Page v2 workflow pass; only Page
  CHECK/CLOSE followed by the matching GI assertion advances a cell. Page Run
  closure does not.
- Replace active Probe/PageX routing with SURVEY Decide, Supporting Run Results,
  frozen Local Input, typed local Results, and exact semantic parent-row lineage.
- Migration: OWE-ON-NEXT-TOUCH; historical PageX and Probe records stay readable.

1.1.0 · 260908
- Validate the selected Wisdom-targeted item execution and RF packet, not whole research-Page completion. Keep local I1/I5 signature, GI6, and X1 authority.

1.0.4 · 260831
- Add the pre-climbed external-parent bridge: a CHECK-current, Wisdom-targeted
  Task RF may supply the already-complete DIKW authority to local I5 only after
  I1 registration and exact PageX binding. Local counsel, signature, GI6, and
  X1 remain mandatory.

1.0.3 · 260831
- Move every phase and partial-final receipt to the granting Folder's canonical
  `outline/<stem>-log.md`; Page `## Log` is no longer an authority.

1.0.2 · 260831
- Strengthen GI2 to the I2 owner contract: accepted QA answer, path, and named
  run are all required.
- Map the Page owner RULING explicitly: none for I0-I4, GI5 receipt for I5;
  Probe read remains a nested workbench tick.

1.0.1 · 260831
- Clarify that the two named gates are Insight cross-phase authority transfers;
  Page-local copilot ticks remain nested authoring controls.
- Make GI5 the outward-export boundary and GI6 the mandatory I1 settlement
  before a cell stops; align the Wisdom phase with that ordering.

1.0.0 · 260831
- I0-I5 are now phase-owned Folder kinds. Dispatch loads the matching phase
  contract and the workflow owns only their order, GI0-GI6, cell frontier and
  receipts; Application crossing reports that frontier unchanged.

0.5.0 · 260828 · the covariate row, and clause ① made mechanical
- The partition test's failure routing gains its SECOND named case. Time wore three guises and had three homes; a COVARIATE had none, so a session wanting a socioeconomic cut could either break clause ① or abandon a good idea. It now routes where `ref/partition.md` already said it belongs, to an I COLUMN, with the reason stated: a covariate cuts ACROSS audiences rather than partitioning them, so its rows are already counted in the groups it overlaps.
- Clause ① stops being prose. The file called all three admission clauses "each mechanically checkable" and none of the three was checked by anything until today. Two rules now exist in `haipipe-board`'s `check.py`: `partition-sum-over-100` (ERROR — disjoint subgroups of one extract cannot cover more than the extract, so percentages summing past 100% is a breach on arithmetic alone) and `partition-cross-cutting` (WARN — a partition filtering on a column no sibling filters on shares no axis with them). A third, `partition-column-unregistered`, catches a filter column MT00 names nowhere outside its own register.
- Occasion: A00 registered `J · minorityzip` and `L · lowincome` on 260828, ran to 136.79% coverage across seven subgroup partitions, grew a page under one of them, and the board checker stayed green for the entire window. A human reader caught it. Both were retired the same day; these rules exist so the next one is caught by the machine.
- Migration: OWE-ON-NEXT-TOUCH for prose. The two checker rules are live immediately and are the deliberate exception — a board whose partitions overlap is producing wrong cross-group contrasts now, not on next touch.

0.1.0 · 260827 · JL
- New skill: the InsightBoard-level phase machine, requested as the insight lane's counterpart to haipipe-paper-workflow and haipipe-page-workflow having machines of their own.
- Six phases named by the lane's six page types (the application machine's naming law, which the lane can satisfy rung by rung): I0 Meta (scope), I1 Question (ask), I2 Data (observe), I3 Information (derive), I4 Knowledge (claim), I5 Wisdom (hand off). One-digit I<n> is a phase, two-digit (+letter) is a page — the digit-count rule that already separates P0 from P01.
- Two positions failed the naming-law test and became gates, not phases: the pooling verdict (rides on an ordinary K page in X → GI4's partition-major clause) and settle (a register act → GI6).
- The frontier's atomic unit is the register CELL (question × partition). Phases climb rows, partitions widen columns, only X lets columns meet.
- The partition axis conceptualized as three moments each owned by a phase: noticed (I3/I4), asked (I1), born (I0, and nowhere else). Late arrival has four mechanical consequences: cells born ⬜ never inheriting a sibling's refusal (A00's sixth defect-class instance, 260827), X reopens, a reopened verdict re-conditions every W, all other partitions' D/I/K untouched.
- Gates GI0-GI6, each an assertion over named files; the two human gates (probe release inside any rung page's RUN, handoff signing at GI5) never have an auto mode; every dispatch pins mode: copilot.
- The partition-major climb order (F first, mirrors in parallel, X, every W last) moved here from haipipe-application-workflow 0.6.0, which keeps a pointer. Refinement mapping declared: 🔎P0 = I0+I1, P1 = I2-I4, P2 = I5.

0.1.0 addenda · 260827 · JL (same day, pre-release)
- Two principles the theory pass surfaced: each phase is one epistemic operation and each gate an authority transfer; refusal is convergence (🚫-with-reason ranks with ✅ as a terminal — the defect is the cell that can neither answer nor refuse).
- The second-axis section gains the ROUTING TEST at I1 (a question needing rows from one partition group is a column question; from two or more, an X question — mechanically checkable from what-would-answer), the X mini-ladder (XI contrast → XK heterogeneity → XK verdict, no D of its own, the two contract exceptions as its raw-material law), and the L0→L1→L2 escalation ladder (column → partition → child board, each promotion with its own trigger).
- The PARTITION TEST at I0: a partition is an AUDIENCE stratum (the unit the counsel is FOR), born only on three yeses — disjoint+stable over the window, exogenous to the design, addressable as its own DS page. Failures route: a design knob (send time, variant, channel) is the arm axis; a pattern is an I column; a new epoch is a new extract and hence a new board. Deep reason recorded: partition columns mirror the design lane's audience axis, because the pooling verdict splits COUNSEL and counsel is per-audience.
- Domain neutrality stated as law (🌐): the machine is content-free; domain enters only at the extract (MT00), the questions (registers), and the venue packs — substituting all three re-instantiates the machine. The counsel unit is whatever MT00 declares, so the partition test generalizes past humans-receiving-SMS.
- The INSTRUMENT SHADOW: the routing and partition tests have a mechanical echo in the task layer — column = same folder per partition config, partition = config never code, X = own folder reading siblings' outputs, new extract = same folders under a new source config. Convergent reasoning (code) is reused across groups and extracts; divergent reasoning (the page's reading) never is.

0.2.0 · 260827 · JL (the first fieldtest's law bin, run on A00 — see /field-test)
- GI5 made testable (F2/F3): the signature is now an ARTIFACT — for-wisdom 0.3.0 adds the handoff's `signed:` row (`⬜` until a person writes `✅ <initials> <YYMMDD>`, machine-write is an error); GI5 reads that row; a deferring W owes none.
- The routing test gains its third class (F4): F-ONLY questions — properties of the extract, identical in every partition — answered once on the template, refused `🚫 F-only` per column; 9 of A00's 39 rows had no seat in the old binary.
- The partition test amended (F5, F6): non-exhaustive is legal (a coverage gap reads by the template alone; an overlap never passes) and the template F is exempt by construction — it contains the partitions and seats on MT00 as the TEMPLATE row.
- `⬜ calc` named in dispatch (F7); zero-card PROBE ruled a legal quiet pass in the door 0.2.0 (F9); board.md ruled a DERIVED HEADER reconciled by the register pen in the door (F10); extension of a digested task run binds to new artifact paths with the reopen question left to the task layer (F8).
- GI6 gains the settled-partial exit: `🟡 <page> final` (for-question 0.4.0, which also unified the 🚫 grammar, F13). The 🧊 mark added for known-stale-but-frozen lines (F14).

0.3.0 · 260828 · JL (fieldtest round 2's law bin — 14 entries, 11 + 3 from execution)
- THE RETROACTIVITY LAW (F5/F6, the round's biggest): every contract bump ships a migration note; default owe-on-next-touch; a bump adding a HUMAN GATE blocks immediately; the bumping desk computes the blast radius by grep and lists it by id; the register never flips backward — "settled under 0.2.0, owing under 0.3.0" stays visible without rewriting history.
- Marks-and-receipts section (F12/F3/F4/F14): a token's spelling includes its spacing, canonical forward, live boards re-spelled only in authorized sweeps that re-pad tables; a mark annotates adjacent and is not an edit, so marking a fenced line is legal; 🧊 carries staling event AND clearing condition, and an over-ripe 🧊 is a finding; a 🟡-final flip leaves a second receipt on the ANSWERING page, because a citation invisible from the cited end cannot carry staleness.
- Derived-header extension referenced (F9/F13, ruled in for-question 0.4.1): all on-register restatements, status words by fixed mapping, authorization is per page.
- Door 0.3.0 in step: the four stale ✅/🚫-only settle spots gained 🟡 final (F1, the patch-split defect); quiet passes are DECLARED (F11); ⬜ annotations named as register-pen state (F10); the AUTO CHARTER section (standing per-run authorization: charterable vs never-charterable classes). for-wisdom 0.3.1 seats signed: as the block's last line and blesses record-on-stated-decision (F2).

0.4.0 · 260828 · JL (fieldtest round 3's law bin — 10 entries, first automated run)
- §Phase receipts reconciled with §Marks (Fr3, my own 0.3.0 split-rule defect, second instance): a 🟡-final settle leaves TWO receipts, stated in both places now.
- The page-side receipt's mechanical shape written into §Marks (Fr4): dated row, QUESTION id + "final", in ## Log — the shape the checker scans; and the quote duty universalized (Fr6): the register-side receipt quotes the licensing sentence whoever flips, person, lap or charter.
- §Contract bumps extended (Fr9 + the recurring split-rule class): blast radius includes sibling-law version pins; sibling citations are best unpinned; a patch landing a rule greps the family for every sentence stating the old one.
- Checker in step: partial-final scan restricted to ## Log (WARN kept deliberately, reason in code); new tooth mark-spacing-legacy (Fr5). Four rung contracts 0.x+1: the mint-time Queue allocation is the register pen's act (Fr7). 18 proof tests pass.
