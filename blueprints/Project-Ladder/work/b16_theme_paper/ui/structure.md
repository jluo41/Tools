Paper Board · Current structure

**Report → Review Content → Around the Work**. The seven views organize the paper's content and actions. The right rail gathers the Board and its descendants.

## 🪜 Paper ladder

| Level | Owns | Current interface |
| --- | --- | --- |
| Paper Board | Ideas, Story, plans, shared evidence and writing versions. | Seven Report views with eight shared sections. |
| Evidence Job | Displays, values or citations reused across versions. | Its specialized Report and Work views. |
| Writing version | One manuscript version, its Sections and review responses. | Version-specific Report and Work views. |
| Submission Job | One version's cover letter and portal preparation. | Submission-specific Report and Work views. |
| Section Task | A section, abstract or letter and its draft lifecycle. | The shared Page draft workflow. |

The Board frame is implemented. Applying the same frame to Version and Section pages remains a separate design step.

## 💡 Idea

| Section | Content | Layout |
| --- | --- | --- |
| 🔀 Directions | Candidate directions, comparison and the recorded selection. | Left Tabs · Right Content → Direction |
| 🎓 Theory | The theoretical basis of each direction. | Left Tabs · Right Content → Notes |
| 📌 Open points | Recorded unresolved points. | Action rows |

Before a Story exists, Direction and Related can also appear here. The chosen telling belongs to Story.

## 📖 Story

| Section | Content | Layout |
| --- | --- | --- |
| 🧭 Direction | The chosen direction. | Paragraph |
| 💡 Pitch | The paper's claim and why it matters. | Paragraph |
| 🎓 Theory | The theory being tested or extended. | Paragraph |
| ❓ Research Questions | Each question and its narrative. | Left Tabs · Right Content → Question |
| ⚖️ Stakes and evidence | Why the answer matters and what supports it. | Left Tabs · Right Content → Notes |
| 📚 Related | Related papers grouped by the questions they bear on. | Left Tabs · Right Content → Paper |
| 🏛️ Venues | Target venues and their fit. | Left Tabs · Right Content → Venue |
| 🧠 Story by Section | Claims placed in reader order. | Diagram |
| 📌 Open points | Unresolved Story choices. | Action rows |

Studio appears once under Around the Work, with the Topic's drawing and mind map.

## 🗺️ Data + Paper Plan

| Section | Content | Layout |
| --- | --- | --- |
| 🗄️ Data flow | How inputs become the evidence needed for the questions. | MindMap / Diagram |
| 📝 Paper flow | Sections in reader order and the path to a send. | MindMap / Diagram |
| 🗺️ Roadmaps | Planned discovery and analysis work. | Left Tabs · Right Content → Table |
| 🧭 Plan | Dataset, analysis, execution, displays and reading actions. | Action rows → Open / Copy prompt |
| ⚙️ Runs to do | The Run work named in the roadmap. | Action rows |
| 🗓️ Next steps to the send | Recorded steps and dates for the submission. | Action rows |

Opening or copying a prompt does not start a Run or approve a submission.

## 🧩 Support blocks

| Section | Content | Layout |
| --- | --- | --- |
| 🧪 Work | Internal analysis work named by the paper. | Expandable Project → Block → Job → Task → Run tree |
| 🔎 Discovery | External literature work named by the paper. | Expandable Project → Block → Job → Task → Run tree |

Entries open their real pages in a pop-out. These trees reference existing work; they do not create another execution hierarchy.

## 🔢 Evidence

| Section | Content | Layout |
| --- | --- | --- |
| 🔢 Values | Numbers from returned results and their provenance. | Left Tabs · Right Content → Table |
| 📚 Citations | Citation groups and verification records. | Left Tabs · Right Content → Source evidence |

Evidence belongs to the Board and can support multiple writing versions.

## 🖼️ Displays

| Section | Content | Layout |
| --- | --- | --- |
| 📐 Plan | Display design and venue constraints. | Diagram |
| 🖼️ Displays | Main, supplement and other figures or tables. | Left Tabs · Right Content → PDF preview |
| 🔍 Examples | Reference displays from the intended venue. | Diagram / Preview |
| 🧠 Story by Section | The Story view's own section: claims placed in reader order. | Diagram |

## ✍️ Writing

| Section | Content | Layout |
| --- | --- | --- |
| ✍️ Version sections | A section per writing version, titled with its actual name. | Left Tabs · Right Content → Draft section |
| 📄 The assembled paper | The version's built manuscript, when present. | Preview |
| 📮 Ready for the portal | Submission outputs, when present. | Preview / File links |
| 🪜 Sections to finish | Each Section's draft steps and recorded state. | Action rows → Draft step |

The **Delivery** rail entry also opens the assembled outputs. A generated file does not by itself mean the manuscript is accepted or ready to submit.

## 🧭 Around the Work

These sections have the same names, order and renderers as Work, without numbering.

| Section | Content | Layout |
| --- | --- | --- |
| 🎨 Studio | Linked design Topics and their assets. | Left Tabs · Right Content → Drawing / Preview |
| 🙋 Interactions | Topic questions, feedback and confirmation forms. | Left Tabs · Right Content → Questions |
| ⚖️ Decisions | Recorded choices and reasons. | Left Tabs · Right Content → Records |
| 📚 Things to Know | Relevant background and constraints. | Left Tabs · Right Content → Notes |
| 📝 Checklist | Checks recorded in the selected source. | Checklist |
| 🕒 Timeline | Dated events with source links. | Chronological list |
| 🧰 Skills | Skills supporting the view and selected work. | Left Tabs · Right Content → Skill details |
| 📁 Files | Related source directories and files. | Left Folder Types · Right Folder Tree → Pop-out |

**Inside a View:** explicit View assignment takes priority, then the linked Topic. Unassigned records remain in the right rail.

**Right rail:** the Board and its descendants across views. Both entrances read the same original records. Skills and Files use the same selection as the other six sections.

## 🔁 Review loop

Manuscript or display → Feedback → Evidence and Story review → Studio → Decision → Plan and affected Sections → Revised output.

Feedback keeps its Topic and version context. Decisions record what was adopted; draft and build records show what changed.

## 📋 Job and Task matrices

The Job matrix uses the current renderer branches: Writing Version, Display Evidence, Value Evidence, Citation Evidence and Submission. Initial and revised versions share Writing Version. Their purposes and examples appear in Use Cases.

The Task matrix separates the draft workflow from the display, values, tables, citations, submission-letter, portal-walk and portal-fill presentation branches. Manuscript Sections, abstracts, cover letters and reviewer responses are uses of Draft; group checks and whole-paper audits are uses of their evidence branch. These presentation branches are not a new persisted Task-type enumeration.

Source: `paper_jobs.job_kind` and `VIEWS`; `paper_version.version_report_views`; `paper_tasks.kind_of`; `focus_draft.report_views`, `work_views` and `reply_board`. Value Tables is selected from returned `tables.json` when `values.yaml` is absent. Reviewer-response content is selected by `responds-to`.

Use Cases opens source-backed project pages grouped by SPACE, followed by Blueprint examples. Each example exposes its actual Block, Job and Tasks when present, plus a collapsible Path. Cross-SPACE locations stay in the local ignored configuration; public definitions contain only Blueprint paths. Reviewer response and whole-paper value audit currently have Blueprint examples only.

The matrices describe current views and conditional sections. Job and Task pages retain their specialized Report / Work structure; these examples do not prove shared-frame migration or deployment to other SPACEs. Draft Display is conditional; the generic Draft example omits a link when that view does not exist.

## Grant Board · Proposed

Grant Board is a Board type within the Paper theme, alongside the manuscript-oriented Paper Board. Both use the Paper family’s planning, evidence, writing versions, review and assembly structure. One Board coordinates a funding application across its call, aims, research plan, supporting evidence, team, budget and submission versions. Initial application, resubmission and renewal are Use Cases. They do not imply separate renderer types.

Grant uses the shared Idea, Story and Data + Paper Plan Views, including their Sections. In this context, Venues refers to the funding program or call, and Paper flow maps the application narrative. Opportunity supplies the target requirements, Aims supplies the proposed aims, and Research Plan supplies the approach and milestones; the shared narrative and planning Views link these together. Support blocks, Evidence, Displays, Team & Budget, Writing and Submission complete the proposed Views. The eight Around the Work sections keep their shared scope and order. Grant-specific rows extend that shared structure; they have no implemented view routes yet.

This is a proposed contract, not a working Grant page. Grant-specific behavior, an example Board and the mapping to existing Paper skills and Job/Task contracts remain to be designed and implemented. This does not introduce a separate Grant theme or skill family. No Paper example is presented as a Grant implementation.

Related is shared by Idea and Story. Story by Section is shared by Story and Displays. These are two entry points to the same source content, not separately maintained copies. The Paper renderer follows this placement; the Grant design uses the same arrangement.
