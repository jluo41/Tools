# Block folder: the Folder part, made and named s09

## Ask

JL 261012: "我想创建一个 s09。这个 s09 我们是要创建 folder，也就是在 related 和 timeline 下面再搞一个 folder，这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）都长什么内容。" Then: "where is our s09 for this, I want to make it to be the s09-block-folder, do you get it?"

## Summary

Built Studio › Folder: the Block folder as one tree; a folder says its count and what it is for, a file opens in the pop-out; folder rows load when opened via view=dir, 300 then a button (s09-D11 to D13). First made as s33-studio-folder, then renamed s09-block-folder at JL's ask (s09-D10): its decisions start at D10 since the old s09-D01 to D09 live in s01, and the old runs/run-draw-s09 moved to s01 history/. Drawn as two frames: the Folder on screen, read from disk, then how a row is read. Checked on 5623 in a browser; tests 151 passed.

## Changed

- `plugins/haipipe-toolkit/servers/workbench/frame.py (studio_folder · folder_rows · folder_word · _run_word · Folder CSS and loader)`
- `plugins/haipipe-toolkit/servers/workbench/frame_view.py (view=dir)`
- `studio/s09-block-folder/ (face · builder · drawing · preview)`
- `studio/s01-overall-tree-structure/history/run-draw-s09/ (the old s09 session moved here)`
