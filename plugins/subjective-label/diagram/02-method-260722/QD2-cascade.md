# 三层漏斗怎么分工
state: ✅ SETTLED
owner: CC
method: Tier0 embedding-kNN → Tier1 小分类器 → Tier2 大模型 panel，越往下越贵越少

## Question
铺全量的时候，怎么让「大部分容易的样本走便宜路、少数难的才惊动大模型」？

## Diagram
```
  ┌ Tier 0 · embedding k-NN ────────┐  ~$0.00001/条 · 最快 · 吃 60–80%
  │  top-5 gallery 邻居同标签         │
  │  且平均余弦相似度 ≥ 0.85 → 继承    │
  └───────────┬─────────────────────┘ 不服 ↓
  ┌ Tier 1 · 训练过的小分类器 ────────┐  ~$0.0001/条 · 快 · 吃 10–30%
  │  概率 ≥0.70 且 margin ≥0.30 → 用它 │   （怎么训见 QD3）
  └───────────┬─────────────────────┘ 不服 ↓
  ┌ Tier 2 · 大模型 panel（3–5 persona）┐ ~$0.05–0.20/条 · 慢 · 吃 5–15%
  │  多数票 support ≥0.6 → 用；<0.6 → 丢人工队列 │
  └──────────────────────────────────┘
```

## Now
**三层，越往下越贵、越少 —— 全定型了**

- 分工与阈值
  Tier 0 靠 gallery（`cascade_inherit_sim` 0.85）· Tier 1 靠训练（`accept_prob` 0.70 / `accept_margin` 0.30）· Tier 2 靠 panel（support 0.6，再不服丢人工）。
- 每条都记它走了哪层
  annotation 里写 `method: tier0/1/2` + `confidence`，方便审计「给我看所有 Tier 0 判的，有没有明显错的」。
- 能跳层
  `routing=panel`（全 panel，验证集用）· `single`（最便宜）· `cascade`（默认，铺全量用）。

## Done when
- [x] 三层的分工和阈值定死（`cascade_inherit_sim` 0.85 / `accept_margin` 0.30 / `accept_prob` 0.70 / support 0.6）
- [x] 每条记录 `method` + `confidence`，可审计
- [x] 支持 `routing=panel/single/cascade` 三种模式

## Why here
这就是 QC2「剩几千条怎么标完」的**机器答案** —— (a) 全量硬标和 (b) 训小模型接手，在这里被揉成一台漏斗，
JL 那道「选一条」其实变成「设阈值」（多少交给 embedding 继承、多少交给小分类器、多少惊动大模型）。

## Law
- 漏斗 ＝ 迭代搭出来的筛子：每轮 `/sl-iterate` 加一层（gallery 长 → Tier 0 多吃；分类器训 → Tier 1 起来；规则收紧 → Tier 2 更同意）。
- Tier 0 靠 gallery、Tier 1 靠训练、Tier 2 靠 panel；三者阈值都在 `config.yaml`，调高更安全更贵，调低更快更险。

## Glossary
k-NN：找最近的 k 个邻居，看它们的标签。
margin：分类器最高概率和第二名的差；差得越开，决策边界越清楚。
persona：一个带特定视角的打标大模型；panel＝一组不同 persona 同时打。
gallery：已标好并附了理由的例子册，Tier 0 就拿新样本跟它比。

## Discussion
> CC0723: Tier 0 靠 QD1（embedding）；Tier 1 那层怎么训在 QD3；这台漏斗是 QC2 的工程实现。三题串起来读＝铺全量的完整图。内容来自 `ref/ref-cascade.md`。

## Log
260723 1600 · 新建：把 `ref/ref-cascade.md` 的三层/阈值/routing 收进板，标 ✅（已定型）
