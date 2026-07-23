# One file, two modes
state: 🟡 PARTIAL
owner: CC
method: 一个文件两种模式：滚着读 / 一题一屏。JL 已定：合并

## Question
`board.html` 是一页长文档，适合一个人滚着读；开会投屏要的是一屏一页。这两件事要不要出两个文件？

## Diagram
```
             Q*.md ──build.py──► board.html   ← 只有这一个文件
                                    │
                ┌───────────────────┴───────────────────┐
           默认：滚着读                         点一行：一题一屏
           8 题一整页                           屏上只剩那一题
           自己看 / 发给 RA                      开会投屏
                └────── 同一个文件，同一份内容 ──────┘

✗ 不再另出 deck.html          还差：← → 翻页 · 演讲者模式（都要 JS）
```

## Done when
- [x] 一个 Q 一屏，翻页看（board.html 的聚焦模式已经做到）
- [x] 只有一个文件，不出第二份 `deck.html`
- [ ] 方向键 ← → 翻页
- [ ] 演讲者模式（讲者看得到讨论，观众看不到）
- [ ] 内容仍然只从 `Q-xxx.md` 来，不另外维护一份文字

## Why here
原本的想法是出两个文件：`board.html` 自己读、`deck.html` 拿去投屏。**JL 定了：合并成一个。**
理由站得住 —— 两个文件意味着两份要同步的东西；而且开会时经常临时要展开某一题的细节，切文件很别扭。
现在 `board.html` 一个文件就是两种模式：默认滚着读，点目录任意一行进入聚焦，屏上只剩那一题。

## Now
仓库里现在只有 `board.html`，没有任何在用的 `deck.html`。
唯一残留的 `subjective-label/diagram/01-sublabel-license-260722/deck.html` 是旧的坏版本，靠 JS 现场造 DOM，跟 `/html-ppt` 没关系 —— 归 QB3 一起清掉。

还差的是 `/html-ppt` 里那几个纯靠 JS 的能力：方向键 ← → 翻页、演讲者模式（S）、总览宫格（O）。
这些都得引 JS，而 `board.html` 目前坚持零脚本。
可以做成**渐进增强**：没有 JS 时点着翻（现在就能用），有 JS 时方向键也能翻 —— 加不加都不会白屏。
`/html-ppt` 的 `base.css` 把 `.slide` 默认设成 `opacity:0`、靠 `runtime.js` 才显示，那种做法不能照抄；要引也只引一段自己写的、纯增强的脚本。

## Glossary
渐进增强：页面在没有 JS 的时候功能完整，有 JS 的时候更好用。跟「没有 JS 就白屏」正好相反。

## Discussion
> JL: 我们还有 deck.html 还是 board.html？我想把它们合成一个。
>> CC0722: 合了。现在只有 `board.html`，一个文件两种模式。剩下的只是方向键那几个要 JS 的能力。

## Log
260722 · 开题：要不要另出一份 deck.html 拿去投屏
260722 · 原稿写死了「VS Code 预览必然屏蔽 JS」，JL 质疑，查证后发现是错的 —— 真原因是端口没转发
260722 · JL 拍板：合并，不出第二个文件。整题重写
260722 · 编号 Q3 → QA3；状态 OPEN → PARTIAL
