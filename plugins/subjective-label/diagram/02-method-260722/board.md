# 主观标注系统 —— 方法、引擎、和一个不是自己打的分数
spine: 把这套主观标注系统定型 —— 上层的标注方法（JL 会上口头那套）、底下的引擎（句子怎么变向量、三层漏斗、训小模型）、外加一个不是自己打的分数；每一步都盘清「应该长什么样」和「现在代码里有没有」。
close: 下面每个 Q 都到 ✅ SETTLED 或 ⏸️ ON HOLD。全部落定，这套系统就成文了。

## Topic
病人在网上写的医生评论，我们想给每一条打一个人格特质标签 —— 宜人性、尽责性、开放性……每个标签三档：HIGH / LOW / NONE。
请真人来标又慢又贵，所以用一组大模型代替一队人类标注员。
这块板做的事：把 JL 会上口头讲的那套标注方法定型，连同它底下的引擎和一个外部验证，盘清每一步「应该长什么样」和「现在代码里有没有」。
人物：JL = 项目负责人，出方法、拍板（页面上 🧠）。RA = 干活的研究助手。CC = Claude Code，负责迁移和落盘。
来源：collaborations/Event-Subject-Labeling/meetings/2026-07-17-1401 主观标注指南的AI辅助开发.md

## Pipeline
十三个 Q 分四组，编号里的字母就是组：**QA** 方法 · **QB** 扩张与验证 · **QC** 收尾判断 · **QD** 引擎。
QA 是会上定的标注流程，样本从 60 条起步：QA1 造头 60 条 → QA2 分头标这 60 条 → QA3 弱模型考规则写清没。
QB 把样本滚大、每版都验：QB1 从 60 长到 140 挑难例 → QB2 分三层考 → QB3 拿一个不是自己打的分数（外部 license）。
QC 是还没答完、只能 JL 拍板的判断题：QC1 什么时候人能撒手 · QC2 剩几千条怎么标完 · QC3 用什么标准挑构念（objective）。
QD 是底下的引擎，回答 spine 里「现在代码里有没有」那一半：QD1 句子怎么变向量 · QD2 三层漏斗怎么分工 · QD3 小分类器怎么训 · QD4 词表别写死自动生成。QD1/QD2 已在 `ref/` 里定型（✅），QD3/QD4 还在做（🔴/🟡）。
上下两层是咬合的：QB1 挑难例踩在 QD1 上、QC2「训小模型接手」的实现就是 QD3、QD2 漏斗的 Tier 0 就是 QD1、QC3 的 objective 又是 QC1 收敛闸门的一环。
QC3/QD4 和分发到各题的 Di 评论（F1–F8），都来自 Di 的 `_source/note-update-v3-260721.md`（原 01-license 板已折入本板后删除）。

## Roster
### QA · 方法：会上定的标注流程
QA1-coldstart.md
QA2-split-label.md
QA3-weak-exam.md
### QB · 扩张与验证
QB1-grow-140.md
QB2-layered-eval.md
QB3-external-license.md
### QC · 收尾判断（等 JL 拍板）
QC1-when-stop.md
QC2-scale-out.md
QC3-objective.md
### QD · 引擎：机器怎么跑
QD1-embedding.md
QD2-cascade.md
QD3-train-classifier.md
QD4-auto-lexicon.md

## Links
lib/embed.py          ../../lib/embed.py
lib/classify.py       ../../lib/classify.py
lib/license.py        ../../lib/license.py
lib/construct.py      ../../lib/construct.py
lib/converge.py       ../../lib/converge.py
lib/sample.py         ../../lib/sample.py
ref/ref-embeddings.md ../../ref/ref-embeddings.md
ref/ref-cascade.md    ../../ref/ref-cascade.md
ref/ref-datasets.md   ../../ref/ref-datasets.md
ref/ref-config.md     ../../ref/ref-config.md
note-update-v3        _source/note-update-v3-260721.md
workflow-audit        _source/260721-workflow-audit.txt
