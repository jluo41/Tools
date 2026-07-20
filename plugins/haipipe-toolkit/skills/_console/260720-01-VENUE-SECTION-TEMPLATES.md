# 260720-01 · venue-specific section template —— 逐个 (venue, kind) 从范例总结  ✅ CLOSED

**话题**:给每个 `(venue, section-kind)` 建一个可填 `template.md`,从该刊范例总结。
**结局**:本 session 一次做完(不是交给新 session)。JL 定 D1=完整四部分、D2=全建。
全部 95 个 `(venue, kind)` 现各有一个 template.md。venue @ `2dd2fc0`,Tools bump @ `181f97b2`。

```
术语表
  (venue, kind)   一个刊 × 一种 section 类型,如 (MISQ, introduction)
  style.md        已存在:这个 section "读起来怎样"(arc/budget/signature),REFERENCE
  template.md     本次所建:这个 section "骨架长怎样"(可填的槽),从范例总结
  glob            *-<kind>/  —— 前缀不可拼接,必须 glob(MISQ- / jno- / diabcare- 各不同)
  T1              样板 = MISQ-introduction/template.md,158 行,先审后批量的定型基准
```

## 🎯 结局(全部完成)

```
  ✅ 架构:section-edit 解析 (venue,kind) 的 style+template 两路径(commit e9cf0331,先前)
  ✅ T1  :MISQ-introduction/template.md 手写 + JL 审三判断(扁平默认 / 9 段骨架 / 定位图走 DR)
  ✅ 批量:14 刊并发,一刊一 subagent,读同一 spec + T1 样板,产出 94 个 template
  ✅ 统一:所有 95 个 `## Q-Section-<n>`→EOF 区逐字节相同(修正了 20 处漂移 + NMI 2 处 B→P)
  ✅ 验证:95/95 齐 · 四部分全 · 0 个 </tpl> 残留 · 0 个 style.md 被动 · glob 全命中
  ✅ 提交:venue submodule 只 add 95 个 template.md(那 6 个别人的 README 未碰)→ 2dd2fc0
           Tools 只 bump venue 指针 → 181f97b2
```

## ⚖️ 裁决账本(JL 原话逐字保留)

```
D1 · venue template 覆盖多少?
     JL 选:完整四部分(自足)。覆盖我建议的"只 (2)(3)",接受 (1)+(4) 在 95 份里重抄、
     未来改 Q-consumer 要传播的代价。→ 已照办:(1)(4) 统一照抄 T1,(2)(3) 逐刊总结。
> JL: 完整四部分

D2 · 建的顺序?
     JL 选:全建("do all of them")。→ 已照办:14 刊 94 个 template 一次并发建完。
> JL: 全做
```

## 🟡 唯一需要你知道的瑕疵(1 处 thin-source)

```
  jamaim-letter  JAMA Internal Medicine 的 research-letter —— 它自己的 style.md 就被标了薄源:
                 norms 继承自 JAMA flagship letter 指南,没有 JAMA-IM 专属 letter 范例。
                 template 已内联标注 thin-source,并引 flagship 范例 Yang 2026 / Cantor 2025 当格式源。
                 → 若将来投 JAMA-IM Research Letter,补一篇 JAMA-IM letter 范例后可 refresh 这个 template。
  其余 94 个:zero thin-source,每条结构约束都追到 style.md 某行或某具名范例。
```

## 🧾 清账表(闭集)

```
  ✅ D1  覆盖范围 = 完整四部分                         JL 已定
  ✅ D2  顺序 = 全建                                   JL 已定
  ✅ T1  MISQ-introduction/template.md(样板,已审定型) 完成
  ✅ T2  其余 94 个 template,按 D2 批量               完成
  ─────────────────────────────────────────────────
  4 / 4  —— 本板闭合
```

## 📝 收尾提示

```
  · venue submodule 里仍有 6 个 playbook-*/README.md 是另一个 session 的未提交改动,
    本次一个没碰,提交后依旧脏 —— 留给那个 session。
  · Tools→venue 指针已 bump(181f97b2);Physician-SPACE 顶层 → Tools 的指针本次未动,
    与 session 开始时 `M Tools` 的状态一致,留给跨 session 收口。
  · 每个 template.md 是"可填骨架 + <tpl: 指南 + <angle-bracket> 槽";section-edit DRAFT 复制它、
    填内容、删 <tpl: 行。真正的填充由论文的 section-edit 阶段做,不在本板范围。
```
