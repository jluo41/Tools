# 句子怎么变成向量
state: ✅ SETTLED
owner: CC
method: lib/embed.py 包 sentence-transformers / OpenAI；换模型只改 config 一行

## Question
一句评论怎么变成一串数字（向量），好让「挑难例、去重、铺全量」这些按距离算的事有意义 —— 用哪个模型、缓存怎么存、它能不能决定标签？

## Diagram
```
  一句评论  ──►  lib/embed.py  ──►  [0.02, -0.31, …]  384 维向量
                                     意思近的句子 → 坐标近

  ⚖️ 一条铁律：embedding 是【速度工具】，不是【判断工具】
       它只做：找候选 · 去重 · 铺全量        永不决定标签
       标签只从 panel 推理来 —— 否则踩四个坑：
         语义反转（"I feel alive" vs "I feel nothing" 坐标很近，标签相反）
         反讽 / 体裁模仿 在向量空间里像目标
         序数塌缩（"extremely high" vs "very high" 挤成一团）
         不可解释（标错了指不出是哪个词害的）
```

## Now
**一个模块、一个 agent、一段 config —— 全定型了**

- `lib/embed.py`
  全系统唯一碰 HF / OpenAI / sentence-transformers 的地方；对外由 embedder agent 提供 embed / index / nearest / cluster / stratified-sample。
- 默认选型
  `all-MiniLM-L6-v2`（22M · 384 维 · CPU ~2K/秒 · 免费）—— <100K 条英文，想跑就跑。要更好质量或大语料 → OpenAI `text-embedding-3-small`；医学文本 → `biobert`。
- 换模型只改 config 一行
  `config.yaml` 的 `embedding:` 段改 `model` + `dim` 即可；老缓存按 `sha1(model+text)` 存，换模型不失效，新模型首次用才重算。

## Done when
- [x] 定下默认模型（`all-MiniLM-L6-v2`）和换模型的方式（改 config 的 model + dim 一行）
- [x] 定下缓存布局（按 `(model, text)` 哈希存，换模型不失效）
- [x] 定死原则：embedding 只找候选、不决定标签（`ref-embeddings.md` 的四个失败模式）

## Why here
JL 直接问的就是「句子怎么变 embedding」。它也是 spine 里「现在代码里有没有」那一半最底层的地基 ——
QB1 挑难例、QD2 漏斗的 Tier 0、QB2 去重都踩在它上面。不把它写下来，上面几题的「按位置挑」就是空话。

## Law
- embedding 只做 找候选 / 去重 / 铺全量，**永不决定标签**（标签只从 panel 推理来）。
- 换 embedding 模型只动 `config.yaml` 的 `model` + `dim`；缓存按 `(model, text)` 哈希，换模型不失效。
- 一个模块（`lib/embed.py`）、一个 agent（embedder）、一段 config（`embedding:`）—— 别在别处另起炉灶碰 HF。

## Glossary
embedding / 向量：把一句话映射成一串数字，意思相近的句子数字也相近。
余弦相似度：量两个向量方向多接近的数，1＝同向，0＝无关，用来判「像不像」。
faiss：一个按向量找最近邻的库，`faiss-flat`（<100K 条）/ `faiss-ivf`（更大）。

## Discussion
> CC0723: 这题是 QB1（挑难例）和 QD2（漏斗 Tier 0）的地基。内容全部来自 `ref/ref-embeddings.md`，那份文档早定型了，所以这题直接 ✅ —— 板不只装没定的题，也把已定的引擎事实钉在明面上。

## Log
260723 1600 · 新建：把 `ref/ref-embeddings.md` 的选型/缓存/铁律收进板，标 ✅（已定型）
