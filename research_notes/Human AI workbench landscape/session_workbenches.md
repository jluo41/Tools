# Session and artifact workbenches

## Which projects are closest to this workbench?

### Takeaway

The closest candidates to inspect are **AionUi** for generated-file previews and multi-agent cowork, **CloudCLI** for session/file browsing plus pluggable dashboard tabs, and **SpecStory** for preserving existing Claude/Codex history. A small project, **threadle**, is unusually close to the idea of visualizing cross-provider session provenance, but has almost no adoption evidence. No reviewed source established a complete built-in system combining typed questions, approved decisions, source evidence, drawings, slides and data dashboards across Claude and Codex sessions.

### Cited Findings

All popularity figures below are approximate GitHub stars observed November 10, 2026, not active-user counts. Capabilities are documentation evidence, not hands-on verification.

| Project | Popularity / license | Verified capability and fit | Important boundary |
|---|---|---|---|
| **AionUi** | ~34.2k; Apache-2.0 | Integrates Claude Code and Codex alongside other agents. Shared team workspace and task board; file previews for PDF, Word, Excel, PPT, HTML, Markdown, images and code; watches file changes and edits text/code/HTML. Strongest artifact-oriented cowork match. [Repository](https://github.com/iOfficeAI/AionUi) | Existing external transcript import was not verified. A rendered PPT or HTML file is not proof of typed question/decision tracking. |
| **CloudCLI / Claude Code UI** | ~14.6k; AGPL-3.0 | Claude/Codex sessions, history/resume, file explorer/editing, Git, browser use, optional TaskMaster planning. Extension system adds tabs and backend services. Strong session-plus-project-files foundation. [Repository](https://github.com/siteboon/claudecodeui) | No built-in evidence-linked research questions, decision registry or drawing/slides studio located in reviewed feature docs. |
| **SpecStory** | ~1.4k on getspecstory; repository Apache-2.0 | CLI captures Claude/Codex conversations as local Markdown; `sync` exports past sessions. Optional cloud search/share and cross-history Q&A; Lore derives reusable skills. [Repository](https://github.com/specstoryai/getspecstory), [quickstart](https://docs.specstory.com/quickstart) | CLI is open source; IDE extensions are marked closed and cloud should not be assumed self-hostable. A transcript preserving decisions is not a first-class decision object. |
| **Happy** | ~24.6k on slopus/happy; MIT | Multi-agent orchestration across Claude/Codex; own-hardware execution and encrypted device access. [Repository](https://github.com/slopus/happy), [product](https://happy.engineering/) | Original CLI is maintenance-only; new work goes to Happy Desktop. Main fit is controlling and sharing sessions, not publishing a structured results website. [CLI status](https://happy.engineering/guides/terminal/) |
| **HAPI** | ~5.4k; AGPL-3.0 | Claude/Codex and other agent sessions via web/PWA/mobile, local/remote handoff, scoped workspace file browser. [Repository](https://github.com/tiann/hapi) | Remote session/workspace control; no verified structured knowledge/artifact publication layer. Native apps paid; web/PWA free. |
| **Opcode, formerly Claudia** | ~22.4k; AGPL-3.0 | Tauri desktop GUI for Claude sessions, project search, agents, usage analytics, checkpoints and CLAUDE.md. [Repository](https://github.com/winfunc/opcode) | Documentation examined is Claude-focused; Codex not established. Its dashboard is agent usage/cost, not scientific data/results. |
| **claude-code-transcripts** | ~1.7k; Apache-2.0 | Converts local Claude JSON/JSONL into paginated HTML and a prompt/commit timeline; can export all local sessions and publish a Gist. [Repository](https://github.com/simonw/claude-code-transcripts) | Claude-only in reviewed docs. Repository warns web-session commands are currently broken due to undocumented API changes. Useful archive layer, not live workbench. |
| **Vibe Kanban** | ~28.6k; Apache-2.0 | Kanban issues, agent workspaces, Claude/Codex support, diffs/comments, app preview. [Repository](https://github.com/BloopAI/vibe-kanban) | **Maintenance warning:** Bloop shut down April 10, 2026; official announcement says community-maintained continuation and retirement of remote services. Treat as design/code reference, not a healthy hosted-service recommendation. [Announcement](https://www.vibekanban.com/blog/shutdown) |

### Inferences

- For the user's stated objective, AionUi and CloudCLI are more useful comparisons than generic personal assistants such as Muse clones: they already bind agent sessions to local files and visible output surfaces.
- AionUi is the strongest first product demo; CloudCLI is the strongest concrete extension example; SpecStory is the strongest starting reference for cross-provider history preservation. This is a fit assessment based on the sources above, not a performance benchmark.
- “Dashboard” requires disambiguation: Opcode's usage analytics, Vibe Kanban's task progress and AionUi's rendered spreadsheet are different objects from a reproducible scientific dashboard.

### Gaps

- No source reviewed established a complete, evidence-linked question/decision lifecycle. Record this as **not documented in this review**, not as a proven absence from every extension.
- No complete audit of existing-history import was performed for AionUi, CloudCLI, Happy, HAPI or Vibe Kanban. Running Claude/Codex inside an app does not prove discovery of all independently created historical sessions.
- No running installation was tested; model subscription reuse, deployment compatibility and artifact rendering fidelity remain demo checks.

## What should be borrowed for sessions, files and artifacts?

### Takeaway

The useful architecture separates session capture, durable typed records and rendered artifacts. Existing projects provide good implementations of the first and third; the user's question/evidence/decision structure remains a distinct product responsibility.

### Cited Findings

- AionUi's WebUI can run alongside desktop or as a standalone headless server. Desktop modes share conversations and SQLite data; the standalone server uses a separate default data directory, with explicit configuration to share. Thus browser access is a documented deployment mode, not just screenshots of an Electron app. [WebUI guide](https://github.com/iOfficeAI/AionUi/wiki/WebUI-Configuration-Guide)
- CloudCLI's official MIT-licensed starter adds a project-stats tab with charts, file counts and recent activity. Plugins receive project/session context and a context-change callback; optional Node backends communicate through RPC. The documented API cannot interact with the chat system or modify built-in tabs. Frontend plugins are explicitly not runtime-sandboxed. [Plugin starter](https://github.com/cloudcli-ai/cloudcli-plugin-starter)
- SpecStory's CLI can launch either `claude` or `codex`, save Markdown in `.specstory/history`, export past conversations through `sync`, and avoid optional cloud syncing. This is a practical precedent for agent-independent durable session records. [Quickstart](https://docs.specstory.com/quickstart)
- An additional niche design reference is **threadle**, MIT, only **3 observed stars**: its viewer parses existing Claude and Codex storage read-only and draws session maps, tool/file blueprints and timelines. Its own docs warn provider formats are undocumented and changing. A workflow-canvas addon is described as soft-frozen. [Repository](https://github.com/threadle-sh/threadle), [session readers](https://docs.threadle.sh/sessions/overview/), [overview](https://docs.threadle.sh/)

### Inferences

- Suggested adaptation for SPACE: retain original transcript references and file revisions; derive a small index of Session, Question, Decision and Artifact records. Preserve the exact source turn/file version behind each extracted item. Require review before an inferred decision becomes an approved decision.
- Define an artifact manifest rather than relying only on file extensions: kind, title, entry file, source files, generating session/run, version, status and access scope. The website then chooses renderers for tables/data, HTML dashboards, Markdown/PDF, drawings and slides.
- Keep two distinct dashboard families: operational (work/task/run progress and usage) and subject-matter (patient/data/analysis findings). Do not conflate a token dashboard with an Insight Board.
- Take AionUi's preview UX pattern, CloudCLI's context-aware tab/plugin pattern and SpecStory's capture/export pattern without requiring wholesale replacement of the existing theme system.
- HTML execution needs an appropriate isolated preview boundary; source-linked static documents and executable apps should not silently share the same trust level. This follows from CloudCLI's explicit no-sandbox plugin model and the user's aim to display generated outputs.

### Gaps

- A studio drawing shown as SVG/image is not the same as an editable semantic drawing. Need actual renderer/integration testing for editable Excalidraw-style canvases and slide editing.
- threadle is a useful architecture example, not evidence of maturity or popularity; its supported-provider claim should be checked against installed CLI versions before reuse.
- The user's DSH acronym was not identified in this lane. HAPI's current README lists **DeepSeek Harness** as a supported agent; that is a clue only, not an identification of the intended plugin. [HAPI](https://github.com/tiann/hapi)

## Which maturity and maintenance findings affect the shortlist?

### Takeaway

Popularity alone is a poor selection criterion here. Several highly starred tools are execution clients, and Vibe Kanban's official shutdown materially changes the recommendation.

### Cited Findings

- CloudCLI release **1.37.8, November 7, 2026**, includes provider-native side questions, file download, session menu changes, browser upload, notification webhook and Codex SDK updates: useful concrete recent maintenance evidence. [Release notes](https://github.com/siteboon/claudecodeui/releases)
- AionUi's examined releases page shows **v2.2.2**, released September 9 (page omits year in displayed timestamp). It describes file-explorer refresh and worktree rediscovery. Release notes say installers now come from the official website rather than GitHub, so use the current distribution instructions. [Releases](https://github.com/iOfficeAI/AionUi/releases)
- Happy's original CLI documentation explicitly declares maintenance mode; Happy Desktop's releases show **v0.0.103** as latest stable, November 5 (displayed timestamp omits year). [CLI transition](https://happy.engineering/guides/terminal/), [desktop releases](https://github.com/slopus/happy-desktop/releases)
- Opcode's latest shown release is **v0.2.0**, August 31 (displayed timestamp omits year), with rebranding from Claudia and analytics changes. This does not establish current cadence; do not call it abandoned solely from this page. [Releases](https://github.com/winfunc/opcode/releases)
- Vibe Kanban's official April 10, 2026 announcement says the company was closing, remote services would remain for 30 days, and local workspaces would continue. Its release page shows an April 24, 2026 v0.1.44 build. Repository feature descriptions about remote issues/projects must be read alongside that announcement. [Shutdown](https://www.vibekanban.com/blog/shutdown), [releases](https://github.com/BloopAI/vibe-kanban/releases)
- claude-code-transcripts openly documents broken cloud-session export commands; its local JSONL-to-HTML path remains documented. [Repository](https://github.com/simonw/claude-code-transcripts)

### Inferences

- Practical inspection order: **AionUi → CloudCLI plugin starter → SpecStory**. Compare only these three hands-on first, with a fixed sample Claude session, Codex session, HTML dashboard, CSV/table, drawing and slide deck.
- Use Vibe Kanban as a planning/review interface reference, not as the default deployment platform. Use Opcode/Happy/HAPI as session-control comparisons when that becomes a requirement.
- An evaluation should ask whether existing independent sessions appear, whether file changes update artifact previews, whether a question links to the original supporting turn, and whether outputs remain readable after the agent session ends.

### Gaps

- Repository stars were checked through rendered GitHub pages, not independently audited counters; snapshots may be cached and are rounded.
- Commercial support, security posture, operating cost and license obligations were not audited. License names describe inspected source repositories and do not automatically apply to hosted services or every optional component.
