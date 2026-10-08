---
name: table-papers
description: >-
  Write, check and show a workbench's Related Paper table: one row per paper or article
  the workbench builds on, in eight columns (group · role · key · paper · venue · doi ·
  why here · pdf), kept beside the workbench's skill and shown by the shared Related Paper
  cards in Guide › Related Paper. Use to start a workbench's papers, to add or trim
  papers, to check every DOI against OpenAlex, Crossref and DataCite, or to keep a full
  text only under an open license. Trigger: related paper, related papers, papers table,
  table papers, add a paper to the workbench, check the papers, /table-papers.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-03"
  # version history: ./CHANGELOG.md
---

# /table-papers · group · role · key · paper · venue · doi · why here · pdf

A **Related Paper table** is the list of papers a workbench builds on, kept as data
beside its skill and shown the same way on every workbench (JL 261003: "this is the rule
and should be shared"). The first two were the Design and Insight workbenches'; this
skill writes their shared rule down.

```text
group      the part of the workbench the paper supports (a method, a View, a rule);
           `a; b` when it serves two: it shows once, under the first
role       classic · review · evidence · practice (a guideline, documentation or
           engineering article rather than a peer-reviewed study)
key        ★ for the papers that group rests on most, else empty
paper      `Authors Year · Title`: one name, `A & B`, or `A, B, C et al.`;
           a standard as `ISO 9241-210:2019 · ...`; an undated page as `n.d.`
venue      the journal, proceedings, publisher or site
doi        the bare DOI (10.xxxx/...), or the https page of a work with none;
           empty only for a print-only book or report
why here   one line: what the paper gives this workbench
pdf        `papers/<file>.pdf` only when its license lets it be kept, else empty
```


Rules
-----

1. **One file, one table.** `skills/<family>/workbench-<name>/ref/<name>-papers.md`
   holds exactly one table with the eight columns in that order. Prose before it says
   what the papers are for, when they were checked, and against what. A workbench whose
   Guide is drawn by level (Block · Job · Task) leads the table with a ninth column,
   `level`: `Block`, `Job`, `Task` or `all`, several split by `;`, the levels the paper's
   method serves; Guide › Related Paper then shows each paper under those levels.
2. **Every row is checked.** A DOI is looked up before the row goes in
   (`--online`: OpenAlex, Crossref and DataCite; one registry can be wrong). A page
   without a DOI is fetched for its title, author and date. A finding in `why here` read
   in the abstract only says so in the prose.
3. **At least one ★ per group.** The view shows a group's key papers and folds the rest
   under "N more papers"; a group with no ★ shows all, and the check warns.
4. **A full text only under an open license.** A `pdf` file sits in `ref/papers/` and is
   listed with its license in `ref/papers/README.md` (CC BY or another license that lets
   it be shared). Any other paper links to its publisher.
5. **General, not one board.** Papers about one dataset, channel or board belong with that
   board's own work, not in the workbench's table.
6. **Most relevant and most recent.** Keep the papers a person needs to see why the
   workbench is built this way; drop the older or less direct ones rather than letting
   the list grow.
7. **Adding a paper is a Discovery run.** The Workbench Table's `Add a paper` row is done by
   `haipipe-discovery-orchestrator-agent` with `haipipe-discovery`; its Paper Run keeps the
   Bib, abstract and free copy, and the card reads them by DOI. This skill owns only the
   table and its check.


Where it shows
--------------

The shared renderer `servers/workbench/related_papers.py` (`papers_page`) draws the
table as cards: one band per group, a head counting papers by role, journal, UTD24 and
PDF; closed, a card is the title then who · year · venue; open, why it is here, its links
(publisher or source page, the PDF, the Paper Run), the abstract and the PDF itself. A
family names its table as `papers_table` in `servers/workbench/guide_families.py`,
and Guide › Related Paper renders it; Design and Insight frame their own theory pages,
which render through the same module.


Check
-----

```bash
.venv/bin/python Tools/plugins/haipipe-toolkit/skills/0_utils/table-papers/ref/check_papers_table.py <name>-papers.md
    --online             # also look every DOI up on OpenAlex, Crossref and DataCite
    --format blocks      # print the table by group first: reads well in a terminal
```

It fails on an empty group, role, paper or why here; a role outside the four; a key that
is not ★; a paper not in `Authors Year · Title` form; a doi that is neither a DOI nor an
https page; a repeated DOI; a pdf missing on disk or missing from `papers/README.md`; and,
online, a DOI no registry knows or whose record has another title or year. A group with
no ★ is a warning.


Boundary
--------

This skill owns the table's shape, its check and the shared Related Paper cards. It does
not search for papers (`haipipe-discovery` does) and does not change a workbench's code;
the owning workbench skill names its table and reruns the check.
