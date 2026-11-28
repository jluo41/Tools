# Insight ladder

The ladder has three cooperating Block kinds. Read their actual board.md and version faces before creating or changing work. Scripts scaffold the folders and check their implemented conditions; agents must also verify the required reviews and actual human decisions. The shared workbench reads the sources inside a Block page.

## Block, Job, Task and Run

| Block | Job | Task | Execution |
|---|---|---|---|
| Question Book (`prototype`) | question-set version | question definition with needs, method and code | authoring/review operations; answers belong to a Board |
| DataPrep (`insight-dataprep`) | prep-code version | ordered step definition | whole chain executes in the Board prep Task |
| Insight Board (`insight-board`) | fixed question × data, plus prep when used | prep execution or question answer | one prep-chain Run; computed question × segment Runs |

The Book and DataPrep keep code independently of data. A Board Job pins exact signed code versions and frozen data. A new data version, question version or prep version changes that named part of the analysis, not its Job Type. Group labels are views over these records and create no directories.

## Question Book

```text
insight/InsightQuestionBook-〈topic〉/
├── board.md                              board-kind: prototype; serves the named Board
├── proposals/〈slug〉.md                  kind, level, source, state, taken-in, reason
├── sNN-〈topic〉/                        Studio topics
├── runs/                                Book authoring operations
└── jNN_question-vN_〈slug〉/
    ├── jNN_question-vN_〈slug〉.md        release, state, signed, from
    ├── release.yaml                     complete questions and retired ids
    ├── partitions.md                    segments fixed before outcomes
    ├── thresholds.yaml                  floors, alpha, seeds and power threshold
    ├── src/                             shared question code
    └── tNN_〈L〉NN_〈slug〉/
        ├── question.md                  id, level, ask, method, needs, agreement
        ├── scripts/〈slug〉.py           question entry script
        └── runs/                        evidence planning, writing and review
```

`release.yaml` is the membership authority. Resolve each task path relative to that release, including references into another version. Kept questions remain at their source; new or changed questions have a local Task. Changes retain the Book tNN and id and reset agreement. A retired id moves to `retired` with a reason and is not reused. A level change gets a new id and links its source.

```yaml
release: question-v2
questions:
  D01: {task: ../j01_question-v1_〈slug〉/t01_D01_〈slug〉, change: kept}
  K02: {task: t09_K02_〈slug〉, change: new}
retired: {}
```

A proposal is the entry for a new question, fix, retirement or segment. Triage a batch into one version. The question skill defines the neutral ask; the evidence-plan skill declares the needs. Independent reviewers agree the plan, review compute scripts and judge questions. A person signs the segments and release. The signature freezes the version; another change belongs in another version.

## Board and version pins

```text
insight/Insight-〈dataset〉/
├── board.md                              dataset, prototype, optional dataprep, versions
├── meta/meta.md                          data description, no patient rows
├── reports/                             Board readings across Jobs
├── sNN-〈topic〉/
├── runs/                                Board operations
├── delivery/                            signed handoffs and report outputs
└── jNN_data-vM_prep-vK_question-vN/
    ├── jNN_data-vM_prep-vK_question-vN.md release, prototype path, hash, data, prep,
    │                                    dataprep path, prep-hash, ready, moved, previous
    ├── reports/vs-〈previous〉.md          source-linked comparison
    ├── runs/                            Job operations
    ├── t01_prep-vK_〈slug〉/runs/r01_〈dataset〉/
    └── tNN_〈L〉NN_〈slug〉/
        ├── tNN_〈L〉NN_〈slug〉.md         question id, answer, confidence, review
        └── runs/rNN_〈segment〉/          ticket, card, result and reading
```

When the Board uses prepared data directly without a DataPrep pin, a Job fixes question and data versions and is named `jNN_question-vN-〈slug〉_data-vM`. Read the actual face and retain actual folder names. With DataPrep, t01 executes the chain and question Task positions are shifted by one; match questions by id and release reference, not merely by tNN.

A Job pins `release: question-vN`, its release path and hash, plus `data: data-vM`. A prep Job also pins `prep`, its path and signed hash. The combination is unique. From the preceding Job, change one version at a time; `moved` records start, data, code or prep. This comparison control does not itself establish causality. A Job closes only through the required checks and the person's signature.

Data versions are frozen once added. Direct prepared-data versions name their folder and description. With DataPrep a data version names raw data, cut and params; [dataprep.md](dataprep.md) defines their execution. `label` is a short description. `accumulates` records whether later data include the earlier rows. Use SPACE-relative paths or configured variables. No page reproduces individual records.

## Segments and answer Tasks

Segments belong to the question release's partitions.md and thresholds.yaml and are fixed before outcomes. A Board proposes a segment through the Book, rather than mutating a signed release. The segment's position determines rNN. Cross receives the named segment results; it is not another Task or a subset of rows.

Each Board Task corresponds to a release question, apart from the explicit prep Task. A question with a compute need receives tickets for its asked segments. A question with only cited evidence receives no artificial compute Run. Executive questions synthesize cited answers; together their pages form the Overall Report. Wisdom counsel remains bounded by the supported Knowledge and pooling verdict.

Power is checked before a contrast. If evidence cannot answer, record the refusal and minimum detectable effect where applicable. A non-significant difference does not establish equivalence or pooling. `POOL`, `SPLIT` and `UNDETERMINED` apply only with their supported Cross assessment, and Wisdom observes the resulting limits.

A hard ticket reads the source question and script, release segments/thresholds, and the pinned data or ready output. It writes its own result tables, figures, receipt and provenance. Heavy output belongs in the configured result workspace. Generated artifacts are regenerated from source; do not hand-edit them.

The Run's report.md is a reviewed interpretation beside result/, not a replacement for computed evidence. Rerunning preserves the reading and marks it stale. A Task page is the short answer from those readings, checked independently. Its answer-status and check fields are source facts; UI uses the shared marks and controls.

## Version and cross-Job reasoning

A kept question is executed again in a question-code change Job. Equal script and data with different result hashes requires investigation, rather than calling the answer held. A comparison names each question, its source, previous/current result, held/changed/new/dropped/not-comparable judgment and the reason.

A Board reads coverage across question × segment × Job, tracks a question across Jobs and checks consistency. Its Findings link those records. Propose question improvements back to the Book. Synthesis creates a new finding linked to its evidence; showing an existing finding at another level uses a reference.

## Runs and owners

Every soft Run is `run-〈type〉-〈target〉/` with its card, ticket and passes. A hard Run is `rNN_〈segment〉/` with run.sh, run.yaml and result/. Open execution can retry through its ticket; closed result evidence is immutable.

| Scope | Operations | Owner |
|---|---|---|
| Book | triage, open version, question map | question skill; insight scaffold |
| Version | ask, review questions, set segments, sign | question/evidence owners; person signs |
| Question definition | plan evidence, review plan, write script, review script | evidence-plan, insight and independent reviewers |
| DataPrep | open prep, review steps, sign prep | insight and script reviewer; person signs |
| Board | add data, add Job, propose, coverage, track, consistency, counsel, handoff | corresponding Insight skill |
| Board Job | prep, launch, power, compare, propose, close | runner and card owner; person closes |
| Answer Task | segment ticket, write, CHECK, pool, alignment | level skill and independent reviewers |

The precise card inventory is `hai-insight-workflow/ref/run-cards.md`, read by `scripts/run_cards.py`. Its classifications route work; current UI navigation is specified by workbench-insight. Studio passes stay in their topic and are not analysis Runs.

## Scripts and safe completion

- `scripts/insight_ladder.py`: scaffold and inspect versions, questions, data, Jobs and gate records.
- `ref/open_job.py`: pins, answer Tasks and segment tickets.
- `ref/run_job.py`, `ref/run_question.py`: question execution, power and output checks.
- `ref/run_prep.py`: preparation chain, described in dataprep.md.
- `ref/run_report.py`: Run reading and review support.
- `ref/deliverables.py`: answer deliverables and review requirements.
- `ref/question_map.py`: generated question map.
- `ref/overall_report.py`, `ref/overall_figures.py`: Executive report and figures from cited aggregate tables.

Use the script's help for exact arguments. Audit the actual folder before changing it; preserve independent versions and existing evidence. A fresh-context reviewer judges what an agent made. A person supplies signatures explicitly. A completed review Run can contain a returned verdict; a collection placeholder is not consent. Verify the actual review conclusions and stated decision before signing, even when the command accepts its inputs. Do not treat a successful scaffold or rendered page as a review.

A signed Design handoff names its finding, strength, version pins, evidence, limits and design consequence. Design reads the exact signed source. If new evidence changes its basis, create a new handoff and preserve the prior signed record.
