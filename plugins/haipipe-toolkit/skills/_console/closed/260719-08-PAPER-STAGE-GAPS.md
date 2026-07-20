# 260719 · paper stage skill 的载体缺陷

**契约已经改了,载体没跟上。**

上一块板(`closed/260719-01-DRAFT-RAISE-QUESTIONS.md`)把两件事写进了 paper 的 stage 契约:
每份 stage doc 末尾要有 Q-consumer 段(D3),每个 stage skill 要有一段
`## Questions this stage typically raises`(R1)。

契约改完了,**载体有两处没跟上**:两份 template 里根本没有 Q-consumer 这一段,
七份问题类型清单是我起草的、没经过你。这两件事的共同点是 —— 规则已生效,
但照着载体做出来的东西不满足规则。

来源:`260719-07-APPLICATION-PARITY.md` 的 D3 / D4 拆出。
JL:「这是是paper的吗?我以为你这里是work on application的」/「那是不是要开一个paper stage question types的board呢?」

> **怎么用这块板**:每条要你拍板的都在下面「裁决账本」留了 `> JL:` 空槽,
> 直接在冒号后面写你的话(一个字母也行,像 `do A.`)。我只在 `>> CC:` 那行回话,
> **绝不改你写的字**。

**简称全称表**

```
  D<n>   DECISION       裁决项。等你在 `> JL:` 里拍板的事。
  P1     PRIORITY-1     契约已生效、载体没跟上(照载体做 → 过不了自己的闸)。
  P2     PRIORITY-2     内容质量待审(不是错,是要你过目)。
  ──────────────────────────────────────────────────────────────
  以下是这套 skill 本身的词:
  stage skill   paper/1-lifecycle/<N-stage>/haipipe-paper-<stage>/SKILL.md
  template      该 stage skill 自己 ref/ 下的 *-template.md,DRAFT 照它写稿
  Q-consumer    stage doc 末尾那一段,带 stake 的问题,`## Q-<Stage>-<n>` 一条一个
```

---

## ⚖️ 裁决账本(append-only · 你的原话逐字保留)

```
D1 · 两份 template 缺 Q-consumer 段,补哪种形状(P1-1)
     haipipe-paper-draft 的 Step 3 现在明写:claims / pitch / narrative /
     display / section 的结构里都要有 Q-consumer。但 template 这一层:

        narrative-template.md    Q-consumer 出现次数 0
        section-template.md      Q-consumer 出现次数 0
        其余 6 份 paper template 都有;application 的 8 份也都有

     后果:照 template 写出来的稿子,天生缺一段它自己 done-criteria 要查的东西
     —— 和 260719-04-SEED-2PHASE 板 P2-2 是同一个病(那边是 app seed-template
     缺 Answer: 行,同样导致「照模板生成的永远过不了自己的闸」)。

     形状要你定:
       A · 照 seed-template 的 `## Q-Seed-<n> · <title>` 统一写法
       B · 这两个 stage 有自己的挂法 —— narrative 按 beat 挂,section 按段落挂
           (它们的问题天然是 per-beat / per-paragraph 的,统一形状可能反而别扭)

     我倾向 A:形状统一,内容自然会按 beat / 段落写。但 B 也站得住。
> JL:
     >> CC:

D2 · 7 份 paper 问题类型清单的内容,你要逐份看还是抽查(P2-1)
     上一块板 R1 落地的东西:每个 stage skill 末尾一段
     `## Questions this stage typically raises`。paper 侧 7 份,全是我起草的
     (唯一你口述过的 resource 也在这 7 份里,那份不用再看)。

     形状我有把握,内容是领域判断。最没把握的两条:
        claims  📏 robustness       「换个 specification / 样本 / cutoff 还成立吗」
                                    该在 claims 问,还是属于 review 阶段?
        pitch   🏁 competing paper  「有没有人正在讲同一个故事」
                                    和 seed 的 👣 occupied ground 重不重?

     七份分别是:
        seed         👣 occupied ground · 📦 obtainability
        resource     📊DATA × 🧠ALGORITHM 各问 🗄️HAVE / 🌐GET / 🔨BUILD + 🔗linkability
                     ← 你口述的那份,已定
        claims       ⚖️ sufficiency · 🔀 rival explanation · 📏 robustness · 🧱 ingredient
        pitch        🎯 venue fit · 🏁 competing paper · ⚓ anchor source · ⚠️ framing risk
        narrative    ⚓ beat anchor · 🕳️ gap beat · 🖼️ display need · 🧵 arc break
        display      📤 evidence exists · 🧭 coverage sweep · 🎨 form choice · 📐 venue budget
        section-edit 🔢 owed number · ⚓ owed source · 🧩 unearned move · 📛 norm conflict

     三条路:
       A · 你逐份看(6 份要看,resource 已定)
       B · 只看我点名的那两条(claims 的 robustness · pitch 的 competing paper)
       C · 先放着,等真跑一次 seed/claims 的时候按实际感受改
> JL:
     >> CC:
```

---

## 🟠 P1 · 契约已生效,载体没跟上   → 等 D1

```
  paper/1-lifecycle/3-narrative/haipipe-paper-narrative/ref/narrative-template.md      Q-consumer × 0
  paper/1-lifecycle/5-section-edit/haipipe-paper-section-edit/ref/section-template.md  Q-consumer × 0

  对照（都有）:
    seed · resource · claims · venue · pitch · display          ← paper 其余 6 份
    application 全部 8 份

  为什么要紧:haipipe-paper-draft 的 Step 3 要求这两个 stage 有 Q-consumer,
             template 里没这一段 → 照 template 写的稿子过不了自己的 done-criteria。
```

## 🟡 P2 · 内容待审(不是错,是要你过目)   → 等 D2

```
  7 份 `## Questions this stage typically raises`(paper 侧)
     1 份  你口述的,已定    resource
     6 份  我起草的         seed · claims · pitch · narrative · display · section-edit
```

## 🧾 清账表(**闭集**:从 07 号板拆出,不再新增编号)

```
  编号  项目                                    规模    等谁   状态
  ────────────────────────────────────────────────────────────────
  P1-1  两份 paper template 补 Q-consumer 段      2 文件  D1     ⬜
  P2-1  6 份 paper 问题类型清单过目               6 份    D2     ⬜
  ────────────────────────────────────────────────────────────────
  0 / 2    两条都要你先定方向
```

## 📝 来源

```
  260719-07-APPLICATION-PARITY.md 的 D3 / D4
  JL 指出 07 号板混了两个 family 的话题,违反 README 的 One file per TOPIC。
  07 号板现在只留 application;paper-scoped 的两条搬到这里。
```
