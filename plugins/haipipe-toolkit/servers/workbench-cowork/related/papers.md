Related papers
==============

The papers behind the CoWork Workbench's methods (`../guide/method.md`): a Block bounded as one
topic with its gate, one Job for each request, a message drafted inside a checklist step,
the wait named with its date, meetings kept as dated notes (Scope, Job and Record
methods); and the answer written from the Block's own files, then checked by an agent that
did not write it (Report methods). How a Question is asked and reviewed belongs to the
question skills (`skills/1_base/question/`). Guide › Related Paper shows this file; each `group` is
one method card, so a card lists its own papers.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper or article.
`group` is the method card it supports (a row serving two cards names both, split by `;`).
`role` is `classic`, `review`, `evidence` or `practice` (a guideline, documentation or
engineering article); `key` is ★ for the ones that card rests on most; `doi` is the DOI;
`pdf` is empty (no full text is kept here). Kept to the most relevant, general rather than
about one study. Every row has a DOI, checked with `check_papers_table.py --online` on
2026-10-04. The findings in `why here` were read from the abstracts only, except Harris et
al. 2009, whose record has no abstract: only its title was read. Panickssery et al. 2024 is
copied from `task-papers.md`.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| by one topic; by one job per request | classic | ★ | Malone & Crowston 1994 · The interdisciplinary study of coordination | ACM Computing Surveys | 10.1145/174666.174668 | coordination is managing dependencies among activities: a Block names its gate, a job page names who we wait on |  |
| by one job per request | practice | ★ | Harris, Taylor, Thielke et al. 2009 · Research electronic data capture (REDCap): a metadata-driven methodology and workflow process for providing translational research informatics support | Journal of Biomedical Informatics | 10.1016/j.jbi.2008.08.010 | research informatics support for clinical studies as a workflow process: the kind of office a Job's request goes to |  |
| by checklist draft | evidence | ★ | Haynes, Weiser, Berry et al. 2009 · A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population | New England Journal of Medicine | 10.1056/NEJMsa0810119 | a checklist built to improve team communication reduced complications and deaths in eight hospitals: a request keeps its steps in order |  |
| by named wait | evidence | ★ | Herbsleb & Mockus 2003 · An empirical study of speed and communication in globally distributed software development | IEEE Transactions on Software Engineering | 10.1109/TSE.2003.1205177 | work across sites took about two and one half times as long, tied to the number of people involved: each wait is named with its date |  |
| by dated record | review | ★ | Hall, Vogel, Huang et al. 2018 · The science of team science: A review of the empirical evidence and research gaps on collaboration in science | American Psychologist | 10.1037/amp0000319 | collaboration across organizations needs structures and policies that lag demand: a dated record is one we can keep ourselves |  |
| by report from block files | practice | ★ | Wilson, Bryan, Cranston et al. 2017 · Good enough practices in scientific computing | PLOS Computational Biology | 10.1371/journal.pcbi.1005510 | write down what was done and keep inputs, work and outputs apart: a report cites the Block file each claim came from |  |
| by independent review | evidence | ★ | Panickssery, Bowman & Feng 2024 · LLM evaluators recognize and favor their own generations | arXiv | 10.48550/arXiv.2404.13076 | T2, T7: a model evaluator scores its own outputs higher than others that human raters judge equal: the writer of a draft or a report never reviews it |  |
