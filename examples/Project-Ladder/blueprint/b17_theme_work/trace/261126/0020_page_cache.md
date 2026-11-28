---
title: page cache
date: 2026-11-26 00:20
work: [j11t01]
aim: "A focus page is built once into a file and served from it; the build records every file and folder it reads (in its Block or outside it), and each open rebuilds only when one of them, the loaded code or the date changed."
closed: true
plan:
  - do: add
    path: examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0020_page_cache.md
    what: this trace's own record, written first
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/page_cache.py
    what: the fingerprint, reading a built page and writing one, under ~/.cache/haipipe/pages/
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py
    what: the focus page is served through page_cache (serve.py routes /_board/workbench here)
  - do: add
    path: plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_page_cache.py
    what: a second open reads the file; a changed face, a new file or a removed file rebuilds it
  - do: edit
    path: plugins/haipipe-toolkit/servers/workbench/README.md
    what: where built pages are kept and when they are rebuilt
changed:
  - examples/Project-Ladder/blueprint/b17_theme_work/trace/261126/0020_page_cache.md
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/page_cache.py (new)
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/frame_view.py (the focus page through page_cache)
  - plugins/haipipe-toolkit/servers/workbench/page/block_index_page/tests/test_page_cache.py (new)
  - plugins/haipipe-toolkit/servers/workbench/README.md
---

# page cache

## Prompts

- **00:05** I think here we might also need to consider how to make the laoding be quick, and eventually, you know, we donot generate hmtl in real time, it is the file to be rendered into the UI, do you get it?
- **00:12** I am not sure what is the best methods, what is your thoughts?
- **00:20** go

## Check

- What the b17 page reads, recorded by an audit hook: 1234 paths in the Block, 115 outside it (85 skill folders for the Skills part, other example Blocks, .server_config/workbench-examples.json) and one `git log`. So the check follows what the build read, not the Block folder alone.
- 5623, b17: open 1 0.90 s, open 2 0.035 s, open 3 0.031 s; the cached page is byte for byte the built one; a touched j11 face builds again (0.77 s), then 0.033 s.
- 5602, 5607, 5599 restarted: a Block opens twice, the second from the file (0.011 to 0.044 s); no traceback since the restarts.
- test_page_cache.py 6 passed; workbench 308 passed with the reader's known 6 failures; _host 152, workbench-work 62, workbench-design 58, workbench-insight 69, workbench-labeling 85 passed; workbench-paper 114 passed and 1 failed (test_build_in_progress, failing with the cache off too: another session's paper work, not this change).

## Summary

A focus page is a file now: built once, served from ~/.cache/haipipe/pages/, built again only when a file or folder it read, the loaded code or the date changed.
