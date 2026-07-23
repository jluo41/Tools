# Where a board lives
state: ✅ SETTLED
owner: JL
method: 板放在「所属单位/diagram/」，跟 skill 本体分开；名字是 编号-主题-日期

## Question
一块板的文件夹该放在仓库的哪个位置？名字怎么起？

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

## Done when
- [x] 定下这块板放哪
- [x] 定下下一块板放哪
- [x] 名字规则定下来，光看名字知道是哪块板

## Why here
板会越开越多，还要指派给 RA。位置和名字一乱就找不着，也没法在别的文档里指过来。

## Now
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

## Glossary
所属单位：这块板服务于哪个东西 —— 一组 skill、一个 task 文件夹、一篇 paper。板就放在那个东西下面的 `diagram/` 里。

## Discussion
> JL: 这块板应该在 `Tools/plugins/haipipe-toolkit/skills/0_utils/diagram`
>> CC0722: 已搬。`haipipe-board/` 里只剩 skill 本体（`build.py` + `ref/`）。规则记在上面「现在什么样」里。

## Log
260722 · 开题时只有一条 JL 给的硬要求：名字是「编号-主题-日期」
260722 · JL 拍板：板放在所属单位的 diagram/ 下，跟 skill 本体分开
260722 · 这块板从 haipipe-board/diagram/ 搬到 0_utils/diagram/
260722 · 编号 Q7 → QC1；状态 → ✅ SETTLED，3/3
