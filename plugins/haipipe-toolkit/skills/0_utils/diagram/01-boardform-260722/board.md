# /haipipe-board —— 把「一块板」定成一个能重复用的东西
spine: 一块板 = 一个文件夹，里面一题一个 md，外加一页谁都打得开的 html。把这个形状定死，写成 SKILL.md，让别人（和以后没有记忆的我）能照着开板。
close: 板上每一个 Q 都到 ✅ 或 ⏸️。SKILL.md 写完、一个没有背景的新 agent 只看它就能开出一块合格的板 —— 这个 skill 才算做完。

## Topic
board（板）是干什么用的：一个话题下面有几个还没定的问题，把它们摊在一页上，谁都能打开看、能在上面写评论；问题一个个定完，这块板就关掉。
人物：JL = 拍板的人。CC = Claude Code，干活的。RA = 研究助手，将来会被指派一块板做几天。
这块板特殊在：它讨论的就是「板」这个东西本身 —— 用一块板来定义板。

## Pipeline
五组，编号里的字母就是组。前两组是主线，后三组各管一摊，可以并行想。

**QA · Defining a board** —— 先把「一块板」这个东西本身定下来：文件夹形状 → 一个 Q 文件的模板 → 投屏怎么办 → 单题那一页怎么排 → 正文怎么写才是人话 → 怎么加行内评论 → 一条评论的 lifecycle。这组不定，后面全悬着。

**QB · Shipping the skill** —— 再把它交出去：写成 SKILL.md → 拿一个全新 agent 冷读验收 → 把已有的老板子迁到新格式。

**QC · Index and structure** —— 板的骨架：板放在哪儿、叫什么名字（QC1）；首页那张清单长什么样、怎么三秒看出该动哪题（QC2）。注意跟 QA4 分工：QA4 管**点进去之后的单题页**，QC2 管**还没点进去的首页**。

**QD · Working on the board** —— 现场层：能不能直接在板上干活。一题一 session 的规则（QD1）、受限的网页抽屉（QD2）、不受限的真终端（QD3）、组标题图标让 LLM 配（QD4）、作用域放大到整块板的 agent（QD5）、页面实时更新怎么做（QD6）。

**QE · Sharing the board** —— 放出去给别人看（QE1）。板一直号称是给第二个人看的，但至今只活在本机 `127.0.0.1`。

## Roster
### QA · Defining a board
QA1-form.md
QA2-qtemplate.md
QA3-htmlppt.md
QA4-pagelayout.md
QA5-readable.md
QA6-comments.md
QA7-lifecycle.md
### QB · Shipping the skill
QB1-skillmd.md
QB2-newcomer.md
QB3-migrate.md
### QC · Index and structure
QC1-where.md
QC2-indexdesign.md
### QD · Working on the board
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD4-topicicon.md
QD5-boardagent.md
QD6-liveupdate.md
### QE · Sharing the board
QE1-hosting.md

## Links
SKILL.md            ../../haipipe-board/SKILL.md
build.py            ../../haipipe-board/build.py
watch.py            ../../haipipe-board/watch.py
CHANGELOG.md        ../../haipipe-board/CHANGELOG.md
ref/                ../../haipipe-board/ref/
ref/q-template.md   ../../haipipe-board/ref/q-template.md
ref/board-form.md   ../../haipipe-board/ref/board-form.md
ref/writing-rules.md ../../haipipe-board/ref/writing-rules.md
ref/board-example.md ../../haipipe-board/ref/board-example.md
haipipe-board/      ../../haipipe-board/
02-method-260722/   ../../../../subjective-label/diagram/02-method-260722/
