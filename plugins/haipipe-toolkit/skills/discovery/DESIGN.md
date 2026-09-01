# Discovery — architecture

Discovery is the durable external-evidence executor. Its unit is a research
Topic represented by one Folder with a Page Face and a Task Face.

Runtime authority lives in:

~~~text
haipipe-discovery/SKILL.md
haipipe-discovery/ref/lifecycle-map.md
haipipe-discovery/ref/paper-run-contract.md
haipipe-discovery/ref/discovery-yaml-schema.md
~~~

This file explains their relationship; when details differ, those runtime refs
win.

## Four levels

~~~text
L1 Block    discoveries/
L2 Drop     discoveries/<GROUP>/
L3 TaskPage discoveries/<GROUP>/<NN_topic>/
L4 Run      runs/<RUNNAME>.sh <-> results/<RUNNAME>/
~~~

L3 owns one Topic/question. L4 owns one canonical evidence Subject, normally
one paper. Result is the generated projection of Run, not an additional level.

## Two Faces

~~~text
Page Face                              Task Face
<topic>.md                             discovery.yaml
outline/                               scripts/ optional
evidence/bibex/<topic>.bib             runs/
topic-level synthesis                  results/
~~~

Configuration is not a Folder kind. Each workflow phase configures the Face it
owns. The manifest plans the Topic; a .sh ticket plans one Paper Run.

## Three orthogonal dimensions

~~~text
Hierarchy   Block -> Drop -> TaskPage -> Run
Lifecycle   Plan -> Build(optional) -> Execute -> Report
Type        Search | Review | Idea
~~~

Search resolves and admits evidence Subjects. Review synthesizes completed
Results. Idea generates at Topic level and uses Paper Runs for novelty
evidence. Worker/API/CLI calls are runtime detail inside a Run receipt.

## Trigger and Subject

~~~text
Trigger -> resolve -> canonical Subject -> numbered Run -> same-stem Result
~~~

A Trigger may be a paper URL, short link, social post, DOI, PDF, citation, or
request. It explains why work started. The canonical Subject owns RUNNAME and
the Bib entry. One Trigger may fan out to many Subjects; one Run never bundles
multiple papers.

## Evidence authority

Each complete Result owns:

~~~text
<RUNNAME>.md
facts.md
runtime.yaml
<RUNNAME>.bib   exactly one authoritative entry
~~~

PDF, raw extraction, and captured Trigger are optional. Result Card cite key
and Bib key are identical. The Page Evidence Bib is a deterministic derived
union of complete Result Bibs; conflicts hard-fail.

## Synthesis

Topic Content and Paper Results are many-to-many. A paper may support several
divisions, and a division normally synthesizes several papers. The Page links
to Results; it does not copy their entire readouts into a flat notes ledger.

## Compatibility

Existing sources.md and notes.md remain readable as legacy/derived indexes.
They are not the authority for new evidence. Old prose is not mass-converted:
a paper earns a Result only when canonical identity and authoritative BibTeX
can be verified.
