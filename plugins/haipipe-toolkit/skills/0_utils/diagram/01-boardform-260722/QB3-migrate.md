# Migrate the two old boards
state: 🔴 OPEN
owner: CC
method: 重写成新格式 + 重新生成 html + 清掉旧中间产物

## Question
`subjective-label/diagram/` 下面已经有两块板，是旧格式。要不要迁？迁到什么程度？

## Diagram
```
01-sublabel-license-260722/        02-method-260722/
  board.md    旧格式                  board.md    全塞在一个文件里
  board.html  靠 JS 造 DOM → 白屏      board.html  已经是静态 ✅
  deck.html   坏的，删                 fig/
  render.py   删
       │                                    │
       └──────► 都改成 QA1 定的形状 ◄────────┘
                一题一个 QX-xxx.md + 重新生成
```

## Done when
- [ ] 两块板都改成 QA1 定下的格式
- [ ] `board.html` 重新生成，打开能看
- [ ] 旧的中间产物（`render.py`、`deck.html`）清掉

## Why here
这两块板是这个 skill 目前唯一的实物证据。它们要是还停在打不开的旧版本，SKILL.md 里写的东西就一个能指的例子都没有。

## Now
`02-method-260722/` 已经换成了新的静态版本（7 个 Q、页面里 0 个脚本），但写法还是「全部塞在一个 board.md 里」，没拆成一题一文件。
`01-sublabel-license-260722/` 还是旧的：靠页面里的 JS 现场造内容，在 VS Code 预览里必然白屏；文件夹里还留着 `render.py` 和 `deck.html`。

## Glossary
白屏：旧版页面的正文全靠页面里一段 JS 现场生成，而 VS Code 的预览窗口不许跑这段 JS，所以打开就是一片白。新版把正文直接写死在 HTML 里、一个脚本都没有，因此不可能白屏。

## Discussion

## Log
260722 · 开题
260722 · 02-method-260722 已改成静态版（7 题、零脚本），但还没拆成一题一文件
260722 · 编号 Q6 → QB3
260722 · 清单里加了「删掉旧的 deck.html / render.py」
