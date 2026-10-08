Related papers
==============

The papers behind the Shared Workbench: the rule that the agent who makes a thing never
judges it, the checkpoints where a person signs, the Space and View rows, the Guide's split
into Description and Method, and drawings generated from source. Guide › Related Paper
shows this file on `/w/shared` and on every workbench's Guide.

Shape and check: `skills/0_utils/table-papers/SKILL.md`. Each row is one paper or article.
`group` is the part of the Shared Workbench it supports; `role` is `classic`, `review`,
`evidence` or `practice` (a guideline, documentation or engineering article); `key` is ★
for the ones that part rests on most; `doi` is the DOI, or the page of a work that has
none; `pdf` is empty (no full text is kept here). Kept to the most relevant and most
recent (JL 261003). Rows with a DOI were checked with `check_papers_table.py --online` on
2026-10-03; each page was fetched for its title, author and date the same day. An
undated page writes `n.d.`.

| group | role | key | paper | venue | doi | why here | pdf |
| --- | --- | --- | --- | --- | --- | --- | --- |
| make and judge apart | evidence | ★ | Panickssery, Bowman & Feng 2024 · LLM Evaluators Recognize and Favor Their Own Generations | NeurIPS 2024 | 10.48550/arXiv.2404.13076 | models rate their own output higher, so a different agent reviews what another made |  |
| make and judge apart | practice |  | Schluntz & Zhang 2024 · Building Effective AI Agents | Anthropic Engineering | https://www.anthropic.com/engineering/building-effective-agents | one model generates and another evaluates; agents pause for a person at checkpoints |  |
| human sign-off | classic | ★ | Amershi, Weld, Vorvoreanu et al. 2019 · Guidelines for Human-AI Interaction | CHI 2019 | 10.1145/3290605.3300233 | make clear what the system can do and support efficient correction: the Description View and the Person signs column |  |
| Space and View rows | practice | ★ | Sunwall 2024 · Tabs, Used Right | Nielsen Norman Group | https://www.nngroup.com/articles/tabs-used-right/ | keep navigation tabs and in-page tabs distinct: the Space row above the View row |  |
| Guide views | practice | ★ | Procida n.d. · Diátaxis | diataxis.fr | https://diataxis.fr/ | documentation split by purpose, as Guide splits Description from Method |  |
| drawings from source | practice | ★ | Brown n.d. · Structurizr | structurizr.com | https://structurizr.com/ | many diagrams generated from one text model, as RoadMap Draw is drawn from the Workbench Table |  |
