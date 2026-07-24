# Board-level agent
state: 🔴 OPEN
owner: CC
method: 把现场层的作用域从「一题」放大到「整块板」，先定 session 规则再动手

## Question
现在 chat 和 terminal 都钉在**某一题**上（`QD1`/`QD2`/`QD3`）。但很多活是**整块板**的：加一题、改 `## Roster`、重排分组、把各题的 `## Question` 批量重写成新结构。这些活该怎么在板上干？

- 为什么难
  一放大到整块板，`QD1` 那条 LAW（**一题一 session · 一 session 一窗口**）就不够用了：板级 agent 要同时碰很多题的文件，跟正开着的单题 session 会撞车。
- 不定会怎样
  「整理问题清单」这类活现在只能回到 CLI 里手敲，板上干不了 —— 板就只是个只读的展示页，不是工作台。
- 定了会影响什么
  serve.py 的 session / HOLD 机制、页面上入口放哪、给它多大权限（能不能删题、能不能改别人正在编辑的题）。

## Boundary
- ✅ 这题管
  **作用域是整块板**的 agent：加 Q、改 Roster、重排分组、跨题批量改写；它的入口、session 规则、权限边界。
- ❌ 这题不管
  钉在单题上的 chat / terminal —— 那是 `QD2`（SDK 抽屉）和 `QD3`（真终端）。也不管首页清单**长什么样** —— 那是 `QC2`；这题只管「谁来动它」。

## Diagram
```
现在（QD1/2/3）                     这题要加的
┌──────────────┐                  ┌──────────────────────────┐
│ QA4 ─ session│ 一题一条           │ 整块板 ─ 一条 board session│
│ QD3 ─ session│ 各自独立           │   能动：board.md · 任何 Q.md│
└──────────────┘                  │   要解决：跟单题 session 撞车 │
   一 session 一窗口（LAW）          └──────────────────────────┘
                                        ↑ HOLD 怎么扩？板级开着时
                                          单题还能不能开？
```

## Items to Finish
- [ ] 定下跟 `QD1` 那条 LAW 怎么衔接
      板级 session 开着的时候，单题 chat/terminal 还能不能开？谁让谁？这是最要紧的一条。
- [ ] 定下作用域和权限
      能改 `board.md` 和所有 `Q*.md`；能不能**新建**题、能不能**删**题、能不能改动别人正开着的那题。
- [ ] 定下入口在哪
      首页上一个按钮？还是只能从 CLI 起？（跟 `QC2` 的首页设计有交叉，别各做各的。）
- [ ] 用 Claude Code 还是 Codex，还是都支持
      现在 `QD2` 走 claude_agent_sdk、`QD3` 走真 CLI。板级这条走哪套，要不要复用。
- [ ] 做出来并验过一次真活
      验收方式：让它把某一组的 `## Question` 批量重写成新结构，人只做审阅。

## Where we are
**只有「一题一 session」，板级完全没有。**

- 现在能干的
  在某一题上开 SDK 抽屉（`QD2`）或真终端（`QD3`），作用域是那一题的文件；session id 存在那题 md 的 `session:` 行里。
- 现在干不了的
  跨题的活：加一题、改 Roster、重排分组、批量重写。这些现在只能回 CLI 手敲。
- 已经存在、可以复用的零件
  serve.py 的 OAuth + SDK + HOLD 机制、`/_board/term` 的 ttyd 反代、`/_board/chat` 的流式与权限回调 —— 板级这条不用从零起。

## Files
- `serve.py`
  session / HOLD / chat / terminal 都在这里。板级这条要么复用、要么扩展这套机制。
- `build.py`
  入口按钮要是放首页，渲染在这里（跟 `QC2` 有交叉）。
- `board.md`
  板级 agent 主要动的就是它的 `## Roster`。

## Log
260723 · 开题：把「板级 agent」从 `QC2` 挪进 QD 组 —— 它的机制跟 `QD1`/`QD2`/`QD3` 同源（serve.py + session + 窗口），只是作用域放大到整块板；跟 `QD1` 的 LAW 直接冲突，必须挨着放
