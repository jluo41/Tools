# Q file template
state: 🟡 PARTIAL
owner: CC
method: 定一份可以直接复制的空模板，标清楚哪些必填

## Question
打开一个空的 `QA9-xxx.md`，我该往里面填什么？哪些段落必须有、哪些可以整段删掉？

- 为什么难
  生成器只认几个固定段落名，写错名字那段就**不显示也不报错** —— 静默失败，最难查。
- 不定会怎样
  模板不清楚，每个人写出来的 Q 都不一样，页面就乱；RA 和以后的 agent 每天动的就是这个文件。
- 定了会影响什么
  模板直接决定页面上能显示什么。它跟 `QA4` 是一体两面：`QA4` 改了台面顺序，这份模板必须同步，否则新写的题会走回老样子。

## Boundary
- ✅ 这题管
  **一个 Q 文件内部**：有哪些段落、谁必填谁选填、每段该写什么、`ref/q-template.md` 长什么样。
- ❌ 这题不管
  文件夹里有哪些文件、Q 怎么挂上板 —— 那是 `QA1`。也不管**每段里的字怎么写才是人话** —— 那是 `QA5`（这题管结构，那题管文字）。

## Diagram
```
复制 ref/q-template.md                    必填? → 显示在哪
┌────────────────────────────────┐
│ # 短标题        ≤14 字          │ 必填 → 索引行 + 幻灯片大标题
│ state: 🔴 OPEN                 │ 必填 → 状态徽章（只填一个词）
│ owner: CC   method: …          │ owner 必填 / method 选填 → 卡片头
├────────────────────────────────┤
│ ## Question   一段话 + 要点     │ 必填 → ❓ 大字领句
│ ## Boundary   管/不管           │ 建议 → 🚧 灰边
│ ## Diagram    ascii 图         │ 选填 → 招牌图
│ ## Items to Finish - [ ] 清单   │ 必填 → 🎯 绿框（自动数 2/5）
│ ## Where we are                │ 必填 → 📍 黄框
│ ## Files      牵动哪些文件       │ 建议 → 📁 蓝边
├────────────────────────────────┤ ↓ 全折叠，不上台面
│ ## Law    ## Lesson            │ 选填 → 规矩 / 踩坑
│ ## Glossary   ## Discussion    │ 选填 → 生词 / 讨论
│ ## Comments   ## Log           │ 选填 → 行内评论 / 日志
└────────────────────────────────┘
```

## Items to Finish
- [x] `ref/` 下有一份能直接复制的空模板文件
      `ref/q-template.md`（`board.md` 的 `## Links` 把它指到 skill 的 ref）。build.py parse 测过：state/owner/method 不被污染、11 段全取得到、顶部 `<!-- 用法 -->` 注释生成时被丢掉不上页面。
- [x] 每个段落上面一行注释：这儿写什么、写多长
      每段正文第一行就是引导句（写什么 + 多长），填的时候直接覆盖掉。
- [x] 标明哪些必填、哪些选填
      引导句开头标 `必填 ·` / `选填 ·`；顶部四行（标题·state·owner 必填，method 选填）写在用法注释里 —— 标记不能进 `state:` 这种行，会被 meta 解析器吃掉。
- [x] 新加一题＝复制模板改文件名，不用参考任何已有的板
      一个零背景 agent 只拿到模板就填出了一张合格卡（`/tmp/QA9-testfill.md`，parse 验过），全程没翻任何现成的板。
- [x] 模板跟上 260723 改版
      新顺序、新段名（`Items to Finish` / `Where we are`）、新增 `## Boundary`、`## Question` 改成「一段话 + 要点」、`## Why here` 退役 —— `ref/q-template.md` 已重写。
- [ ] 用新模板再跑一次零背景填卡
      上次冷读验的是旧模板。结构换了就得重验：新 agent 只拿新模板，能不能填出一张「零背景读得懂」的卡。

## Where we are
**模板已跟上 260723 改版，但新版还没被零背景验过 —— 所以退回 🟡。**

- 模板长什么样
  顶部 `# 标题 / state / owner / method`，加 11 个 `##` 段。每段正文第一行是引导句，开头标 `必填 ·` 或 `选填 ·`，填的时候覆盖掉。顶部一段 `<!-- 用法 -->` 注释讲怎么用，生成时被丢掉、不上页面。
- 必填 / 选填
  必填六样：`# 标题`、`state`、`owner`、`## Question`、`## Items to Finish`、`## Where we are`。`## Boundary` 和 `## Files` 选填但强烈建议；其余（`method`、`## Diagram` 和全部折叠段）选填，用不上就整段连标题一起删。
- 顺手修好的三处 drift（模板、`board-form.md`、`SKILL.md` 三处原来对不上）
  ① 补了 `## Law`（拍定的规矩）和 `## Lesson`（踩过的坑）—— build.py 早认这两段、别的题也在用，就这三处漏写；已同步。
  ② 老模板写「Log 最新的放最下面」，跟 1120 定的倒序（`sort_log` reverse=True，最新在最上）自相矛盾，已改。
  ③ 顶部四行原来不在必填/选填规矩里，冷读的新 agent 只能猜；已补进用法注释，并给了 `state` 图例。
- 之前「还没定的」现在也定了
  段落顺序随便排（build.py 按名字取内容，折叠段在页面上的顺序由 build.py 固定）；`## Glossary` 选填，不是每题都要；`state:` 后面只跟一个状态词，别把图例抄进去。

## Files
- `ref/q-template.md`
  这题的交付物本身 —— 加一题就是复制它。
- `build.py`
  `ALIAS` / `sec()` 决定认哪些段名；段名写错就静默取不到。
- `ref/board-form.md`
  §4 段落↔页面对应表 + 必填/选填。

## Law
- 段落名必须原样保留
  build.py 拿 `## ` 后面整串当 key（`ln[3:].strip()`），`## Question（必填）` 就取不到了。所以必填/选填标记只能写进正文第一行，不能写进标题行。
- 必填六样（260723 改版后）
  `# 标题`、`state`、`owner`、`## Question`、`## Items to Finish`、`## Where we are`。
  `## Boundary` 选填但强烈建议；其余全选填，用不上就整段删掉。
- 台面顺序定死
  `Question → Boundary → Diagram → Items to Finish → Where we are` —— 先意图后状态（`QA4` 定的）。
- 折叠段顺序由 build.py 固定
  页面上永远是 Why here · Discussion · Comments · Law · Lesson · Glossary · Log。文件里怎么排都行。
- 改段名必须走 ALIAS
  一个槽位认多个名字（`Done when`＝`Items to Finish`、`Now`＝`Where we are`、中文老名照旧），
  老板子一个字不改也要能重新生成。
- Log 倒序
  最新的在最上面（`sort_log` reverse=True，md 和页面一致）。

## Lesson
- 用法注释里别让某行以 `state:` / `owner:` / `method:` 开头
  meta 解析器（parse_q）对首词是这几个的行照单全收，会把 `state` 图例当成真状态值吃进去 —— 第一版就这么把状态写坏了，改成 `· state …` 才躲开。
- 顶部四行不在「## 段」的必填/选填规矩里
  第一版模板只给 `##` 段标了必填/选填，冷读的新 agent 得猜 state/owner 是不是必填。补进用法注释才算清楚。
- 老模板自相矛盾要清
  模板里还留着「Log 最新的放最下面」，而倒序早在 1120 就定了 —— 正是零背景读者第一眼挑出来的那种过期话。

## Glossary
必填：缺了就算这个 Q 文件不合格。生成器不会报错，但页面上会缺一块。
选填：用不上就把整段连标题一起删掉，不留空壳。

## Discussion

## Log
260723 · 按新结构重写：Question 展开成「一段话 + 要点」，补 `## Boundary` 和 `## Files`；退役的 `## Why here` 并进 Question
260723 · 跟 260723 改版同步：模板重写（新顺序 · `Items to Finish` / `Where we are` · 新增 `## Boundary` · Question 改「一段话+要点」· `Why here` 退役）；必填从七样改六样。state ✅ → 🟡 —— 结构换了，旧的零背景填卡验收不再算数，要重跑
260723 1450 · 冷读验收：全新 agent 只拿模板就填出合格卡；顶部四行补必填/选填 + `state` 图例（写进用法注释，避开 meta 解析器）
260723 1445 · 落地 `ref/q-template.md`：每段标必填/选填、补 `## Law`/`## Lesson`、Log 改倒序；`board-form.md` 与 `SKILL.md` 同步 → 四条完成线全达到，本题 SETTLED
260723 1130 · 模板补 `## Lesson`（折叠，放踩过的坑）
260723 1120 · Log 改成时间倒序，最新的在最上面（md 和页面都是）
260723 1105 · 模板补 `## Comments` 段（带状态的行内评论）
260723 1010 · 模板补要点式语法（`- 小标题` + 缩进解释）
260723 0950 · Log 行加时间：`YYMMDD HHMM · 改了什么`，时间可省
260723 0919 · 段落名全部改英文，模板示例同步
260723 0910 · 模板里加 ## Diagram 和 ## Log 两段
260722 2330 · 状态词从自造的「半有 / 没做」换成 OPEN / PARTIAL / SETTLED / ON HOLD
260722 2325 · JL 当场定两条：标题必须是短语（≤14 字）、完成线一律写成勾选清单
260722 2310 · 编号 Q2 → QA2
260722 2255 · 从 QA1 拆出来单独立题
