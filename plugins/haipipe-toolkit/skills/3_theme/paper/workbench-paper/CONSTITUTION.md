# Paper workbench constitution

These current rules govern the Paper reader. The shared `hai-ui/CONSTITUTION.md`
governs page words, navigation, marks and layout. Source reports and verification
are in `ref/topics.md`; design history is retained in the Blueprint Trace.

## A01 · Delivery items name their artifacts

Every Delivery item uses its full artifact name, such as Paper-Latex,
Paper-Latex-Diff, Paper-Word, Paper-Word-Tracked, Supplement-Latex,
Supplement-Word, Combined-Latex, Cover-Letter and Portal. A generic label must not
hide which file a reader opens.

Guard: `servers/workbench-paper/tests/test_delivery_item_names.py`.

## A02 · Keep the source Idea Job

A Paper developed from an Idea Job links to that source and the reviewed human
selection. The source owns scientific evaluation and its revisions. The Paper
projects the selected source; it does not create a second scientific Card or
move the source Job into the manuscript.

Contract: [source adapter](../hai-paper-ideation/ref/idea-job-source.md).
Guard: ideation `tests/test_idea_job_selection.py`. A dedicated Idea example and
any origin-file UI controls need their own live-page verification.

## A03 · Separate groups, types and names

Paper and Grant structure design groups work as Story, Evidence, Display,
Writing and Presentation. Idea groups candidate Jobs and their `ideation`
assessment Tasks. A group organizes selection; a type defines a work contract;
a name identifies an instance. Neither a version nor a writing step creates a
type. A changing name uses `〈 〉`; an agreed name does not.

Story and Evidence are shared Jobs in the target structure. Main, Appendix and
Explore are Display roles. Review and Submission belong inside Writing. Story
headings are content, not automatically Tasks. Read the owning skill and real
face before mapping a type; a drawing never registers a type or migrates records.

Guard: b16 `delivery/page-spec/check_block_structures.py` and the owning record
checks. Contract gaps remain explicit in `ref/topics.md` T07.

## A04 · Structure follows S71's folder tree

Every Block Structure instance's Structure view presents Folder, Job-Task and
Studio as folder-style trees, using b17's shared tree renderer. Folder opens to
the Job and puts folders before files. Job-Task has at most four levels: Job
group → Job name → Task group → Task name. Each level uses the common S71 colour
in light and dark modes. A Job without Tasks ends at the Job.

Each row's purpose appears on hover. Keep names short and show the level beside
each Job-Task name. Structure and Draw derive their names and parentage from the
same authored outlines. Preserve human-authored drawings. Structure must not
bind a focus-map route or render mind-map cards.

Guard: b16 `check_block_structures.py` checks active tree bindings, every source
row and parent, level classes, hover text, default expansion and common palette;
it also checks every Draw node's name and parent against Structure.
Execution and example gaps are tracked separately from Studio conformance.

## A05 · Share Studio Bands and embed real examples

Every Blueprint reads Band names and order from Work's shared `studio_types` and
its type topics. Each topic remains an independent fold. Themes supply their
own Block/Job/Task types and Studio content; they do not define another Band
catalog or add empty topics to fill it.

Each Idea, Grant and Paper structure topic instantiates b17's Block Structure
Studio Type. Its current views and element requirements are the common source;
the theme supplies content. Structure has Folder, Job-Task and Studio. Job types
and Task types come from the topic's four `types.md` lists, each with `for:` and
`holds:`. Draw opens one canvas; Structure uses the shared folder tree.
Examples appears only for a verified Block; Skills opens real owner files.
Examples reads Folder, Jobs and Studio through the existing live Block routes.
Generated inventories are reference snapshots. Type-member links select the
member inside its Block, with the Job and Task selection parameters.

The Studio model inside Structure describes the research Block's own Band names,
number ranges and topic types. It is not a copy of the Blueprint Band registry.
Use 〈 〉 for proposed names. A semantic design catalog does not register an
executor or silently rewrite research records.

Guard: b16 `check_block_structures.py` reads b17's view contract, requires every
catalog, validates source bindings and generated pages, and checks actual example
inventories. Zero discovered catalogs is a failure. Verify each live Studio and
invoke the changed skill from a fresh context before closing the topic.
