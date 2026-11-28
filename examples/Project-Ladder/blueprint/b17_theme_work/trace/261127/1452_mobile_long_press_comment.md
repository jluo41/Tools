---
title: mobile long press comment
date: 2026-11-27 14:52
work: [s74]
aim: "On a phone, a long press of about 500 ms on any page element lights it up with a thin border and opens the element menu that a right-click opens on a desktop (Info, Comment, Copy address); Comment opens the comment card as a bottom panel that stays above the software keyboard. The page gains no standing button or icon. A move, a scroll, a pointercancel or a second finger cancels the press; a press inside an input keeps the browser's own text selection; a tap on blank space closes the menu and the highlight; the desktop right-click is unchanged; a touch browser's own contextmenu event never opens a second menu. Comments use the existing element address and the one writer, POST /_board/item-card."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1452_mobile_long_press_comment.md
    what: this trace's own record, written first
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
    what: "STYLE and SCRIPT: a touch long-press entry beside the contextmenu one (one shared menu opener), its cancels, the duplicate-contextmenu guard, and the comment card as a bottom panel above the keyboard on a touch press; the about list and about(el) of trace 1342 kept"
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/element_marks/tests/test_element_info.py
    what: tests that the layer carries the long-press entry, its cancels and the bottom panel, and still the contextmenu entry
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261127/1452_mobile_long_press_comment.md
  - plugins/haipipe-toolkit/servers/workbench/page/element_marks/element_info.py
  - plugins/haipipe-toolkit/servers/workbench/page/element_marks/tests/test_element_info.py
---

# mobile long press comment

## Prompts

- **14:20** (delegated by the coordinating session, on JL's word "开始去执行，发 message 给他们") build the phone long-press comment entry of b17 s74 UI Plugin: read-only check and a file plan first.
- **14:50** Go for the three listed files. Relayed by Codex on JL's delegation ("你就直接输入Go吧，代替我去输入Go吧"); not typed by JL in this terminal.

## Coordination

- b17_theme_work (SendMessage, answered): no unfinished change or open trace on element_info.py; keep the about list and about(el) of trace 1342; this session may restart 5623 with the same command. The S71 What/Why/Must show label column is its own (hai-studio/scripts/type_requirements.py), not touched here.
- Before the edit: element_info.py unchanged since 13:42 (md5 aacbf8b8…), 126 lines, untracked in git.

## Check

- Unit tests: `PYTHONPATH=_host uv run --python 3.13 --with pytest --with pyyaml python -m pytest workbench/page/element_marks/tests workbench/side_pane/files_tree/tests`: 50 passed (3 new checks in test_element_info.py).
- Scratch server, 127.0.0.1:5673 over a temp copy of examples/Project-Ladder/work/b01_example_work, headless Chromium with iPhone 13 and Pixel 7 touch emulation (touches sent by Input.dispatchTouchEvent), 25 checks passed: a short tap opens nothing; a move, a scroll, a second finger and a pointercancel each cancel the press; an 800 ms press opens one menu with the element outlined, inside the screen, and it survives the lift; a tap outside closes menu and outline; Comment opens the card as a full-width bottom panel with the box focused at 16px; with the visual viewport made 300px shorter the panel sits 300px up; a press inside the comment box arms nothing; a comment saves through POST /_board/item-card and after a reload is bound to the same address (el.title); desktop right-click opens the menu and the floating 360px card, a press outside closes it, a left click opens nothing.
- Duplicate guard, by a synthetic contextmenu event (the emulator sent none of its own): one arriving after the timer is prevented and the menu stays one; one arriving before the timer opens the one menu at once and the timer adds nothing. A menu for an element at the bottom edge is lifted into the screen.
- Found on the real page and fixed: a press on a fold with a path sent wb:show-files, and the phone's Files drawer opened over the menu. A touch press no longer sends it; the desktop right-click still does.
- 5623 restarted twice with its own command (agreed with b17_theme_work), then the b17 Studio page rechecked with the same emulation: move cancels, long press opens one menu on el.page.fold.s31-ui-plugin-files, Comment opens the bottom panel, a tap outside closes, desktop right-click opens the menu, no page errors. No comment was saved on the real Block.
- Not checked: a real phone. iOS Safari's own text-selection callout, a real software keyboard's height and Android Chrome's real long-press contextmenu were only emulated or simulated.
- At restart serve.py printed that its python has no claude_agent_sdk (chat would answer 400); the command is the one the server ran with before.

## Summary

A long press of 500 ms on a phone opens the element menu a right-click opens on a desktop, and Comment opens the comment card as a bottom panel above the keyboard, saved by the existing writer under the element's address. Checked by touch emulation in headless Chromium, not on a real phone.
