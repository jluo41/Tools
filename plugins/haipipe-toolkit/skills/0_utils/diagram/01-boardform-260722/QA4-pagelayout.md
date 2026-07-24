# Single Question Webpage Layout
state: 🟡 PARTIAL
owner: CC
method: 先给意图（问什么·边界·什么算完）再给状态（现在到哪），零背景读一页就懂
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534

## Question
点开一题、屏上只剩它的时候，这一页该怎么排，才能让一个**完全没背景的人**从上往下读一遍，就明白：这题在问什么、什么算做完、现在到哪了？

- 为什么难
  一页要同时装「意图」和「状态」。顺序一反 —— 先甩一堵实现细节，再给目标 —— 读的人还没搞懂在决定什么，就已经被淹了。
- 不定会怎样
  板是拿来跟人讨论、交给 RA 的。一页读不懂，这块板对第二个人就没价值：「如果不易读，写那么多都是 rubbish」。
- 定了会影响什么
  段名、顺序、什么上台面什么折叠，全由 `build.py` 生成。这题一改，`ref/q-template.md` 和板上每一题的写法都得跟。

## Boundary
- ✅ 这题管
  `board.html` 自己的**单题聚焦模式**：段落顺序、段落名、什么上台面 / 什么收进折叠、字号层级。
- ❌ 这题不管
  「另出一份 deck 拿去投屏」—— 那归 `QA3`。也不管每一题的**文字写得好不好** —— 那归 `QA5` 的写法规矩。

## Diagram
```
┌ 跑马条 ≈110px ──────────────────────────┐
│ /haipipe-board   │ 主干 · 关板            │  永远在
├─────────────────────────────────────────┤
│ QA4  🟡 PARTIAL  🔧 CC                   │  状态条
│ Single Question Webpage Layout  ← 38px   │  .h2
│ ❓ Question   一段话 + 2–4 个要点         │  .ask   ← 光这节就该 orient
│ 🚧 Boundary   管什么 / 不管什么           │  .bnd
│ ┌───── ascii 图 ─────┐                  │  .dia
│ 🎯 Items to Finish  ☑☑☑☐        7/9     │  .col.goal  先意图
│ 📍 Where we are                          │  .col.now   后状态
│ ▸ Law ▸ Lesson ▸ Why here ▸ Log          │  折叠，不上台面
│ ← QA3       ☰ Index       QA5 →          │  贴到底
└─────────────────────────────────────────┘
不带框 = 没有边框 · 没有圆角 · 没有卡片底色
```

https://app.excalidraw.com/s/1JWkKv8oMIX/4SD9kLApiQC?element=gFrVKXlBG2d-IrA9PD7Wv

## Items to Finish
- [x] 不带框
      单独打开一题时没有边框、圆角、卡片底色，内容直接铺在页面上。
- [x] 一眼看出差距
      不用读完全文就知道「在问什么」和「现在离做完差多远」。
- [x] 翻页不用回目录
      每一屏底部一行：← 上一题 · ☰ Index · 下一题 →。
- [x] 长短不齐也不留大片空白
      两块上下叠，不左右并排。
- [x] 长段落能分块
      「小标题 + 缩进解释」+ 整行加粗的组标题；勾选清单每条也能带解释。
- [x] 顺序改成「先意图、后状态」
      `Question → Boundary → Diagram → Items to Finish → Where we are`，已落到 build.py 并验过渲染。
- [x] 段名换成人话
      `Done when → Items to Finish`、`Now → Where we are`；老名走 ALIAS 仍解析，老板子不用改。
- [x] 板上每一题都按新结构重写过 Question
      18/18 全转完：Question 一段话 + 要点、新增 `## Boundary` 和 `## Files`、退役的 `## Why here` 并进 Question。
      验收方式是查**生成出来的页面**有没有 `.bnd` / `.fls`，不是查 md 里有没有那串字 —— 查字串会被 ascii 围栏骗（QA2 就这么漏了一节）。
- [ ] 零背景的人读一页就懂
      找个全新 agent 冷读一题，能复述出「在问什么 / 什么算完 / 现在到哪」才算达到。

## Where we are
**✅ 版式和生成器改完了，验收还差两步。**

- 顺序与段名（260723 改版）
  台面顺序定死：`Question → Boundary → Diagram → Items to Finish → Where we are`。先意图后状态。段名换成 `Items to Finish` / `Where we are`；`Why here` 退役，它的活并进 `## Question` 的要点。
- `## Question` 变成「一段话 + 要点」
  走 `body()` 渲染，第一段是大字领句（21px），要点跟在下面。光这一节就该让零背景的人 orient。
- `🚧 Boundary` 新增
  这题管什么、更要紧的是不管什么。不写清「不管什么」，读的人会拿别题的期待来读它。
- 老板子不会碎
  `ALIAS` 一个槽位认多个段名：`Done when`＝`Items to Finish`、`Now`＝`Where we are`、中文老名照旧。老题一个字没改也能重新生成。

**只差最后一步：**

- 冷读验收 —— 找个全新 agent 读一页，看它能不能复述出「在问什么 / 什么算完 / 现在到哪」。
  板上 18 题已经全部转成新结构（不再只有 QA4 是样板），所以这次冷读验的是真实状态。

## Files
- `build.py`
  生成器。台面顺序、段名、`ALIAS`（一个槽位多个名字）、`.ask`/`.bnd`/`.fls` 的渲染与 CSS —— 这题一改，先改这里。
- `ref/q-template.md`
  加一题时复制的那份。段落顺序和引导句必须跟这题一致，否则新写的题会走回老样子。
- `ref/board-form.md`
  完整规格：§4 段落↔页面对应表 + 必填/选填、§8 上台面顺序与三级层级。
- `SKILL.md`
  「一个 Q 文件」那张段落表 + 台面顺序那句；`sync` 那张回写表里的段名也要跟。
- `board.html`
  生成物，**永远不要手改** —— 改 md 然后重新生成。

## Law
- 台面顺序定死：先意图，后状态
  `Question → Boundary → Diagram → Items to Finish → Where we are`。改版前是 Now 在上，零背景先撞实现细节 —— 那是这版式最大的毛病。
- `## Question` 是一段话 + 2–4 个要点
  要点承担「为什么难 / 不定会怎样 / 定了影响什么」。验收标准：**光读这一节，零背景的人就该明白这题在干嘛。**
- `## Boundary` 写清「不管什么」
  只写「管什么」没用 —— 读的人是拿别题的期待来误解你的。不管什么、归哪题，都要点名。
- 聚焦 = 幻灯片，不是卡片
  去掉边框圆角底色，内容直接铺开，`min-height` 撑满一屏。标题 38px、领句 21px、正文 16px，宽 1000px。纯 CSS（`:target` + `:has()`）。
- 什么上台面、什么收起来
  上台面：标题、Question、Boundary、Diagram（招牌图不折）、节标题（底下一条线）、item 名字、勾选项的框+名字。
  默认收起：item 的解释、代码块（收成一行 `</> code · N 行`）。
  沉到底部折叠：Why here · Discussion · Comments · Law · Lesson · Glossary · Log。
- 每个节标题右边一个 expand all
  一起开合这一节的 item / 代码，纯增强；脚本剥掉后每条仍能单独点开。
- 长题就滚动，不截断、不拆屏；不锁 16:9，随窗口高走
  锁画幅是投屏 deck 的事（`QA3`）。
- 标题那行 id 后面留一个真空格
  复制大标题才不会粘成 `QA4Single…`。
- 改段名必须走 ALIAS，不许让老板子碎
  一个槽位认多个名字；老板子一个字不改也要能重新生成。

## Lesson
- 「定了」也可能被一句话推翻
  这题 260723 关成过 ✅，当天就被 JL 一句「零背景很难读懂」打回 🟡 —— 因为当时的验收线里没有「零背景读得懂」这一条。**完成线里缺了真正的用户，勾满了也不算数。**
- 顺序比措辞更影响可读性
  同样的文字，Now 在上 vs 目标在上，读起来是两回事。先改顺序，再谈遣词。

## Glossary
不带框（unbounded）：不用边框、圆角、卡片底色把内容围起来，让它直接铺在页面上。
组标题：正文里整行加粗的一句，领着下面一串 item，页面上带 🔹 或作者自写的 emoji。

## Discussion
> JL: 能不能让这个 slide 更像 /html-ppt 里的 slide？我不想让它被框住。
>> CC0722: 聚焦模式下已经把边框、圆角、卡片底色全去掉，标题放到 38px，头部压成一条跑马条。
> JL: 最要紧的是 Question 那节 —— 一段话加几个要点。现在零背景的人非常非常难读懂。
>> CC0723: 按这个改了顺序和段名，并新增 🚧 Boundary（管什么 / 不管什么）。QA4 打回 🟡，等各题重写 + 冷读验收。

## Comments
- [x] JL 「四条没定的全定了 —— 本题关掉」 · 260723 1524
      这句是「组标题」（item group name），想跟下面的 item 长得不一样。
      >> CC0723: 加了组标题层级 —— 整行加粗 `**…**` 渲染成带 🔹 的一层，比 item 大一号，夹在节标题和 item 中间。
- [x] JL 「点开一个 Q」 · 260723 1217
      能不能把 Question 段的标签也写出来、更直白？原来 `.ask` 那行只剩一个 `❓`。
      >> CC0723: 加了「❓ Question」小标签，跟 📍 / 🎯 一样显示段名。
- [x] JL 「Now 和 Done when 上下叠」 · 260723 1010
      这个 section 的排版可以做得更好一些。比如按照 bullet point 来，就是一个 topic，然后下面是解释。
      >> CC0723: 加了要点式：md 里写 `- 小标题`，下面缩进两格就是解释。
- [x] JL 「一个 Q 在页面上生成的骨架」 · 260723 1030
      能不能把 slide 的 html 模板写进这一题。
      >> CC0723: 加过 HTML 骨架 + 对应表；260723 改版后骨架已过期，删掉了 —— 对应表以 `ref/board-form.md §4` 为准，不在这里维护第二份。

## Log
260723 · 板上 18 题全部转成新结构（Question 要点化 + Boundary + Files + Why here 退役）→ 完成线只剩「零背景读一页就懂」这一条
260723 · 改版：顺序改成「先意图后状态」（Question 一段话+要点 → Boundary → Diagram → Items to Finish → Where we are）；`Why here` 退役并进 Question；新增 `🚧 Boundary`；老段名走 ALIAS 保住老板子。state ✅ → 🟡，还差各题重写 Question + 冷读验收
260723 · 标题 `Single-Q slide layout` → `Single Question Webpage Layout`；文件改名 `QA4-slidedesign.md` → `QA4-pagelayout.md`
260723 1720 · 关板：写 `## Law`，完成线第 6 条打勾，state → ✅（当天被 JL 打回，见 Lesson）
260723 1650 · 大标题 id 后补真空格 —— 复制不再粘成 QA4Single…
260723 1630 · 代码块默认折成「</> code · N 行」；`## Diagram` 招牌图不折
260723 1620 · 节标题底下加线；右边加 expand all
260723 1400 · item 的解释收进 native `<details>`；section heading 放大到 18px
260723 1100 · 两条评论从 Discussion 挪进新的 `## Comments`
260723 0905 · 现在 vs 算做完 从左右并排改成上下叠
260722 2315 · 去掉边框 / 圆角 / 卡片底色，标题放到 38px，头部压成跑马条
260722 2305 · 聚焦模式落地：纯 CSS `:target` + `:has()`
260722 2300 · JL 提出「slide 要像 /html-ppt，不想被框住」，新开此题
