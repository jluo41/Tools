# 词表别写死，自动生成
state: 🔴 OPEN
owner: RA
method: 让大模型根据构念定义自动生成 lexicon，喂给 lib/sample.py

## Question
引擎第一步要先估「这个特质在语料里大概多常见」（base rate），靠的是一份关键词表（lexicon）。现在这份词表照着 openness 手写死。怎么改成：根据构念的定义，让大模型自动生成？

## Diagram
```
  construct.definition ──► 大模型自动派生 ──► lexicon（关键词表）
                                                  │
                                                  ▼
                                          估 base rate（特质多常见）
                                                  │
                                                  ▼  喂给
                                          lib/sample.py（按 base rate 抽代表性样本）

  ✗ 现在：probe_base_rate.py 的词表照 openness 硬编码 —— 换个构念就得重写
  ✓ 目标：换任何构念，全程没有一行写死的词
```

## Now
`probe_base_rate.py` 里的词表是硬编码的（照 openness 手写）。`lib/sample.py` 已经写好了，就等这份词表喂给它。
Di note-update-v3 Part 12 把「LLM construct→probe 词表生成」列在「还没做 = 真实运行」那一档 —— 引擎代码在，这一段生成逻辑还没接上。

## Done when
- [ ] 换一个跟医生完全无关的构念（比如「讽刺」），跑一次能自动出词表
- [ ] 用那份词表算出 base rate，全程没有一行写死的东西
- [ ] 结果贴在这条下面

## Why here
这是「这是一台通用引擎」这句话里**最后一块写死的东西** —— 词表不自动化，换构念就得手改代码，通用就是假的。
它也是 QD 引擎组的一员：对应流水线的第 0 步（先摸底 base rate），在 QD1（embedding）之前。它从 01-license 的 ③ 折进来。

## Glossary
base rate：这个特质在语料里大概多常见（如实测 openness 约 6.6%）。抽代表性样本要先知道它，才不会抽偏。
lexicon：一份关键词表，用来粗略估 base rate。
construct→probe generator：Di 起的名字 —— 把「构念定义」变成「探针词表」的那段自动生成逻辑，取代手写死的词表。

## Comments
- [ ] ZD 「probe_base_rate.py 里的词表是硬编码的」 · 260721 1400
      Di note-update-v3 Part 8：把 openness 专用的写死资产泛化成机制 —— `probe_base_rate.py` 的硬编码 lexicon → construct→probe 生成器（大模型从 `construct.definition` 派生词表）；`sample_candidates.py` 的 confound 分层 → 由 `discriminant_from` 驱动。这两条是「去 openness 化」的关键。

## Log
260723 1615 · 新建：从 01-license 的 ③ 折入；吸收 Di note-update-v3 Part 8（construct→probe 生成器）
