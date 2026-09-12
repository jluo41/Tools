# Haipipe-page: ownership and workflow
state: 🟡 Initial Page draft; Outline approval pending
owner: Codex

## Opening

Haipipe-page turns one document into a continuing workspace: its own source, readable Page, planning records, and delivery files.
This Page explains how to create and revise that workspace, how its plugins use the same files, and how Board can organize it without owning its content.

**Covered elsewhere**: Board group descriptions and ordering belong to haipipe-board; plugin implementation details belong to each plugin's own skill.

## Content

### 1 · Page ownership

**Division map**: editable sources and generated delivery in one Page Folder.

```text
Page Folder
├── page.toml         source registration
├── Page.md           Opening · Content · Aims
├── outline/          plan · context · evidence
└── delivery/web/     generated reading site
```

#### 1.1 · Source and delivery
(Identify the files to change and the files to rebuild.)
A Page Folder owns the document and the records used to develop it. <!-- realizes: C1.P1.B1 -->
For this Page, the editable document is haipipe-page-guide.md; page.toml selects that document as the entry. <!-- realizes: C1.P1.B1 -->
The website is generated from that source, so a later build must not depend on edits made only to delivery files. <!-- realizes: C1.P1.B2 -->
When starting from an existing HTML file instead, the Page skill imports an editable copy and binds it as Content. <!-- realizes: C1.P1.B3 -->

### 2 · Board and plugins

**Division map**: Board navigation and plugin workspaces share the Page's sources.

```text
Board membership ──▶ Page Face
                       │
                 Page Folder
                 ├── Outline   planning and evidence
                 ├── Studio    chat and drawing
                 ├── Runs      tickets and results
                 ├── Delivery  generated outputs
                 └── Folder    file inventory
```

#### 2.1 · Shared content authority
(Separate Page ownership from Board organization.)
Board supplies grouping, ordering, and navigation by registering the same Page Face. <!-- realizes: C2.P1.B1 -->
Removing that membership should leave the Page Folder and its content intact. <!-- realizes: C2.P1.B1 -->
Plugins present the Page's planning records, conversations, runs, outputs, and files through their own declared writers. <!-- realizes: C2.P1.B2 -->
A plugin is not enabled merely because a folder or a button bears its name; its surface must reach the real records and supported actions. <!-- realizes: C2.P1.B3 -->

### 3 · Continuing work

**Division map**: feedback changes a bounded source before delivery is refreshed.

```text
Your request
    ↓
Context and current plan
    ↓
Candidate change + feedback record
    ↓
Explicit scoped acceptance
    ↓
Adopted Content → refreshed delivery
```

#### 3.1 · Scope and acceptance
(Show how to continue work without losing prior decisions.)
A request to revise Opening sets the editing boundary; it does not authorize rewriting the rest of the Page. <!-- realizes: C3.P1.B1 -->
During planning, the Outline workspace pairs each planned point with candidate prose for discussion. <!-- realizes: C3.P1.B2 -->
A Writing Run preserves the goal and feedback history through Versions and Steps, while accepted wording is adopted into Content through the Page workflow. <!-- realizes: C3.P1.B3 -->
Those records do not imply that a browser button executes an agent, and accepting one passage does not accept the whole Page. <!-- realizes: C3.P1.B3 -->


## Aims

### A1 · Page ownership
- 🔨 A1.1 · The reader can identify the editable Page and its generated site.
  **Done when:** source selection and a current rendered Page are checked independently of Board.
  **Now:** page.toml resolves the Markdown Face; the Page CLI builds it and the standalone server renders the standard Page with its generated Outline.

### A2 · Board and plugins
- 🔨 A2.1 · Page and Board share one content authority.
  **Done when:** ownership and membership are explicit, and each claimed plugin capability has been exercised.
  **Now:** standalone Page exposes Outline, Runs, Delivery, and Folder through the same category-plugin order as Board. Evidence remains inside Outline; Studio is omitted until its chat/draw backend is available. No Board membership is registered.

### A3 · Continuing work
- 🔨 A3.1 · Subsequent feedback can target the real Page records.
  **Done when:** the real Outline and source open, and supported edits are distinguished from unavailable actions.
  **Now:** this is an initial draft, not an accepted Content release; the hosted workspace is read-only and no browser-triggered Writing Run is claimed.

### P · Page-level
- ⬜ P1 · The Page satisfies the user's requested workflow.
  **Done when:** the user reviews the standard Page and its actual workspaces and accepts the requested scope.
  **Now:** not accepted; the earlier custom HTML is retained as an unused draft, not the current Page entry.
