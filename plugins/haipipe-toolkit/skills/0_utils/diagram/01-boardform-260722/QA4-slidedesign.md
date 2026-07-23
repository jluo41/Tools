# Single-Q slide layout
state: ✅ SETTLED
owner: CC
method: 聚焦模式去掉卡片框，照 html-ppt 的幻灯片来排
session: cd5e7f5f-15c7-49ba-a97f-bdf90ef3f534
## Question
点开一个 Q、屏上只剩它的时候，这一屏该长什么样？什么放大、什么收起、什么根本不该出现在台面上？

## Diagram
```
┌ 跑马条 ≈110px ──────────────────────────┐
│ /haipipe-board                          │  板名
│ │ 主干 · 关板                            │  永远在
│ ▸ 这块板在干嘛   ▸ 这些 Q 是怎么排的      │  全局入口
├─────────────────────────────────────────┤
│ QA4  🟡 PARTIAL  🔧 CC                   │  状态条
│ 单题幻灯片怎么排              ← 38px      │  .h2
│ ❓ 点开一个 Q、屏上只剩它时…    ← 21px     │  .ask
│ ┌───── ascii 图 ─────┐                  │  .dia
│ │ 📍 Now                                │  上
│ │ 🎯 Done when  ☑☑☑☐          5/6       │  下
│ │ 💡 Why here                           │
│ ▸ Discussion  ▸ Glossary  ▸ Log         │  折叠，不上台面
│ ← QA3       ☰ All 10       QA5 →        │  贴到底
└─────────────────────────────────────────┘
不带框 = 没有边框 · 没有圆角 · 没有卡片底色
```

## Done when
- [x] 不带框
      单独打开一个 Q 时没有边框、圆角、卡片底色，内容直接铺在页面上，像一张幻灯片。
- [x] 一眼看出差距
      不用读完全文就知道「在问什么」和「现在离做完差多远」。
- [x] 翻页不用回目录
      每一屏底部一行：← 上一题 · ☰ 全部 · 下一题 →。
- [x] 长短不齐也不留大片空白
      Now 和 Done when 从左右并排改成上下叠，两边字数差多少都不空。
- [x] 长段落能分块
      写成「小标题 + 缩进解释」，不是一段接一段的散句。勾选清单每一条也能带解释。
- [x] 这套规则写下来，不只是「现在长这样」
      规矩落进 `## Law`：什么上台面（标题/问句/招牌图/节标题/item 名字）、什么默认收起（解释、代码块）、什么沉底部折叠（Discussion/Log…）。最后这道靠这次的「代码默认折 + expand-all + 节标题带线」定死了。

## Now
**✅ 排版落地、规矩写进 `## Law`、四条没定的全定了 —— 本题关掉。**

- 节标题带一条下划线 + 右边 expand all（JL 260723）
  📍 Now / 🎯 Done when / 💡 Why here 底下各一条线；右边一个 expand all，点一次把这一节的 item 和代码全开/全合。只在真有可折叠内容的节才挂这按钮。
- 代码块默认折（JL 260723）
  正文里的 ``` 代码收成一行「</> code · N 行」，点开才铺；`## Diagram` 那张招牌图不折。跟 expand all 联动。
- 大标题可复制不粘连（JL 260723）
  `QA4` 和标题之间补了个真空格 → 复制那行是 `QA4 Single-Q slide layout`，不再粘成一坨。
- 聚焦靠纯 CSS
  点目录任意一行进入，`:target` + `:has()`，这一块不需要任何脚本。
  （整页有一段脚本，是 QA6 的评论层，跟排版无关。）
- 不带框
  聚焦时去掉边框、圆角、卡片底色，内容直接铺开；`min-height` 撑满一屏。
- 字号阶梯
  标题 38px、问句 21px、正文 16px，正文宽度放到 1000px。
- Now 和 Done when 上下叠
  各自带一道颜色边（黄=现在、绿=目标）。
  原本照 html-ppt 的 `comparison.html` 左右并排，两边长短一差就空掉半边，改成了上下。
- 长段落分块
  写成「小标题 + 缩进解释」，勾选清单每条也能带解释。
- 解释可折叠，名字留台面（JL 260723）
  一个 item = 名字 + 解释。解释收进 native `<details>`，默认收着、点名字才展开——一屏先看到的是一列干净的名字，想细读哪条再点开。仍是零脚本，逐条独立开合。`.blt` 名字左边 ▸/▾，勾选项名字行尾 ▸/▾，没解释的 item ▸ 淡掉、点不开。
- section heading 放大
  聚焦时 📍 Now / 🎯 Done when / 💡 Why here 从 13px 提到 18px、上前景色，压过下面的 item 名字。5/6 那个计数还留 13px，不抢戏。
- 头部压成跑马条
  约 110px：板名 + 主干 + 两个全局入口（这块板在干嘛 / 这些 Q 怎么排），折叠着，任何一题上都点得到。
- 底部一行导航
  ← 上一题 · ☰ 全部 · 下一题 →，`margin-top:auto` 贴到底。

**原来「还没定的」四条，现在都定了（进了 `## Law`）：**

- 长题塞不下 → 滚动（不截断、不拆屏）
- 锁 16:9 → 不锁，随窗口高走；锁画幅归投屏 deck（QA3）
- 折叠区算不算噪声 → 已解：解释 + 代码默认折进台面、Discussion/Log 沉底部折叠
- 标题 38px → 够了，不再调


一个 Q 在页面上生成的骨架（`build.py` 出的就是这个）：

```html
<section class="slide q wip" id="QA4" data-file="QA4-slidedesign.md">

  <div class="qh">                        <!-- 状态条，一行小字 -->
    <span class="qid">QA4</span>
    <span class="pill wip">🟡 PARTIAL</span>
    <span class="mut">🔧 CC</span>
    <span class="mut">· method 那一句</span>
  </div>

  <h2 class="h2"><span class="hid">QA4</span>短标题</h2>   <!-- 聚焦时 38px -->
  <div class="ask">❓ ## Question 那一句</div>              <!-- 聚焦时 21px -->

  <div class="dia"><pre>## Diagram 的 ascii 图</pre></div>

  <div class="cmp">                        <!-- 上下叠，不是左右 -->
    <div class="col now"> <div class="ch">📍 Now</div>    <!-- ch 聚焦时 18px -->
      <div class="blt"><details class="it">           <!-- 要点：解释收进 details -->
        <summary class="bt">小标题</summary>         <!-- 名字留台面，▸/▾ 在左 -->
        <div class="bd">缩进的解释</div></details></div>
    </div>
    <div class="col goal"><div class="ch">🎯 Done when <span class="cnt">5/6</span></div>
      <div class="ck on"><span class="bx">☑</span>
        <div class="itw"><details class="it">          <!-- 勾选项同理，▸/▾ 在行尾 -->
          <summary class="ct">小标题</summary>
          <div class="bd">缩进的解释</div></details></div></div>
    </div>
  </div>

  <div class="f"><span class="fl">💡 Why here</span><div>…</div></div>

  <div class="folds">                      <!-- 收起来，不上台面 -->
    <details><summary>💬 Discussion (n)</summary>…</details>
    <details><summary>📖 Glossary</summary>…</details>
    <details><summary>📜 Log (n)</summary>…</details>
  </div>

  <div class="nav">← QA3 · ☰ All 10 · QA5 →</div>          <!-- 聚焦时贴到底 -->
</section>
```

md 段落 → 页面位置，一一对应：

```
## Question    → .ask        问句，最显眼那行
## Diagram     → .dia        ascii 图，紧跟问句
## Now         → .col.now    上面那块，黄色边
## Done when   → .col.goal   下面那块，绿色边，栏头自动数出 5/6
## Why here    → .f          再下面一栏
## Glossary    → .folds      折叠
## Discussion  → .folds      折叠
## Comments    → .folds      折叠，未解决默认展开
## Law         → .folds      折叠
## Lesson      → .folds      折叠
## Log         → .folds      折叠
```

聚焦模式（点目录任意一行）跟平铺模式的差别，全在 CSS 的 `body:has(.q:target)` 那一段：
`.q:target` 去掉边框圆角底色、`min-height: calc(100vh - 230px)`、标题 38px、
头部压成约 110px 的跑马条、`.folds` 用 `margin-top:auto` 贴到底、`.nav` 显示出来。

## Why here
QA3 管的是「另出一份 deck.html 拿去投屏」，这一题管的是「board.html 自己的聚焦模式」—— 两件事，容易混。
而且这是最影响「一眼能不能看懂」的一题：同样的文字，排成一个带框的小卡片，和排成一张不带框的幻灯片，读起来完全是两回事。

## Law
- 聚焦 = 幻灯片，不是卡片
  单独打开一题时去掉边框、圆角、卡片底色，内容直接铺开，`min-height` 撑满一屏。字号阶梯：标题 38px、问句 21px、正文 16px，正文宽 1000px。纯 CSS（`:target` + `:has()`），不靠脚本。
- 什么上台面、什么收起来（这题的核心规矩）
  上台面：标题、问句、`## Diagram`（招牌图，不折）、节标题（底下一条线）、item 的名字、勾选项的框+名字。
  默认收起（点名字 / 按 expand all 才现）：item 的解释、代码块（收成一行「</> code · N 行」）。
  沉到底部折叠区：Discussion / Comments / Law / Lesson / Glossary / Log。
  一屏第一眼 = 一列干净的名字 + 招牌图；想细读哪条点哪条。
- 每个节标题右边一个 expand all
  把这一节所有 item / 代码一起开合，纯增强；脚本剥掉后每条仍能单独点开，全文一直在 DOM。
- 现在 vs 算做完：上下叠，不左右分栏
  两边长短不一时并排会空掉半边。各自带一道颜色边（黄=Now、绿=Done when）。
- 长题就滚动，不截断、不拆屏
  截断会藏内容（读物大忌），拆屏破「一题一屏」。溢出就让它滚。
- 不锁 16:9，随窗口高走
  锁画幅是投屏 deck 的事（QA3）；board.html 自己的聚焦模式跟着窗口高度。
- 标题那行 id 后面留一个真空格
  复制大标题才不会粘成 `QA4Single…` → `QA4 Single…`（那 11px 视觉间距是 CSS margin，不是字符）。

## Glossary
不带框（unbounded）：不再用边框、圆角、卡片底色把内容围起来，让它直接铺在页面上 —— html-ppt 的幻灯片就是这么排的。
跑马条：聚焦时顶上那一条压扁的头部，只占约 110px，保证不管翻到哪一题都还知道这块板在干嘛。

## Discussion
> JL: 能不能让这个 slide 更像 /html-ppt 里的 slide？我不想让它被框住。
>> CC0722: 聚焦模式下已经把边框、圆角、卡片底色全去掉，标题放到 38px，头部压成一条跑马条。还没定的几条列在上面「现在什么样」里。

## Comments
- [x] JL 「四条没定的全定了 —— 本题关掉」 · 260723 1524
      这句是「组标题」（item group name），想跟下面的 item 长得不一样。
      （在页面上选中那句加评论；serve.py 误写进了「md 段落→页面位置」示例里的 `## Comments`，已挪来这里。）
      >> CC0723: 加了组标题层级 —— 整行加粗 `**…**` 渲染成带 🔹 的一层，比 item 大一号，夹在节标题和 item 中间。build.py + `ref/q-template.md` + `ref/board-form.md §5/§8` 都对齐了。
- [x] JL 「点开一个 Q」 · 260723 1217
      能不能把 Question 段的标签也写出来、更直白？原来 `.ask` 那行只剩一个 `❓`，没有「Question」这个词。
      >> CC0723: 加了「❓ Question」小标签，跟 📍 Now / 🎯 Done when 一样显示段名（`.ql`，蓝色小字）。
- [x] JL 「Now 和 Done when 上下叠」 · 260723 1010
      这个 section 的排版可以做得更好一些。比如按照 bullet point 来，就是一个 topic，然后下面是解释。
      （在 QA6 页面上提的，但按 JL 自己的归类它讲的是 slide 的 display，所以归这一题。）
      >> CC0723: 加了要点式：md 里写 `- 小标题`，下面缩进两格就是解释。Now 和 Done when 都按这个重排了。
- [x] JL 「一个 Q 在页面上生成的骨架」 · 260723 1030
      能不能把 slide 的 html 模板写进这一题。
      >> CC0723: 加了 HTML 骨架 + 「md 段落 → 页面位置」对应表。

## Log
260723 1720 · 关板：写 `## Law`（上台面 vs 折叠 + 4 条裁决），完成线第 6 条打勾，state → ✅ SETTLED；毕业进 SKILL.md
260723 1650 · 大标题 id 后补真空格 —— 复制不再粘成 QA4Single…
260723 1630 · 代码块默认折成「</> code · N 行」；`## Diagram` 招牌图不折
260723 1620 · 节标题底下加线；右边加 expand all（一键开合这一节的 item / 代码）
260723 1400 · item 的解释收进 native `<details>`（想看再点开，仍零脚本）；section heading 放大到 18px。JL 要的
260723 1100 · 两条评论从 Discussion 挪进新的 `## Comments`，都标成已解决
260723 1035 · Now 也改成要点式；顺手清掉一条过期说法（「board.html 坚持零脚本」）
260723 1035 · Diagram 更新：全部 8 题 → All 10，折叠区补上 Log
260723 1030 · 把 slide 的 HTML 骨架和「md 段落 → 页面位置」的对应表写进本题
260723 1030 · Done when 每条改成「小标题 + 解释」
260723 1010 · JL 要「一个 topic + 下面的解释」的要点式排版，已实现（`- 小标题` + 缩进解释）
260723 0945 · 修掉一处自相矛盾：正文还写着「左右并排」，跟实际的上下叠打架（QA5 那次审查挑出来的）
260723 0905 · 现在 vs 算做完 从左右并排改成上下叠 —— 两边长短差太多时并排会空掉半边
260722 2315 · 去掉边框 / 圆角 / 卡片底色，标题放到 38px，头部压成跑马条
260722 2305 · 聚焦模式落地：纯 CSS `:target` + `:has()`，当时零脚本
260722 2300 · JL 提出「slide 要像 /html-ppt，不想被框住」，新开此题
