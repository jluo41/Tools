Labeling · Current structure and migration boundary

**Report → Review Content → Around the Work** is implemented on Labeling Blocks and Jobs. Task steps retain their existing Report / Work workflow. The matrices describe each level; clicking a Section shows its content, source, layout, skills and corresponding example View.

## 🪜 Labeling ladder

| Level | Owns | Current interface |
| --- | --- | --- |
| Block | Related labeling Jobs and their outputs. | Overview · Status · Findings · Delivery, followed by eight shared sections. |
| Job | One corpus snapshot × target construct × identified human authority. | The same four Views, scoped to this Job and its descendants. |
| Items Task | Source description, accepted item recipe and embedding build. | Data · Items · Embedding in Report / Work. |
| Meaning Task | Human agreement and repeated meaning refinement. | Frame · Prepare · Preferences · Update in Report / Work. |
| Expression Task | Executable wording under approved meaning, evaluation and release. | Rewrite · Run · Evaluate · Release in Report / Work. |
| Run | One recorded execution or interaction, with its own results and signatures. | Existing Run details and guarded forms. |

```text
b02_labeling_walkthrough/
├── board.md
├── data/                         synthetic input and provenance
└── j01_example_response_safety/
    ├── j01_example_response_safety.md
    ├── t01_example_items/
    │   └── runs/                 source, recipe and build records
    ├── t03_example_meaning/
    │   └── runs/                 agreement, reports, answers and updates
    └── t04_example_expression/
        └── runs/                 rewrite, execution, evaluation and release
            └── r07_release_e02/
                ├── run.yaml
                └── result/       labels, signature and runtime record
```

Topics live beside the owning page’s work. Their associations select View context. Existing preparation and labeling engines retain their own stores and writers; this diagram describes the real walkthrough, not a migration of every legacy Job.

## 🧭 Overview

| Section | Content and source | Layout |
| --- | --- | --- |
| 🎯 Goal | Authored goal or spine from the Block or Job face. | Paragraph |
| 📋 Requirements | Recorded requirements and Questions register. | List and question records |
| 🧠 MindMap | Topic associations and the actual work hierarchy. | Left Topics / Work Structure tabs · right diagram |

The source is `work_frame.overview`. Missing requirements are not inferred as satisfied.

## 📊 Status

| Section | Content and source | Layout |
| --- | --- | --- |
| 📊 Job progress — Block | Existing Job bands, Task completion and current Run state. Band headings use the Block’s own names. | Numbered bands → expandable Job and Task rows |
| 📋 Tasks — Job | The Job’s state line and each Task’s latest recorded state or result. | Numbered disclosure → Task rows |
| 🧩 View BJTR | Real Block → Job → Task → Run relationships grouped by Topic. | Left Topic tabs · right expandable tree → pop-out |
| 🔗 Dependencies | Authored Dependencies section, only when present. | Markdown disclosure |

The source is `work_frame.status` with Labeling’s Task completion wording. Status displays existing work; expanding a tree does not start a Run. Work’s BJTR grouping is reused without changing the Labeling sequence.

## 💡 Findings

| Section | Content and source | Layout |
| --- | --- | --- |
| 🏷 Final labels | Latest expression release result, including its actual signed or unsigned state. | Per-Job disclosure → label table and case details |
| 🧠 The rules they follow | Approved meaning version returned by the meaning engine; absent when no approved version exists. | Per-Job disclosure → guideline mind map |

The source is `labeling_focus.findings_html`. With several Jobs, their names distinguish the sections. A visible result is not proof of a signed release or a validated production worker.

## 📦 Delivery

| Section | Content and source | Layout |
| --- | --- | --- |
| 📦 Signed releases | Expression release Runs that are both done and signed: labels, file, approved rules, signature date and owning Run. Actual bars read “Final labels, release …”. | One numbered disclosure per release → key-value records and pop-outs |
| 📁 The Block’s delivery/ | Existing handoff artifacts returned by the delivery reader, when present. | Existing delivery content and file links |

The source is `labeling_focus.releases` and `delivery_html`. Opening the View signs nothing and does not create missing files. The walkthrough contains a synthetic signed e02 release; it is a UI example, not production-quality evidence.

## 🧭 Around the Work

These unnumbered sections use `work_frame.SHARED` and `shared_bodies` in the same order as the right rail.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🎨 Studio | Selected Topics and their drawings. | Left Topic tabs · right drawing and content |
| 🙋 Interactions | Selected questions, existing forms and answers. | Left Topic/question tabs · right form or record |
| ⚖️ Decisions | Recorded Decisions sections from selected pages and Topics. | Left record tabs · right text |
| 📚 Things to Know | Selected notes and to-know interaction records. | Left record tabs · right notes |
| 📝 Checklist | Authored Checklist sections in the selected source. | Source tabs → Markdown checklist |
| 🕒 Timeline | Selected Run history, interactions and decisions with actual dates. | Chronological records and source links |
| 🧰 Skills | View mappings plus selected Task kinds and Run skill fields. | Left skill tabs · right details |
| 📁 Files | Existing related work, Tools skills and UI directories. | Left folder types · right directory tree → file pop-out |

**Inside a View:** explicit View association takes priority, then Topic association. Unassigned records remain in the rail. Skills and Files use the same selection as the other shared sections. Private raw files remain subject to the host’s source boundary.

**Right rail:** the current Block or Job and its descendants across Views. Both entrances read the original records. Actual `code/` and `_WorkSpace/` directories appear only when applicable; empty directories are not invented.

## 🛠 Task workflow

| Task | Current sequence | Boundary |
| --- | --- | --- |
| Items | Data → Items → Embedding | Existing preparation receipts and human acceptance. |
| Meaning | Frame → Prepare → Preferences → Update | One identified human remains semantic authority. |
| Expression | Rewrite → Run → Evaluate → Release | Fixed approved meaning, measured results and human release signature. |

Task examples open `section=work` and the exact step key. The shared-section row in Task UI is explicitly a target and has no implemented example link. Ground Truth, legacy Building, Scanning and Score require separate review. This update does not claim their migration or implement missing workers.

## 📋 Alignment and verification

| Check | Current state and evidence |
| --- | --- |
| Block and Job have four Views and eight shared sections. | Implemented; `test_labeling_focus` checks navigation and old-link aliases. |
| Unassigned interaction records stay in the rail. | Implemented through shared scope; `test_labeling_focus` checks assigned versus unassigned records. |
| Findings and signed Delivery preserve domain gates. | Existing readers retained; `test_labeling_steps` checks result and release behavior. |
| Matrix sections explain content, source, layout and skills. | Authored in `view-guide.json`; example routes point to the actual walkthrough and View. |
| Missing conditional sections remain absent. | Dependencies and Block delivery are documented as conditional; the example link opens the View without fabricating content. |
| Task shared-frame migration. | Pending; current domain-step links remain usable. |
| Four Checklist states with verification evidence. | Discussion proposal; no new public schema or acceptance writer is claimed. |

Detailed checks and current limitations are recorded in `ui/verification.md`. Old Work and MindMap links at Block and Job level remain usable. No source folders, Runs or signatures are moved by this design update.
