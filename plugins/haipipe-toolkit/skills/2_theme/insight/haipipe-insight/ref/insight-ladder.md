Insight ladder: the Prototype, the insight Board, and how they work together
===========================================================================

(JL 261007 plan C, designed in Tools/designs/b11_theme_insight: s00 the thinking, s11 Board, s12 Job, s13 Task,
s21 Runs and skills; special boards JL 261008.) Insight sits on the shared ladder as two special boards. The
**Prototype** holds the questions and the code that answers them; each of its Jobs is one version, a release. The
**insight Board** holds one dataset and its dated versions; each of its Jobs runs one release on one data version.
Each level has the six Spaces of the base workbench (Description · Idea Studio · Audience Report | Work Details |
Runs · Delivery); the insight workbench fills them (servers/workbench-insight: insight_plan_c.py reads this tree,
insight_views.py draws it). `scripts/insight_ladder.py` makes each folder and keeps the gates.

Read this reference when creating, naming, growing or auditing an insight folder. Two older layouts stay readable
until they are carried over: the Insight Block with one Job per DIKW level ([block-contract.md](block-contract.md))
and the register board ([board-contract.md](board-contract.md)). The question file and the script keep the contract
written there (block-contract.md § The question file, § The script); only where they live has changed. A release, from
its proposals to its signature, is [release.md](release.md).


The two trees
-------------

```text
<Project>/tasks/Prototype-bNN-<Topic>/        the Prototype: questions + scripts, by version
├── board.md                                  board-kind: prototype · serves: insights/Insight-<name>
├── proposals/                                the backlog: <slug>.md (kind · level · from · state · why), README.md
├── studio/ · runs/                           the question map, its own Runs (triage · open a version · carry)
└── jNN_pN_<slug>/                            one version (a release), frozen once a person signs it
    ├── jNN_pN_<slug>.md                      release · state: open | closed · signed: ✅ <YYMMDD> · from: p<N-1>
    │                                         · carried-from (when a Block was carried in)
    ├── release.yaml                          release · questions: {<L><NN>: {task, change}} · retired: {<L><NN>: why}
    ├── partitions.md                         the cuts (front matter partitions:), set before any outcome
    ├── thresholds.yaml                       shared floors, alphas, seeds · power.smallest_effect_pp
    ├── src/                                  code two or more scripts share
    └── tNN_<L><NN>_<slug>/                   a question new or changed in this release
        ├── question.md                       the question (block-contract.md § The question file)
        ├── scripts/<slug>.py                 its one entry script (SPEC line; § The script)
        └── runs/                             its making Runs: plan the evidence · review · write · review the script

<Project>/insights/Insight-<name>/            the insight Board: one dataset, its versions, a Job per pair
├── board.md                                  board-kind: insight-board · workbench: insight · dataset: <D> ·
│                                             prototype: tasks/Prototype-… · accumulates: yes | no | ? ·
│                                             versions: [{version: v<M>, folder, frozen, new, preview}]
│                                             ## Questions (```yaml questions:): the Board's own questions
├── meta/meta.md · meta/status.md             what the extract holds · the status grid (the checker writes it)
├── studio/ · reports/qNN_<topic>/            topics · the Board's questions, answered across Jobs
├── runs/run-<type>-<target>/                 every Board Run is soft (add a version, add a Job, readings, …)
├── delivery/                                 the signed handoffs: handoff-<W>.md names its pair (pN × vM)
└── jNN_pN_<D>vM/                             a Job: release pN × data version vM, frozen once closed
    ├── jNN_pN_<D>vM.md                       release · prototype (the release's path) · hash · data · state ·
    │                                         moved: start | data | code · previous
    ├── reports/vs-<prev>.md                  run-compare's table: question · previous · this · status · why
    ├── runs/                                 soft: launch · power · compare · propose · close
    └── tNN_<L><NN>_<slug>/                   a Task: one question of the release, the same name as there
        ├── tNN_<L><NN>_<slug>.md             THE PAGE: question · answer-status · answer · how-sure · check
        └── runs/
            ├── rNN_<partition>/              hard: run.sh (the ticket) · run.yaml · result/ (tables, figures,
            │                                 partition_power.csv, runtime.yaml, report.md, provenance/)
            └── run-<type>-t<NN>/             soft: write · check · pool · check-alignment
```

**Names.** Both are special boards, named by their kind (JL 261008): the Prototype `Prototype-bNN-<Topic>` in
`tasks/`, the Board `Insight-<name>[-<YYMMDD>]` in `insights/`. The folder name is a label: a reader knows each by its
`board.md` (`board-kind:`; a Board also by `prototype:`). An older `bNN_<topic>` name stays readable. Inside, Jobs and
Tasks keep `jNN_` and `tNN_`: a release `jNN_pN_<slug>` (the slug says what it is, JL 261008; its id stays
`pN` in release.yaml, the faces and Run names; an older `jNN_pN` stays readable), a Board Job `jNN_pN_<D>vM` (`<D>` the dataset, `vM` its version:
`j01_p1_<D>v1`), a question `tNN_<L><NN>_<slug>` (`t03_D03_<slug>`).


How they work together
----------------------

```text
          Prototype (tasks/Prototype-bNN-<Topic>/)                    insight Board (insights/Insight-<name>/)

proposals/<slug>.md ◀─────────── propose (questions, a cut) ──────────── a Job's vs-previous · Coverage's gaps
      │ triage: one batch                                                 · a weak or refused answer
      ▼
jNN_pN_<slug>/ open ▶ ask · plan · script ─▶ set the cuts ─▶ SIGN (frozen)
                 (another agent reviews each)        a person              │
                                                                          ▼
                                     data: a new extract ─▶ add v<M> ─▶ add a Job jNN_pN_<D>vM
                                                         (frozen)        moved: start | data | code
                                                                          │ launch · power · the hard Runs
                                                                          ▼
                                                     write · check each page ─▶ close the Job (a person)
                                                                          │
                                         compare with the Job before ◀────┤  (vs-<prev>.md)
                                         Board readings: coverage · tracks · consistency · the Board's questions
                                                                          ▼
                                                         W counsel ─▶ handoff, signed ─▶ Design
```

Two clocks: the **code** clock (a release) moves in the Prototype, the **data** clock (a data version) on the
Board. A new data version needs no release, and a new release needs no new data; a Job moves exactly one of them,
so a change in an answer has one cause.


The rules
---------

1. **One release × one data version per Job, one clock at a time.** The face pins `release: pN` (with the
   release's path and `hash:`, the first 12 hex of a sha256 over release.yaml, the cuts, the thresholds and every
   question's files) and `data: vM`. `moved:` says which clock moved from the Job before it: `start`, `data` (the
   same release on the next data version) or `code` (the next release on the same data). Both at once is refused:
   add the one, then the other. One Job per pair; a Job is frozen once closed (`run-close-jNN`, a person signs).
2. **A release is signed, then frozen.** A version opens from the newest one (`run-open-version-pN`): every
   question kept, its Task pointed back to the release that holds it (`task: ../j01_p1_<slug>/t02_I01_…`), the cuts,
   thresholds and `src/` copied. A question new or changed in this release has its Task here; a changed one is
   carried forward under the same `tNN` and its `agreed:` resets. Signing (`run-sign-release-pN`, a person) needs
   every new or changed question agreed by an agent that did not draft it, and the cuts set. A Board runs only a
   signed release.
3. **A question id is never reused, and a question keeps its `tNN`** in every release and every Job. A retired
   question leaves `questions:` for `retired: {<L><NN>: why}`; its id is not asked again.
4. **The cuts belong to the release.** `partitions.md` and `thresholds.yaml` are set in the version
   (`run-set-cuts-pN`, a person signs the cuts) before any outcome is seen. A Board never sets a cut; it proposes
   one (`run-propose-cut-<slug>`). A Run's `rNN` is the cut's place in the release's `partitions.md`.
5. **Proposals are the only way in.** A question, a fix, a retirement or a cut reaches a release only as
   `proposals/<slug>.md` (`kind: new question | fix | retire | cut`, `level:`, `from:` the Job or report it came
   from, `state: open | taken | declined`, `taken-in: pN`, why). The Board's and a Job's Propose Runs write there
   and nowhere else. Decided (261008): **a release is cut per triaged batch** (`run-triage-proposals-pN` takes a
   batch into the next version), never per single proposal, so one new question does not make a new Job each time.
6. **A data version is frozen once added.** `run-add-version-vM` appends `{version, folder, frozen, new}` to
   board.md `versions:` (261008: a version is its data folder, not one file): the folder holds the data file
   (named by its manifest.json `output_file`, else the one .parquet on top), and may hold manifest.json,
   data_dictionary.csv, cohort_summary.txt, figures/ and documents, all shown on Description › Dataset; a name
   starting with `_` is work beside it, listed, never read. `preview:` names the columns its few sample rows show
   first. An older version may still name one `extract:` file (with `rows:`). Paths are SPACE-relative (or
   through a variable), never absolute.
   `accumulates:` says whether a later version holds the earlier rows. `meta/meta.md` says what the extract holds.
7. **A Job's Tasks are its release's questions.** `run-add-jNN` writes the face, one Task per question (the same
   name as in the release) and one ticket per cut the question is asked on (`ref/open_job.py`). A question with no
   compute need has no ticket; its page cites the answers below it.
8. **A hard Run reads the release, never a copy.** `runs/rNN_<partition>/run.sh` runs `ref/run_job.py`: the
   question and its script from the release, the cut from its `partitions.md`, the extract from the data version.
   It writes only its Run: `result/` (the spec's tables, their figures, `partition_power.csv`, the `runtime.yaml`
   receipt, the generated `report.md`, `provenance/`) and `run.yaml`. Power is checked before any contrast and the
   output gated against the spec (`ref/run_question.py`, unchanged). Heavy output goes to
   `_WorkSpace/ProjectResult/<Project>/<Board>/<Job>/<Task>/<run>/`.
9. **Decided (261008): a kept question reruns on a code-moved Job.** Same script, same data, same tables: the
   compare checks the tables' sha256, so every kept question is also a reproducibility check, and every Job stays
   whole and self-contained. A difference there is a finding about the code, never a held answer.
10. **The page is the short answer.** `run-write-tNN` writes the Task's page from its Runs' reports, through the
   level's skill (`haipipe-insight-data`, `-information`, `-knowledge`); `run-check-tNN` is another agent's CHECK.
   The face's `answer-status:` walks `open → partial → answered`; `check:` records the CHECK.
11. **A Job reads the Job before it.** `run-compare-jNN` writes `reports/vs-<prev>.md`, one row per question:
   `held · changed · new finding · new question · dropped · not comparable` and why (which clock moved). Its
   Propose Run (`run-propose-jNN`) turns new or changed questions into proposals.
12. **The Board reads across Jobs.** Coverage (`run-coverage`: which question × cut × Job has an answer), tracks
   (`run-track-<q>`: one question across Jobs), consistency (`run-consistency-<jA>-<jB>`), and the Board's own
   questions (`run-ask-qNN`, `run-report-qNN`, `run-check-qNN`). Its Wisdom counsel (`run-write-counsel`) becomes a
   handoff (`run-draft-handoff`) that names its pair (`pN × vM`) and is signed by a person
   (`signed: ✅ <YYMMDD>`, never a name); Design reads only a signed handoff.


Runs
----

Every soft Run is `run-<type>-<target>/` with its `run.yaml` card (`run · kind · type · scope · target · ticket ·
skill · agent · signs · status · passes · writes · feeds`) and its ticket, written by the shared writer
(haipipe-run `scripts/soft_run.py`); a pass is `passes/pNN-<MMDD>/`. A hard Run is `rNN_<partition>/` (`run.sh` ·
`run.yaml` · `result/`): it counts as evidence, retries in place while open, and its `result/` never changes once
closed. A button the shared frame also has keeps the frame's name (haipipe-run `ref/run-types-by-space.md`).

```text
level      Run                              kind  does                                       skill
Prototype  run-triage-proposals-p<N>        soft  take a batch of proposals into p<N>        haipipe-insight-question
           run-open-version-p<N>            soft  the next version, from the newest          haipipe-insight
           run-map-questions                soft  draw the question map                      haipipe-insight
           run-carry-<board>                soft  carry an older Block or board in, once     haipipe-insight
version    run-ask-<l><nn>                  soft  a new question's Task                      haipipe-insight-question
           run-review-questions-p<N>        soft  Q1–Q7 on the release (another agent)       haipipe-question-review
           run-set-cuts-p<N>                soft  partitions.md · thresholds.yaml (a person) haipipe-insight
           run-sign-release-p<N>            soft  freeze the release (a person signs)        haipipe-insight
question   run-plan-evidence-<l><nn>        soft  its needs and work specs                   haipipe-insight-evidence-plan
           run-review-plan-<l><nn>          soft  agree the needs (another agent)            haipipe-insight-evidence-plan
           run-write-script-<l><nn>         soft  its one script                             haipipe-insight
           run-review-script-<l><nn>        soft  review the script (another agent)          haipipe-insight
Board      run-add-version-v<M>             soft  a data version, frozen                     haipipe-insight-meta
           run-add-j<NN>                    soft  a Job: release × data version              haipipe-insight
           run-propose-cut-<slug>           soft  a cut, into the Prototype's proposals/     haipipe-insight-question
           run-propose-<target>             soft  questions, into proposals/ (coverage gaps) haipipe-insight-question
           run-coverage · run-track-<q>     soft  readings across Jobs                       haipipe-insight-check
           run-consistency-<jA>-<jB>        soft  two Jobs' answers, judged by the reviewer  haipipe-insight-knowledge
           run-ask-q<NN> · run-report-q<NN> soft  the Board's own questions                  haipipe-question · -report
           run-check-q<NN>                  soft  a Board report's CHECK (another agent)     haipipe-report
           run-write-counsel                soft  the Wisdom counsel                         haipipe-insight-wisdom
           run-draft-handoff                soft  the Design handoff (a person signs)        haipipe-insight-wisdom
           run-close-j<NN>                  soft  check, then close a Job (a person signs)   haipipe-insight-check
           run-draw-s<NN>                   soft  a studio topic (every level)               haipipe-studio
Job        run-launch-j<NN>                 soft  run the Job's tickets                      haipipe-insight
           run-power-j<NN>                  soft  measure n and power per cut, before outcomes haipipe-insight
           run-compare-j<prev>              soft  reports/vs-<prev>.md                       haipipe-insight-knowledge
           run-propose-j<NN>                soft  new or changed questions → proposals/      haipipe-insight-question
           run-close-j<NN>                  soft  check, close and freeze (a person signs)   haipipe-insight-check
Task       r<NN>_<partition>                hard  the question on one cut (run_job.py)       haipipe-insight
           run-write-t<NN>                  soft  the page                                   haipipe-insight-<level>
           run-check-t<NN>                  soft  the page's CHECK (another agent)           haipipe-report
           run-pool-t<NN>                   soft  pool or split on Cross                     haipipe-insight-knowledge
           run-check-alignment-t<NN>        soft  each answer against its question           haipipe-insight-check
```

Run cards by level and Space (button, agent, sign, prompt) are `haipipe-insight-workflow/ref/run-cards.md`, checked by its
`scripts/run_cards.py --check` (against this list too). `haipipe-insight-workflow` routes Runs and keeps the gates; it is
no card's skill: each card names the skill that does the work.


The six Spaces at each level
----------------------------

```text
          Description                  Idea Studio        Audience Report                 Work Details        Runs · Delivery
Board     Map (releases × data         question map ·     Partition × Reading: Coverage · the Jobs: All ·     soft Runs ·
          versions) · Prototype ·      topics             Tracks · Consistency · Findings p1 · p2 …           Handoff
          Dataset · Partitions
Job       the Job's line (pN × vM ·    topics             Partition × Period: Current ·   Job → Task → Run    launch · power ·
          state · moved) atop                             vs previous                     (All · hard · soft) compare · propose ·
          Prototype · Dataset                                                                                 close
Task      Question · Records           topics             Table · Reading                 Partitions          All · hard · soft
Prototype (no level drawing yet: b11 s21 lists its run types; its Spaces follow when one is drawn)
```


Scripts
-------

```text
scripts/insight_ladder.py   make each folder; the gates: a signed release, a data version, a new pair, one clock
ref/open_job.py             a Job's face, its Tasks and one ticket per asked cut (insight_ladder.py job calls it)
ref/run_job.py              the runner of a hard Run's ticket: reads the release, writes only the Run
ref/run_question.py         the statistics, the power check and the gate, shared by both runners
ref/figures.py              the run report's figures, from result tables only
ref/question_map.py         the question map
ref/prototype_from_block.py carry an Insight Block (one Job per level) into a release, word for word
ref/carry_over.py           carry a register board into an Insight Block, word for word
```

A new topic: `insight_ladder.py prototype`, `version`, one `question` per question, then the review, the plan, the
scripts and `sign`; `board`, `data v1`, `job --release p1 --data v1`; the tickets; then the pages.
