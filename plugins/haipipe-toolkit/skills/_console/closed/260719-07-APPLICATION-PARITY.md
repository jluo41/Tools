# 260719 · application 缺一套「洞」的标记法

**paper 有一整套「每个洞要么填掉、要么有主」的机制。application 一样都没有 —— 但不是"忘了建",是它连"洞"长什么样都还没定义。**

R2 定的是「以 paper 为主,然后 apply 到 application 上去」。paper 那半边做完了
(`closed/260719-01-DRAFT-RAISE-QUESTIONS.md`,33/34),application 只跟上了
`haipipe-application-draft` 一个文件。

```
   磁盘事实:application/ 全域 `{VAL:?}` / `\cite{TOADD}` 命中 = 0
```

application 的 stage doc 是短 markdown、一行一段、没有 LaTeX 引用。它**压根不用这套占位符标记**。
没有标记,lane 无洞可找,checker 无物可查。它现在的等价物是 descriptions 的
anchored summaries(statistic + pointer + as-of date)—— 概念在,但**没有标记、也没有检查器**。

> ⚠️ **本板 v2**(2026-07-19 重写)。v1 的开板诊断是「application 缺三条 lane + 缺 checker 规则」——
> 那是拿 paper 的形状去量 application,前提错了。JL:「我感觉这个board有点割裂」→ 选 A 原地重写。
> 你写过的每个字都在下面「裁决账本」里逐字保留。paper-scoped 的两条已搬到
> `260719-08-PAPER-STAGE-GAPS.md`。

> **怎么用这块板**:每条要你拍板的都在「裁决账本」留了 `> JL:` 空槽,
> 直接在冒号后面写你的话(一个字母也行)。我只在 `>> CC:` 那行回话,**绝不改你写的字**。

**简称全称表**

```
  D<n>   DECISION       裁决项。等你在 `> JL:` 里拍板的事。
  P0     PRIORITY-0     机制缺口:paper 有、application 完全没有。
  P2     PRIORITY-2     内容待审(不是错,是要你过目)。
  ──────────────────────────────────────────────────────────────
  以下是这套 skill 本身的词:
  占位符      正文里的待填标记 `\cite{TOADD} [Q-X-n]` / `{VAL:? <what>} [Q-X-n]`
  方括号      占位符后面的 `[Q-<Stage>-<n>]`,指向欠它的那个问题
  lane        DRAFT 的三条洞探测器 haipipe-paper-draft-{citation,values,display}
  hub         haipipe-<family>-draft,DRAFT 相位的主 worker,唯一执笔者
  Q-consumer  stage doc 末尾那段,带 stake 的问题,`## Q-<Stage>-<n>` 一条一个
  a-executor  probe 文件 ENTRY 里抄回来的答案
  DR row      _DISPLAY_REQUEST.md 里的一行,display 的「欠条」
  checker     check-probe-cards.sh,PROBE VERIFY 跑一次,CHECK 闸再跑一次
```

---

## 📖 已定的模型(不再是裁决项,是这块板的地基)

### 占位符不是 question,是 question 的欠条

```
   ## Q-Claim-3  ←──┬── \cite{TOADD} [Q-Claim-3]        §2 第 4 句
   (一个问题)        ├── \cite{TOADD} [Q-Claim-3]        §5 第 1 句
                     └── {VAL:? mean MME} [Q-Claim-3]    §6 表 2
```

关系是**多对一**:一个问题能同时欠好几个占位符,而且可以是不同 kind
(`draft-citation:86`「reuse its id. Most citation holes land here」)。

反证:如果占位符 ≡ question,方括号就是多余的 —— 占位符本身就是 id 了。
方括号存在,恰恰证明它们是两个东西。

**所以 citation / values / display 是【欠的东西的类型】,不是问题的类型。**

### 三种欠条贯穿四个相位

```
            DRAFT                PROBE                 REVISE              CHECK
            ─────                ─────                 ──────              ─────
 citation   draft-citation                             revise-place        check-evidence
 values     draft-values    ──►  haipipe-paper-probe ──► 三条替换规则   ──► + checker
 display    draft-display         一个 worker                                unowned 规则
            ─────────────         ────────────          ─────────────
            三个 skill            三条 harvest lane      一个 skill
            走一遍找洞            (不是三个 skill)      里的三条规则
```

```
 DRAFT   lane 只读、报告;hub 写占位符 + Q-consumer + 1-probes/ ENTRY
 PROBE   【不碰正文】。haipipe-paper-probe:120「Placing any of this INTO manuscript
         prose is REVISE's job」。它只填 `### a-executor`,正文占位符原封不动
 REVISE  haipipe-paper-revise-place 才动正文,跑在 revise 链第一位:
           `\cite{TOADD} [Q-X-n]` → `\citep{key}`
           `{VAL:? …} [Q-X-n]`    → 12.9(按 source 精度,不许四舍五入)
           DR row `done`          → `\input` + `\ref`
         :71「A bracket comes off ONLY when the thing it owned is actually in the prose」
 CHECK   checker 的 cite-unowned / value-unowned + haipipe-paper-check-evidence
```

**PROBE / REVISE 分两步不是啰嗦,是可判定性**:答案落地 ≠ 答案被织进句子。
PROBE 若直接改正文,`state: read` 就分不清这两件事,checker 也废了。

### display 和另外两个不对称

```
   citation / values   占位符【在正文里】
   display             正文里【没有占位符】,只有 _DISPLAY_REQUEST.md 的一条 DR row
```

`draft-display:90-93` 禁止预置 `\ref`:「compiles to `??` and ships that way, because
nothing downstream re-checks a reference that was already written」。
这也是三条 lane 里**只有 display 保留写权限**的原因 —— 它有独占 inbox。

**一句话**:question 是债主,占位符是欠条,方括号是借据编号;
PROBE 把钱汇到账(a-executor),REVISE 才还债(正文)、撕借据。

---

## ⚖️ 裁决账本(append-only · 你的原话逐字保留)

```
D1 · application 要不要有一套自己的「洞」标记法(P0-1 · P0-2 都从属于它)

     ── 已答的部分(v1 的问答,原话保留)─────────────────────────
> JL: 我们其实是不是也可以，不如就直接留着吧。然后我还有个问题，在 probe和revise的时候，citation values display是怎么work的，还是都归于Q-consumer和A-consumer来解决了？
     >> CC0719: 四相位链路已答,沉淀进上面「已定的模型」。
                不是都归 Q-consumer / A-consumer —— 三种欠条各有各的处理,
                方括号才是串起来的那条线。

> JL: 我的想法就是 citation display 和values就是question的一种不同的形式，对吗？在probe和在revise里，他们会被fill back，这是对的吗？
     >> CC0719: 一半对,也沉淀进「已定的模型」了:
                占位符是 question 的【欠条】不是【形式】(多对一);
                fill back 是【两步】不是一步(PROBE 填 a-executor,REVISE 才动正文);
                display 和另外两个【不对称】(正文里没有它的占位符)。

     ── 还没定的部分 ──────────────────────────────────────────
     你那句「不如就直接留着吧」我仍不确定指哪个:
        (a) 三条 lane 只给 paper 用,application 不建 —— 但 application 仍需要
            某种「洞」的标记,否则「每个洞要么填掉要么有主」在这边根本不可执行
        (b) 整条搁置,application 保持现状,承认这条规矩只对 paper 生效

     如果选 (a),接着要定标记长什么样。两个候选:
        · 复用 descriptions 已有的 anchored summary(statistic + pointer + as-of date)
          —— 它已经是「这个数字有没有出处」的答案,只差一个"还没有出处"的写法
        · 一个和 paper 同构但更轻的标记,例如 `{?: <what>} [Q-<Stage>-<n>]`
          —— 一种标记吃掉 citation / values 两类(application 不写 LaTeX,不必分开)
> JL:
     >> CC:

D2 · checker 补 unowned 规则(从属于 D1,不独立)
> JL: 也补一下吧。
     >> CC0719: ⚠️ 我这条问错了,先别执行。v1 我写的对照是
                「paper 有 4 处规则,application 有 0 处」—— 数字没错,但我漏查了
                application 根本不产生这两种标记。照原样补上去,等于加两条
                【永远不会触发的死规则】。
                我的错在于:拿两份脚本对 grep,没去问「被查的东西存不存在」。
                → 这条从属于 D1:先有标记,才谈得上 unowned 检查。

D3 · 板子范围(已执行)
> JL: 这是是paper的吗？我以为你这里是work on application的，如果这样的话，需要新加一个board 专门处理paper stage的template的问题吗？
     >> CC0719: 你说对了,是 paper 的,我把板混了 —— v1 标题是
                「application 追平 paper + 两个 template 缺口」,那个「+」
                就是一块板装两个话题,违反 README 的 One file per TOPIC。
                ✅ 已拆:P1-1 → `260719-08-PAPER-STAGE-GAPS.md`。

> JL: 这个也是application的问题吗？if not, 那是不是要开一个paper stage question types的board呢？
     >> CC0719: 一半一半 —— 16 份里 paper 7 份、application 9 份。
                ✅ 已按 family 拆:08 号板装 paper 的 template ×2 + 清单 ×7;
                   本板只留 application 的 9 份(全文见下面 P2-1)。

D4 · 板子重写(已执行)
> JL: 如果想看，还是 在这里都列出来他们吧。这些 template都是啥。我感觉这个board有点割裂。
     >> CC0719: 割裂是我造成的 —— v1 被改了四次(诊断被推翻 / 我认错 / 拆走 paper /
                反复补槽),成了补丁本。你选了 A(原地重写),这就是 v2:
                已定的东西写成正文,只留真正没定的当裁决槽。
                「template 是啥」也答了 → 见下面「📎 template 是什么」。
                九份清单全文列出 → 见下面 P2-1。

D5 · advice 的 ⚠️ harm 要不要按 venue 分档
     我写的是「谁会因为照做而更糟?部署前问,不是出事后问」。
     对 report / dashboard 这种重 venue 合适;
     对 sms / push / reminder 这种一句话 venue,每条建议都过一遍伤害评估可能太重。
       A · 保持无条件 —— 伤害评估不该按渠道打折
       B · 按 venue 分档 —— 重 venue 必问,轻 venue 只在建议涉及用药 / 就医时问
> JL:
     >> CC:
```

---

## 📎 template 是什么(答 D4 的第二问)

```
  template = 每个 stage skill 自己 `ref/` 下的骨架文件,DRAFT 照着它写稿。
             例:1-lifecycle/0-seed/haipipe-paper-seed/ref/seed-template.md
             它规定 stage doc 有哪几段、什么顺序、哪里留 <!-- RULE --> 提示。

  缺口在 paper 侧两份(已搬到 08 号板,不在本板):
     narrative-template.md   Q-consumer 段 × 0
     section-template.md     Q-consumer 段 × 0
  而 haipipe-paper-draft 的 Step 3 要求这两个 stage 必须有 Q-consumer
  → 照 template 写出来的稿子,天生缺一段它自己 done-criteria 要查的东西。

  application 的 8 份 template 都有 Q-consumer,这一条不欠。
```

## 🔴 P0 · 机制缺口   → 全部等 D1

```
                              paper                   application
  ──────────────────────────  ──────────────────────  ─────────────
  正文里的「洞」标记          {VAL:?} / \cite{TOADD}   ❌ 无（命中 0）
  找洞的 lane                 三条 skill              ❌ 无
  hub 的扫洞步骤              Step 4a                 ❌ 无
  checker 的 unowned 规则     4 处                    ❌ 0 处
  ──────────────────────────────────────────────────────────────
  「每个洞要么填掉要么有主」  机器强制                 只是散文里的一句话
```

> ⚠️ 先后顺序是硬的:**没有标记 → lane 无洞可找 → checker 无物可查**。
> D1 不定,P0-1 和 P0-2 都动不了。

## 🟡 P2 · 九份 application 问题类型清单(全文)   → 等 D5 + 你的过目

上一块板 R1 落地的东西:每个 stage skill 末尾一段 `## Questions this stage typically raises`。
application 侧 9 份,全是我从各 stage 的 done-criteria 反推起草的。

```
seed
   👣 occupied ground   这个 intervention 在这个人群上被人做过吗?点名最近的先例,或声明这块地是空的
   🧪 mechanism         假设的机制【在任何地方、对任何人】有过证据吗?不是"听起来合理",是"谁做出来过"
   📡 channel reach     这个渠道真能触达这个人群吗?给覆盖率,不是给意图

descriptions
   🗄️ what we HAVE      哪个 store 已经装着这个人群,里面到底有什么?路径 + 产出管线 + as-of 日期
   📏 magnitude         多少人、多长窗口、完整度多少?要锚定的数字,不是写进散文的估计
   🕳️ missingness       缺失比例多少,是不是随机缺失?一份藏着这个的摘要会误导它上面每一级
   🌐 what to GET       有没有外部数据集能补这个缺口,拿得到吗?

themes
   📚 outside evidence  文献给这个模式起过名吗?叫什么?没有外部锚的 theme 只是一个观察
   🔁 is it real        这个模式跨子群 / 跨时间窗还成立吗,还是某一片的产物?
   🆕 unnamed pattern   数据里有没有文献【没命名过】的东西?那是最有意思的情况,也最需要证据

claims
   ⚖️ sufficiency         这条证据是支持了 claim,还是只是没能反驳它?给效应量和 N
   🔀 rival explanation   还有什么能产生同样的模式,什么能区分?没点名对手的 claim 等于没测
   🎯 generalization      它对【我们真要部署的那群人】成立,还是只对发现它的样本成立?
   🧱 ingredient          前提还缺着?那这条是 BLOCKED-ON-DESCRIPTIONS,别在这里重问 1a 的问题

advice
   🎬 actionability     收信人真能做到吗?做不到就点名障碍 —— 没人能执行的建议不是建议
   ⚠️ harm              如果照做、而 claim 后来被推翻,谁会更糟?部署前问,不是出事后问   ← D5
   📐 dosage            多少 / 多久一次 / 持续多长?没有剂量的建议只是一种情绪
   🏛️ standard of care  和已发布的指南冲突吗?冲突的话,凭什么证据?

pitch
   🎯 audience fit      这群人以前对这类信息有过反应吗?给可比项目和它的 response rate
   📡 channel norm      这个渠道的惯例允许什么 —— 长度、语气、频率?违反了就没人看
   ⚠️ framing risk      哪种说法会让这群人觉得危言耸听或自作主张?要保留的话需要什么证据?
   🏁 competing message 这群人在这个渠道上已经在收什么?撞车的信息会被忽略

narrative
   ⚓ beat anchor      这个 beat 在断言某件事。哪条 claim 撑着它?没有 claim 的 beat 是文案不是叙事
   🕳️ gap beat        完全没证据的 beat —— 值得去做,还是砍掉?每个 gap 要么是问题要么是砍,没有"再说"
   🖼️ element need    这个 beat 需要收信人【看见】东西吗?那它欠一个 display unit,不是一句承诺
   🧵 arc break       换成这个顺序后信息还立得住吗,还是需要一个我们没建立的事实?

display
   📤 evidence exists   有没有 task 产出的结果能让这个元素去渲染?没有产出 task 的元素刷不新
   🎨 element form      面板 / 图表 / 表格 / 还是一句话?在 venue 预算让它成为真取舍时才问
   📐 venue budget      这个 modality 允许几个元素,砍掉的是哪个?
   🖥️ render context   在什么屏幕 / 什么客户端里被看到?在手机上裂开的元素不算做完

section-edit
   🔢 owed number       正文里一个没有出处的数字。值得去取,还是把这句话砍了?
   ⚓ owed source       一个关于世界的断言,背后什么都没有
   🧩 unearned move     这一段做了一个读者没被给出依据的跳跃 —— 任何 sweep 都找不到,
                        它不是缺一个 token,是缺一个论证
   📛 norm conflict     venue profile 和这一节自己的惯例在这里打架。谁赢,凭什么?
```

## 🧾 清账表(**闭集**:不再新增编号)

```
  编号  项目                                        规模    等谁   状态
  ────────────────────────────────────────────────────────────────
  P0-1  application 的「洞」标记法(先定义,再建)      ?      D1     ⬜
  P0-2  checker 补 unowned 规则                      2 规则  D1     ⬜  从属于 D1
  P2-1  9 份清单过目(advice 的 harm 另等 D5)         9 份    D5     ⬜
  ────────────────────────────────────────────────────────────────
  0 / 3

  拆出去的(在 260719-08-PAPER-STAGE-GAPS.md):
     两份 paper template 补 Q-consumer · 7 份 paper 问题类型清单
```

## 📝 为什么这份板子不会变成跑步机

```
  v1 的毛病是【把过程当成了内容】—— 诊断被推翻、我认错、拆走 paper、反复补槽,
  全堆在板上,读起来是一条改动日志而不是一块板。

  v2 的规矩:【已定的写成正文,没定的才是裁决槽】。
  上面「📖 已定的模型」那一节是从四轮问答里沉淀出来的,它不会再变;
  真正开着的只有 D1(标记法)和 D5(harm 分档)两件事。
```
