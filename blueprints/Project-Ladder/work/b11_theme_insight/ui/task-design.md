# Insight Task design · discussion

The Board's enduring purpose is to improve what we understand about its dataset and what we can responsibly do with that understanding. Enrich Data, Develop Questions and Review Literature/Theory are recurring activities. Each Task should be a bounded contribution to one of them, with an output that another Task can use.

This proposal does not change the current ladder: an Analysis Job is one signed plan × one frozen dataset; its Tasks are that plan's questions. Prototype Tasks prepare reusable question definitions and scripts. Hard Runs execute cuts; writing and checking use their own Runs. Creating new activity Jobs inside an Insight Board would require a separate contract and reader change.

## Activity and answer role

| Board activity | A bounded Task | Inputs | Output | Completion evidence | Current owner / placement proposal |
| --- | --- | --- | --- | --- | --- |
| Enrich Data | Add a defined measurement to the next dataset version | Current freeze, source, join definition, intended question | Versioned enrichment, dictionary and provenance; coverage/missingness comparison | Mapping and quality checks; unresolved linkage limitations recorded; existing freeze unchanged | Work data Task performs preparation; Insight meta registers the resulting freeze. Show its link in the Board. Exact enrichment Task type remains to be selected. |
| Develop Questions | Propose or revise one answerable question | Evidence gap, weak/refused answer, literature finding or user question | Proposed question, DIKW role, evidence needs, competing explanations and dependencies | Reviewer can determine what evidence would answer it; proposal accepted, revised or declined with reasons | Existing Prototype proposal → question/evidence-plan work; multiple proposals may enter one release. |
| Review Literature / Theory | Assess one mechanism or a bounded body of evidence | Named question, inclusion scope and source set | Claim–source table, theory relationship, contradictions and transfer limits | Sources checked; claims traceable; unresolved disagreement explicit; implications linked to proposals | Discovery handles retrieval/review; Insight records the relevance to its questions. A new Insight-native review Task is an alternative, not a current type. |
| Analyze | Answer one planned question on one freeze | Signed question/needs, freeze, cuts and thresholds | Results, answer, uncertainty and permitted claims | Applicable Runs and checks complete, including refusal when evidence is insufficient | Existing Insight question Task in an Analysis Job. |
| Synthesize | Resolve one higher-level question from specified evidence | Checked answers; relevant external findings with provenance | Conclusion, competing explanations, limits and next question/action | Each claim traceable; conflicting evidence addressed; review recorded | Existing K/W/X question Task where its plan fits; broader cross-Job synthesis can use a Board question/report. |

A Task may finish with “insufficient evidence” or a declined proposal. Completion means the agreed work and review are complete, not that the desired conclusion was found. “Continually improve the questions” cannot itself be a Task's completion condition.

DIKW describes the **claim**, not the activity: a literature review may inform a Knowledge claim; enriching a measurement may enable several Data and Information questions. Executive is an audience-facing synthesis of supported answers. Do not force every activity through D → I → K → W as four execution stages.

## Common Task face

| Part | Required content | Display |
| --- | --- | --- |
| Aim | One question or deliverable, scope and stop condition | One clear aim; details under the plan |
| Inputs | Exact data/plan versions, cited Tasks and source records | Linked dependencies with their real state |
| Plan | Method, evidence needs, expected artifact and review criteria | Needs table; decisions remain linked |
| Work | Runs and dependencies appropriate to the activity | Actual Run tree or source-reading work; no fabricated cut grid |
| Result | Artifact or answer, what changed and what remains uncertain | Answer first, then figure/table/document suitable to its content |
| Check | Reviewer, verdict and the evidence inspected | Source review record; no automatic acceptance from a completed Run |
| Feeds into | Next question, release proposal, data freeze or handoff | Explicit outgoing links; acceptance/signature remains with its owner |

These are semantic requirements, not a proposed new set of seven View buttons. Keep the current Answer/By cut/Across Jobs/Plan/MindMap inventory visible while deciding how new Task activities fit it. A review Task may need Sources where a compute Task has By cut; a data Task may need Changes and Validation. That specialization is still discussion.

## Where the new work lives

| Option | Benefit | Cost / compatibility | Recommendation |
| --- | --- | --- | --- |
| Board coordinates linked Work, Prototype and Discovery Tasks | Reuses current owners and preserves analysis reproducibility | Needs a Board view that shows cross-Block dependencies and returned evidence clearly | Start here. First specify the bounded Task contract and Board links. |
| Add activity Jobs inside the Insight Board | All activity appears under one Board tree | Analysis-only Job assumptions in scaffold, readers, comparison and signatures must become explicit Job-type handling | Evaluate only if cross-Block navigation proves insufficient. Do not add miscellaneous Tasks to an existing Analysis Job. |

“Review Literature” is an activity, not a permanent Job that can never close. If activity Jobs are later introduced, each Job should be a finite batch, such as “assess the evidence for mechanism A,” with its Tasks and completion criteria.

## The intelligence loop

Evidence changes → identify the gap or contradiction → choose the next useful question or data improvement → perform and check the work → update the supported conclusion → propose the next change.

The intelligence is in choosing and justifying that next step, connecting external theory to internal evidence, and revising the conclusion when evidence changes. Store the supporting sources, alternatives, uncertainty and review so the judgment is inspectable. A Board that only collects files and marks Tasks done does not yet express this loop.

For example, an apparent outcome difference may motivate a literature Task about a possible mechanism. That review may propose an additional measurement and a testable Knowledge question. Prepare the new measurement in a new freeze and review the question in a new plan. Apply the existing one-clock-per-Analysis-Job rule to compare changes in sequence. The final answer may strengthen, weaken or refuse the mechanism claim; all three are useful outcomes.

## First implementation slice

Specify one enrichment Task, one question proposal and one literature review as linked work for an existing Board. Show what each contributes, its input/output links and the current review state. Validate the loop through one Analysis Task and one synthesis answer before adding new storage types or replacing every Insight View.

This is a design recommendation. No new activity schema, Job kind, Task folder, source ingestion or execution is created by these documents.
