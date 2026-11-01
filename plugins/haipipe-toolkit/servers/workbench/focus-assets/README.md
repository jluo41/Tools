# Focused page

Content uses one full-width item per row at every viewport size. Keep question
cards and other content lists in a single vertical column, never side by side.
Show section content directly. Do not add disclosure triangles or click-to-expand
containers for completion criteria, linked work, reasoning, or folder rows.

There is no mode selector. Each side is one navigation rail: quiet marks become
names in place when the pointer enters, and return to marks when it leaves.
Keyboard focus also reveals names; Escape closes them. On touch screens, the
first tap reveals names and the next tap follows a link. Old mode preferences
are ignored. The content stays in place during navigation reveal.

Open `/_board/workbench?path=<folder>&layout=focus`. The existing route without
`layout=focus` keeps its existing presentation. This is a read-only presentation;
it does not execute work or generate or rewrite Markdown.

The current folder's `<folder>.md`, falling back to `board.md`, owns its content:

| Section | Source, in precedence order |
|---|---|
| Goal | `## Goal`, `goal:`, `spine:`, `develops:` |
| Completion criteria | `## Completion criteria`, `close:` |
| Takeaways | `## Takeaways` only |
| Goal question cards / Questions | Current face's Questions register, preserving order and wording |
| Context / Pipeline | Current face's Topic / Pipeline sections |
| Reports | Registered report files: first Opening paragraph, state and results-read date |
| Deliverables | Current face's Deliverables register, with existing file links |
| Jobs / Job-Versions / Tasks | Direct child folders, using the existing level reader |
| Studio-All / Studio-group | This folder's Studio topics and their recorded tags |
| Timeline | Dated entries in this face's `## Log` |
| Folders | Two visible folder levels inside the serving root; deeper folders link to their own page |

Work defaults to Goal; Paper defaults to Takeaways. Other themes prefer authored
Takeaways, otherwise Goal. A face can set `home-section: goal` or
`home-section: takeaways`, in YAML front matter or its existing header fields.
An explicit `section=goal` or `section=takeaways` URL chooses an available section.
The other section is offered when its content exists. Missing content is stated,
never summarized from Studio or inherited from the parent. Reload rereads the face.
Goal completion criteria are always visible. Results and completed files do not imply
that the goal was accepted.

Sibling and section rails use the same name-only interaction, with no preview
bubble or summary. The current item has a longer mark and its name is highlighted
when revealed. Section links preserve `layout=focus`, and browser Back restores the prior
URL. Drawing and document links use the existing viewers. Mind maps render their
Markdown live in read-only mode. A missing representation has no invented preview.

Run the focused regression checks with the workspace Python and
`PYTHONPATH=servers/_host python -m unittest discover -s servers/workbench/tests -p test_focus_page.py`
from the plugin folder. Real page checks should cover both a work face with
`spine:` / `close:` and a paper face without Takeaways.

## Existing Overview–Report view

A face may opt in with `home-section: overview-report`. Its `overview-map:` field
names an existing `.mindmap.md` relative to that face; only files within the
serving root are rendered. The existing live map viewer handles the map.
Overview and Reports are local views under the same right-rail entry. The URL
`section=overview-report&group=reports` selects Reports; the older `section=reports`
link resolves to that same view for an opted-in face.

Reports reads the registered source pages and keeps recorded answer status,
acceptance criteria and existing `work:` links together. Execution completion
does not establish goal acceptance. No separate Item store or generated preview
is required. Pages without this opt-in retain their current default view.
