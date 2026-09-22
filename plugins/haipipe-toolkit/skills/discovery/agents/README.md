# Discovery agents

The agents execute the contract owned by haipipe-discovery. They do not define
an alternate folder shape. A Block is a live Discovery Board from its first
durable write; a Task Folder is the Page Folder rendered inside that Board.
Use `haipipe-discovery/scripts/board_sync.py` at structural and handoff
checkpoints. The Board engine builds `board/`; no agent edits generated files.

The three live capability skills sit flat at the family root:
`haipipe-discovery-search` resolves candidates, `haipipe-discovery-review`
inspects one source/Result, and `haipipe-discovery-synthesize` combines accepted
Results. The numbered `1_search/` and `2_review/` folders hold only the vendored
originals those skills may call. None of this is an agent stage or a D1 phase.
Agents dispatch into the live skills while D1 remains the sole Discovery
workflow phase.

If a legacy description uses 0/1/2/3 or 1/2/3/4 as if those were folders, use
`../haipipe-discovery/ref/bjtr-alignment.md`. The project address is always
Block -> Job -> Task Page -> Run; skill-family and Page-phase numbers stay
orthogonal.

~~~text
discoveries/ -> bNN_ Block -> jNN_ Job -> tNN_ Task Page -> rNN_ Run
compact address: bNNjNNtNNrNN
~~~

## Roster

| Agent | Owns | Never owns |
|---|---|---|
| orchestrator | FULL/ENRICH routing, dispatch, final state | paper search details |
| creator | D1 Task/Run/Result writes; Page writes only under the current Page phase | reviewing its own work |
| reviewer | Plan/Run/Bib/Report gates | searching or creating evidence |
| search worker | one read-only channel/verification batch | relevance, Runs, writes |

## Flow

~~~text
D1 SCOPE       creator -> reviewer                         Board head present
D1 PREPARE     creator -> reviewer                         optional
D1 ACQUIRE     creator resolves Trigger -> one Run/Result pair per Subject
D1 SYNTHESIZE  Bib builder -> shared Page workflow -> reviewer
Page CHECK     fresh Page checker
D1 CLOSE       creator reconciles Task Face -> Board build/check -> reviewer
~~~

`discovery_type` chooses the root article form; Search, Review, and Synthesize
are the live specialist routes. Semantic ideation uses the separate
`haipipe-ideation` skill after Discovery synthesis; Discovery has no Idea route.
Only D1 ACQUIRE creates local Runs, one for each admitted canonical Subject.
SCOPE, PREPARE, SYNTHESIZE, shared Page Workflow Steps, and CLOSE do not create Runs in the
D1 root Folder.

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

Questions are handled through the ordinary Discovery Run/Result path. A consumer
never writes into the Discovery bank: it records Supporting Run ids and owns any
Local Run/Result needed for a focal Page Evidence Item. There is no separate
answer-bank side door or folder.

Board source is deliberately small: `board.md` declares the Block identity,
spine, close condition, Pipeline, map, and managed Job headings. The direct
`jNN_/tNN_` tree supplies membership and Task order. Do not paste Task state,
Result prose, or Run inventories into the Board source.
