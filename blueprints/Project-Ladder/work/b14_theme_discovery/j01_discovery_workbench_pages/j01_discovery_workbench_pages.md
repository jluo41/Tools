# j01 · The discovery pages, level by level

goal: the discovery theme's three pages on the focus page, each in its three sections: Block, Job and Task × Report, Work and Studio
close: all nine sNN are agreed and each names the code change for its owner (the discovery workbench server, workbench-discovery skill)
answers: Q01,Q02

## Topic

The discovery theme climbs three levels: a Block (one field of prior work, `discovery/b01_<topic>/`), a Job (one
inquiry, `j01_<inquiry>`) and a Task (one sub-question, `t01_<question>`), whose hard Runs are one per paper
(`r01_<author><year>_<subject>`: a Result Card, facts, a receipt, one BibTeX entry), beside its collection Runs and
the Run that builds and hands over the Evidence Bib. Every page has three sections with three aims: Report checks,
Work does, Studio thinks. So the design is the same 3 × 3 grid as the paper's (b16 j01), labeling's (b15 j01),
insight's (b11 j01) and work's (b17 j03): one Task per level, and in each Task one sNN per section.

```text
                 Report · check    Work · do    Studio · think
t01 Block        s51               s52          s53
t02 Job          s54               s55          s56
t03 Task         s57               s58          s59
```

The numbers are the siblings' (s51 to s59), so the same number names the same cell in every theme Block. All nine
are drawn by `discovery_ui_cells.py`, copied from b17's `work_ui_cells.py` and b11's `insight_ui_cells.py`: every
view is the same full screen, lettered A, B, C, settled one letter per round; Report and Work of one page share
letters; each new screen carries its dated green ✎ note.

The screens are drawn from the live discovery pages (261108) on the theme's public example, `discovery/b01_example_prior_work`
(three made-up papers, `j01_policy_effect_inquiry`, `t01_policy_prior_work`): the Block and the Job read MindMap ·
Status · Findings, the Task MindMap · Status; Findings and the Task's Status hold the discovery sections, 📚 Papers
(one side tab a paper, its Card), 📖 Evidence Bib (the entries, then the BibTeX) and 🧾 Synthesis (the topic summary);
Work repeats each view, ⚙️ Process first when it has a step, then 📊 Results. Tools is public: every name is a placeholder.

The "before" every screen replaces is the old Discovery workbench (b14 s02): four Spaces at Block level only (Scope ·
Work · Check · Delivery), Papers and Questions under Work, Runs and Citations under Check, the Bib under Delivery.

## Tasks

<!-- in order; new_job.py task adds each -->
1. t01_block_page · The discovery Block page
2. t02_job_page · The discovery Job page
3. t03_task_page · The discovery Task page
