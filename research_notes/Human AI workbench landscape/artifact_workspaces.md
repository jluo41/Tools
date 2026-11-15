# Artifact publishing and durable knowledge workspaces

Research checked November 10, 2026. Scope: web artifacts, data publishing, durable notes and visual knowledge workspaces. Session-viewer projects are covered by another researcher. Capabilities below are documented, not installed or runtime-tested. GitHub stars are rounded popularity signals, not active users or reliability measurements. Current docs can describe development versions: LibreChat's docs explicitly say Latest (dev), and its attached workspaces are labeled highly experimental in the repository. [LibreChat docs](https://www.librechat.ai/docs), [repository](https://github.com/LibreChat-AI/LibreChat).

## Which existing products are closest to the requested workbench?

### Takeaway

The strongest matches occupy three layers: LibreChat/Open WebUI for conversation plus artifacts; AFFiNE/SiYuan for lasting knowledge and visual organization; marimo/Quarto for computed results published as multiple web/document views. This classification is an inference from the capabilities below. No reviewed documentation establishes an out-of-the-box system that imports arbitrary old Claude Code and Codex sessions, extracts governed questions/decisions, and links all workbench types with source provenance.

### Cited Findings

| Project | Documented native capability | Relation to SPACE and its boundary |
|---|---|---|
| **LibreChat** | Native side-panel artifacts render React, HTML, SVG, Markdown and Mermaid. Source can be edited and downloaded. Code execution files also appear in that panel. [Artifacts](https://www.librechat.ai/docs/features/artifacts) | Strong example of chat + inspectable output. It documents artifacts belonging to its agent/chat mechanism; that is not evidence of a historical Claude Code/Codex importer. |
| **Open WebUI + Open Terminal** | Open WebUI has artifacts, persistent notes, and a connected filesystem/shell workspace with live app previews. Coding agents explicitly include Claude Code and Codex. [Artifacts](https://docs.openwebui.com/features/chat-conversations/chat-features/code-execution/artifacts/), [Open Terminal](https://docs.openwebui.com/features/open-terminal/), [coding agents](https://docs.openwebui.com/features/open-terminal/coding-agents/) | Closest broad ready-made web environment in this subset. Existing agent conversations retain their workspace; docs specify new-message continuation, with no branching/regeneration for agent chats. Historical session import and first-class decision/question lifecycle were not established. |
| **AFFiNE** | Combines documents, edgeless canvas, linked pages, embedded webpages, multiview databases, shapes and slides. Offers local-first storage and collaboration. [Repository](https://github.com/toeverything/AFFiNE) | Closest visual knowledge/product reference. A database can represent a question/decision tracker, but a specific source-linked review lifecycle would be custom configuration/integration. |
| **SiYuan** | Block references/backlinks, custom attributes, SQL embeds, tables, diagrams, PDF annotation links, API, Docker hosting; exports Markdown/assets, HTML, PDF and Word. [Repository](https://github.com/siyuan-note/siyuan) | Strong reference for persistent linked knowledge. Its editor blocks are not SPACE's Block/Job/Task entities. Source-linking could be built from attributes and links; no automatic Claude/Codex session promotion was verified. |
| **AnythingLLM** | Local/cloud model connections, document ingestion, RAG, agents, multi-user setup, and an embeddable chat widget. [Repository](https://github.com/Mintplex-Labs/anything-llm) | Relevant if the goal is querying project files. Ingesting a transcript as a document is different from preserving message-level lineage and producing typed work objects. No full question/decision/studio/slides workbench verified. |
| **marimo + marimo pair + Studio** | Reactive Python/SQL notebook, app mode, web publishing and agent pairing; Studio builds multiple custom report/app/presentation views backed by notebook outputs. [Core](https://github.com/marimo-team/marimo), [pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/), [Studio](https://marimo-team.github.io/marimo-studio/) | Particularly close to the user's “data, dashboard, artifact” goal. It couples authored views to computed results rather than mining historical chats. Studio is experimental, not equivalent in maturity to core marimo. |
| **Quarto** | Markdown/notebook publishing to reports, websites, dashboards and slides; Python/R/Julia/Observable execution; HTML, PDF, Word and presentation formats. [Guide](https://quarto.org/docs/guide/), [dashboards](https://quarto.org/docs/dashboards/) | Strong publication backend for agent-written files. Question/decision state needs authored metadata and a custom index; Quarto is not a session manager. |
| **Observable Framework** | Static data apps/reports from Markdown, reactive JavaScript and data loaders in multiple languages; built-in chart/diagram/data libraries; host anywhere. [Official framework docs](https://observablehq.github.io/framework/) | Good dashboard renderer. Snapshots are computed at build time, so provenance and freshness should be made explicit in the enclosing workbench. |
| **Evidence** | SQL-and-Markdown BI reports, local development server, static-site publishing or hosted Evidence Studio. [Repository](https://github.com/evidence-dev/evidence) | Good business-data dashboard reference. The commercial website advertises additional agent, access-control and operational features; do not assign all of those to the MIT repository without checking the exact edition. [Product](https://evidence.dev/) |
| **JupyterLab** | Extensible notebook/terminal/editor/file-browser workspace with rich outputs. [Repository](https://github.com/jupyterlab/jupyterlab) | Strong computational authoring environment; reader-facing publication and work-state navigation are additional layers. |
| **Excalidraw** | Embeddable drawing editor, PNG/SVG export and editable `.excalidraw` JSON. The hosted example has collaboration and read-only sharing. [Repository](https://github.com/excalidraw/excalidraw) | Reusable Studio renderer, preserving editable drawings. Hosted-app collaboration is not automatically included in an arbitrary embedded npm editor. |
| **Slidev** | Markdown slides, Vue components, Mermaid diagrams, presenter mode, annotations, PDF/PNG/PPTX export. [Repository](https://github.com/slidevjs/slidev) | Reusable slide renderer that agents can author as files; deck/project/session relationships remain SPACE's responsibility. |

Open WebUI Notes are independent of single conversations; pages/subpages, file blocks, sharing, full-content context and model tools for searching/reading/writing notes are documented. Multiple chats can attach to a note. This is a relevant pattern for turning conversation into a lasting object. [Notes](https://docs.openwebui.com/features/notes/)

LibreChat's Code Interpreter documentation describes code running in an isolated service, resulting files returned to the conversation, and previews for HTML, Markdown, CSV and Office documents including slides. Stateful execution and attached-machine options are separate opt-in features, not guaranteed by the basic artifact panel. [Code Interpreter](https://www.librechat.ai/docs/features/code_interpreter)

### Inferences

- “Similar work exists” is clearly supported; “one competitor already does our entire workflow” is not established by this research. The distinctive integration opportunity is a durable relationship among **question → discussion → decision → execution → evidence → artifact**, across different agent sessions.
- A report, drawing or slide should exist as a project object independently of a chat. A chat can reference/update that object, as illustrated by Open WebUI Notes and marimo's separate notebook/view model.
- Choose an existing engine for each renderer rather than inventing a notebook, drawing editor and slide system simultaneously. Preserve the shared work model and provenance in SPACE.

### Gaps

- No hands-on deployments, compatibility tests or security audits were performed. Feature presence is based on official docs/repositories.
- No reviewed artifact/knowledge project's docs established a first-class importer for both arbitrary historical Claude Code JSONL and Codex session histories with source-turn identifiers. This is a research gap, not a categorical assertion that no plugin exists.
- Question and decision tracking can be represented by generic documents/databases, but native status transitions, evidence requirements and approval semantics were not verified for those representations.

## Which options are popular and genuinely reusable under open licenses?

### Takeaway

Popularity and fitness differ: the largest chat/knowledge tools are broad product shells; smaller publication tools can be more useful building blocks. Licensing also differs materially between core code, enterprise components, and hosted services.

### Cited Findings

| Project | Approximate GitHub stars observed | License finding |
|---|---:|---|
| Open WebUI | 158k | Custom Open WebUI license with branding condition from v0.6.6; pre-v0.6.6 contributions remain BSD-3-Clause. [Repo](https://github.com/open-webui/open-webui), [license explanation](https://docs.openwebui.com/license/) |
| Excalidraw | 135.5k | MIT. [Repo](https://github.com/excalidraw/excalidraw) |
| AFFiNE | 74.4k | Mixed: general code MIT, designated backend/native directories governed separately, CE portions there MPL-2.0 and non-CE portions enterprise terms. [Repo](https://github.com/toeverything/AFFiNE), [root license](https://github.com/toeverything/AFFiNE/blob/canary/LICENSE), [backend license](https://github.com/toeverything/AFFiNE/blob/canary/packages/backend/server/LICENSE) |
| AnythingLLM | 68.2k | MIT. [Repo](https://github.com/Mintplex-Labs/anything-llm) |
| Slidev | 49.4k | MIT. [Repo](https://github.com/slidevjs/slidev) |
| SiYuan | 47.2k | AGPL-3.0; some product features paid. [Repo](https://github.com/siyuan-note/siyuan) |
| LibreChat | 47k | MIT application. [Repo](https://github.com/LibreChat-AI/LibreChat) |
| marimo | 23.5k | Apache-2.0. [Repo](https://github.com/marimo-team/marimo) |
| JupyterLab | 15.4k | BSD-3-Clause. [Repo](https://github.com/jupyterlab/jupyterlab) |
| Evidence | 7k | MIT repository; do not conflate with all hosted Studio services. [Repo](https://github.com/evidence-dev/evidence) |
| Quarto CLI | 6.2k | Current repository identifies MIT; dependencies retain their own licenses. [Repo](https://github.com/quarto-dev/quarto-cli) |
| Observable Framework | 3.7k | ISC. [Repo](https://github.com/observablehq/framework) |
| marimo Studio | 71 | Apache-2.0; explicitly experimental and changing rapidly. [Repo](https://github.com/marimo-team/marimo-studio) |

Open WebUI's current terms require visible branding unless an exception applies: at most 50 users in a 30-day period; substantive contributor with prior written permission; or an enterprise agreement permitting changes. Therefore describe it as **source available with custom branding terms**, rather than casually calling the current release unconditionally BSD or MIT. [License](https://docs.openwebui.com/license/)

AFFiNE's backend license permits non-CE enterprise code in production only under applicable subscription/agreement terms; it specifically places CE-distributed and designated client-side material under MPL-2.0. A product fork must inspect the actual files/edition used. [Backend license](https://github.com/toeverything/AFFiNE/blob/canary/packages/backend/server/LICENSE)

### Inferences

- Strong first evaluations: **LibreChat** for artifact UI; **Open WebUI + Open Terminal** for an integrated file/chat/code shell; **AFFiNE** as a visual-product reference; **marimo** for data analysis; **Quarto/Excalidraw/Slidev** for reusable output renderers.
- marimo Studio deserves a prototype evaluation because of unusually close feature fit, but its low adoption and explicit experimental label argue against assuming mature operational behavior.
- GitHub popularity cannot establish patient-data suitability, ease of maintenance, or trustworthy provenance.

### Gaps

- Star counts were taken from rendered repository pages, rounded, and can change or lag live counts.
- License analysis is a technical inventory, not a legal conclusion. Transitive dependencies and commercial features were not exhaustively audited.
- Latest docs and main/canary branches are not necessarily the features in an existing deployment or pinned stable release.

## How could SPACE add Claude style data and artifacts while retaining its workbench model?

### Takeaway

The closest concrete implementation pattern is **agent-authored files + a typed artifact registry + dedicated renderers + source links**, with notebook outputs reused across dashboard/report/slides. Add cross-session extraction and governance as their own layer; they are not supplied merely by putting an agent in a web chat.

### Cited Findings

- **Direct Claude/Codex pairing exists:** marimo pair explicitly connects Claude Code, Codex and other coding agents to running notebooks. Agents inspect variables, test in a scratchpad and edit cells while the human sees/edits the same notebook. This is live shared work, not an importer of old transcripts. [marimo pair](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/)
- **One result, multiple presentations exists:** marimo Studio places cell outputs or individual values into independent view folders, with traces back to their computing cells. Views may use HTML, React, Svelte, Reveal.js, Quarto, Typst or LaTeX. It supports live Python, browser execution or static exports; docs show reports, dashboards, slide decks and papers backed by the same notebook. [Studio overview](https://marimo-team.github.io/marimo-studio/), [repository](https://github.com/marimo-team/marimo-studio)
- **Data apps can have a gallery:** `marimo run` serves notebook outputs as apps, supports grid and slides layouts, and can serve a directory of notebooks as a card gallery. [App guide](https://docs.marimo.io/guides/apps/)
- **Publishing need not mean public internet:** Quarto creates standard HTML and supports both static hosts and authenticated organizational publishing through products such as Posit Connect. [Publishing](https://quarto.org/docs/output-formats/html-publishing)
- **Agent shell and workspace already connect:** Open Terminal documentation covers data analysis, file operations and in-chat dev-server previews; Open WebUI's coding-agent layer can run Claude Code or Codex in that workspace. [Terminal](https://docs.openwebui.com/features/open-terminal/), [coding agents](https://docs.openwebui.com/features/open-terminal/coding-agents/)
- **Avoid a deprecated branch of the ecosystem:** Open WebUI Computer (`cptr`) is being gradually deprecated, with new users directed to Open WebUI plus Open Terminal. [Official notice](https://docs.openwebui.com/ecosystem/computer/)

### Inferences

Suggested SPACE architecture, offered as a design proposal rather than a claim about current implementation:

1. **Source adapters:** read Claude and Codex session records plus registered project files. Preserve agent, session, turn/event identifiers and file revisions. Keep the original records; do not replace them with summaries.
2. **Work objects:** Question, Decision, Evidence, Artifact and Session links attached to the existing Block/Job/Task/Run scope. Extracted decisions begin as proposed; human acceptance is distinct from an assistant assertion.
3. **Artifact registry:** stable `artifact_id`, type, owning work scope, source file, source session/turn, source revision, data/code version, renderer and state. The renderer reads this registry rather than guessing meaning solely from extensions or scanning every file into a public page.
4. **Views:** dashboard (structured tables/results), question tracker (status/evidence/next action), decision log (rationale/alternatives/authority/supersession), Studio (editable diagram + preview), slides (editable source + HTML/PDF), and report (source-cited narrative). Each view navigates to its sources.
5. **Rendering:** reuse marimo for live analysis and potentially Studio views, Quarto for publication, Excalidraw for drawings, Slidev for decks; a sandboxed HTML/React preview can cover custom artifacts in the style of LibreChat. Choose a small initial set to avoid multiple overlapping stacks.
6. **Update behavior:** explicit file registration or end-of-task hooks update a derived index; changed inputs mark dependent artifacts stale until regenerated. Preserve accepted decision records and earlier versions.

Useful first demonstration: take one Claude session and one Codex session concerning the same question, register the resulting data/table/drawing/slide files, and show a single question page with the answer, accepted decision, evidence, artifact previews and links back to exact sources. Acceptance should include “can the reviewer trace this number and this decision?” as well as whether the previews render.

### Gaps

- The session schema adapters, acceptance transitions and renderer contracts require a separate implementation review; they were not prototyped in this research.
- No source here verifies a named “DSH harness” plugin's features. That investigation belongs to the separate researcher identifying the exact plugin.
- Broad drawing frameworks such as tldraw, and commercial products such as Hex, may provide useful adjacent UI patterns, but they were not fully evaluated here. Do not claim an exhaustive market census.
