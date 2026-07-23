# /haipipe-board —— 把「一块板」定成一个能重复用的东西
spine: 一块板 = 一个文件夹，里面一题一个 md，外加一页谁都打得开的 html。把这个形状定死，写成 SKILL.md，让别人（和以后没有记忆的我）能照着开板。
close: 下面十四个 Q 全部到 ✅ 或 ⏸️。SKILL.md 写完、一个没有背景的新 agent 只看它就能开出一块合格的板 —— 这个 skill 才算做完。

## Topic
board（板）是干什么用的：一个话题下面有几个还没定的问题，把它们摊在一页上，谁都能打开看、能在上面写评论；问题一个个定完，这块板就关掉。
人物：JL = 拍板的人。CC = Claude Code，干活的。RA = 研究助手，将来会被指派一块板做几天。
这块板特殊在：它讨论的就是「板」这个东西本身 —— 用一块板来定义板。

## Pipeline
十四个 Q 分四组，编号里的字母就是组：**QA** 定形状、**QB** 交出去、**QC** 等 JL 拍板、**QD** 板上直接干活。
QA1–QA6 先把「一块板」这个东西本身定下来：文件夹形状 → 一个 Q 文件的模板 → 投屏怎么办 → 单题那一屏怎么排 → 正文怎么写才是人话 → 怎么在上面加行内评论 → 一条评论的 lifecycle。这七个不定，后面全悬着。
QB1–QB3 再把它交出去：写成 SKILL.md → 拿一个全新 agent 验收 → 把已有的两块板迁到新格式。
QC1 是唯一一个跟怎么做无关、只能 JL 拍板的：板放在哪儿、叫什么名字。
QD 是新开的一路：能不能给每个 Q 挂一个对话窗口，直接在那一题上干活。跟 QA/QB 都不冲突，可以并行想。
QD1 定规则（分级和边界），QD2 是受限的网页抽屉（已能用），QD3 是不受限的真终端（还没动）。

## Roster
### QA · 先把「一块板」定下来
QA1-form.md
QA2-qtemplate.md
QA3-htmlppt.md
QA4-slidedesign.md
QA5-readable.md
QA6-comments.md
QA7-lifecycle.md
### QB · 再把这个 skill 交出去
QB1-skillmd.md
QB2-newcomer.md
QB3-migrate.md
### QC · 要 JL 拍板
QC1-where.md
### QD · 板上能不能直接干活
QD1-chat-per-question.md
QD2-chat-sdk.md
QD3-chat-terminal.md
QD4-topicicon.md

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
