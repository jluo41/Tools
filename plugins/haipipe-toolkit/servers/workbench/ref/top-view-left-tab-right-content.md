# top-view-left-tab-right-content

The layout inside one open fold when the fold holds several kinds of view, each with one or more things (JL 261125:
"I want to give it a name, this framework"). Short name: **top-view-left-tab**.

```text
top-view        [Page]  Draw   Delivery                    the kinds of view
left-tab        ▌Metro map    •──────────────────────•     the things in the picked view
                 Marks + card │                      │
                 Metro, by …  │   right-content      │     the picked thing
                 Tree + …     │                      │
                              └──────────────────────┘
                hide dot •  on the frame's top-left corner      open dot •  on its top-right corner
```

## The three parts

1. **top-view**: a row of buttons, one per kind of view the fold has (Page, Slide, Draw, Work, Delivery; no
   MindMap, its file stays in Files). Only the kinds that exist show; the first is picked. The row is one line and
   never wraps: when the buttons do not fit, it scrolls left and right (`.studio-view-buttons`, `.top-views`, `.jov-views`).
2. **left-tab**: the things inside the picked view, one tab each, as narrow as the longest name. An earlier version
   reads faded (opacity .5), never under a word like "Earlier".
3. **right-content**: the picked thing in one frame (`.pb-panel`), loaded only when its tab shows.

A view with one thing has no left-tab; the thing takes the full width.
One exception: a UI preview topic's Page and Effect (`hai-studio` ref/ui-preview-topic.md) keep their left-tab
even for one view, so another view or effect is one more tab. So does a Job's Brief fold (Goal, Requirements,
MindMap): each top view opens left tabs and the framed content, a single thing too.

## The two dots

No words around the frame (AGENTS.md › UI design). Two grey dots sit on its top corners and say what they do on hover:

- **hide dot**, top-left (`.pb-fold`): hides the left-tab, the frame then starts at the left edge with no margin; a
  second click brings it back. One choice for every list in this browser (`localStorage['wb:pb-folded']`). The
  frame's left line runs down from the dot.
- **open dot**, top-right (`.open-dot`): opens the picked thing (popped out, or its own tab); hover reads
  "Open <name>". Never an "Open <name> ↗" button under the frame.

On a phone (700 px or less) the left-tab is a row on top and the hide dot does not show.

## Code

| piece | where |
|---|---|
| left-tab and right-content, the hide dot | `servers/workbench/page/parts_and_map/ui_parts.py` › `_side_tabs`, `PB_CSS`, `PB_JS` |
| the open dot | `ui_parts.open_dot(inner, href, name, pop, new_tab)` |
| top-view in a Studio fold | `servers/workbench/studio/tabs/studio_tabs.py` › `render` (`.studio-view-buttons`) |
| a page's own previews as left-tab | `studio_tabs.page_items`: the `<button data-src>` of a topic's `<sNN>.html`; `class="old"` reads faded |
| the UI view's live pages | `servers/workbench/page/parts_and_map/focus_ui.py` › `ui_view.live` |

## Example

`examples/Project-Ladder/blueprint/b17_theme_work`, Studio, `s06 · Files pane`: top-view Page · Draw · Delivery;
Page's left-tab Metro map, Marks + card, then three faded earlier previews; the Metro map on the right.

## Where it sits among the page parts

`view-button-list` › `band` › `fold` › **top-view-left-tab-right-content** (hai-ui SKILL.md › Page parts). The
view-button-list switches the views of a section; a top-view switches the views of one fold.
