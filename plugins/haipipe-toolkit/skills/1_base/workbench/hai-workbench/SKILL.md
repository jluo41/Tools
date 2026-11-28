---
name: hai-workbench
description: "Open and inspect a SPACE, Project or Block workbench. Resolve a Job, Task, Run or Studio topic to its owning Block before opening it. Holds shared page and material ownership rules. Trigger: wb, open the workbench, open a block, workbench link, /wb, /hai-workbench."
metadata:
  version: "1.36.0"
  last_updated: "2026-11-27"
  aliases: [wb]
---

# Workbench

Open the requested work where it belongs and inspect the records its page displays.
`/wb` and `/hai-workbench` invoke this same skill.

Read [the shared UI constitution](../hai-ui/CONSTITUTION.md) before interpreting or
changing a page. [Work pages](ref/work-pages.md) defines the shared Work and Blueprint
reading rules. The owning theme and record skills define their content and writers.

## Resolve the owner before opening

1. Resolve the SPACE root, requested records and existing host. A Project or theme
   folder is an index; the Block owns the workbench page.
2. For a Job, Task or Run, walk its real folder ancestry to the owning Block. Keep
   the requested Job/Task identity for selection, then pass the **Block path** to
   `cli/wb.py`. Select that Job and Task through the Block's Jobs controls. Do not
   pass the child path as the page destination.
3. For an `sNN` topic, resolve its owning Block and open that topic in Studio. Keep
   the Block's title and route while changing topics or work selections.
4. If the input is words, use `--find` to inspect candidates before opening. Read
   the candidates' faces and choose the place that matches the request. Do not
   infer a Block's type or a Job's use case from a name substring.
5. Resolve a supplied file through the record that owns it. Preview its content
   inside that Block or through its owning material surface.

## Open and verify

Run this skill's `cli/wb.py` from the SPACE with a supported Python interpreter and
its host dependencies. Locate the interpreter from the environment; do not assume
that the SPACE contains `.venv/bin/python`.

```text
/wb                         SPACE Home
/wb 〈Project〉              Project index
/wb 〈Project〉/〈theme〉      theme index
/wb 〈Block〉                the Block's focus page
/wb 〈words〉 --find          candidates, without opening
/wb 〈Block〉 --no-open       verify the page and print its link
/wb restart --root 〈SPACE〉  restart that SPACE's host
```

The launcher discovers hosts rooted at the SPACE and reads its configuration. A
Block or Project is selected by path within that host. Do not start a host rooted
at the Block just to open it. Keep origin, bind address, authentication and terminal
settings intact. `--no-open` suppresses opening a browser; it is not a promise of
no service changes. `--no-restart` prevents restarting an unresponsive host.

For a strictly read-only check, inspect an already-running host directly. If none
is available, report browser verification as pending rather than starting one.

Verify the returned page and requested selection before delivering the link.
Use the host's configured reachable origin, including its Tailscale address when
configured. Repository links remain origin-relative. A failed request is a failed
verification, not proof that the requested records are missing.

## Read and route

Read real records before explaining the page. A file's presence does not establish
completion, acceptance or release. The page's view, item and source address should
agree. Selection and inspection do not execute a Run or rewrite work records.

| Request | Owner |
|---|---|
| Read Work or Blueprint pages and their shared controls | This skill and [Work pages](ref/work-pages.md) |
| Propose or align Work records | `hai-work`, including its `update --check` procedure |
| Create or edit Block, Job, Task or Run records | `hai-block`, `hai-job`, `hai-task`, `hai-run` |
| Studio topics, bindings and drawings | `hai-studio` and the applicable drawing skill |
| Theme-specific page content | The corresponding `workbench-cowork`, `workbench-discovery`, `workbench-paper`, `workbench-insight`, `workbench-design` or `workbench-labeling` skill |
| Draft material, evidence, document delivery or a Page's Runs | [workbench-task-draft](../../draft/workbench-task-draft/SKILL.md) and the writer it names |

For Work record alignment, load `hai-work/ref/update.md`. Its commands are
agent procedures; do not substitute an unrelated CLI command that changes folders
or execution metadata. List concrete changes and follow the repository's approval
rules before writing.

## Page material ownership

A material surface has four responsibilities: storage, presentation, one writer,
and a discovery boundary. [The storage roster](ref/roster.md) locates material
owners. Resolve a row with its owning skill before writing to its storage.
A folder does not require a separate callable skill or a new top-level tab.

- Authored drawings, kept conversations and writing feedback are original records.
  Preserve them and use their owning writer. A generated preview is not a substitute
  for the authored source.
- Derived exports are generated by their declared builder. Verify inputs and the
  target path before rebuilding; do not overwrite human edits as a side effect.
- Page discovery must not treat material folders or conversation transcripts as
  new independent pages.
- An imported file becomes evidence only when the evidence owner records its
  binding. Result existence and a successful export do not grant acceptance.

The Page workspace's Draft, Evidence and Delivery content is governed by
[workbench-task-draft](../../draft/workbench-task-draft/SKILL.md). Its
[Run contract](../../draft/workbench-task-draft/ref/run-space.md),
[delivery contract](../../draft/workbench-task-draft/ref/delivery.md) and
[folder contract](../../draft/workbench-task-draft/ref/folder.md) own those details. Studio
owns its drawing and conversation material. Domain surfaces retain their theme
contracts and writers. Do not duplicate these storage grammars here.

An applicable Page material surface uses the shared registry's
`id`, `label`, `hint`, `order`, `applies`, `open` and `tab` fields. Keep one picker
and one applicable registry order. A surface without its presenter or writer is
not applicable. Preserve per-page open tabs and live editors while switching;
a close action affects only its own tab and must not also activate the tab beneath
it. Read the owning surface contract before altering its controls.

## Share and host operations

Sharing uses this skill's `cli/wb_share.py` through `cli/wb.py`:

```text
/wb share 〈folder〉 〈email〉
/wb 〈folder〉 share
/wb share --serve 〈SPACE〉
```

Read the SPACE's `.server_config/access.yaml` and effective configuration. A share
host is distinct from the SPACE's owner host; access is bounded by the declared
folder grants and roles. Preserve the configured authentication. Secrets and
access grants remain deployment configuration, outside repository defaults.
A request to open a page does not authorize adding recipients or changing grants.

Coordinate an authorized shared-host restart with active sessions, use its existing
launch settings, then verify the affected Block. Do not restart every SPACE as part
of one page inspection.
