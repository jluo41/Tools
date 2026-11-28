---
title: PRINCIPLE.md and the cNN chat folder
date: 2026-11-21 00:46
aim: A plugin is a Folder System, a UI System and the map between them (PRINCIPLE.md); a kept chat is a Block folder (cNN, retired 261126 for trace/).
closed: true
plan:
- do: edit
  path: AGENTS.md
  what: a pointer to PRINCIPLE.md
- do: add
  path: PRINCIPLE.md
  what: how a plugin is designed
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat/SKILL.md
  what: hai-chat, retired 261126
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat/ref/chat-contract.md
  what: hai-chat, retired 261126
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat/scripts/new_chat.py
  what: hai-chat, retired 261126
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat/scripts/qa.py
  what: hai-chat, retired 261126
- do: add
  path: plugins/haipipe-toolkit/skills/1_base/project/hai-chat/tests/test_new_chat.py
  what: hai-chat, retired 261126
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_frame_sessions.py
  what: hai-chat, retired 261126
changed:
- AGENTS.md
- PRINCIPLE.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-chat/SKILL.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-chat/ref/chat-contract.md
- plugins/haipipe-toolkit/skills/1_base/project/hai-chat/scripts/new_chat.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-chat/scripts/qa.py
- plugins/haipipe-toolkit/skills/1_base/project/hai-chat/tests/test_new_chat.py
- plugins/haipipe-toolkit/servers/workbench/side_pane/rail_sections/tests/test_frame_sessions.py
---

# PRINCIPLE.md and the cNN chat folder

## Prompts

- **00:46** please pull the latest code from remote.
- **00:50** What I want to have is. File Systems for skill folder structure , and block folder structure, and UI Systems how the file system is mapped to the UI system so we will have the things like the File …
- **00:52** What I want to have is. File Systems for skill folder structure , and block folder structure, and chat folder structure? (I am not sure whether the chat should go to the block folder structure as …
- **00:56** Principle, I mean only conceptional things, at most 15 lines
- **00:56** Also this gudie use how to design the plugins
- **01:00** No, this is the principle about how to design the plugin, do you get it?
- **01:01** please add all the changes and then push it to the remote. Do you get what I mean? we have sNN, jNN in blocks, so I think we can have the cNN, which means the chat, how do you think about this …
- **01:02** we might have a still named hai-chat, right? how do you think?
- **01:04** yes, please go ahead nad do it.
- **01:11** we need to think about what is the chat tracing looks like, one QA is one basic element, is that so? we don't need to take so many details, right? but need to track questions, and the outputs.
- **01:14** you should not update the chat everytime, it should be at the end of the answer, and then you update it, how do you think? I even what to make it as concise as possible.
- **01:17** please add all the changes and push it to remote

## Check

- PRINCIPLE.md written and pushed (ad54ab904); hai-chat built and pushed (b077f4e2a)
- carried over from b10 c01_plugin_principle_and_chat on 261126, when cNN was retired for trace/

## Summary

PRINCIPLE.md says how a plugin is designed. The cNN chat folder and hai-chat it made were retired on 261126: a trace keeps the prompts and the files.
