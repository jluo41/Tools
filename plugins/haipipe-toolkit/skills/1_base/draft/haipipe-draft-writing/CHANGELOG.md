## 0.26.0 · 2026-10-22 · Examples first

- JL 261022: "我突然忘了第一件事：你应该先找 example，看看别人是怎么写 abstract 的，然后再看怎么写。所以在 write 的时候，你应该
  先找到相应的 example，这样我们就可以 follow 别人的参考了". New `ref/writing.md` § 0 · Examples first: before a Section is
  written or rewritten whole, read 3 to 4 published papers of the venue writing the same Section (a Studio topic
  `sNN-<task>-<venue>-examples`, /excalidraw-read), note each paragraph's or heading's move and length, write to that
  pattern, and name each departure with its reason. The workbench's 2 · Write shows the 📚 Examples card and its prompt
  starts with them (finding them first when there are none).

## 0.25.3 · 2026-10-21 · A Revise pass answers the person's comments first

- JL 261021: "你每次改的时候，能不能通过我的 comments 来回复那种？"; "你的 change 怎么跟我的 comments 一起来做交互、解决我的
  comments 呢？". ref/revise.md: a pass reads the open comments in `draft/records/<stem>-comments.md` first, as
  rulings; it changes the sentence as an Edit card with `Answers: Comment <n>` or says why not, appends a
  `- Reply · <time>: …` line and sets `State: answered`; only the person writes Notes, closes or deletes. The
  running line and the Revise rules file (0.25.2's workbench side) are described there too.
- JL 261021: "你需要给每一个 sentence 句句过关"; "每句话都要看一下上下文，review 它的逻辑关系是否通顺，并且给每句话打分".
  A Revise review report lists every sentence in its context (haipipe-draft-review 0.3.0 `ref/sentence-logic.md`),
  and the loop ends only when each scores 8 or more on logic and read, with no broken link.
- JL 261021: "可以用 A、B、C 几个不同的方法去修改，propose 一些选项". A card whose fix is a choice gives 2 or 3
  `Option A (<approach>): <sentence>` lines and `Chosen: A`; A is applied by default, the person may pick another.
- JL 261021: "在 reply 的时候，难道不能说得更 concise 一些". A pass's Reply to a comment is at most two short
  sentences (30 words): what changed, and its rule.
- A pass that rewrites the cards file keeps every decision the person made on a card (State accepted, rejected or
  edited; Chosen), refreshing the rest (`ref/revise.md`; JL 261021, after his ✓ on the Abstract's Section question was
  written back to proposed and restored).

## 0.25.2 · 2026-10-21 · A Revise pass opens with its review report

- JL 261021: "我感觉这里面每一句话都写得非常不顺畅。你来 review 一下它，我觉得你应该先写一个 review report，然后再
  propose 怎么去改这些内容"; on the whole-Section card: "单独作为一个卡片放到 revise card 里面。名字你可以写 current draft
  review report"; then "above the section of 'The text and its Revise cards' you should give me the section 'Revise
  Review Report' and tell me for each rubric, how you feel about this draft". ref/revise.md: a pass opens with
  `### Revise review report` (Reviewer, Verdict, one row per rubric axis plus the venue's rule, each with its verdict,
  reading and smallest fix, then Now and Proposed), no State, then its cards; a sentence the person wrote is carded as
  a Review, never an Edit.
- JL 261021: "你这个 rubric 怎么没有分数？... 句子连贯性、反 AI 写法 ... 你有没有拿那个来测试"; "还是一个 sentence
  一个 sentence 改吧"; "我觉得还是用十分制吧". Each report row carries a score out of 10 (haipipe-draft-review 0.2.0); two rows join the four axes, Coherence and
  Anti-AI (haipipe-draft-review's `cli/anti_slop.py audit` and `ref/ai-tells.md`); a `Cards:` line scores the
  cards' own text on that audit; cards are one per sentence with a finding.

## 0.25.1 · 2026-10-20 · Revise is 5 · Revise

- ref/revise.md: a Section's Revise cards are in the draft Task's 5 · Revise tab (4 · Display came before it, 261020).

## 0.25.0 · 2026-10-20 · Where a Section's Revise cards live (b32 s41)

- `ref/revise.md`: the 4 · Revise tab's cards are `draft/records/<stem>-revise.md`, one `### <kind> · S<n> · <what>`
  card each with Why, Original, Expected and State; an accepted card goes into `## 3 · Draft` as the next version.
- A pass per run (`## Pass <k> · <yymmdd> · on draft v<N>`), and the reviewer's stance first: who reviews, what they
  look for, how; then Section questions on structure before Edit and Review cards (JL 261020).

## 0.23.0 · 2026-10-16 · Auto revise (JL 261016, b32 s41-D13)

- `ref/auto-revise.md` and `cli/auto_revise.py`: rounds of revising a candidate copy, each judged by a fresh
  haipipe-draft-review agent, stopping on the rubric verdict, no improvement, or 3 rounds; small fixes applied, big ones
  held as decision cards; nothing reaches the Draft before the person picks.


## 0.24.0 · 2026-10-16 · ref/drafting.md is ref/writing.md, and opens with its rules (JL 261016)

- `ref/drafting.md` renamed `ref/writing.md` (JL 261016: "COULD WE CHANGE THIS TO THE ref/writing.md, and do we have
  any writing rules here?"). It now opens with "The rules every sentence is written by": the five sections of
  `haipipe-draft-review/ref/plain-rules.md` in one line each. The rules stay in that one page, so the writer and the
  reviewer read the same list. Every mention follows (SKILL.md, haipipe-draft-review, haipipe-draft-logic's
  structure page, the workflow test, the changelogs).

## 0.22.0 · 2026-10-16 · The Revise Run moves in (JL 261016, s41-D11)

- `workflow-runs/haipipe-draft-revise` is folded in as `ref/revise.md`; its ledger format is `ref/revise/change-ledger.md`;
  its changelog is `ref/history/haipipe-draft-revise-CHANGELOG.md`. Text unchanged except the header and two links.
- New short section "The Revise Run" in SKILL.md; the revise triggers are in the description.
- The Run name `run-revise-<target>` and the Revise view are unchanged.

## 0.21.0 · 2026-10-16 · The writer gets its own skill (JL 261016, s21-D06)

- Moved up from `workflow-runs/haipipe-draft-writing/` to `skills/1_base/draft/haipipe-draft-writing/`, beside `haipipe-draft-review` (the judge). Whoever writes never reviews.
- Folded in `haipipe-sentence` (retired): its contract is `ref/sentence.md`, its history `ref/history/haipipe-sentence-CHANGELOG.md`. Evidence on a span of words is now a pointer to `haipipe-evidence`'s `anchor`, not a second contract.
- Folded in the drafting half that lived in `haipipe-draft/ref/writing/` (writing.md, writing-request.md, realize-from-plan.md, weaving.md, writing-dna-adapter.md, change-record.md, holes.md) as `ref/`.
- Description and triggers: THE writer; old `haipipe-sentence` triggers and the drafting triggers added. Run contract content unchanged. `../` links in moved files lost one level.
- `haipipe-draft/cli/wdiff.py` stays in `haipipe-draft`.

## 0.20.1 · 2026-09-29 · outline/ to draft/ in current-layout prose (JL 260929)

- Paths that describe the current Page layout say `draft/`: the plan `draft/<stem>-draft-v<G>.<S>[.<E>].md`, records `draft/records/`, `draft/previous/`, `draft/skill/`, the Evidence Markdown `draft/<stem>-evidence-items.md`, `draft/evidence/bibex/` and `draft/evidence/materials/` (JL 260929: "it should be draft"). Mentions of legacy Pages, retired `outline/evidence/` lanes and the migration keep `outline/`, as do the OUTLINE stage, the Outline table and the `outline:` grammar key.

## 0.20.0 · 2026-09-28 · No content hashes (JL 260928)

- CONTENT reruns the declared lanes' fixed Delivery Runs (`page.py export`) instead of commissioning numbered RD Runs (JL 260928).
- `cli/promote_paragraph.py` writes and compares no sha256. Staleness is file time: the Page is
  stale when saved after the Run read it (`read_at` on the `page-source` input, else `started_at`).
  Idempotency and interrupted-write recovery compare the addressed paragraph's text.
- The promotion receipt drops `result_sha256`, `page_before_sha256`, `planned_page_after_sha256` and
  `page_after_sha256`; it records `page_read_at`, the locator and times. Leftover `sha256` keys in
  an older runtime.yaml are ignored, never required.
- `SKILL.md` and `ref/paragraph-run.md` name inputs by path, version and date, never by hash.

## 0.19.0 · 2026-09-28

- ⛔ Hard rule under the title (JL 260928, AGENTS.md rule 6): never modify a generated file directly; change the code that writes it, then rerun.
- The Adopt movement is `haipipe-draft/cli/page.py adopt <page>` (dry run first); sentences are
  never retyped into `## Content` by hand (haipipe-draft 0.119.0).

## 0.18.0 · 2026-09-22

- Renamed from `haipipe-page-content` and moved to `skills/page/workflow-runs/`: the skill is named
  by its Runs, `rp-sec-NN` and `rp-para-NN_Pxx[-Pyy]`. Delivery moved out to its own
  skill, `haipipe-draft-delivery`.

## 0.17.1 · 2026-09-20

- Treat adoption as a controller action and apply shared profile-specific release decisions.

## 0.17.0 · 2026-09-20

- Use the shared Writing request, method selection and bounded evaluation in the delegated paragraph Ticket.
- Keep Page adoption and delivery separate from candidate generation and self-review.

## 0.16.0 · 2026-09-15

- Define CONTENT as the release/adoption Run Spec owner and keep adoption,
  delivery, and pre-check inside the bounded release work.

## 0.15.0 · 2026-09-14

- Update the release barrier to consume typed RP identities and the unified
  Evidence/Card label contract before delivery.

## 0.14.0 · 2026-09-12

- Require the reserved `rp00_mermaid-structure` gate before Page-level Content
  release; paragraph Page Runs begin at `rp01`.

## 0.13.0 · 2026-09-12

- Add a Page release barrier: CONTENT waits until every planned Page Run and
  required evidence Task Result is complete and bound.
- Keep individual Writing Steps and Page Run closures in the Bullet Workspace;
  they do not modify Page Content or delivery.
- Adopt all accepted candidates and generate declared web/LaTeX/Word outputs
  once in the Page-level CONTENT pass before CHECK.

## 0.12.0 · 2026-09-11

- Make agreed-text adoption the default CONTENT handoff. No automatic redraft/humanizer or replacement Run per paragraph. Retain explicit delegated single-paragraph promotion and formal delivery gates.

## 0.11.0 · 2026-09-10

- Consume reviewed SHAPE preview slices as prior candidate prose in Paragraph Runs, revalidate evidence and style, then use normal promotion.

## 0.10.0 · 2026-09-09

- Add a concrete-before-polished default writing style for paragraph Runs:
  subject-first sentences, one primary reader move, specific language, and no
  process/AI-shaped scaffolding; owner and venue policies still take priority.
- Require Page-changing CONTENT responses to return direct Bullet Workspace
  (`lens=div`) and Evidence Workspace (`lens=workspace&seg=items`) links from
  the same verified public Board route.

## 0.9.2 · 2026-09-08

- Connect the optional HAI anti-slop adapter to Paragraph Writing Runs as a
  post-draft diagnostic artifact, without making its score an acceptance gate
  or allowing external auto-fix commands to bypass `wdiff.py` and promotion.
- Record the selected audit/report in the CONTENT receipt and route findings to
  bounded CONTENT revisions while preserving plan, evidence, claim strength,
  citations, numbers, and neighboring seams.

## 0.9.1 · 2026-09-08

- Add the deterministic `cli/promote_paragraph.py` CONTENT write path for
  moving one accepted Paragraph Result back into its exact `C<n>.P<m>` Page
  source span.
- Pin promotion to the frozen Page hash, serialize per-Page writes, preserve
  sibling/annotation records, verify the post-write target and hash, and record
  an idempotent/recoverable promotion receipt in `runtime.yaml`.
- Add focused promoter tests covering replacement, insertion, explicit-heading
  ambiguity, stale Pages, fenced headings, interrupted preparation, and blocked
  structural input.

## 0.9.0 · 2026-09-08

- Default new writing to one Cn.Pm Paragraph Run, with an embedded-prompt Markdown Ticket and paragraph/trace/runtime Result.
- Freeze owner style, exemplars, feedback and neighboring context; promote only the addressed paragraph, then check division/Page continuity.
- Carry an optional frozen Writing DNA packet into the Paragraph Run and trace; style remains subordinate to claim strength, Evidence, and venue rules.
- Carry an optional Page-owned Narrative Decision into the entry check and
  Paragraph Run so the approved paragraph organization is frozen before DNA
  surface realization.
- Make claim-strength compatibility with the bound Evidence Result an explicit
  pre-allocation CONTENT gate; mismatches route upstream before a Paragraph Run.
- Preserve historical division Results; revise through explicit replacement Runs, without new paragraph workbenches or QA lanes.

## 0.8.4 · 2026-09-07

- After Build, return the four-surface user-check packet: evidence to open now,
  whether Revise ran (a first draft is never presented as final), then the
  Page-level PDF as the delivery surface.
- The receipt no longer carries a `delivery_report`; when an owning build emits
  one, it names the single `delivery/build-manifest.json`, with no delivery-QA
  sibling.

## 0.8.3 · 2026-09-07

- Load the Task Page companion and require its display inventory and
  table/figure/diagram gate during CONTENT drafting and Build.

## 0.8.2 · 2026-09-07

- Require CONTENT/Build to return the shared user-check packet with the
  Outline Board URL, current Display PDFs, and current Page-level PDF.

## 0.8.1 · 2026-09-07

- Apply the Section owner's subsection-title contract during revision and
  synchronize authorized naming repairs without expanding their scope.

## 0.8.0 · 2026-09-06

- Permit explicit draft mode after local evidence work is exhausted: use an
  old accepted value plainly or one visible `[E## pending]` marker for a named
  server/person gate; final mode rejects every marker.
- Keep workflow vocabulary out of manuscript prose and shape normal paragraphs
  as 4–6 one-point sentences with a median near 21 words.
- Require a humanizer pass and fresh-context MISQ style verdict before Build;
  add writing-only review for drafts with unresolved values.
- On complete-version requests, deliver the requested PDF/LaTeX and Word,
  report pages and viewer link, and trim figure PDF margins.

## 0.7.0 · 2026-09-06

- Admit only generation `G>=1` plans to CONTENT; every `v0.*` state remains
  planning-only.
- Refresh Content for every Shape or evidence version change. Evidence-only
  revisions inherit Shape approval and revalidate only affected realizations.

## 0.6.1 · 2026-09-06

- Treat sentence length as a distribution: an 18–24-word median is a readable
  MISQ house-style center, while 30+ words triggers review rather than an
  automatic split or writing blocker.
- Split long sentences only when they stack distinct reader moves or obscure
  the main claim; preserve coherent longer relations and varied prose rhythm.

## 0.6.0 · 2026-09-06

- Add a formal OUTLINE → CONTENT entry check before any Division Writing Run.
- Separate hard authority/evidence gates from manuscript-form warnings.
- Require Section name/structure, paragraph and sentence-slot budgets, expected
  sentence length, and citation-density units to be reported distinctly.
- Measure existing and drafted prose with `haipipe-paper-draft/cli/section-stats.py`;
  never present pre-draft estimates as actual prose measurements.
- Follow only the current Evidence Items' selected Local Result pointers and
  stop once each checklist row has a supported verdict.

## 0.5.0 · 2026-09-06

- Make one point per Section sentence binding during WRITE.
- For MISQ, target the outline's 23–26-word center, split routine 30+ word
  clause stacks, and avoid formulaic connective ladders and AI-style framing.

## 0.4.0 · 2026-09-06

- Forbid paragraph-level and sibling-Bullet evidence inheritance during WRITE.
  Reused sources still trace through a distinct CITE Item at every realizing
  Bullet.

## 0.3.0 · 2026-09-06

- Enforce evidence at the realization address: a citation or concrete value in
  CONTENT must have a CITE or VALUE Evidence Item on that same Bullet.
- Treat `Evidence: none` as a binding source-free contract and route any later
  material need back to OUTLINE/SHAPE.

## 0.2.1 · 2026-09-04

- Route CONTENT through the exact Page Face owner and load a canonical family
  owner only once when it also owns the Folder.

## 0.2.0 · 2026-09-04

- Remove the retired DRAFT and REVISE redirect skills and agent identities.
- Preserve their receipt tokens only in the lifecycle auditor; all current
  dispatch is CONTENT/WRITE.

## 0.1.1 · 2026-09-04

- Use the canonical Page dependency order and carry the target cycle separately
  from the phase route in CONTENT receipts.

## 0.1.0 · 2026-09-04

- Add the unified `03 CONTENT` phase with one `WRITE` cycle.
- Fold Draft, Revise, Build, and Pre-check into internal movements rather than
  separate Page phases.
- Define one normal Level-4 `Page · Division Writing` Run per commissioned
  Content division, with candidate, trace, runtime, and promotion contracts.
- Keep `04 CHECK` independent and solely authorized to close a Page.
## 0.15.0 · 2026-09-14

- Require the structure/Bullet, Section, paragraph, and evidence release
  dependencies before CONTENT adoption.
