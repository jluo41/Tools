# A04 · Every link to a page lands on the focus page, never the old tabbed frame

> "the […] old style" (JL 261118, opening /w/b12_<block> on its SPACE's port; relayed by a Project session)

## 1. Need
A short link to a Block (`/w/<block>`, `/b/<block>`) opens the page JL works on: the focus page with its
numbered sections (Report, Studio, Delivery), not the retired tabbed frame.

## 2. Now
`home_routes.resolve_workbench` returned `home_boards.frame_url(rel)` = `/_board/workbench?path=<rel>` with no
layout. `frame_view.workbench_frame_view` drew the focus page only when `layout=focus`, so the short route,
and every bare `?path=` link, fell through to `frame.render`: Guide · Studio · Block · Job · Task · Delivery.

## 3. Gap
- The focus page was added beside the frame as an opt-in (`layout=focus`), and the default was never flipped.
- `frame_url` kept its 261007 meaning ("every Block opens in the base frame").
- The short-route test pinned the old address, so nothing failed.

## 4. Methods
1. Add `layout=focus` to `frame_url` only: fixes `/w/` and `/b/`, but any other bare link still lands on the frame.
2. Also make a bare address (only `path`, `theme`) the focus page, keeping the frame on `layout=frame` and on its
   own `tab`/`sub`/`view`/`format` keys: chosen; it fixes every writer of a bare link at once.
3. Delete the old frame: too wide today; its tab views still serve Page Task views and JSON.

## 5. Update
- `servers/workbench/home/home_boards.py`: `frame_url` adds `&layout=focus`
- `servers/workbench/page/frame_view.py`: bare address renders the focus page
- `_host/tests/test_workbench_short.py`, `workbench/tests/test_focus_runs.py`: expect focus; frame on `layout=frame`
Live, a SPACE's server (restarted): `/w/b01_<block>` → `…&layout=focus`; bare `?path=` → focus;
`&layout=frame` → old frame. Suites: 621 passed.
Cases: ✅ short routes · ✅ Home Block links · ✅ any bare link · ⬜ other servers until restarted.

## 6. Never again
- The default is now the focus page, so a new link written without `layout` cannot reach the old frame.
- The two route tests fail if `frame_url` or the default changes back; `/haistack sweep` reruns them.
- Still open: a server shows the change only after it restarts.
