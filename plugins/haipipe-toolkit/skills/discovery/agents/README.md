# Discovery agents

The agents execute the contract owned by haipipe-discovery. They do not define
an alternate folder shape.

The numbered `1_search`, `2_review`, and `3_idea` directories are skill-family
groups, matching the organization of `haipipe-task`; they are not agent stages
or D1 phases. Agents dispatch into those families while D1 remains the sole
Discovery workflow phase.

~~~text
discoveries/ -> bNN_ Block -> jNN_ Job -> tNN_ Task Page -> rNN_ Run
compact address: bNNjNNtNNrNN
~~~

## Roster

| Agent | Owns | Never owns |
|---|---|---|
| orchestrator | QA/FULL/ENRICH routing, dispatch, final state | paper search details |
| creator | D1 Task/Run/Result writes; Page writes only under the current Page phase | reviewing its own work |
| reviewer | Plan/Run/Bib/Report gates | searching or creating evidence |
| search worker | one read-only channel/verification batch | relevance, Runs, writes |

## Flow

~~~text
D1 SCOPE       creator -> reviewer
D1 PREPARE     creator -> reviewer                         optional
D1 ACQUIRE     creator resolves Trigger -> one Run/Result pair per Subject
D1 SYNTHESIZE  Bib builder -> shared Page workflow -> reviewer
Page CHECK     fresh Page checker
D1 CLOSE       creator reconciles Task Face -> reviewer
~~~

`discovery_type` chooses the root article form; Search, Review, and Idea are
derived specialist routes. Only D1 ACQUIRE creates local Runs, one for each
admitted canonical Subject. SCOPE, PREPARE, SYNTHESIZE, Page phases, and CLOSE
do not create Runs in the D1 root Folder.

ENRICH follows the same Level-4 law but adds the minimum new Paper Runs to an
existing Task Page. It never appends anonymous source prose.

## Truth gates

~~~text
runs/<RUNNAME>.sh <-> results/<RUNNAME>/runtime.yaml
runtime family: discovery; operation matches paper/source Subject kind
runtime address: bNN.jNN.tNN.rNN and bNNjNNtNNrNN
complete -> <RUNNAME>.md + facts.md + one-entry <RUNNAME>.bib
Card cite key == Bib key
Task Page Evidence Bib == deterministic union of complete Result Bibs
~~~

QA remains a side door governed by haipipe-discovery/fn/qa.md. A consumer never
writes into the Discovery bank.
