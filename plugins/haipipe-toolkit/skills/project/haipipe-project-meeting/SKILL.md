---
name: haipipe-project-meeting
description: >-
  Keep and route a meeting record at project or SPACE level. One dated Folder
  holds a required digest and optional transcript; decisions are routed into
  the owning Pages' Outline records rather than attaching the meeting to one
  Page. Trigger: keep meeting notes, meeting digest, project meeting,
  workspace meeting, route meeting decisions, /haipipe-project-meeting.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-project-meeting · one conversation above the Pages it changes

Meetings are project/SPACE source records, not Page plugins. A conversation
may affect several Pages; storing it beside one Page makes that Page a false
owner and hides the other routes.

## 🧭 Resolve the owner

```text
one project affected       <project>/meetings/<YYMMDD-HHMM>/
several projects affected  <SPACE>/meetings/<YYMMDD-HHMM>/
```

Use the narrowest true owner. The server or executing agent stamps the time;
never trust a client clock. `meetings/` is optional and appears only when the
first record is kept; project scaffolding does not create an empty lane.

## 🗂 Record shape

```text
<owner>/meetings/
└── <YYMMDD-HHMM>/
    ├── digest.md       REQUIRED · decisions, open questions, reading path
    └── transcript.md   OPTIONAL · raw conversation, reference only
```

The writer only adds a dated Folder; it never rewrites or deletes a kept
record. If the digest is empty, do not keep the meeting.

## 🔀 Route effects, do not copy the meeting

After keeping the source record, inspect each decision and question:

```text
unsettled Page question  → <page>/outline/<stem>-discussion.md · D<nn>
settled Page decision    → <page>/outline/<stem>-log.md        · dated record
plan change              → haipipe-page-outline                · new plan version if frozen
content change           → haipipe-page-content                · WRITE cycle
task work                → owning Task Folder                  · new Run or rerun
```

Every routed row cites the repository-relative meeting digest path. The Page
stores only the effect and provenance, never a copied transcript or a new
`meeting/` lane.

Legacy `<page>/meeting/` folders are read-only migration input. The Board
server no longer exposes Page-local meeting writers; move a legacy record only
when its true project/SPACE owner is known, preserving its original dated name.

## ✅ Return

```text
owner:     <project|SPACE path>
record:    meetings/<YYMMDD-HHMM>/digest.md
routed:    [<Page or Task addresses changed>]
unrouted:  [<items needing an owner decision>]
```

## 📂 Related contracts

- `../haipipe-project/SKILL.md` · project/SPACE container ownership
- `../../board/page-workflows/haipipe-page-outline/SKILL.md` · discussion and plan routing
- `../../board/page-workflows/haipipe-page-content/SKILL.md` · content routing
