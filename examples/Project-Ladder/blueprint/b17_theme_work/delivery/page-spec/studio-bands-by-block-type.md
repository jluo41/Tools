# Studio bands by Block type

The Work theme defines five Block types: Work, Blueprint, CoWork, Discovery and Knowledge.
A Band is a fixed content group. A Studio topic is named for a question in the actual work. Names in 〈 〉 below
are illustrative slots, not existing work records or mandatory Studio types. Create a topic only when its question
exists; omit empty Bands in actual work. Bands add no directory layer and do not renumber existing topics.

## Content bands

The English labels are the page labels; the Chinese labels explain the same groups.
Knowledge uses the agreed display names Resource / Method / Application / Question, in that order.

| Block | Band | 中文 | Purpose |
|---|---|---|---|
| Work | Work Design | 工作设计 | Discuss the problem, boundaries and choice of approach. |
| Work | Implementation Design | 实现设计 | Design how the work will run and how its outputs will be presented. |
| Work | Results Discussion | 结果讨论 | Interpret results and decide what needs improvement. |
| CoWork | Collaboration Planning | 协作安排 | Agree on the shared goal, responsibilities and collaboration conditions. |
| CoWork | Materials Review | 材料讨论 | Discuss application materials and communication drafts; formal messages remain in Delivery. |
| CoWork | Handoff Review | 交付确认 | Discuss recipient feedback and the acceptance and handoff arrangements. |
| Discovery | Question Design | 问题设计 | Set the question, scope and criteria for evaluating evidence. |
| Discovery | Evidence Discussion | 证据讨论 | Discuss reliability and disagreement; source reading belongs to execution work. |
| Discovery | Synthesis | 综合解释 | Interpret what the evidence supports and what remains unresolved. |
| Knowledge | Resource | 学习资源 | Prepare and locate the materials used for learning. |
| Knowledge | Method | 方法 | Explain what a thing is and how it works, as numbered steps a learner follows. |
| Knowledge | Application | 应用 | Use the methods on practical problems and name their limits. |
| Knowledge | Question | 提问 | Keep the questions that come up while learning, each answered in its own topic. |

## Blueprint

Blueprint uses `studio-bands.json` in this directory as its single registry, including its order.
Consecutive numbered ranges sharing one label (Skills) form one displayed group. Its map shows the allowed
organization; actual Blueprint pages omit groups with no topics. Shared types are referenced; a theme defines
only additional types it needs. Task Procedure and Guide content do not require separate same-named type topics.

## Ownership and execution

- Work Studio discusses work choices; Jobs and Tasks implement and execute them.
- CoWork Studio discusses arrangements, materials and acceptance; formal messages and accepted outputs remain in Delivery.
- Discovery Studio discusses questions and evidence; source searches and readings stay in their execution records.
- Knowledge Studio explains concepts, methods and their applications. Pure conceptual learning need not have a code Job;
  one practice Job may support several knowledge topics.
- These Band labels are content categories, not execution stages or a required sequence of work.

## Knowledge Resources Band

Resources is the first Studio Band of a Work Block (Knowledge), followed by
Methods, Applications and Questions. Their numbered ranges
are s0N, s1N and s2N (both Methods), s3N and s4N. Bands add no folders and do not renumber existing topics.
Resource-related Studio topics belong directly in Resources. There is no required
same-named Resources or Knowledge Sources Studio, and no separate Sources view.

A resource entry identifies its original source, link, applicable version and precise
chapter/page/video time, together with the knowledge topics or practices it supports.
Each knowledge topic references that same source record. A source does not automatically
become a separate Studio. Reuse Related records and Discovery results without maintaining
another bibliography or copying evidence analyses. Unknown locations remain unknown.

The [Knowledge structure](../../s05-knowledge-structure/s05-knowledge-structure.md)
defines the organization. The A2UI Block demonstrates actual English Studio topics in these four Bands.
Its example link opens Studio; Report summaries do not substitute for learning topics.
Practice records are created only when their execution contract and inputs are ready.

## Structure bindings and checks

S01–S04 render Structure → Studio with the existing collapsible Folder Tree: Block → Band → 〈Studio topic〉.
The root opens initially; each Band expands to its topic slots. The authored organization records supply content
only; their file format does not choose the UI renderer. Draw retains the existing hand-edited drawing.
No folder is created by the displayed grouping.

Run `delivery/structure/check_studio_bands.py` to verify Band content, tree markup and manifest destinations.
The guard rejects a Structure → Studio binding to the mindmap viewer and preserves the original Draw entry.
