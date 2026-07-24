# Where a board lives
state: ✅ SETTLED
owner: JL
method: 板放在「所属单位/diagram/」，跟 skill 本体分开；名字是 编号-主题-日期

## Question
一块板的文件夹该放在仓库的哪个位置？名字怎么起？

- 为什么难
  板服务的对象五花八门（一个 plugin、一个 task 文件夹、一篇 paper），没有单一的「板都放这儿」的地方。
- 不定会怎样
  板会越开越多、还要指派给 RA。位置和名字一乱就找不着，也没法在别的文档里稳定地指过来。
- 定了会影响什么
  `## Links` 的相对路径、以及将来把板放出去（`QE1`）时的目录结构。

## Boundary
- ✅ 这题管
  **板文件夹放哪、叫什么**：挂在谁名下、编号和日期怎么起。
- ❌ 这题不管
  文件夹**里面**有什么 —— 那是 `QA1`。也不管首页那张清单长什么样 —— 那是 `QC2`。

## Diagram
```
skills/0_utils/
├── diagram/                    ← 板：工作产物，天天变
│   └── 01-boardform-260722/
│         编号  主题       日期
└── haipipe-board/              ← skill：要交付的包
      SKILL.md  build.py  ref/

规则：<所属单位>/diagram/编号-主题-YYMMDD/
```

## Items to Finish
- [x] 定下这块板放哪
- [x] 定下下一块板放哪
- [x] 名字规则定下来，光看名字知道是哪块板

## Where we are
JL 已拍板：板放在**所属单位的 `diagram/`** 下面，跟 skill 本体分开。这块板自己已经搬到
`Tools/plugins/haipipe-toolkit/skills/0_utils/diagram/01-boardform-260722/`。

```
skills/0_utils/
  diagram/                  ← 板住这儿（工作产物，天天变）
    01-boardform-260722/
  haipipe-board/            ← skill 本体住这儿（要交付的包）
    SKILL.md  build.py  ref/
```

这条规则顺带解决了一件原本没想清楚的事：**板是工作产物，skill 是要交付的包**，不该混在一个文件夹里。
之前这块板塞在 `haipipe-board/diagram/` 里，等于把一份会天天变的工作记录打包进了 skill。

名字仍是 `编号-主题-日期`（`01-boardform-260722`），编号在前、日期在后。

剩两件小事不挡路，边用边定：日期是开板那天之后永不改，还是每次大改都更新；编号是每个 `diagram/` 各自从 01 开始，还是全仓库统一编。

## Files
- `ref/board-form.md`
  §1 文件夹 —— 位置和命名规矩写在那儿。
- `SKILL.md`
  「🗂 形状」那一节的第一条（所属单位 = 这块板服务于谁）。

## Glossary
所属单位：这块板服务于哪个东西 —— 一组 skill、一个 task 文件夹、一篇 paper。板就放在那个东西下面的 `diagram/` 里。

## Discussion
> JL: 这块板应该在 `Tools/plugins/haipipe-toolkit/skills/0_utils/diagram`
>> CC0722: 已搬。`haipipe-board/` 里只剩 skill 本体（`build.py` + `ref/`）。规则记在上面「现在什么样」里。

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 0919 · 编号 Q7 → QC1；状态 → ✅ SETTLED，3/3
260722 2249 · JL 拍板：板放在所属单位的 diagram/ 下，跟 skill 本体分开；这块板当场搬过去
260722 2240 · 开题时只有一条 JL 给的硬要求：名字是「编号-主题-日期」
