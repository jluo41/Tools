---
name: hai-knowledge
description: "Organize learning and understanding in a Project's knowledge Blocks: bound a learning goal, develop Studio topics, and connect optional reproducible practice. Use for learning a concept or method and keeping a reusable explanation; route source evidence to Discovery and dataset conclusions to Insight."
---

# Knowledge

Help a learner explain a concept, recognize its limits and apply it where useful.
Read [CONSTITUTION.md](CONSTITUTION.md) first. Work Block (Knowledge) is the working name
for this learning contract; its final public name remains a design decision.

## Start from the learning goal

Read the Project guidance and existing Blocks. Identify what the learner wants
to understand or do, their starting point when relevant, and one concrete case.
Reuse an existing Block when its learning goal fits. Ask only for information
that changes the scope; a named example is enough to begin a proposal.

One Block holds a coherent learning goal, not a whole discipline by default.
State what a useful explanation or application would demonstrate and what lies
outside the goal. Do not impose a fixed curriculum, a quiz or a coding exercise.
Keep source claims, the learner's interpretation and unresolved questions distinct.

## Organize the learning

```text
〈Project〉/knowledge/bNN_〈learning-goal〉/
├── board.md
├── sNN-〈knowledge-question〉/
├── trace/
└── jNN_〈practice-goal〉/                  when execution is useful
    └── tNN_〈executable-unit〉/
        └── runs/rNN_〈execution〉/result/
```

This is a containment pattern, not a scaffold to fill. Create only records with
content. Preserve the owning writers' formats and numbering. Use direct sNN
folders; a knowledge theme adds no topic/ or studio/ container.

- A Studio topic develops one question or explanation through a drawing, the
  shared mindmap and conversation. Include a concrete example and a boundary or
  unresolved question when they help understanding. Small concepts are nodes
  within a topic, not automatically more topics or Tasks.
- Several Studio topics can feed one practice Job; one topic can also inform
  several Jobs. Put shared topics at the Block, and a local topic at the Job or
  Task that uses it. Link to the source explanation instead of copying it.
- A Job is an optional, bounded execution workflow with an observable close
  check. Its Tasks divide genuinely separate executable work; its Runs record
  specific executions. A check can verify an artifact or behavior, not certify
  the person's understanding.
- Concept-only learning can have Studio topics and no Jobs. Explanation,
  discussion and choosing an interpretation do not require an execution Task.

Studio's instruction to infer topics from existing Tasks applies when explaining
existing execution work; it does not require inventing Tasks for concept-only
learning. The Studio owner's artifact and delivery requirements still apply,
including its deck requirement. This skill does not waive them. If a lightweight
discussion needs a different durable topic contract, keep it as a proposal for
the Studio owner rather than silently omitting required artifacts.

Reuse related topics before splitting. Split a Block when it contains learning
goals that can be pursued and handed on independently. Follow hai-studio's
per-level limits (9 at a Block, 5 at a Job, 3 at a Task); never manufacture
child Jobs merely to evade the limit or renumber existing topics.

## Connect evidence, understanding and practice

| Need | Owner |
|---|---|
| Durable source acquisition, reading and evidence synthesis | hai-discovery |
| Learning explanation, conceptual map and application boundary | this skill with hai-studio |
| Reproducible code, data or calculation practice | shared Work record owners and applicable Task type |
| Conclusions about fixed data and question versions | hai-insight |

A short learning explanation can cite official documentation directly. A source
campaign or durable evidence bank belongs in Discovery. Consumers reference its
exact Task or Run Result and source identity; do not duplicate its source cards,
BibTeX or result authority. Reference existing Work results by their real path
and configuration, and Insight findings by their pinned versions. Creating a
learning Block does not authorize migration or rerunning those producers.

The Insight Knowledge level compares and tests analytical results. Learning a
method is a different scope; resolve by the requested outcome, not the word
"knowledge" alone.

For a practice, choose a small behavior that makes the concept visible. Declare
its inputs, outputs and checks before execution. Record whether the example uses
fixed messages, simulated data or a live model. Pin the relevant specification
and dependency versions when implementing it. Use the existing upstream renderer
when learning a UI protocol; custom application components are distinct from a
replacement workbench renderer.

Before creating execution records, resolve an allowed Job type and Task type
from their owning contracts. A practice goal is not itself a new type. If no
existing type fits, retain the practice in the Block's plan and name the missing
contract for its owner; do not invent a type or force a UI demo into an LLM
campaign or data-summary type. A learning proposal can proceed without resolving
that execution gate.

Keep the explanation linked to the practice result. A successful Run supports
the behavior it checked. The learner's explanation or explicit review supports
understanding; record neither a learning judgment nor approval by inference.
An agreed explanation is kept in the topic's delivery through its owning writer.

## Execution organization and types

The design pins four lists in S05's types.md: Job group type, Job type, Task group
type and Task type. Each entry has a purpose, required content and owning source.
Reference shared Work definitions instead of maintaining another copy.

- Job group type 〈Practice theme〉 groups independently deliverable Jobs around one
  application question. Each instance names its group and binds a jNN range on
  the Block's bands: line.
- Job types code, check and doc reference Work: build a usable artifact, deliver
  independent verification, or publish independently useful documentation. Simple
  checks can stay within the build Job; conceptual explanation stays in Studio.
- Task group types Make and Show reference Work. The Job names each actual group
  and its tNN range on its bands: line. Empty groups are omitted; these are not
  mandatory stages or additional folders.
- Task types code and display reference Work's structural definitions. Resolve
  each through hai-task/ref/types.md before creating execution records.
  The structural code definition has no matching execution route there yet.
  The display execution contract covers display-safe summary material; it is
  not an A2UI renderer. Keep unsupported practices as plans until an owner and
  compatible execution contract are established.

A complete type definition does not require every learning Block to instantiate
all groups or types. Concept-only learning can have no Jobs. Group type, group
name, member type and member name remain separate. Label simulated examples
explicitly, and read actual instance members from disk.

## Records and page

Design this Block type in the owning Work Blueprint's Studio; actual learning
belongs in a knowledge/ instance. Use
[Block Structure: Knowledge](../../../../../../examples/Project-Ladder/blueprint/b17_theme_work/s05-knowledge-structure/s05-knowledge-structure.md)
to discuss Folder, Job-Task and Studio organization. An A2UI learning topic is
an instance of content, not the place to redesign the whole Block type.

Learning Studio Bands appear in this order: Resource, Method, Question.
Their number ranges are s0N, s1N to s3N (all Method) and s4N; a concept is explained in Method as the steps that read it,
and a use case as the steps that decide it. Keep existing identifiers; a
numbered range is organization, not an extra directory. Omit empty Bands in
actual Studio views. This order provides a resource-first learning entrance;
it does not prescribe mandatory execution stages.

Each learning Band is one Studio Type, named in the singular like its Band: every topic in s2N follows the
Method type, and so on. Only a Blueprint holds Studio Types: the three live in the Work Blueprint's Studio Type
band, after the Work types and together; Block Structure: Knowledge names each Band's type in its Studio. A
type's `instances:` lists the learning topics by exact ID. The face's `bands:` line names s1N, s2N and s3N all
Method, so a topic numbered s1N or s3N keeps its ID. The three types start from hai-studio's learning base type
(`base:`): Page, Draw, Map and Slides, and Try explaining as the last Page tab; each writes only its own Page tabs
before it. Each topic names its type (`check_type`) and passes `type_follow.py check`.

Read every source before describing it. Name it `Resource 〈n〉 · 〈source〉` and show one official
picture of it, listed with its URL and license in the Resource topic's `assets/SOURCES.md`. Write
code and messages as text, never as a screenshot. Draw who does what with one example carried
through: a picture per actor, before and after or a timeline, new parts in green, one value traced
(CONSTITUTION A08 to A10). Write each Page tab as one bold line, then one item per line, each with
the emoji its meaning takes across the Block (A11).

Resource is a Band. Resource-related topics belong directly under it and take
names for their actual questions. Do not require another Resource or Knowledge
Sources Studio, a separate Sources view, or one Studio per source. A source
entry records its original URL, applicable version and exact chapter, page or
time point, and links to the knowledge topics or practices it supports.
Unknown locations remain unknown. Plan-only examples label their proposed
Studio members explicitly and show existing resource links before concept content.

Keep source information with one owner. Reuse existing Related records for
retained materials and source links, and Discovery for durable evidence analysis.
When no such record exists, a Resource topic may hold the original link and its
reading location directly in its learning notes; other topics cite that entry.
Do not create a second bibliography or an additional storage layer just to hold
these links. Follow Related's allowed kinds and fields when creating its records: book or course
labels do not add schema values, and practice links do not extend feeds to Jobs.
Keep consumer navigation in the resource topic; raise unsupported source formats
with the owning skill before creating records.

S05's Structure uses the shared collapsible Folder Tree for Folder, Job-Task and
Studio, with purposes on hover and the shared four-level Job/Task colours.
The authored structure outline supplies content; its filename does not select
the renderer. Draw keeps one canvas. Actual learning topics still follow their
own Studio artifact contract, including mindmaps where that contract requires them.
Each Block records its own changes in its own trace/; related definition and
example changes link their two traces rather than sharing one Block's history.

Use hai-block for the face, hai-studio for topics, hai-job and
hai-task for execution records, hai-run for tickets and receipts, and
hai-trace for the approved file plan. Read each owner before writing its records.

Knowledge examples use the existing task-block face and shared Work framework
(`workbench: work`); this contract adds no server kind or registry entry. The
current host may require `theme=work` in the Block entry to select that framework;
verify the face's real title and content, not merely an HTTP success code. The
Block alone owns the page. Jobs, Tasks, Runs and Studio selections remain inside
it. Reuse the top-view / left-tab / right-content controls and existing mindmap.

A Band groups topics; a Studio Type defines content requirements; a Studio is
an instance. Actual learning Blocks hold no type-definition topics. A future
Knowledge Blueprint references shared types from Work and defines only content
requirements demonstrated by learning cases. Read the shared studio-bands.json
through hai-studio; do not copy its registry or invent parallel numbering.

Proposed Studio and practice names use 〈 〉 until agreed. Keep a proposed tree
in the face as a plan; do not expose it as actual folders, runs or results.
Add interactive type examples through the shared preview mechanism when its
contract is available. A static mockup is not a verified Block entry.

## Example and validation

The first case is
[A2UI learning](../../../../../../examples/Project-Ladder/knowledge/b18_a2ui_learning/board.md).
It specifies conceptual topics and a fixed-message interaction exercise. Its
face distinguishes plans from actual work. Read it as a learning case, not as a
template that requires every subject to have those topics or any code.

Before reporting a change, check scope and references, record truthfulness, and
the owner's applicable checks. Verify the running Block before sharing its
configured Tailscale entry. A successful page load is not proof an embedded
exercise works. Validate skill changes using the repository's fresh-context
process, including a concept-only case and reuse of existing evidence or practice.

## English learning content in the actual Studio

Author labels, explanations and diagrams in English; conversational replies may use the user's language.
When asked to implement a learning Studio, create the real sNN topics with content, drawings and shared view bindings.
A proposed topic list under Report / Plan + Results does not satisfy that request.
Band order comes from the existing Studio group order and each topic's Tags; keep the board bands: ranges aligned.
The A2UI example opens section=studio and contains s01, s11, s21 and s31.
Verify that real page, including a narrow viewport; generated-file checks alone cannot establish UI acceptance.
Preserve original quoted requests in historical traces.
