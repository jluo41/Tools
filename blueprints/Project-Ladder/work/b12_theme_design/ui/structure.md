Design Board and Design Method Book · Current Block structure

**Report → Review Content → Around the Work**. The Design Board reads Designs, Goals, Inputs, Rounds, Tests and MindMap; the Design Method Book reads Method, Versions, Ideas, Scorecard and MindMap (JL 261109). Delivery remains a rail entry. The Block’s old Work links open the corresponding Report view.

## 🪜 Design ladder

| Level | Owns | Current interface |
| --- | --- | --- |
| Design Method Book | The designer of one channel: its method types, each version signed; its proposals. | Method, Versions, Ideas, Scorecard, MindMap; merged Block Report with eight shared sections. |
| Design Board | One application and channel; signed goals, rules, inputs versions, Jobs and experiment totals. | Merged Block Report with eight shared sections. |
| Design Job | One goal × one signed method version × one inputs version. | Setup, Ideas, Designs, Ranking, Release; existing Report and Work. |
| Reason-ideas Task | Input-bounded reasoning, chains, ideas and the fence check. | Inputs, Chains, Ideas, Fence check; existing Report and Work. |
| Design Task | One design’s generation, verification, revision and prediction. | Draft, Verify, Revise, State; existing Report and Work. |
| Review-whole Task | Ranking, coverage and the kept set. | Rank, Coverage, Kept; existing Report and Work. |
| Run | One execution and its result or pass. | Original Run details and receipts. |

A person signs goals and shared rules at the Block. A Job’s **Review and approve** performs the existing checked release and prediction freeze. Opening a page or copying a prompt never signs or releases a design. Task verification and revision remain unchanged.

## 📊 Designs

Design Board. Was Summary.

| Section | Content and source | Layout |
| --- | --- | --- |
| 📊 Where each Job stands | Show each Job’s recorded state and next permitted action. Held and unsigned releases remain distinguishable. Source: Job faces, verification and release Run receipts. | Table → Job |
| ➡️ Next | Separate the person’s pending review from agent work; retain links to the original Job. Source: The same Job states and gates. | Action summary |
| 📋 What each Job kept | Distinguish kept designs waiting for review from released designs. Source: Task states and release receipts. | Table → Job |
| 📄 Build the summary | Copy the prompt that rebuilds the summary from recorded results. Viewing does not build or release anything. Source: delivery/summary.pdf and the summary Run card. | Action row → Copy prompt |

## 🎯 Goals

Design Board.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🎯 The goals | Show aim, audience, channel, N, rules, exclusions and actual signature for each goal. Source: board.md Goals. | Left Tabs · Right Content → Goal |
| 📏 The shared rules | Read the common rules and their recorded signature; missing signatures remain pending. Source: design-goal.md. | Rules and signature |
| ❓ What the Block asks | Show each recorded question and the status read from its report; do not create an answer from a state count. Source: board.md Questions and reports/. | Table → Report |
| 🎯 Goals and rules | Expose goal and rule preparation actions with their real signature gates. Source: Goal and rules records; setup Run cards. | Action rows → Copy prompt |

## 📥 Inputs

Design Board. Was Rounds.

| Section | Content and source | Layout |
| --- | --- | --- |
| 📥 Inputs versions | Inspect the frozen input manifests and their actual source files. Source: inputs/inputs-vN/manifest.yaml. | Input cards → Manifest |
| 🔁 The rounds | Group Jobs, releases and returned experiments by frozen inputs version. Source: inputs/inputs-vN, Job pins and observed/eNN. | Left Tabs · Right Content → Round |
| 🔁 The next round | Copy the prompts to record returned per-arm totals and create the next frozen inputs version. Source: Observed totals and input-version Run cards. | Action rows → Copy prompt |

## 🔁 Rounds

Design Board. Was Jobs: a round is one Job, one method on one inputs version.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🗺️ Goals × methods | Place existing Jobs by goal and pinned method version. A cell opens the real Job. Source: Job goal, method, version and inputs pins. | Matrix → Job |
| 🧭 What moves across the grid | Identify whether method or inputs changed between Jobs; flag changes of both. Source: Job pins and moved field. | Comparison table |
| 📋 The Jobs | Browse each Job with its design Tasks and recorded states. Source: Job and Task faces; Run results. | Left Tabs · Right Content → Job preview |
| 🧭 Each Job's next move | Link a ready Job to Review and approve; show preparation or closure actions without executing them. Source: Workflow gates and release receipts. | Action rows → Review / Copy prompt |
| ➕ A new Job | Choose a goal, registered method and inputs version, then copy the setup prompt. Source: Signed goals, method registry, inputs versions. | Selectors → Copy prompt |

## 🧪 Tests

Design Board. Was Methods. The method scorecard shows only on a Board with no Design Method Book.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🎯 Predicted vs observed | Compare frozen predictions with recorded experimental totals and scores. Preserve the prediction basis. Source: prediction.yaml, observed/eNN/arms.csv and score results. | Comparison table |
| 🏅 Method scorecard | Group measured scores and design verification results by the pinned method version. Source: Method pins, verification results and scores. | Left Tabs · Right Content → Method |
| ⏱️ What each Job cost, by method | Read timing and usage from Run receipts; missing measurements remain unknown. Source: Run started_at, finished_at and usage fields. | Table |
| 📏 Score and learn | Expose scoring and method proposal actions; a proposal still requires its recorded human sign. Source: Score Runs and proposal passes. | Action rows → Copy prompt / Proposal |

## 🪜 Method

Design Method Book.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🪜 The five steps | Each method type in its newest signed version, step by step: ① See input to ⑤ Review whole. Source: each type's newest frozen mK.md. | Table → step |
| 👀 What step ① sees | What each method type reads at step ①; the types differ here, side by side. Source: each type's mK.md, ① See input. | List |
| 📏 The channel's rules | The channel's own rules: length, tone, what every design in this channel keeps. An application's shared rules stay on its Board. Source: the Guide's venue/venue-<channel>/README.md. | Table |

## 🔖 Versions

Design Method Book.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🔖 The versions | Each type's signed versions: what changed from the one before, its sign, and the Board Jobs that run it. Source: each type's face (versions:) and the served Boards' Job faces (method:). | Left Tabs · Right Content → Release |
| 🧭 What changed between versions | Which steps changed from one version to the next of the same type; types are never compared here. Source: the versions' steps. | Table |

## 💡 Ideas

Design Method Book.

| Section | Content and source | Layout |
| --- | --- | --- |
| 💡 Proposals | The ideas sent back from Jobs and experiments; a type's next version is cut from here once a person signs. Source: proposals/<slug>.md. | Left Tabs · Right Content → Proposal |
| ✍️ Ideas to settle | Sign or return each waiting idea; copy the prompt to write a new one. Source: proposals/ and run-propose-method-<slug>. | Action rows → Copy prompt |

## 🏅 Scorecard

Design Method Book.

| Section | Content and source | Layout |
| --- | --- | --- |
| 🏅 Each method, on the Boards it serves | Pass rate, first try and predicted vs observed of each method version, from the Boards' own scores. Source: the served Boards' Jobs, score Runs and observed totals. | Table |

## 🧠 MindMap

| Section | Content and source | Layout |
| --- | --- | --- |
| 🧠 MindMap | Show the Block’s existing topics and linked work, preserving the actual hierarchy. Source: Block face, topics and work links. | Expandable MindMap |

## 🧭 Around the Work

| Section | Content and source | Layout |
| --- | --- | --- |
| 🎨 Studio | Linked Topics and their existing drawing, slide, map and delivery assets. Source: Topic faces and assets. | Left Tabs · Right Content → Preview |
| 🙋 Interactions | Questions and forms explicitly assigned to this View or a linked Topic; waiting counts use that selection. Source: Interaction Run cards and forms. | Left Tabs · Right Content → Questions |
| ⚖️ Decisions | Recorded choices and reasons from assigned pages or Topics. Source: Decisions sections on selected faces. | Left Tabs · Right Content → Records |
| 📚 Things to Know | Relevant constraints and notes from assigned pages or Topics. Source: Things to Know sections and note records. | Left Tabs · Right Content → Notes |
| 📝 Checklist | Read the checks actually recorded for the selected View or Topic. Do not infer completion from the presence of code or a file. Source: Checklist sections on selected faces. | Recorded checklist |
| 🕒 Timeline | Read dated events from the selected Runs and records, with their original sources. Source: Selected Run receipts and dated records. | Chronological list |
| 🧰 Skills | Show declared support skills plus the selected Runs and Topics; use the same selection in Files. Source: Design VIEW_SKILLS, selected Run cards and skill catalog. | Left Tabs · Right Content → Skill |
| 📁 Files | Browse selected Topic and Run directories, assigned page faces and supporting tools. Unassigned files stay reachable through the rail. Source: Original files, skill catalog and Design renderer files. | Left Folder Types · Right Folder Tree → Pop-out |

Inside a View, explicit `view:` wins; otherwise the linked Topic must match the View. Unassigned records remain in the right rail. The rail aggregates the current page and descendants. All eight sections share that scope. No source record is copied or relabeled to fill an empty View.

Files uses Workspace (`_WorkSpace/`), Blocks, Code (`code/`), Tools · Skills and Tools · UI only where the original sources exist. Runs remain inside their Block–Job–Task hierarchy; file details open in a pop-out.

## 🔁 Design feedback loop

Release → returned experiment totals → prediction score → Studio and method proposal → recorded decision → new inputs or method version → a new Job. A new method or input does not rewrite a released Job. Sending and conducting the experiment remain downstream.

## 📐 Implementation boundary

- Implemented in the focus page: the Design Board’s merged Report, its six views (Designs, Goals, Inputs, Rounds, Tests, MindMap), eight shared sections, strict View scope and full rail, existing Job-release links, and this Block UI matrix with routed examples.
- Preserved: Job and Task specialist pages, verification loops, human release approval and the older six-Space and Design Folder pages.
- Implemented 261109: the method's own Block, the **Design Method Book** (`design/DesignMethodBook-<Topic>/`, views Method · Versions · Ideas · Scorecard · MindMap), beside the Design Board it serves; a Board Job runs one method version on one inputs version, `jNN_<goal>_M0x-<slug>-mK_inputs-vM/`.
- Still a proposal: replacing Design’s business views with Overview / Status / Findings / Delivery; the four-state Checklist acceptance workflow. No new Checklist state API or reviewer sign is claimed here.
- Historical: s11–s13 and j01’s s51–s59 drawings document earlier screens. They have not been redrawn to match this Block frame. This structure and matrix describe the current Block implementation.

## 📝 Checklist

- [ ] Open each Block View: content and its existing actions appear once under Review Content, followed by eight shared sections in shared order.
- [ ] Open a legacy Work bookmark: it selects the matching Report View; Job Release still contains its original approval control.
- [ ] Select a View with explicit and unrelated records: only related records appear in all eight supporting sections; the rail retains unassigned records.
- [ ] Open every matrix section’s example: the correct Design-Example View is selected, and its source and skill are explained in the dialog.
- [ ] At 390px: open Pages and Sections, select a Topic and inspect a file; no page-wide horizontal overflow.

These are verification requirements, not recorded human acceptance. Automated checks and remaining visual checks are reported in the server guide.

## 💼 Use cases

Block and Job matrices link SMS and checklist design examples. The Task matrix links the three implemented roles: reasoning from frozen inputs, drafting and verifying one design, and ranking the whole set. Each dialog groups sources by SPACE and distinguishes Project example from Blueprint example, with original hierarchy links and expandable Tasks and Path.

Use cases do not define additional UI types. Design Job remains one contract; method, inputs and workflow state are variants. Job and Task matrices describe their existing Report views, while Work retains execution and approval. Cross-SPACE mappings are local configuration; public blueprint files contain only synthetic example paths. Opening an external example does not establish that its service has adopted this frame.
