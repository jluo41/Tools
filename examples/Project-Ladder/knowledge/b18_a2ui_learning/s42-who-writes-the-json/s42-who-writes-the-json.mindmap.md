---
mindmap: 1
title: Who Writes the JSON?
written: yes
---

# Who Writes the JSON?

- The model writes <!-- branch-0 -->
  - A2UI Express between <a2ui> tags <!-- node-0-0 -->
  - $/path = value lines set data <!-- node-0-1 -->
  - root = Card(...) is the component tree <!-- node-0-2 -->
- The SDK compiler <!-- branch-1 -->
  - Runs on your agent's server <!-- node-1-0 -->
  - Checks against the catalog <!-- node-1-1 -->
  - Emits createSurface, updateComponents, updateDataModel <!-- node-1-2 -->
- The client receives <!-- branch-2 -->
  - Only JSON messages <!-- node-2-0 -->
  - Never sees Express <!-- node-2-1 -->
