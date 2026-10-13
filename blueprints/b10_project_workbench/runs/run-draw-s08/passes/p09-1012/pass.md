# Timeline: stay in place on a group pick

## Ask

JL 261012: "当我 click（点击）这些 button 的时候，它会跳到最上面，而不是留在 timeline 这里。你知道这该怎么处理吗？"

## Summary

Picking a group hid the topic cards above, so the page shrank or grew and the Timeline left the screen (its toolbar went from 969 px to 391, then 1247). keep(fn) now scrolls by how far the toolbar moved. In a browser on 5623 it stays at 459 px through Guide and by group, and at 524 px through Levels and All. It moves only when the page above is too short to hold it in place (s08-D15).

## Changed

- `plugins/haipipe-toolkit/servers/workbench/frame.py (.tl-map handler keep)`
- `studio/s08-studio-timeline/ (face D15)`
