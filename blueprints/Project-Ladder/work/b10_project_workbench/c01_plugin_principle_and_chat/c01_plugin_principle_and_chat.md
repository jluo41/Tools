---
session: Tools-PRINCIPLE-cNN
provider: claude
date: '2026-11-21'
goal: PRINCIPLE.md and the cNN chat folder
paths:
- ../../../../AGENTS.md
- ../../../../PRINCIPLE.md
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/scripts/new_chat.py
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/tests/test_new_chat.py
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/SKILL.md
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/ref/chat-contract.md
- ../../../../plugins/haipipe-toolkit/servers/workbench/tests/test_frame_sessions.py
- ../../../../plugins/haipipe-toolkit/skills/1_base/project/haipipe-chat/scripts/qa.py
cards: []
---

# c01 · PRINCIPLE.md and the cNN chat folder

A plugin is a File System, a UI System and the map (PRINCIPLE.md); a Block holds jNN, sNN and cNN; haipipe-chat keeps a chat as QAs, refreshed once when each answer ends.

## QA

- **q01** 00:46 · please pull the latest code from remote.
  → 已拉取完成：`main` 已快进到 `ce1508c7b`，和 `origin/main` 一致，你本地的改动都保留着。
- **q02** 00:50 · What I want to have is. File Systems for skill folder structure , and block folder structure, and UI Systems how the file system is mapped to the UI system so we will have the things like the File …
  → 做了，用的是你说的 `PRINCIPLE.md`：核心内容写在仓库根目录的新文件里，AGENTS.md 只加了一段指向它。
  ⇢ `AGENTS.md`, `PRINCIPLE.md`
- **q03** 00:52 · What I want to have is. File Systems for skill folder structure , and block folder structure, and chat folder structure? (I am not sure whether the chat should go to the block folder structure as …
  → 对，chat 应该放进 Block 文件夹结构里，不单独建一棵树。我已经按你列的结构把 `PRINCIPLE.md` 重写了一遍。
  ⇢ `PRINCIPLE.md`
- **q04** 00:56 · Principle, I mean only conceptional things, at most 15 lines
  → 改好了：`PRINCIPLE.md` 现在 14 行，只写概念，不写路径，也不写归哪个文件管。
  ⇢ `PRINCIPLE.md`
- **q05** 00:56 · Also this gudie use how to design the plugins
  → `PRINCIPLE.md` 加上了插件（plugin）怎么设计，现在 14 行，还在 15 行以内。
  ⇢ `PRINCIPLE.md`
- **q06** 01:00 · No, this is the principle about how to design the plugin, do you get it?
  → 明白了，我改过来了：整份 `PRINCIPLE.md` 讲的就是怎么设计一个插件，而不是在别的内容后面加一条插件规则。
  ⇢ `PRINCIPLE.md`
- **q07** 01:01 · please add all the changes and then push it to the remote. Do you get what I mean? we have sNN, jNN in blocks, so I think we can have the cNN, which means the chat, how do you think about this …
  → 提交并推送好了：远端 `main` 现在是 `ad54ab904`。cNN 这个想法我觉得好，已经写进 `PRINCIPLE.md`；但它和现在的 skill 合同还对不上，见第 2 节。
  ⇢ `PRINCIPLE.md`
- **q08** 01:02 · we might have a still named haipipe-chat, right? how do you think?
  → 对，应该有一个 `haipipe-chat`。仓库里现在还没有这个 skill，chat 的规则分散在三个地方。
- **q09** 01:04 · yes, please go ahead nad do it.
  → `haipipe-chat` is built and works: this session is saved as the first `cNN` in a real Block, and the page shows it. Pushed as `b077f4e2a`.
  ⇢ `new_chat.py`, `test_new_chat.py`, `SKILL.md`, `chat-contract.md`, `test_frame_sessions.py`
- **q10** 01:11 · we need to think about what is the chat tracing looks like, one QA is one basic element, is that so? we don't need to take so many details, right? but need to track questions, and the outputs.
  → Line 97 of `three-views.md` now contradicts `qa.py`: it says the session file can't tell which files were changed, but it can (from the Edit and Write …
  ⇢ `qa.py`
- **q11** 01:14 · you should not update the chat everytime, it should be at the end of the answer, and then you update it, how do you think? I even what to make it as concise as possible.
  → Close. One leftover: Claude Code's "[Request interrupted by user]" marker is being counted as a question, so I'm filtering it out.
