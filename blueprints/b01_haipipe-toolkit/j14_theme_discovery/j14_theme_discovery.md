# j14 · Theme: discovery

job-of: b01_haipipe-toolkit (the Block `b14_theme_discovery` until 261009; its questions, studio and runs moved with it)
spine: Design questions about the discovery Theme as one ladder: what a Discovery Block, an inquiry Job, a sub-question Task and a Paper Run each hold and show, where papers, citations and the Bib appear at each level, and how a synthesis is handed to the paper or task that reads it.
close: Each recorded question has a report Page with an answer status, and every answered question names the skill, workbench or builder change that settled it.

## Topic

The discovery Theme reads outside evidence: it finds papers and sources, reviews each one
through a numbered Paper Run (`rNN_<author><year>_<subject>/`: a Result Card, facts, a runtime
receipt, one BibTeX entry), and synthesizes them into a topic article. Its Block holds inquiry
Jobs; an inquiry's Tasks are sub-questions, each a Page with its Paper Runs.

Today the Discovery workbench shows it at Block level in four Spaces (Scope · Work · Check ·
Delivery): Papers, Tasks and Questions are Views of Work; Runs, Citations and Reports are Views
of Check; Reports and BibTeX are Views of Delivery.

The shared ladder (b03) gives every level the same six Spaces: Description · Idea Studio ·
Audience Report | Work Details | Runs · Delivery. This Block asks how discovery fits that ladder level
by level, and what it needs that no other Theme has.

Most answers here are a change to the discovery skills (`2_theme/discovery/haipipe-discovery`, `-inquiry`, `-review`, `-synthesize`, `workbench-discovery`), the Discovery workbench
server, or b03's shared builder, not a Task Run. A Question may have no work entries; its report
links the changed files and the drawings.

Excluded: the ladder itself and what every Theme shares (b03_project_workbench); the paper that cites a
synthesis (b16_theme_paper).

## Pipeline

```text
chat section -> Related question -> haipipe-question -> skill, workbench or builder change -> report Page
                                                     -> studio/ drawings (shared by the questions)
```

## Pages

No Jobs yet. The studio holds the theme's drawings, one topic each, each beside the script that
draws it (261007: the servers hold code only):

```text
studio/
├── s01-discovery-ladder/     the discovery ladder: Block · Job · Task · Run, proposed and today (Q01)
├── s02-discovery-workbench/  the Discovery workbench as built today (Guide › RoadMap Draw)
└── s32-discovery-element-ui/ every element the theme draws, today, old and planned, with its proposed look
```

s01's rows come from b03's shared definitions (`b03_project_workbench/studio/s01-overall-tree-structure/`);
its own builder draws the overview and the Run frame, and b03's `studio/_build/make.sh` rebuilds it.
s02 is drawn from the theme's `workbench-discovery/ref/workbench-table.md` by its own script.

## Questions

```yaml
questions:
- id: Q01
  title: How does an inquiry climb the ladder?
  question: What do the Discovery Block, an inquiry Job, a sub-question Task and a Paper Run each
    hold and show on screen, and which of today's Discovery Views moves to which level?
  hypothesis: The Block keeps the inquiries and their Questions; a Job is one inquiry with the six
    Spaces, Work Details = its sub-question Tasks; a Task is one Page whose Work Details = its papers;
    a Paper Run is hard, one per source.
  acceptance: Answered when every level names its folder, its six Spaces' content and the today View
    it replaces, drawn in studio/.
  work: []
  report: reports/q01_discovery_ladder/q01_discovery_ladder.md
- id: Q02
  title: Where do papers, citations and the Bib show?
  question: Where do the papers read, a citation still waiting on a person, and the derived Evidence
    Bib appear at each level, once there is no Check Space?
  hypothesis: Papers are the Task's Work Details, grouped by role; a citation waiting on a person
    is a chip on its paper row; the Bib is a Delivery item at Task level, merged at Job and Block.
  acceptance: Answered when each of today's Work, Check and Delivery Views has a place in the six
    Spaces.
  work: []
  report: reports/q02_papers_citations_bib/q02_papers_citations_bib.md
- id: Q03
  title: How is a synthesis handed on?
  question: How does a Task's synthesis reach the paper Section or work Task that reads it, and where
    does that link show on both sides?
  hypothesis: 'By exact identity: the reader names the synthesis Result; the Discovery Task''s Delivery
    lists who reads it; no copy crosses.'
  acceptance: Answered when the handoff path is written for a paper reader and a task reader.
  work: []
  report: reports/q03_synthesis_handoff/q03_synthesis_handoff.md
```

## Related resources

```yaml
resources:
- title: haipipe-discovery skill (the Discovery door, Paper Runs)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/discovery/haipipe-discovery
  questions:
  - Q01
  - Q02
  - Q03
- title: workbench-discovery skill (the Discovery workbench)
  url: https://github.com/jluo41/Tools/tree/main/plugins/haipipe-toolkit/skills/2_theme/discovery/workbench-discovery
  questions:
  - Q01
  - Q02
  - Q03
```
