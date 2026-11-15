# Native artifacts and DSH workbenches

## What does Claude actually provide today?

### Takeaway

The user's premise is correct: Claude Code can publish session results into live websites, and Claude's wider app now includes Data, Whiteboards, Sheets, documents and slides. Use current product documentation, because the June artifact launch post has already been superseded on plan availability and public sharing.

### Cited Findings

- **Current Claude Code artifacts:** a self-contained interactive page hosted on claude.ai; source can include session context, repository files and connected tools. Updates publish revisions at the same URL; another session can continue by attaching the artifact or supplying its URL. Concurrent stale edits are rejected before republishing. Private, organization and public sharing exist subject to policy. This is one page with no application backend or multiple routes. Current eligibility: Pro/Max/Ultra/Team/Enterprise, claude.ai login; API-key and cloud-provider credentials cannot publish. Organization HIPAA, CMEK or ZDR configurations disallow this feature. Live connector calls use the viewer's claude.ai connection; local MCP servers can supply build-time data but are not callable by the published artifact. These are product constraints, not recommendations. — [Current Claude Code artifact documentation](https://code.claude.com/docs/en/artifacts)
- **Claude Data is the current name for Claude Dashboards:** on November 10, 2026, Anthropic announced Data GA and Whiteboards/Sheets beta on paid plans. Data connects to company data systems, supports dashboard caching/refresh and tracked edits; certified queries and live sharing remain beta. Whiteboards support collaborative planning and conversion to docs/decks; Sheets supports basic spreadsheet creation/editing and export. The Data product requires a connector such as a warehouse or CRM. It is not described as an automatic importer of arbitrary Claude/Codex transcript directories. — [November 10 product announcement](https://claude.com/resources/articles/sheets-whiteboards-data)
- The current help center says artifacts can store personal/shared text data between sessions; the storage limit is 20 MB per artifact and excludes binary files. It also describes connectors and Claude-powered artifacts. Do not generalize that storage limit to all Claude Data/backend data sources. — [Artifacts help](https://support.claude.com/en/articles/17153992-what-are-artifacts-and-how-do-i-use-them)
- The **June 18 launch article** documents the original Code feature as Team/Enterprise beta and organization-only sharing. Those historical restrictions conflict with the current Code docs and should not be repeated as today's limits. The architectural analogy—session context converted into a versioned web page—is still useful. — [Historical launch article](https://claude.com/resources/articles/artifacts-in-claude-code)

### Inferences

- The reference product has three separable layers: session-to-page publishing, shared editable artifact surfaces, and live data access. Matching its visible dashboard without its identity/version/source/update contracts will give SPACE a screenshot, not a durable product.
- Claude's hosted artifacts can be a useful output destination when eligible, but they do not replace a cross-harness repository-native website with several workbench types. No official cross-harness transcript ingestion was established in the sources inspected.
- For the user's earlier patient-data product, the documented HIPAA configuration exclusion is material when considering Claude-hosted artifact publishing. It need not dominate this workbench comparison.

### Gaps

- No login/product plan was inspected and no Claude artifact was published. Exact user entitlement is unknown.
- The announced Claude Data features were checked in official documentation, not exercised in a live account.
- No independently verified usage/adoption number was found for these proprietary feature surfaces.

## Does DSH have dashboards and artifacts?

### Takeaway

DSH is very likely **DeepSeek Harness**, corroborated by this repository's own README, which explicitly calls its tool-neutral skill consumer DeepSeek Harness (`dsh`). Yes, its ecosystem has both artifact rendering/sharing and web workbench extensions. Distinguish those from the many token-usage dashboards: operational analytics about an agent are different from dashboards containing the work the agent produced.

### Cited Findings

- **DeepSeek Harness core** is MIT licensed, developed under `deepseek-ai`, with an everything-is-a-plugin architecture and a web UI. The official repository had about **278,200 stars** when inspected November 10, 2026, but labels itself **developer preview** and warns of breaking changes. Core popularity says nothing about individual plugin stability. — [Official repository](https://github.com/deepseek-ai/deepseek-harness)
- **DSH Better Sidebar** is a genuinely relevant web workbench extension: file management, editable CodeMirror, Markdown/Mermaid, sandboxed HTML, JSONL record cards, Git, terminals, subagent views, side chats and plugin-extensible sidebar pages. MIT; about **5,100 stars** at inspection. Its existing object model centers files/sessions/tasks; no dedicated research-question/decision/evidence registry was established. — [Repository and feature table](https://github.com/omdsh-dev/DSH-better-sidebar)
- **Abid's `dsh-visualizer`** (`abiddotdev`, formerly referenced as `abidhmuhsin` in its own package metadata) provides streaming HTML artifacts, inline previews, downloads, UI-targeted comments, export/share, an artifact gallery and persisted widget state. MIT; about **14 stars**. Current README says export is explicit, not automatic: successful logged tool output is mirrored to disk on request. Content-based names produce stable links for identical bytes and different links for revisions; capability-key sharing differs from per-user authorization. Default retention is 30 days; pinning exempts artifacts. The README's old installation URL and current owner should be resolved before installation. — [Repository](https://github.com/abiddotdev/dsh-visualizer)
- Code verifies the Abid plugin's `visualizer` tool stores the generated HTML in durable tool-call arguments, replays it from logs and registers an export path reading the successful logged call. Its configuration exposes artifact directory, retention and sharing key. Package version inspected: 0.9.0, MIT, with host/client DSH declarations. This is more than a screenshot or download-only prototype, but it remains a small community plugin. — [Host source](https://raw.githubusercontent.com/abiddotdev/dsh-visualizer/master/src/index.ts), [package manifest](https://raw.githubusercontent.com/abiddotdev/dsh-visualizer/master/package.json)
- **Moses14159's `dsh-visualizer` is a separate implementation**, despite identical package names. It registers `visualize` accepting `spec` or `widget`; structured charts use ECharts and fenced SVG/HTML can stream from assistant events. It uses existing tool/session events; no new event family is required. MIT; version 0.3.0; about **7 stars**. Do not attribute Abid's export/gallery/sharing feature set to it. No fork relationship was established. — [Repository](https://github.com/Moses14159/dsh-visualizer), [host source](https://raw.githubusercontent.com/Moses14159/dsh-visualizer/main/src/index.ts), [manifest](https://raw.githubusercontent.com/Moses14159/dsh-visualizer/main/package.json)
- **DSH Session Insights** creates offline HTML and companion JSON from session history, with project/workflow activity, failures, retries and completion evidence. Deterministic local analysis is supported; optional model analysis sends selected excerpts to the configured provider. It is a workflow retrospective rather than a domain-result dashboard. MIT; about **2 stars**; documented version 0.8.0 requires DSH >=0.2.2-rc.1 and Node >=24.9.0. — [Repository](https://github.com/GreenLv/dsh-session-insights)
- A representative **usage dashboard** provides token accounting, account balance, per-conversation costs and remaining-turn estimates. This is a useful control-plane component but is not a substitute for the user's research results, decisions, drawings or slide galleries. — [Usage dashboard README](https://github.com/gongshiyun/dsh-usage-dashboard/blob/main/README.en.md)
- Local identity corroboration: Tools-SPACE README lines 93–94 explicitly names DeepSeek Harness (`dsh`) and `.agents/skills` discovery. — [Local README](../../README.md)

### Inferences

- DSH's closest combination is **Better Sidebar + an artifact visualizer + optional session retrospectives**. This is a composable partial analogue of SPACE, not proof of a ready-made replacement containing the user's full semantic workbench model.
- DSH can become another producer or launch surface for SPACE: a thin plugin can register a result and open its SPACE URL. There is no need to move the canonical questions, decisions and reports into harness-specific session storage.
- Borrow Abid's explicit publish/export, source-event binding, replay and render-error feedback pattern. For SPACE, prefer a stable artifact ID with revisions over a different human-facing URL for every content hash.
- Tiny plugin star counts are evidence of limited public adoption, not proof of poor implementation. Pin a compatible revision and test required behavior rather than selecting by name or core harness popularity.

### Gaps

- User has not yet confirmed a particular DSH plugin URL; this note identifies the harness using local and public evidence, then names specific plugins rather than treating “DSH plugin” as one product.
- No plugin was installed or run. No end-to-end export/authentication test was performed.
- No DSH plugin was verified to natively import both historic Codex and Claude sessions and automatically maintain a first-class question→decision→evidence→artifact graph. That means **not established in inspected sources**, not “impossible” or “none exists.”

## What should SPACE reuse and add?

### Takeaway

SPACE already contains many of the surfaces the user is asking for. The additive opportunity is a shared session/result publication contract and cross-harness provenance, not a new general agent framework or replacement website.

### Cited Findings

- Existing shared host declares session listing/log/keep routes, drawing-save actions and automatic deck/drawing endpoints. — [Host implementation](../../plugins/haipipe-toolkit/servers/_host/serve.py), [host registry](../../plugins/haipipe-toolkit/servers/_host/host_registry.py)
- Existing session implementation reads registered Claude-style JSONL sessions, shows a bounded recent log in the drawer, and can keep full transcript/digest files for page-associated sessions. Re-keeping updates the same identified session rather than indiscriminately collecting all conversations. Inspection of this module did not establish a Codex adapter. — [Session implementation](../../plugins/haipipe-toolkit/servers/workbench/chat.py)
- Existing Studio renderer discovers a topic's HTML slide deck, Excalidraw drawing/preview, Markdown mind map, Work view and Delivery view. It embeds/links these under the topic's existing ownership. — [Studio renderer](../../plugins/haipipe-toolkit/servers/workbench/studio_tabs.py)
- Page Delivery already has **Preview / Artifacts / Checks** surfaces, discovers built files and renders previews. A whole new “artifact viewer” would duplicate this existing capability. — [Page delivery renderer](../../plugins/haipipe-toolkit/servers/workbench/workbench-task-draft/space_views.py)
- Workbench documentation describes Questions with Logic/Work/Report links, source-backed Run states, result headlines, report delivery and Studio drawings. Shared-host documentation calls for a single Page reader and family-owned semantics. These were inspected read-only; descriptions may include historical conventions, so implementation verification is needed before any migration. — [Work workbench documentation](../../plugins/haipipe-toolkit/servers/workbench-work/README.md), [shared host documentation](../../plugins/haipipe-toolkit/servers/README.md)

### Inferences

Recommended design, explicitly proposed rather than an existing implementation:

1. **Keep canonical files and owners.** Questions, decisions, Studio topics, Pages and Run receipts retain their current homes. Build a searchable index/read model over them. Do not create a second decision ledger whose state diverges from the authored record.
2. **Add provider adapters.** Normalize selected Claude/Codex/DSH session references to provider, session ID, turn/event ID, timestamps, scope and source hash. Archive selected source material or retain a secure resolvable reference. Preserve enough provenance to reopen the exact supporting event; a conversation summary alone loses the evidence.
3. **Separate extraction from acceptance.** Agent extraction can propose questions, decisions, actions and outputs. A candidate decision becomes accepted only from explicit evidence or human review, never because an agent summary calls it finished. Keep superseded/rejected state and conflicting sources.
4. **Add a thin result registration/publish operation.** A result needs stable ID, type, owning work scope, canonical file/reference, source session/event, source file hashes, creator, revision, inputs, build status and review state. Discover existing outputs first; permit explicit registration for ambiguous/generated artifacts. Make indexes rebuildable from canonical files.
5. **Use existing renderers.** Page for narrative, current tables for questions/decisions, Studio for drawings, existing HTML deck surface for slides, Page Delivery for exports; attach a sandboxed HTML/SVG dashboard renderer where needed. Avoid executing arbitrary generated JavaScript with the workbench's own origin privileges.
6. **Distinguish snapshot and live data.** A dashboard says which data snapshot/query produced it and when it refreshed. Explicit dependencies should mark it stale when upstream files change; refresh updates a revision with a receipt. A new chat message should not blindly rebuild or overwrite accepted results.
7. **Cross-workbench publication.** One artifact/result index can expose filters by Project, work scope, type, question, source session and status; family workbenches remain projections of the same records. Share an explicitly chosen revision or latest accepted output, not private raw conversation by default.

An initial end-to-end demonstration should use **one Claude session, one Codex session and the same project files**. Produce a question tracker, a decision record, a data dashboard, a drawing and a slide deck, each linked back to its source and owner. Reimporting the same sessions must be idempotent. Revising a decision must preserve its predecessor; changing a dataset must flag the affected dashboard; sharing the dashboard must not expose raw session history. This is a focused product acceptance test rather than a platform rewrite.

### Gaps

- This was a bounded source inspection, not a running-browser audit of every workbench. Existing code presence does not prove all routes currently work.
- No existing general artifact manifest or cross-harness provenance index was confirmed. Further code inspection is needed before naming new files or APIs.
- Exact Codex transcript support elsewhere in the full repository was not exhaustively audited; only the shared workbench/host paths were searched.
