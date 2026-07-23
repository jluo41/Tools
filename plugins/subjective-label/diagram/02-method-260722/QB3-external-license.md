# 拿一个不是自己打的分数
state: 🟡 PARTIAL
owner: RA
method: 在公开 per-rater 数据集（battery）上跑，看 κ 有没有到人类天花板

## Question
我们自己那个 0.93 是拿「规则作者看过、还亲手标过」的题考出来的，不算数。怎么拿一个**不是自己给自己打的分数**？

## Diagram
```
  出题的人 = 答题的人  ──►  0.93   但换没看过的题 → 0.667   ⬅ 方法上的一个洞

  出路：正确性只能从外面借
     公开数据集里有一类特殊的：保留了【每一位】人类标注者的原始打分（per-rater）
        └─► 于是能算出「真人和真人之间彼此多不一致」＝ 人类天花板（human ceiling）
     引擎在这组数据集（battery）上跑，κ 够到天花板 ＝ 拿到 autonomy license
        └─► 一次性、引擎级：换新构念也继承这份可信度（前提是跟 battery 沾边，沾多远要写明）
```

## Now
`lib/license.py` 写好了、自测过了（喂好数据判 PASS，喂随机数判 BELOW），但**从没碰过真实数据**；一个真实数据集都还没下载。
候选来自 RA 调研 P02：POPQuorn · DICES · GoEmotions · LeWiDi。
⚠️ GoEmotions 标的是情绪，跟人格特质不是一回事（已实测 κ 只有 0.25–0.30）—— 放进去得先想清楚它到底证明了什么。
两个 JL 决定压着这条：**battery 名单** 和 **objective 标准**（见 Discussion）。

## Done when
- [x] `lib/license.py` 自测过了（喂好数据 PASS，喂随机数 BELOW）
- [ ] battery 名单定下来，每个数据集配两样：人类天花板 κ 是多少、为什么选它 —— 🧠 等 JL 拍板
- [ ] 整条引擎在 battery 上真跑一遍，每个数据集落一行：名字 · 样本量 · 引擎 κ · 人类天花板 · 过没过
- [ ] 写一句总判定，并如实写明这份 license 覆盖哪类构念、不覆盖哪类，然后写进 `ref/ref-datasets.md`

## Why here
引擎已经写好，但从没在真实数据上跑过。做完这条，才敢对外说这套方法有效。
它也是 QB2「再加一层跟外部比」的展开：QB2 管自己那三层，这条管从外面借来的正确性。

## Glossary
battery：用来考引擎的那组公开数据集（`ref-config.md` 里的字段名 `license: {battery: [...]}`）。
autonomy license：一次性认证 —— 引擎在 battery 上达到人类天花板，之后换新构念也继承这份可信度。
human ceiling：人类天花板 —— 真人之间彼此的一致性，我们的上限。
per-rater：数据集保留了每一位标注者的原始打分，而不是只给合并后的「标准答案」。

## Discussion
> CC0723: 这条从旧板 `01-sublabel-license-260722` 折进来 —— 折的是它的**验证内核**（原 ①battery / ②license-run / ⑤rerun-3dims）。旧板其余三件也各自安了家：③auto-lexicon → QD4 · ④objective → QC3 · ⑥b02-naming → QC2 的评论。
>> CC0723: 折完旧板已删；Di 的设计原文（note-update-v3 + workflow-audit）移到了本板 `_source/`，board.md 的 ## Links 指过去。

## Comments
- [ ] ZD 「换新构念也继承这份可信度」 · 260721 1400
      Di note-update-v3 F2：构念迁移缺口 —— 在数据集 A 上验证却宣称在 B 上成立。license 只覆盖跟 battery「沾边（adjacent）」的构念，沾多远要如实报告、不能默认。battery 越多样，license 越宽。
- [ ] ZD 「人类天花板」 · 260721 1400
      Di note-update-v3 F3：没有人类天花板，κ 高低没有参照。天花板来自公开的 per-rater 数据集（保留每一位标注者的原始打分），引擎级摊销一次，不是每个项目各算一次。

## Log
260723 1615 · ③④⑥ 各自安家（QD4 / QC3 / QC2 评论）；旧板已删、Di 原文移入 `_source/`；加 Di 的 F2/F3 评论
260723 1600 · 新建：从 `01-sublabel-license-260722` 折入验证内核（0.93 不算数 → 借外部 → license）
