# 小分类器怎么训
state: 🟡 PARTIAL
owner: RA
method: 冻结的 embedding 上跑 logreg（默认），SetFit 可选升级；每轮 sl-iterate 重训

## Question
漏斗中间那层（Tier 1）的小分类器，拿什么训、什么时候训、什么时候信它？

## Diagram
```
  已标好的样本 ──► 冻结的 embedding（QD1）──► logistic regression（秒级训完）
                                              │
                                              ▼  预测 {label, prob, margin}
                          prob ≥0.70 且 margin ≥0.30 ── 用它（Tier 1 出结果）
                          否则 ──────────────────────► 升到 Tier 2 panel

  重训：每轮 /sl-iterate 末尾自动重训
  升级：sl-scale 前可 opt-in 换 SetFit / LoRA-BERT 做一次性高质量训
  兜底：CV F1 < 0.6 → 收紧阈值，或干脆跳过 Tier 1（全交 panel）
```

## Now
**默认最轻**

- backend
  冻结的 embedding 上一个 logistic regression，秒级训完；可选升级 SetFit / LoRA-BERT（`/sl-scale` 前一次性高质量训，researcher opt-in）。
- 重训触发
  每轮 `/sl-iterate` 末尾自动重训；`residual` 模式下，下一批只从「当前分类器还搞不定的」里抽 —— 每轮都在打筛子的下一层。
- 信不信它
  top 概率 ≥0.70 且 margin ≥0.30 才用，否则升 Tier 2；CV F1 < 0.6 就收紧阈值或跳过 Tier 1。
- 现在
  代码在 `lib/classify.py`，自测有，但**没在真实项目文件夹里真跑过**。

## Done when
- [x] 定默认 backend（logreg on frozen embeddings）
- [x] 定重训触发（每轮 `/sl-iterate` 末尾）和信任阈值（prob 0.70 / margin 0.30）
- [ ] 定 SetFit / LoRA 升级什么时候值得（跟 QC2 的路线选择联动）
- [ ] 在真实项目文件夹里跑通一次（现在只有自测）

## Why here
JL 点名要 modeling / embedding / **training** 这条线。training 这块就是它 ——
也是 QC2 (b)「训个小模型接手」的具体实现。QD2 漏斗中间那层能不能顶住，全看这个分类器训得好不好。

## Glossary
logreg：logistic regression，最轻的分类器，在冻结向量上几秒训完。
frozen embedding：直接用 QD1 的向量当特征，不再微调 embedding 模型本身。
SetFit：在少量样本上微调句向量模型的方法，比 logreg 准但更重。
CV F1：交叉验证的 F1 分数，衡量分类器好坏；<0.6 就别太信它。

## Discussion
> CC0723: 这题＝ QC2 (b) 的工程实现、QD2 Tier 1 那层的内幕。留 🟡 的原因是「真跑」还没做、SetFit 升级判据跟 QC2 的 JL 决定绑在一起。

## Log
260723 1600 · 新建：把 Tier-1 分类器的 backend/重训/阈值收进板；「真跑」和「升级判据」留 🟡
