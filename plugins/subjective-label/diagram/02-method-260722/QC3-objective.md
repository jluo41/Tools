# 用什么标准挑构念
state: 🔴 OPEN
owner: JL
method: 二选一：downstream 预测力 / discriminance（跟兄弟特质分得开）

## Question
让多个大模型各提一个构念候选、再自动挑最好的那个 —— 挑的时候用哪个标准（objective）？downstream（标签能不能预测下游结果，比如医生的阿片类处方量）还是 discriminance（这个标签跟兄弟特质分不分得开）？

## Diagram
```
  mode=auto：多个大模型各提一个构念定义 + 各标一批样本
        │
        ▼  按 objective 打分，挑最高的那个
     ┌─ downstream    标签能预测下游结果（opioid-Rx 回归）
     └─ discriminance  标签跟兄弟特质（尽责性/开放性…）分得开
        │
        ▼  针对模型之间的分歧再自动打磨
     选出的构念 = 工程构念（operational），不等于教科书上的那个心理特质

  ⚠️ objective 是「全自治」唯一保留的人类输入 —— 没有它，「哪个构念/标签对」欠定，必须有人拍。
```

## Now
`lib/construct.py` 两种 objective 都支持了（自测：好的候选赢、冗余/退化的判 0），但**医生这个项目的标准还空着**。
⚠️ 卡点：CMS 数据是 PHI，`_WorkSpace/1-CMS-Store` 和 `2-Data-Store` 只能待在安全服务器上 —— 笔记本上跑不了真的 downstream，除非找一个能合法搬出来的聚合指标当代理。

## Done when
- [ ] 二选一并写下理由 —— 🧠 等 JL 拍板
- [ ] (a) 选 downstream：说明接哪个指标、怎么在不搬 PHI 的前提下算出来
- [ ] (b) 选 discriminance：这一轮先用它，downstream 推到下一块板
- [x] `lib/construct.py` 两种都实现并自测过

## Why here
Di 的 note-update-v3 Part 2 点破：这套引擎能做到「近乎全自治」，唯一的前提是**有一个标准替代人的判断** ——
没有 objective，「哪个构念、哪个标签是对的」就是欠定的、必须有人一条条拍；有了它，就变成一个能优化、能自动化的问题。
所以这一题不定，QC2 的 auto-select 无从下手，QB2 跑出来的成绩也没法判好坏。它从 01-license 的 ④ 折进来。

## Glossary
objective：挑构念候选、判收敛时用的那个标准（downstream / discriminance / dataset_match）。是这套引擎里不可自动化掉的那一点人类输入。
downstream：看标签能不能预测下游结果（如医生的阿片类处方量）。
discriminance：看标签跟兄弟特质分不分得开。
工程构念 / 理论构念（operational vs theoretical）：objective 挑出来的是「最服务于这个目的的标注」，不一定就是教科书意义上的那个心理特质 —— 除非它另外通过构念效度交叉核对，否则不许直接叫它「开放性」。

## Comments
- [ ] ZD 「唯一保留的人类输入」 · 260721 1400
      Di note-update-v3 Part 2/3：全流程里需要人的地方只剩三个 —— 说出 objective（每类构念一次，本来就在研究设计里）、给 engine license 签字（引擎一辈子一次）、极端个案人工复核（可选、可关）。其余全自动。这一题就是那三个里的第一个。
- [ ] ZD 「工程构念（operational），不等于教科书上的那个心理特质」 · 260721 1400
      Di note-update-v3 Part 10 诚实边界：objective 挑出来的构念要如实报成「工程特征」，不能直接宣称它就是「开放性」；还要防 objective-gaming（自动挑出的构念可能钻 confound 空子 → 用 downstream held-out 兜：换没见过的数据还预测得准吗）。

## Log
260723 1615 · 新建：从 01-license 的 ④ 折入；吸收 Di note-update-v3 Part 2/3/10（objective 是自治的唯一人类输入 + 工程构念诚实边界）
