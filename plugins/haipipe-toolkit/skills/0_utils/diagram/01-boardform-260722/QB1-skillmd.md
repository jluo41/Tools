# What SKILL.md must say
state: 🟡 PARTIAL
owner: CC
method: SKILL.md 保持最短，细节放 ref/ 三份

## Question
别人（或者以后没有这次对话记忆的我）敲下 `/haipipe-board`，要照着做什么？

## Diagram
```
用户敲  /haipipe-board
          │
          ▼
      SKILL.md  128 行 —— 只答操作，细节不塞进来
          ├─ 形状：一块板长什么样
          ├─ 五个动作：open · add · build · comment · close
          ├─ 一个 Q 文件的段落
          ├─ 写法三条（不许造词 / 清过期话 / 全新 agent 冷读）
          └─ 不许做的四条
                │
                ▼  要细节才去翻
        ref/q-template.md     加一题直接复制
        ref/board-form.md     完整规格：编号 · 段落↔页面 · 语法表 · Comments 格式
        ref/writing-rules.md  怎么写才是人话 + 冷读提示词 + 收敛判据
        ref/board-example.md  一块两题的最小示例
```

## Done when
- [x] SKILL.md 写完
      形状 · 动作（open/add/build/sync/link/close + serve/comment）· Q 文件段落 · 写法 · 禁令 · ref/ 索引。
- [x] 答清楚怎么开一块新板
      open 那一节五步，含唯一一处必须停下来问用户的地方（Q 列表要点头）。
- [x] 答清楚怎么往板上加一个 Q
      复制 `ref/q-template.md` → 改文件名 → 进 Roster → 重新生成。
- [x] 答清楚这块板什么时候该关掉
      每题到 ✅ 或 ⏸️；`close:` 就是关板条件，要能验收。
- [x] 定下 SKILL.md 怎么跟板保持同步
      **毕业机制**（见 ## Law）：一条 Q 到 ✅，它的 `## Law` 抄进 SKILL.md；没定的不进。
      SKILL.md 里写成一节「板 ↔ SKILL.md」。这条本身就是「SKILL.md 必须说清的事」之一。
- [ ] 现场层（serve/chat/terminal）写成规矩
      现在 SKILL.md 里只放了指针（provisional，指向 QD 组），因为 QD1/QD2/QD3 还 🟡。
      等它们 ✅ 再按毕业机制逐条抄进来。
- [x] 换个全新 agent 只看它就能开出一块合格的板
      QB2 跑过了（260723，GPU 集群话题）：全新 agent 只给 SKILL.md + ref/，一次开出 5 题的合格板，判决 YES。
      挑出的唯一真 gap（build.py 怎么调）已修进 SKILL.md。


## Why here
现在这套流程只活在这次对话里。换个 agent 进来，看到的只有一个 `build.py` 和两块试验板，它猜不出该怎么走。
skill 的全部价值就是把流程写下来 —— 不写，这次做的东西下次就没了。

## Now
**写完了，但还没被验过。**

- `SKILL.md` 128 行
  只放操作：形状、七个动作（open / add / build / comment / sync / link / close）、
  一个 Q 文件有哪些段落、写法三条、不许做的四条、ref/ 索引。
  规格和写法细节一概不塞进来 —— 它每次调用都要进上下文，越短越好。
- `ref/` 四份
  `q-template.md` 加一题直接复制（已含 `## Comments`）。
  `board-form.md` 完整规格：文件夹、编号、段落↔页面对应、语法表、Comments 格式、不变量。
  `writing-rules.md` 写法硬规矩 + 零背景审查的提示词和收敛判据 + 历史成绩。
  `board-example.md` 换掉了 —— 原来那份还是 0.1 之前的单文件 `[BOARD]`/`[Qn]` 老格式，会把人带偏。
- `CHANGELOG.md` 记到 0.2.0
  含一条自我更正：0.1.0 写的「输出里零个 `<script>`」在评论层上线那一刻就不成立了，
  而且那本来就不是真正要保的东西。改成「删掉所有 script，每题和全部正文仍然在」，每次生成都断言。

还没做的：换个全新 agent 只看 SKILL.md 去开一块板 —— 那是 QB2。


## Law
- 毕业机制：SKILL.md = 板上已定问题的结晶
  这块板（`diagram/01-boardform-260722/`）是完整的设计记录；SKILL.md 只留 `✅ SETTLED` 的题的结论。
  一条 Q 到 ✅，就把它 `## Law` 那段的规矩抄进 SKILL.md 对应位置。**没定的题（🟡/🔴）不进 manual** ——
  免得把「随手定的」写成铁律（QD1 的权限规则就这么被写死又推翻过）。
  所以 SKILL.md 永远 = 已定规矩之和；改 SKILL.md 之前，先看那题 ✅ 了没。
- SKILL.md 保持最短
  只放操作；规格、语法、写法细节全进 `ref/`。它每次调用都要进上下文，越短越好。
- 现场层先放指针，不写成规矩
  serve.py 的 comment 落盘已随 QA6 ✅ 毕业；chat/terminal（QD 组）还 🟡，SKILL.md 里只给指针。

## Glossary
`SKILL.md`：Claude Code 里一个 skill 的入口文件。用户敲 `/haipipe-board` 的时候，被读进去的就是它。
毕业：一条 Q 定案（✅）后，把它拍定的规矩从板搬进 SKILL.md，成为给人照着做的一条。

## Discussion

## Log
260723 1720 · QB2 验收通过 → 勾掉「全新 agent 能开板」；顺手补进 SKILL.md：build.py 带路径调 + slug/默认状态/owner 约定
260723 1700 · 定下毕业机制（Q ✅ → Law 抄进 SKILL.md），写进 ## Law 和 SKILL.md 的「板 ↔ SKILL.md」一节；
              顺手毕业已 ✅ 的三题：修掉 comment 那节过期的「Sync」说法（QA6：Save 即写盘）、
              引入 serve.py 动作、现场层只放 provisional 指针；版本 0.2.0 → 0.3.0
260723 1210 · 加 sync 和 link 两个动作 —— 板和产物的联动之前完全没写
260723 1210 · board.md 加 ## Links；正文里的路径变成可点链接
260723 1150 · SKILL.md 写完（128 行）+ ref/ 四份；CHANGELOG 记到 0.2.0
260723 1150 · ref/board-example.md 换掉老格式；ref/q-template.md 补 ## Comments
260723 0919 · 编号 Q4 → QB1；标题压到 12 字；完成线改成勾选清单
260722 2255 · 开题
260722 2249 · skill 文件夹从 skills/board/ 搬到 skills/0_utils/haipipe-board/
