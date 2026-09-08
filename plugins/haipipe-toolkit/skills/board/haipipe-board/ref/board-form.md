# Board source contract

This file defines current Board source shape. `SKILL.md` owns routing;
`operations.md` owns procedures; `haipipe-page` owns the Page Face.

## Board kinds

| Kind | Declaration | Membership | Reader projection |
|---|---|---|---|
| Generic | omit `board-kind` | Page-shaped Markdown below the Board root | Q/S Pages grouped and ordered by `## Pages` |
| Task Block | `board-kind: task-block` | direct `jNN_*/tNN_*` Task tree | Block → Board, Job → Group, Task → Page |
| Discovery Block | `board-kind: discovery-block` | direct `jNN_*/tNN_*` Discovery tree | Block → Board, Job → Group, Discovery Task → Page |

The kind changes discovery and projection only. It does not change the base
Page contract or create a new Page Type.

## Generic Board tree

```text
<owner>/diagram/<NN>-<topic>-<YYMMDD>/
├── board.md
├── 1-G1-<group-slug>/
│   ├── draw/group.excalidraw
│   └── G1-<slug>/
│       ├── G1-<slug>.md
│       ├── outline/
│       ├── workflow/
│       ├── studio/
│       ├── runs/
│       └── delivery/
├── 2-QB-<group-slug>/
├── fig/
├── _archive/
└── board/                         generated
```

The Board folder normally lives under the owning task, project, or paper. A
plugin skill-design Board lives under the plugin's `skills/diagrams/` folder.
`NN` orders Boards within one topic series. The date is the creation date and
never changes.

One Group uses one descriptive folder. Its numeric prefix mirrors `## Pages`
order; its Q letters carry identity. A Page normally owns a same-stem Folder.
A Page may instead live inside the subject folder it describes when that tree
already supplies the correct ownership boundary.

Only these stay at the Board root: `board.md`, Board-owned maps, `fig/`,
`_archive/`, and generated `board/`.

## Task or Discovery Block tree

```text
bNN_<block>/
├── board.md
├── jNN_<job>/
│   ├── src/
│   ├── workflow/
│   ├── results/
│   └── tNN_<task>/
│       ├── tNN_<task>.md
│       ├── scripts/
│       └── runs/
├── diagram/
└── board/                         generated
```

The Task tree supplies membership and default order. A Task Page declares:

```yaml
folder-kind: task
task: .
```

Its compact Board id is derived from the path, for example `b02j01t03`. Run is
never a Board Page. Generated Results remain at the Task dialect's resolved
Job Results path.

A Discovery Block uses the same structural projection but declares
`board-kind: discovery-block`; its Pages declare `folder-kind: discovery`, and
its Paper/Source Results remain Folder-local under each Discovery Task.

## board.md

```markdown
# <Board title>
board-kind: task-block   # Task Block only
spine: <one sentence naming the problem this Board organizes>
close: <one observable condition for closing the Board>
source: <optional source address>

## Topic
<context a new reader needs before choosing a Page>

## Pipeline
<actual dependencies among Groups and Pages>

## Board Map
<optional ASCII relationship map>

## Board Structure
<optional source-versus-generated explanation>

## Pages
### G1 · <group title>
<optional one-line introduction>
G1-<slug>.md

## Links
<optional label-to-path declarations>
```

Required fields are title, `spine`, `close`, `## Topic`, `## Pipeline`, and
`## Pages`. `board-kind` is required only for a non-generic dialect.

`## Board Map` shows relationships, not a second Page roster. Page and Group
ids inside an ASCII map become links. Use one map source; do not declare
competing ASCII and external-canvas maps.

`## Board Structure` explains the Board only when a new reader needs it. Keep
the editable source tree separate from the generated web routes.

## Pages is presentation, not membership

A Generic Board discovers supported Page filenames anywhere below its root,
excluding hidden, generated, archived, and plugin-owned segments. `## Pages`
then assigns their display Groups and order. An unlisted Page remains visible
under a warning Group; registration failure must not hide work.

Page filenames must be unique across a Generic Board. Q ids use
`Q<group><number>-<slug>.md`. S lifecycle Pages use
`S-<Family>-<unit>-<slug>.md`. Filename slugs are short lowercase recognition
labels; ids, not slugs, carry identity.

A Task Block discovers only direct Job/Task Pages. `## Pages` may contain Job
headings without restating every Task. An explicit Task row uses its full
Board-relative path; a bare filename is accepted only when unique.

Plain lines after a Group heading and before its first Page row are the Group
introduction. The first line is always visible; additional lines may fold.

## Page source

Current Q and S Pages use the base order:

```text
Opening → generated Outline → Content → Aims
```

`## Opening` and `## Aims` are always required. Q Content is optional. S
Content is required. An S may carry `## Stage Contract`; manuscript Section
requirements resolve through the Page Outline workspace.

Do not author these retired process sections on a current Page:

```text
## States
## Files
## Discussion
## Log
```

Their current homes are records under `outline/`. Do not author `## Outline`
or `## Diagram`; the renderer projects the current versioned plan, while Draw
lives under `studio/draw/`.

An Aim is one stable row with its target, test, and current fact:

```markdown
## Aims
### A1 · <Content division name>
- ⬜ A1.1 · <durable target>
  **Done when:** <observable test>
  **Now:** <current fact>
```

Aim status vocabulary is `⬜` not started, `🔨` active, `🧠` waiting on a
ruling or external input, `✅` met, and `❄️` deliberately held. Page `state:`
uses `🔴`, `🟡`, `✅`, or `⏸️` and is a different field.

## Page-local records

```text
<page>/outline/
├── <stem>-context.md
├── <stem>-outline-v<G>.<S>[.<E>].md
├── <stem>-evidence-items.md
├── <stem>-requirement.md
├── <stem>-feedback.md
├── <stem>-discussion.md
├── <stem>-files.md
└── <stem>-log.md
```

The Outline plugin owns their schemas. Writers append or regenerate the
specific record they own; they do not recreate Page-level process sections.

## Links and embeds

`## Links` maps a stable label used in Page prose to a real path relative to
the Board root:

```markdown
## Links
SKILL.md  ../../haipipe-board/SKILL.md
```

Declared paths must resolve. Ordinary Markdown links are also supported.

A whole-line embed reads a source at build time without adopting it as a Page:

```text
![[path/to/file.md]]
![[path/to/file.md#Section]]
![[path/to/file.md#Section|source]]
```

The optional section selects one heading. `|source` renders bytes rather than
interpreting Markdown. Nested embeds do not expand recursively. The source is
never modified through the consuming Page.

## Body grammar

| Source form | Meaning |
|---|---|
| `### n · name` | one Content division |
| `**n.m · name**` | a labelled group of related items |
| `#### n.m.k · name` | one paragraph heading |
| `(job line)` immediately after `####` | the paragraph's scan-level job |
| `- heading` plus indented explanation | one folded item |
| fenced block | code, data, or copy-safe ASCII figure |
| `> Comment WHO …` | sentence-local comment |
| `> ✎ …` | sentence-local edit record |
| `> Card <words>: …` | card bound to words in the preceding sentence |

One prose sentence occupies one source line. Sentence-local apparatus binds by
adjacency to the preceding sentence. A Page-level concern belongs to an Aim or
an Outline record, not to an unattached sentence lane.

## Generated site

```text
board/
├── index.html
├── <GROUP>.html
├── <GROUP>/<page>.html
└── _assets/
```

The Index carries Board orientation, relationships, roster, and aggregate
status. A Group route carries that Group and its Pages. A Page route keeps one
Page focused while preserving Board navigation.

All essential content and navigation must remain available without JavaScript.
Scripts may enhance drawers, live navigation, Chat, terminal, comments, and
plugin surfaces; they may not become the content source.

## Compatibility boundary

The parser may continue to read historical aliases and retired sections so an
old Board can render. Compatibility is read-only: current templates,
generators, browser writers, and instructions must emit only the shape above.
Compatibility schemas that still require documentation live under
`ref/legacy/` and are never loaded for current authoring.
