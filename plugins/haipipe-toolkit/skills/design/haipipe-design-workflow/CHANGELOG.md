# haipipe-design-workflow · version history

0.4.0 current · 260920 (version unchanged at 0.4.0)
- Define Workflow first as a list of actual Runs. Commission/Generate/Verify
  are current Run types; route graphs describe relationships and Delivery is
  the read-only projection after independent Verify passes.
- Count C Commission + N Generate + J Verify records. Holds remain immutable
  when a later Commission releases the Item; at most one release is allowed.
- Distinguish blocked repairs from human holds, completed valid reviews from
  invalid review retries, and inherited config fields from mode/review_mode.
- Read current render evidence from Results, preserve supported historical
  Adopt ids, and align all venue instructions with the same completion boundary.

0.4.0 · 260918 (version unchanged at 0.4.0)
- Routing says what the code does: a draft that fails the records check goes
  back to Generate (the person queues a revise); a review that fails it,
  unresolved checks included, goes back to Verify (the person queues the
  review again); a fail verdict goes to a revise Generate; the agent side
  never routes to HOLD. HOLD is a person's decision at Commission or Adopt,
  and a held Commission or Adopt can be decided later.
- One Commission per Design Item; it pins its config and the item's evidence
  files, not the Brief version or venue packs; Generate and Verify copy the
  released config. Runs are counted per item; `rdNN` counts across the folder.
- A queued run whose pinned file changed is replaced ("Queue again", the old
  run `superseded` with its reason), never re-pinned in place.
- The Adopt preview is a copy of the exact draft, one per draft, for all four
  decisions, not a rendered picture.
- The page refuses any action the item's state does not show; a draft that
  passed its review is revised only by a person's Revise decision.
- run-profile.md: the run record fields are split into decision run records
  (Commission, Adopt) and worker run records (Generate, Verify), the latter
  exactly as `check_unit.py` requires; the runtime receipt example matches
  what the code writes; `<DS>` became `<Design Folder>`; examples use
  `_item01` slugs; "Runtime Workspace cards" became Run Space rows.

0.4.0 · 260913 · user ruling
- Keep the current workflow pre-1.0. Later-looking labels below are retracted
  as release assignments and retained only as development provenance.
- Any future `1.0.0+` requires explicit user approval.
- 260915 ontology rewrite: keep version 0.4.0 while replacing the phase map
  with `Design.commission → N Design.generate → J Design.verify →
  Design.adopt`; Gate/Route live inside each Run and expected count is
  `1 + N + J + 1`. No compatibility route was added.
- 260916: every Run Ticket names its Design Item, first as `item: DI<NN>`
  and, the same day, as `item: ITEM<NN>` (DI read as the Insight workbench's
  Data → Information). The Workspace bindings table became Space bindings
  (`Space` is the only reader-facing word), first over three Spaces and then
  over five, Goal · Design · Insight · Run · Delivery; Commission's pinned
  inputs show in Insight Space. Version unchanged.
- Earlier use of the same label (260828, JL, "design 不是 conclusion；它有一个收和开的过程"):
  Generate realization becomes TWO MOVEMENTS: DIVERGE then CONVERGE on the unit's ideation.md — the machine's first lawful divergence surface; every prior surface converged, which is why two live rounds could only redistribute fielded copy. GD2 checks both movements (5+ candidates, 2+ angles, all dispositioned, finalists ⊆ candidates); GD3 audits the selection honesty and never re-judges discards. The propose posture admits brief-only insight (direction 0.5.0): both information regimes design.

4.0.1 · 260913
- Forbid “read-only/readable migration history” language for unsupported
  Design bytes and stop content inspection after a decisive old-shape marker.

4.0.0 · 260913
- Adopt independent `rdNN_generate_*` / `rdNN_verify_*` identities.
- Remove every D0-D5, PageX, v1, old thread, and migration route.
- Treat non-current Design folders as unsupported instead of read-only input.

3.0.0 · 260913
- Replace the native D-style round vocabulary with Commission → Generate →
  Verify → Adopt and make each Commission an explicit frozen bet.
- Define the independent Page interlock: rp00/paragraph Runs and Page release/
  CHECK never mint, edit, judge, or renumber Design Results.
- Reuse human adoption as the Page domain gate; candidate changes route to a
  revise Design Run and Page-only prose changes remain Writing Steps.

1.0.3 · 260831
- Canonicalize every GD receipt under the granting Brief/Design Folder's
  `outline/<stem>-log.md`; Cards and Units keep state fields, not private Logs.

1.0.2 · 260831
- Make GD6 the unconditional round stop; a later round re-enters D0 only by a
  new commission.
- Map the Page owner RULING: D1/GD1 and D4/GD5 reuse their domain receipts;
  D0/D2/D3/D5 add no Page-local ruling.

1.0.1 · 260831
- Define Card → Unit → Verdict as in-place identities of one stable DU Folder
  with append-only phase history; give PageDown a minimal round-receipt Folder.
- Canonicalize DS identity as audience × job × venue and render storage as
  `delivery/render/`.
- Distinguish Design cross-phase authority gates from nested Page-local ticks;
  GD5 blocks outward work while D5/GD6 still seal the round.

1.0.0 · 260831
- D0-D5 are phase-owned Folder kinds. Dispatch loads the matching phase
  contract; this workflow keeps only D/GD order, thread/round frontier and
  receipts. The Application workflow adds no interior Design phase.

0.7.2 · 260828 · JL ("what I mean is: D5 PageDown")
- The phase NAME is PageDown, one word — JL overruled 0.7.1's Page-plus-alias split. The naming law gains its recorded exception: PageDown fuses the authority artifact (the Page) with its act (setting the round down onto it), and the artifact-class test still holds because the page is what D5 owns. "page down" stays the prose verb.

0.7.1 · 260828 · JL ("page down 相当于是把东西写下来")
- D5's verb alias renamed reconcile → page down, JL's own word and the plainer one — the round's record finally set down on the page, whole and readable. The phase NAME stays Page (the artifact-naming law wants an artifact class, and "PageDown" is a verb wearing one word). One boundary kept sharp: page down is the round-end SEAL, not the per-round sync duty — the write-back-in-the-same-round law is untouched and D5 catches what accumulation broke, it never licenses deferring write-back to the end.

0.7.0 · 260828 · JL ("这个 phase 是不是专门为了更新我们的 page？…这个 phase 不然就叫 page 呢")
- The lane gains D5 Page (reconcile) and GD6, the round seal. Root cause it cures, found the hard way the same day: every round APPENDS its own rows back (the sync law is append-shaped), but no phase owned the pages' GLOBAL claims — title, Opening, Diagram, scope, Law, board.md's Topic and close — so six rounds in, B00's pages still described round 1 and a colleague JL showed the board could not tell what it was about. D5 rereads the grown pages as documents and repairs staleness, PROSE only, decisions untouched; GD6 closes the round only when no era-frozen claim survives and stated counts match the rows on disk, with a fresh zero-background cold read (haipipe-board-reviewer-agent, judge-class, not a fifth human gate) mandatory at milestone rounds and before any outside showing. Rider: D1 renamed Direction → Card, retiring the last live use of the word deleted with haipipe-workbench-direction earlier the same day.

0.6.0 · 260828 · JL (the one-thread-one-folder merge)
- The THREAD becomes literal: one folder under design/, born at proposal holding only card.md, grown after release. D1's authority artifact is design/DU<NN>/card.md; GD2's back-pointer clause replaced by the card's state flip; release-before-realize is folder purity, a checker ERROR.

0.5.1 · 260828 · consistency pass before the first brainstorm run: postures header counts four; the commission entry gains the brainstorm form; pool-unit anatomy aligned with the design workbench 0.7.1.

0.5.0 · 260828 · JL ("我们是完全摒弃任何现在的 message" · "我不要求你测")
- The BRAINSTORM posture: designing a message SET and designing an EXPERIMENT are separate acts, and charging comparator duties (control cell, allocation, predicted effect) to the act of writing is what made two rounds retreat to fielded copy. A brainstorm round lands a POOL — N newly authored messages for one audience, zero reuse, no comparator, no forecast. GD2 checks pool-target, newness and mutual distinctness; GD4 does not reach a pool unit; fielding is the task layer's decision downstream.

0.3.0 · 260828 · JL ("我们肯定是要敢于创新的，敢于大胆去设计新的 message")
- The `generate` stance joins explore and bet-against (§The three stances): field rounds 2 and 3 both retreated to redistributing fielded copy — the lawful maximum was exploitation-shaped, and the abductive move (Dorst; C-K) had no legal entry. License = warrant-insight + warrant-theory per haipipe-workbench-direction 0.4.0 law 4; boldness at the card, honesty at the verdict.
- GD1 gains release-binds-existing-cards (the round-3 inversion friction: blanket recorded before its cards were authored). GD2 gains the generate novelty block; GD3 gains the acceptance-list audit ruling and the generate byte-check; GD4 admits a theory-typed direction with its QA anchor, never a numeric one.

0.2.0 · 260827 · JL (cold-read repair round: 2 BLOCKER + 7 MAJOR findings from a fresh-context audit, all resolved; see also the 0.1.0 entries repaired in place)
- The frontier unit renamed THREAD: a card until it lands (proposed/released/landed/killed), the division row after — the door's "one division per landed unit" untouched; a proposed card never blocks round-close, it carries over.
- The judge's verdict got a home: the unit README's judged: line, written by the judge and never the arm (haipipe-workbench-design 0.4.0 §verdict); D3's authority artifact now resolves on disk.
- EMIT got a route: an emitted: division row + a new BR00 needs row → the register question is born NEED-FIRST from it. No third birth; no pen crosses.
- GD5 defers to haipipe-page-for-design's acceptance-row grammar instead of inventing a third field list that failed every live row on B00.
- The forecast's score got a home: a dated scored: line appended to prospect.md at read-back, same bookkeeping class as staleness clearing.
- prospect.md moved to where it is actually written: D2 (the arm's step 5), checked at D3/GD4; GD2's completeness list now includes it; GD4 gained the non-retroactivity clause.
- Receipts land only on surfaces that HAVE Logs: BR00 for GD0, the DS page for GD1-GD5, rows naming artifact ids.
- Blanket release/accept legalized properly: a person's recorded act over a NAMED set, transcribed clerically with the person's words cited (haipipe-workbench-direction 0.3.0; app-workflow 0.8.0 in step).
- DELIVER coinage dropped for the family word ACCEPTED; DR<NN>-<slug> slug restored; P4 mapping made self-consistent (proposal included); GD3's machine-checkable claim split (stance fidelity is the judge's cold read); reflect's third on-disk word acknowledged (judged); failed-verdict edge D3→D2 added; stale "workbench bump owed" note replaced (only the unit-no-prospect checker rule remains owed).

0.1.0 · 260827 · JL
- New skill: the DesignBoard lane's phase machine, mirroring haipipe-insight-workflow 0.1.0. Five phases named by the lane's authority ARTIFACT classes (D0 Brief, D1 Direction, D2 Unit, D3 Verdict, D4 Division), a stated one-step extension of the naming law from authority page to authority artifact, since one DS page hosts many divisions.
- The DIVISION as the frontier's atomic unit; a ROUND as one D0→D4 pass; round one always completes — insufficiency exits only through the EMIT edge (a new register question, need-first birth), which is the problem-solution co-evolution edge (Dorst & Cross 2001) made mechanical.
- Evaluation split into two mandated faces with the alias law: reflect (ex-post) — conformance to spec, rails and the grant chain — and prospect (ex-ante) — a scored forecast of the artifact in use, written to the unit's prospect.md. Three guardrails: grant-only citation, forecast-typed output that never lands on an InsightBoard, scored-not-cited. The outer loop scores forecasts against measured effect, making bets calibrate across rounds.
- Gates GD0-GD5 as per-division assertions; GD0 = the app machine's G4, GD5 = its G5; the two human gates (card release GD1, acceptance GD5) complete the application's four, two per door.
- The commission entry: one sentence ("design X for Y on Z, reading W") drives the round end-to-end, stopping only at the ✋ gates; a person's recorded blanket release is a person's act.
- Owed follow-ups recorded here: haipipe-workbench-design contract bump to add prospect.md to the unit anatomy; theory anchors under verification by the 260827 discovery sweep.
- Same day: the literature section reduced to a pointer (JL: lit lives on a board page, not in a skill) — the anchors are on ApplicationSkillBoard QD4-round-theory, the full lists in five QA files under designs/Project-Application-SMSDesign/discoveries/S02_design-process-theory/ (59 verified sources, five colliding S02 groups merged same day).
