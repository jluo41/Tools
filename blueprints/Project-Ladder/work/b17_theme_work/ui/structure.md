Shared focus-page structure. Specialized workflows retain their own contracts.

Report combines results and actions under **📋 Review Content**, followed by
**🧭 Around the Work**. Next steps stay with their view without a separate Process heading.
Work is no longer a separate rail entry; existing Work links open Report.

## 🧭 Overview

**What are we trying to achieve?**

| Section | Content | Layout |
| --- | --- | --- |
| 🎯 Goal | The intended outcome and boundaries. | Short paragraph |
| 📋 Requirements | What must be true, who requested it, and how it will be checked. | Table → Details |
| 🧠 MindMap | Topics and the work connected to them. | Expandable MindMap |

Overview replaces the MindMap view button. MindMap remains a section inside Overview.

**Data → Insight → Design:** Overview brings together the context and inputs. Requirements may also contain design constraints.

## 📊 Status

**How is the work moving?**

| Section | Content | Layout |
| --- | --- | --- |
| 🧩 View BJTR | Topics and their related work with its current state. | Left Tabs · Right Content → B–J–T–R |
| 🔗 Dependencies | Prerequisites, waiting conditions, and the work they affect. | Relationship Table |

Topics match Overview's MindMap. A Topic links existing work; it does not add a level to the ladder or duplicate records.

At Block level, show related Jobs → Tasks → Runs. At Job level, show Tasks → Runs with Block context. At Task level, show relevant Runs with Block and Job context.

**Illustrative topic navigation** — sample states, not live progress.

Expand a work item for its latest Run and history; open it to visit its real page.

### 🗃️ Data Readiness

**Block · Model Evaluation**

```text
Job · Prepare Data — Completed
└─ Task · Check Dataset — Completed
   └─ Latest Run · Quality Check — Passed
```

**Dependency:** Model Comparison uses the checked dataset.

### ⚖️ Model Comparison

**Block · Model Evaluation**

```text
Job · Compare Models — In progress
├─ Task · Evaluate Baseline — Completed
│  └─ Latest Run · Baseline — Completed
└─ Task · Evaluate Candidate — Running
   └─ Latest Run · Candidate — Running
```

**Dependency:** Release Preparation waits for the comparison.

### 📦 Release Preparation

**Block · Model Evaluation**

```text
Job · Prepare Release — Waiting
├─ Task · Review Comparison — Waiting
└─ Task · Package Model — Not started
```

**Dependency:** Review the comparison before packaging. No Run exists yet.


## 💡 Findings

**What did we learn, and what supports it?**

| Type | Findings |
| --- | --- |
| ⚙️ Execution | Answers, measured values, supporting evidence, and limitations. |
| 🎨 Theme Development | Design findings, UI review evidence, and remaining limitations. |
| 🤝 CoWork | Agreements, unresolved differences, and supporting communication. |
| 🔎 Discovery | Source findings, synthesis, disagreements, and evidence gaps. |

Findings carries Insight. A file can support a finding and also appear in Delivery; both reference the same artifact.

## 📦 Delivery

**What can someone receive and use?**

| Section | Content | Layout |
| --- | --- | --- |
| 📦 Deliverables | The actual outputs and their versions. | Left Tabs · Right Content → Preview |
| ✅ Acceptance | Whether an output meets its requirements and has been accepted. | Requirements Table |
| 📖 Usage | How to use the selected output and its known constraints. | Short Guide |

Models, datasets, services, maps, UI packages, handoff documents, and source collections belong here.

Acceptance links existing requirements and checks. It does not create a second Checklist.

Delivery carries the outputs of Design. Design itself also happens in Studio and in execution.

## 🔁 Feedback Loop

**Each delivery becomes input to the next design.**

1. 📦 **Delivery** — Release a usable version.
2. 🙋 **Interaction** — Collect feedback and comments on that version.
3. 💡 **Findings** — Identify what the feedback and usage evidence tell us.
4. 🎨 **Studio** — AI and people develop and compare design options.
5. ⚖️ **Decision** — Record the selected approach and its reasons.
6. 📋 **Requirements** — Update the affected requirements.
7. 📊 **Status** — Follow the linked B–J–T–R work to the next delivery.

Feedback becomes new **Data**, interpretation produces **Insight**, and the next **Design** produces another delivery. Status follows the process throughout.

AI can carry out already-authorized changes. Unresolved choices stay in Interactions; Decisions keeps the resulting records.

## 🧭 Around the Work

Every work-family view ends with these sections, in this order, **without numbering**.

| Section | Purpose | Layout |
| --- | --- | --- |
| 🎨 Studio | Develop and compare ideas and designs. | Left Tabs · Right Content → Drawing |
| 🙋 Interactions | Feedback and questions to confirm. | Left Tabs · Right Content → Topic Questions |
| ⚖️ Decisions | Recorded choices and reasons. | Left Tabs · Right Content → Topic Records |
| 📚 Things to Know | Terms, assumptions, and useful references. | Left Tabs · Right Content → Notes |
| 📝 Checklist | Checks and actions still needed. | Checklist |
| 🕒 Timeline | Dated page history, linked to original records. | Chronological List |
| 🧰 Skills | Skills that support this view and Topic. | Left Tabs · Right Content → Skill Details |
| 📁 Files | Workspace, Blocks, Code, Tools · Skills, Tools · UI: expandable directory trees with file pop-outs. | Left Folder Types · Right Folder Tree |

The same names and order appear on the right rail. View sections show related records; the rail opens the current page and its descendants. Only explicitly linked View or Topic records appear within a view; unassigned records remain in the right rail. The same scope applies to all eight supporting sections, including Skills and Files. One record, linked where needed. Feedback identifies its Topic and delivery version; accepted changes link to Requirements and Decisions.

Work, CoWork, and Discovery share this frame. Theme Development keeps Block UI, Job UI, and Task UI as additional views. Labeling has its own theme.


## 🧩 UI Types

| Dimension | What it describes |
| --- | --- |
| Page layout | The actual renderer, views and sections. |
| Execution kind | Declared task-type or discovery-type and its skill/workflow. |
| Use case | The purpose of an instance, such as model training or data preparation. |

Work uses one general Job page. CoWork and Discovery provide real adapters; CoWork People is a reference variant. A different Job title does not create a new UI type.

The Job matrix follows these contracts. The Task matrix still needs reconciliation with execution kinds and dedicated layouts. Workflow-layout parity and external result browsing also remain open.

[Compatibility review and open checks](compatibility.md)
