# 260719 · DRAFT 相位的提问能力



> JL: 什么是皮肤？

>> CC0719: 我造的词，指的就是 **skill** —— repo 里的 `skills/<family>/<name>/SKILL.md`。
>>          已把本文件里 9 处「皮肤」全部改回 `skill`（你上面这句原话保留不动）。
>>          来源交代一下：审计员的返回里写了「姊妹皮肤」「该皮肤」，我照抄进来没拦。
>>          规矩重申：**用 repo 里的原词，不给它起别名** —— 包括子代理带回来的词。


> JL: change this emoji: seed      💀 这个角度被人占了吗?

>> CC0719: 换成 👣（有人先走过这里）。两处都改了：R1 展开的对照表 + seed 的形状示例。
>>          💀 是我从「杀伤 / 什么会让它死」那套词带过来的，但这条问的是
>>          「这块地被人插旗了吗」——是**领地**问题，不是**存活**问题，配错了。




> JL: haipipe-skill-diagnose/SKILL.md:46 please also change this, and make SKILLS to save things to a _console folder? 

```
  A · _console/ 取代 bucket 根   → 要改 haipipe-skill-diagnose/SKILL.md:46
                                   现存 4 份是否搬过来（它们都已结案）
  B · 两者并存                    → _console/ 放**在制品**，bucket 根放**已结案的 review**
                                   那本文件结案后要搬回 paper/2-phase/
```



=========================

`_console/` 是跨 skill 在制品的工作台：review、迁移计划、裁决账本。不出货，不是 skill 本身，不是图集。
文件名取**出生日**，以后不改（与 `diagram/<YYMMDD>-<topic>/` 一致）；一个 topic 一个文件，后续会话往里 append。
批注协议：`> JL:` 是你的，`>> CC{MMDD}:` 是我的回。你的原话永不删改。

起点：JL —— 「我感觉是 draft 这边。我们是不是应该把 draft 的 raise 问题's ability，也提得更重要一些？」


## 🎯 现在在哪

```
  ✅ 已做   三个 fresh-context 审计员跑完 DRAFT 相位 → 28 findings
  ✅ 已做   你给了 R1–R4 四条裁决（见下）
  ✅ 已做   第 0 轮复核完成 —— 行号已全部重编
  ✅ 已做   第 0.5 / 0.6 / 1 / 2 / 3 轮全部落地（paper 侧 [M] 已清）
            七个 stage skill 各自持有问题类型；RAISE+PLAN 升为顶层 Step 4b
  ⏸️ 未动   application（R2：paper 之后）· 要动 probe 的两条（跨 family）

  ▶️ 下一步   **看上面的「🙋 待你确认（六件）」** —— 六个 `> JL:` 空槽等你
             按 R5，一个 tag 都还没发；你说停我一次性发


  ── 第 0 轮复核：不重跑，只核 haipipe-paper-draft ──────────────

  为什么不重跑三个审计员：三个审查对象里只有一个动过。

    haipipe-paper-draft        v4.4.0(307行) ──▶ v5.0.0(320行)   🔥 动了
    haipipe-application-draft  v1.3.1(94行)  ──▶ 同           ✅ 原封未动
    probe/haipipe-probe        v9.5.0(349行) ──▶ 同           ✅ 原封未动

  → 打在后两个上的 11 条，行号一字未改，全部仍有效
  → 打在 haipipe-paper-draft 上的 17 条，派一个只读复核员逐条核过 v5.0.0
     主会话抽查 5 条全部证实

  复核结果：

    ✅ 已修      1   D2
    🟡 部分      4   A9 · B1 · B2 · D3
    🔴 仍成立   11   A4 A5 A8 A10 B4 B5 B6 C1 C3 C4 D1
    ⬜ 未复核    1   D5
    🆕 新缺陷    5   N1–N5（v5.0.0 自己引入的，见 Findings 末尾）

  🔴 最要紧的是 N1：v5.0.0 的旗舰步骤 Step 4a 按声明跑不起来。
```


## 🙋 待你确认（六件 · 直接在 `> JL:` 后面写）

paper 侧能做的都做完了。以下六件我停在这里。

---

### C1 · N2 执笔权 —— 我按证据落了「hub 单写」，你确认或翻案

Step 4a 的三条 lane 和 hub，原本**互相都说是对方写**：

```
  改之前                                    我改成
  ─────────────────────────                ─────────────────────────
  hub :158    「Fold those new questions    hub   THIS HUB HOLDS THE PEN
               into the Q-consumer and            ①② 都由 hub 写
               author their ENTRIES」
  citation:90 「RAISE a new ## Q-...」      lane  REPORT it as UNOWNED
  values  :78 「RAISE a new Q-consumer」    lane  REPORT it as UNOWNED
  display     「file a DR row」             lane  照旧（不同 inbox，是它自己的）
```

理由：三条 lane 同时写一个 `1-probes/PPNN_<topic>.md` 是 write race，而 bank 的 QA 文件
早就定了 ONE WRITER + `set -C`。同一个形状，同一条规矩。

连带后果：citation / values 因此**不再需要 `Write`**（只改正文，Edit 够），我已撤回；
display 保留 `Write`（它要建 `_DISPLAY_REQUEST.md`）。

翻案代价：5 个文件，不大。

> JL: 什么意思？我以为draft会call draft-citaton, draft-values, ... 最后之后haipipe-paper-draft 在该 draft.md 和Q-consumers？ 




---

### C2 · 七份问题类型清单的**内容**

形状我有把握（每个 stage 一段 `## Questions this stage typically raises`，英文，R3）。
但内容是我从各 stage 的 done-criteria 反推的，**领域判断是你的**。最没把握的三条：

```
  claims    📏 robustness      「换个 specification / 样本 / cutoff 还成立吗」
                               —— 是真该在 claims 问，还是这属于 review 阶段？
  resource  🔁 reusability     「有没有现成模型可复用，而不是重训」
                               —— 这是 resource 的问题，还是 claims 的？
  pitch     🏁 competing paper 「有没有人正在讲同一个故事」
                               —— 和 seed 的 👣 occupied ground 重不重？
```

其余四组（seed / narrative / display / section-edit）我比较有把握。

> JL:resource 我们现在有什么数据，有什么算法，要去网上找什么数据，找什么算法，是不是自己要开发算法，自己构造数据之类的。
pitch： 是为了说能不能让对应venue的人听得懂，能不能吸引他们的注意力之类的。
claims    📏 robustness      「换个 specification / 样本 / cutoff 还成立吗」
                               —— 是真该在 claims 问，还是这属于 review 阶段？ 
            > JL: 我同意，这个我们应该控制claim的量，最好只有三四个，不要啥都问/


---

### C3 · 什么时候发 tag（R5）

按你的规矩现在一个都没发：

```
  haipipe-paper-draft            5.1.0  ⚠️ IN PROGRESS（一直往里追加）
  haipipe-paper-draft-{citation,values,display}   1.0.0（改动在，tag 没动）
  七个 stage skill               版本未动
  haipipe-skill-diagnose         1.3.0（这个是完整的一件事，已收口）
```

你说停，我一次性发。

> JL: 可以的。现在直接改到5.1，但是更新并没有很多。以后代际更新要谨慎。

---

### C4 · 我的 D1 / D4 要不要让位

```
  本文件 D1「四行 PROBE: 归错相位」  ≈  260719-PHASE-BOUNDARY-REFACTOR.md 整场重构
  本文件 D4「mode 按 per-question 汇报」 ⊂ 260719-MODE-RETIREMENT.md
```

D1 我已经按 R1 执行了（搬进七个 stage skill）。D4 还没动。
问题是：D4 划掉交给 MODE-RETIREMENT，还是留在这份里？

> JL: 留给他们。

---

### C5 · 第 4 轮 application 现在开吗

R2 说 paper 优先 —— paper 侧已经清完。application 那边等着的：

```
  A1  🔴 整份文件没有人类闸之前的自审（probe 的 DRAFT rule 4 两个 family 都要求）
  A2  🔴 allowed-tools 缺 Agent，A1 的改法跑不动
  A3 A6 A7 · B7 · C2 C5 C6 · D4        🟡🟢
```

> JL: 先等着，把application做完再说。

---

### C6 · 两条要动 `probe` 的（跨 family，我没敢动）

```
  D5  ENTRY vs section 混用
      probe/haipipe-probe/SKILL.md 自己也混（:162 entry / :96 section）
      单改 paper 会和它不一致 → 要一起规范化

  B3  probe 的 DRAFT rule 2 仍以 "For each open question" 开头
      预设问题已经存在，没指向新建的 per-stage 清单
      但 probe 是 paper + application 共用的
```

动 `probe` 会同时影响 application，所以停在这里等你。

> JL: 可以直接去改。

---


## ⚖️ 裁决账本（append-only · 你的原话逐字保留）

```
R1 · 2026-07-19 · 提问方法放哪（原 thread T1）
> JL: 是不是我们给每个stage写上，我们这里要写什么东西，一般会问到什么类型的问题？

     >> CC0719: 同意，而且比我原来提的「五条通用 lens」好。见下面「R1 的展开」。
> JL: this is good. But we need to use the English to write the skills.
     >> CC0719: ✅ 已确认。持有方 = stage skill（haipipe-paper-<stage>/SKILL.md），
                haipipe-paper-draft 只留指针。R1 关闭。写法归 R3。

R3 · 2026-07-19 · 工作台用中文，出货物用英文
> JL: But we need to use the English to write the skills.

     >> CC0719: 分工定死：
                _console/*.md（这里）· 对话 · diagram   →  中文
                SKILL.md · CHANGELOG.md · ref/*.md      →  **英文**（出货物）
                → 下面 seed 的形状示例已改成英文，就是将来落进 SKILL.md 的那个样子

R4 · 2026-07-19 · 旧 review 删不删
> JL: 删掉吧，直接。

     >> CC0719: ✅ 已删 probe/haipipe-probe/SKILLSET_REVIEW.md。
                你的原话在 R1/R2 里逐字存着。该文件从未 commit 过，git 无痕。
                顺带查到一个**不是这次造成的**悬空引用 → 见 C7。

R5 · 2026-07-19 · 一轮活只发一个 tag
> JL: only add it or assign the new tags until we really have the final version, not everytime, we have a new tag

     >> CC0719: ✅ 已执行，并且**推翻了 haipipe-skill-diagnose 自己的规矩**
                （原文 Phase 4：「Every fixed skill gets a version bump + CHANGELOG entry
                  in the same pass」，MUST NOT 里还有一条对应的）
                已改成：ONE TAG PER BODY OF WORK，末尾才发；开着的时候标 ⚠️ IN PROGRESS 往里追加
                本轮已经碎掉的 tag 全部合并回去：
                  haipipe-paper-draft            5.0.2 + 5.1.0  → 只留 5.1.0（IN PROGRESS）
                  haipipe-paper-draft-citation   1.0.1          → 回滚到 1.0.0
                  haipipe-paper-draft-values     1.0.1          → 回滚到 1.0.0
                  haipipe-paper-draft-display    1.0.1          → 回滚到 1.0.0
                改动本身都留着，只是不发 tag

R2 · 2026-07-19 · 双生收敛顺序（原 thread T2）
> JL: 现在我们以paper为主，然后apply到application上去。

     >> CC0719: 收到。两个后果记下来：
                (a) A1 / A2（application 唯二的 🔴：没有自审 + allowed-tools 缺 Agent）→ 延后，不取消
                (b) 这**推翻**了审计员 C 的建议 —— 它认为 application 是更好的「骨架」、
                    主张对称收敛。按你的裁决：paper 是参考实现，application 跟随。
                    记在这里，免得以后有人照审计报告改回去。
```


### R1 的展开 —— 为什么你这条比「五条通用 lens」好

v5.0.0 新加了 `### Step 4a. 🕳️ SWEEP THE HOLES`，派发三条 lane：

```
Skill("haipipe-paper-draft-citation")   →  \cite{TOADD} [Q-<Stage>-<n>]
Skill("haipipe-paper-draft-values")     →  {VAL:? <what>} [Q-<Stage>-<n>]
Skill("haipipe-paper-draft-display")    →  一条 DR row
```

这三条 lane 已经把「通用 + 机械」那一半吃掉了。剩下没人管的，正好是你说的那一半：

```
┌─ 🔧 通用 · 机械 ─────────────┬─ 🧠 per-stage · 判断 ──────────────────┐
│ 「这句缺个数 / 引用 / 图」    │ 「这个 stage 天生该担心什么」          │
├──────────────────────────────┼────────────────────────────────────────┤
│ draft-citation               │ seed      👣 这个角度被人占了吗         │
│ draft-values                 │           📦 外部数据拿得到吗           │
│ draft-display                │ resource  📦 连得上医生级吗             │
│                              │ claims    ⚖️ 这条证据够撑 H1 吗         │
│    ✅ v5.0.0 已建好           │           🔀 还有别的解释吗             │
│                              │    ❌ 没有家 ← R1 要补的就是这个        │
└──────────────────────────────┴────────────────────────────────────────┘
```

**不是新东西，是把已经在做的事写下来：**

```
haipipe-paper-seed/SKILL.md 的 FEASIBILITY pair   = seed 的两个判断型问题
haipipe-paper-draft/SKILL.md 那 4 行 `PROBE:`      = 各 stage 的问题类型，归错了相位（= D1）
haipipe-paper-draft/SKILL.md 的 section-edit 清扫  = section-edit 的那一份
```

所以我撤回上一轮的「五条通用 lens」——那是我造的抽象层。

✅ **谁持有 —— 已定（R1）**：

```
  stage skill 持有   haipipe-paper-<stage>/SKILL.md 里加两行：
                     「这里写什么」+「这里一般问什么类型的问题」
  draft 指过去       haipipe-paper-draft/SKILL.md 的 Stage-specific notes 只留指针

  → 这样 D1 那四行不是「改标签」，是**搬家**
```

落进 `haipipe-paper-seed/SKILL.md` 的样子（英文 —— R3）：

```
### Questions this stage typically raises
- 👣 occupied ground — has anyone already taken this angle?
- 📦 obtainability   — does the external labelled data exist, and can we get it?
NOT here: profiling OUR OWN data → [FORWARD -> RESOURCE]
```


## 🚧 FIX 计划

```
第 0 轮   重编行号 + 复核                                        ✅
第 0.5 轮 N1 `, Skill` · N5 `, Write`（三条 lane 全中）           ✅
第 0.6 轮 N3 四处裸占位符 · N2 执笔权（按证据落「hub 单写」）      ✅ N2 待你确认
第 1 轮   R1 per-stage 问题类型 —— 七个 stage skill 各自持有       ✅
          D1 四行 `PROBE:` 搬出，draft 只留指针
第 2 轮   B1 RAISE+PLAN 升为顶层 Step 4b · B2 补 Q-consumer 那一半 ✅
第 3 轮   A4 A5 A8 A9 A10 · B4 B5 B6 · C1 C2 C3 C4 · D3 · N4 · C7  ✅
第 4 轮   application（R2：paper 之后）                           ⬜ 未开始
```

**没做的，和为什么：**

```
D5   ENTRY vs section 混用   ⬜ probe/haipipe-probe 自己也混（:162 entry / :96 section）
                                单改 paper 会和它不一致 → 要一起规范化
B3   probe 的 DRAFT rule 2    ⬜ 仍以 "For each open question" 开头（预设问题已存在）
     还没指向 per-stage 清单     probe 是 paper+application 共用，动它要跨 family
D1·D4 让位                    ⬜ 见「跨 console 文件的两个坑」
```

## 📋 Findings（33 条 · 🔴8 🟡19 🟢6 · [M]23 [J]10）

原 28 条 + 第 0 轮复核新增 N1–N5。severity 按 ref/finding-taxonomy.md 只用 🔴🟡🟢。

审查对象：

```
paper/2-phase/0-draft/haipipe-paper-draft/SKILL.md              v5.0.0 · 320 行  ✅ 行号已重编
application/2-phase/0-draft/haipipe-application-draft/SKILL.md  v1.3.1 ·  94 行
probe/haipipe-probe/SKILL.md                                    v9.5.0 · 349 行
```

**四个根因：**

```
🔀 A · 双生漂移        10 条   同一个 DRAFT 相位两个 worker，谁都不是谁的超集
                              paper = 好身体（指向 probe · 自审 · venue guard · gate 协议 · 7 个 stage 备注）
                              application = 好骨架（顶层 RAISE 步骤 · return contract · 完整搜索规则）

🕳️ B · 提问被降级       7 条   相位的第二个产出在结构上被贬成附属品
                              三份文件（含 probe）都只说「问题出现之后怎么办」

🚚 C · 搬家没改地址     6 条   Status board（早已改成生成）· buffer 词汇 · 解析不了的裸路径

⚔️ D · 内部矛盾         5 条   `_EVIDENCE_*` 一边禁一边用 · 四行 `PROBE:` 归错相位 · mode vs route
```


### 🔀 A · 双生漂移

```
▸ A1   🔴 [M]   application/2-phase/0-draft/haipipe-application-draft/SKILL.md:37     ⏸️ R2 延后
   问题   整份文件没有人类闸之前的自审，流程从 4. RAISE+PLAN 直接跳到 5. PRESENT
   证据   probe 的 DRAFT rule 4（probe/haipipe-probe/SKILL.md:247 + 检查表 :91-106）两个 family 都要求
          grep 确认 application/2-phase/ 全域零命中
   改法   :36 与 :37 之间插入 4b. SELF-REVIEW，照搬 paper 的对应段
          Surface A 换成 application 的 artifact spec，Surface B 逐字沿用probe 的检查表，bounded 2 轮

▸ A2   🔴 [M]   application/.../SKILL.md:5                                            ⏸️ R2 延后
   问题   allowed-tools 里没有 Agent，A1 的改法根本跑不动
   证据   paper 的 :5 有；同族 haipipe-application-probe 的 :5 也有
   改法   追加 `, Agent`。必须和 A1 同一批改

▸ A3   🟡 [M]   application/.../SKILL.md:16
   问题   从不按路径指向probe，只在 :79 括号里提过一次「probeon's PHASE MAP」
   证据   probe :241 要求 worker「POINTS here」，:20 声明冲突时probe赢
   改法   照抄 paper 的 `## Rules (follow these — the model is haipipe-probe's)` 段

▸ A4   🟡 [M]   paper/.../SKILL.md v5.0.0 :97   🔴 仍成立
   问题   叫人「Report status: blocked」，但全文没有 return contract 定义 status
   证据   磁盘核验：`## Return contract` 零命中；application 在 :85-94 有
   改法   文件末尾加一段，照 application 的形状

▸ A5   🟡 [J]   paper/.../SKILL.md v5.0.0 :193   🔴 仍成立（L136/L189 说要呈示，Step 5 本体没做）
   问题   STOP 只呈现 draft，不呈现 probe plan
   证据   probe :81/:87 合并成一个闸，人类要审「the draft AND the probe plan」；paper 自己也这么说
   裁决   证据确定 → 按最佳读法：扩成 draft + 每个 raised question 一行 + 自审结论

▸ A6   🟡 [J]   application/.../SKILL.md:41
   问题   镜像的另一半窟窿：5. PRESENT 只呈现问题清单
          没有 draft 呈现、没有 `> USER:` / `> CC:` 协议、没有迭代循环、没有 confirm/交接
   裁决   证据确定 → 按最佳读法：step 5 扩成也呈现 draft，补一个 step 6 镜像 paper

▸ A7   🟡 [M]   application/.../SKILL.md:30
   问题   从不要求把 `→ 1-probes/PP<NN> · QX<n>` 回指写进 stage-doc 的 Q-<Stage>-<n>
   证据   probe :89 要求；grep `backlink|→ 1-probes|-> PP` 零命中
   改法   :30 末尾追加回指子句

▸ A8   🟢 [M]   paper/.../SKILL.md v5.0.0 :143-146   🔴 仍成立
   问题   FORBIDDEN 段没点名唯一入口（application 的 :81 点了 haipipe-application-probe）
   改法   补一句：证据只能经 PROBE 相位派发 haipipe-paper-probe 落地

▸ A9   🟢 [M]   paper/.../SKILL.md v5.0.0 :131 · :134   🟡 部分（a 仍成立；b 被 L33 新规则缓解但 L134 自己写裸 \cite{TOADD}）
   问题   两个小句 application 有、paper 没有
          (a) 只写 WebSearch 没写 WebFetch —— 但 :5 声明了 WebFetch
          (b) 第一个 destination 缺「anything load-bearing stays a raised question」
   改法   两句都镜像过来

▸ A10  🟡 [M]   paper/.../SKILL.md v5.0.0 :146   🔴 仍成立
   问题   只说 CHECK gate 跑 check-probe-cards.sh，漏了 probe worker 的 VERIFY
   证据   probe 的 PROBE rule 6（:256）；application 的 :83 两个都写了
   改法   采用 application 的措辞
```


### 🕳️ B · 提问被降级

```
▸ B1   🔴 [J]   paper/.../SKILL.md v5.0.0 :135-141（仍嵌在 :131 下）   🟡 部分（Step 4a 是扫洞，不是 RAISE+PLAN；规范住所仍在嵌套块内）
   问题   probe 的 DRAFT rule 2 的唯一规范表述，嵌套深度 3：
            ### Step 4. Draft content
              └ 加粗旁注 **Inline WebSearch is ALLOWED here**
                └ 「exactly two legal destinations」有序列表
                  └ item 2 ← 就在这
          作用域被父话题窄化成「when the search reveals a gap」——
          不来自网搜的问题（读上游读出来的、{VAL:?} 撞出来的）无家可归
   注意   v5.0.0 新加的 Step 4a 是**扫洞**（产出占位符），不是 RAISE+PLAN（产出 probe entry）
          两件相关但不同的事，正统那个还埋在原地
   改法   提升为独立顶层步骤，WebSearch 段留一行指针

▸ B2   🔴 [M]   paper/.../SKILL.md v5.0.0 :135-141   🟡 部分（:158 新增了 Q-consumer 折回，但只覆盖三 lane 抛回的；通用路径 :137 仍缺）
   问题   全文从不指示写 stage doc 里的 `## Q-<Stage>-<n>`
   证据   probe 的 rule 2 是个合取：「raise a `## Q-<Stage>-<n>` in the stage doc's Q-consumer
          AND author its probe ENTRY」。paper 只写了 ENTRY 那一半，
          然后预设 id 已存在，自审还去检查它 —— 检查一个从没被要求创建的东西
          application 两半都有（:29-30）
   改法   补上 Q-consumer 那一半

▸ B3   🟡 [J]   三份文件都有                                      ✅ 已由 R1 裁决
   问题   都没有「怎么找到值得问的问题」的方法，只有触发条件
          probe 的 rule 2 开头就是 "For each open question" —— 预设问题已经存在了
   裁决   → R1：per-stage 写「这里一般会问什么类型的问题」。展开见上。

▸ B4   🟡 [J]   paper/.../SKILL.md v5.0.0 :41-47   🔴 仍成立
   问题   `## What DRAFT means` 把相位纯粹定义成产物生产（"DRAFT = settle WHAT to say"），
          零字提及提问
   证据   与自己的 frontmatter 和自己的正文矛盾
   裁决   证据确定 → 按最佳读法：定义里补上第二个产出

▸ B5   🟡 [M]   paper/.../SKILL.md v5.0.0 :137   🔴 仍成立（find-or-open / T0 JOIN 全文零命中）
   问题   写成「author its q-executor ENTRY」，丢了probe的 **find-or-open**（:82）
          成本阶梯的 T0 JOIN（:212）全文不出现 → 起草者会开重复 entry
   改法   恢复 find-or-open + T0 JOIN 子句

▸ B6   🟡 [M]   paper/.../SKILL.md v5.0.0 :177-180   🔴 仍成立（v5.0.0 的头号规则 L33 没进自检）
   问题   自审没有「完整性」检查
          Surface A 查的是 Q → 句子；反过来 句子 → Q 没人查
   证据   这是一条「有规则没检查器」：Rules 段已写「A placeholder with no bracket is a defect」，
          但两个 Surface 都不测它
   改法   Surface A 补一条：每个 {VAL:?} / \cite{TOADD} 都带 [Q-<Stage>-<n>]，
          否则在 _LOG 里显式 decline

▸ B7   🟡 [J]   application/.../SKILL.md:79
   问题   entry 合同的唯一完整表述（route/bank/target 全字段）被条件化在
          「when the search reveals something…」上，藏在 `## DRAFT may search; PROBE must dispatch` 里
          顶层 fenced 块（:28-36）只是压缩版
   改法   规范那半提成独立段落，搜索段留一句回指
```


### 🚚 C · 搬家没改地址

```
▸ C1   🟡 [M]   paper/.../SKILL.md v5.0.0 :137 · :264   🔴 仍成立（fn/probes.md 里 "Status board" 零命中，per 引用悬空）
   问题   叫 DRAFT 手写「a Status board row」，但这个 board 是生成的
   证据   paper/haipipe-paper/SKILL.md:66「the probe FILES are the source of truth —
          the README's Status board regenerates from them」
          probe/haipipe-probe/CHANGELOG.md:286 记「(GENERATED)」
          磁盘核验：fn/probes.md 里 "Status board" 零命中 → 「per fn/probes.md」也是悬空引用
          probe v9.5.0 全文不提 Status board；application 也没有
   改法   两处子句都删掉

▸ C2   🟡 [M]   paper + application 两边
   问题   裸路径（`1-lifecycle/…`、`2-phase/REF/prose-quality.md`）从 skill 自己的目录解析不了
   证据   磁盘核验：haipipe-paper-draft/ 下没有 1-lifecycle/；真实目标是 ../../../1-lifecycle/…
          paper/2-phase/REF/prose-quality.md 确实存在
          同一个文件别处却用了正确的 ../ 前缀 —— 自我不一致
   改法   两个 family 的表格路径都补前缀

▸ C3   🟡 [M]   paper/.../SKILL.md v5.0.0 :175   🔴 仍成立
   问题   自审的子代理 prompt 里传相对路径 `../../../../probe/haipipe-probe/SKILL.md`
          fresh 子代理从仓库根解析，那里不存在
   改法   prompt 内改用仓库根相对路径

▸ C4   🟢 [M]   paper/.../SKILL.md v5.0.0 :212   🔴 仍成立（两个退役词同句）
   问题   退休词汇
          「buffer rule」/「buffered probes」—— probe v9.5.0 全文零命中 "buffer"
          「Probes proposed by this draft」—— 现名是 "Questions raised by this draft"
   注意   args="from-buffer …" **不是**残骸 —— 那是 haipipe-paper-probe 现役的 argument-hint
   改法   只改那两处措辞

▸ C5   🟢 [M]   application/2-phase/0-draft/haipipe-application-draft/CHANGELOG.md:4
   问题   声明「Newest first」，实际顺序错乱
   证据   磁盘核验：1.3.1(:7) → 1.1.0(:14) → 1.0.0(:18) → 1.2.0(:22) → 1.3.0(:26)
   改法   把最后两块整体移到 1.1.0 之上

▸ C7   🟡 [M]   6 个 CHANGELOG（R4 顺带查到，不是这次造成的）
   问题   都指向 `../../SKILLSET_REVIEW.md` = paper/2-phase/SKILLSET_REVIEW.md，该文件不存在
   证据   git：7aadb905 加进来，faeee359（haipipe-session v1.1.0）删掉，引用没跟着改
          paper/2-phase/0-draft/haipipe-paper-draft/CHANGELOG.md:9
          paper/2-phase/0-draft/haipipe-paper-draft-citation/CHANGELOG.md:9
          paper/2-phase/0-draft/haipipe-paper-draft-values/CHANGELOG.md:9
          paper/2-phase/0-draft/haipipe-paper-draft-display/CHANGELOG.md:9
          paper/2-phase/1-probe/haipipe-paper-probe/CHANGELOG.md:9
          paper/2-phase/2-revise/haipipe-paper-revise-place/CHANGELOG.md:9
   改法   等上面「约定问题」定了再动 —— 选 A 就改指 _console/，选 B 就把文件补回 bucket 根

▸ C6   🟡 [M]   application/.../SKILL.md:61
   问题   section-edit 那行的 Template 列写「per-section scaffolds in that skill」，
          但那个 skill 目录下只有 SKILL.md + CHANGELOG.md
   证据   该 skill 的 :81 自己说「There is no single stage template — each section's scaffold IS its outline」，
          scaffold 生成在项目里的 0-lifecycle/5-section-edit/{section}/
   改法   该格改成指向项目里的那个路径
```


### ⚔️ D · 内部矛盾

```
▸ D1   🔴 [J]   paper/.../SKILL.md v5.0.0 :229 :234 :239 :246   🔴 仍成立（5 命中）
   问题   stage 备注里的 `PROBE:` 行把「提问引出」派给了 PROBE 相位
            PROBE: link evidence sources, spawn probes for GAPs
            PROBE: citation audit for anchor papers
            PROBE: citation + display needs per beat
            PROBE: step-0 cross-stage coverage sweep, …
   证据   违反probe 的 PROBE rule 1（:251「do NOT re-author or re-match them」）
          也违反 paper 自己的正文（「DRAFT is where the questions are born AND planned」）
   裁决   → R1：不是「改标签」，是**搬家** —— 搬进各 stage skill，成为该 stage 的问题类型清单

▸ D2   🟡 [M]   paper/.../SKILL.md v5.0.0 :35   ✅ 已修（_EVIDENCE_* 已删；"read sections" → "entries already `read`"）
   问题   T1 LOCAL 把 target 指进 `_EVIDENCE_*` 当 registry，但 Rules 段说 `_LOG_<stage>.md` 是唯一 sidecar
          同一句里还有未定义词汇「read sections」（probe里 read 是 state: 的值，不是 section）
   改法   删掉 `_EVIDENCE_*` 和「read sections」

▸ D3   🟡 [M]   paper/.../SKILL.md v5.0.0 :114-118   🟡 部分（seed 已补；claims/pitch/narrative/section 仍缺；display 用退役词 "Probes rows"）
   问题   Step 3 的结构清单对 claims / pitch / narrative / display / section 都没列 Q-consumer
   证据   磁盘核验：只有 seed 和 resource 列了
          probe :72 要求它「lives at the END of every stage doc」
          1b-claims/.../SKILL.md:69-70 明写「Three sections -- Hypotheses, Claims, Q-consumer」
          2b-pitch/.../SKILL.md:62,76 同
   改法   那五条 bullet 和末尾表格行都补 `+ Q-consumer`

▸ D4   🟢 [J]   application/.../SKILL.md:39 :92
   问题   按 per-question 汇报 mode，但 `**mode**: light | full` 是 probe 文件级的头字段（probe :141）
          per-ENTRY 的派发门是 route（:153 :166），两行都漏了 —— probe :85 称它 AUTHORITATIVE
   证据   CHANGELOG.md:28 显示 1.3.0 本来写的是 route，1.3.1 换成了 bank
   裁决   证据确定 → 改成汇报 route + bank，删掉 per-question 的 mode

▸ D5   🟢 [M]   paper/.../SKILL.md v5.0.0 :147 :251   ⬜ 未复核
   问题   同一个对象混用 ENTRY 和 section
   证据   application 全文统一用 ENTRY。但probe 自己也混（:162/:136 说 entry，:96/:219 说 section）
          paper 是继承的漂移，不是自己发明的
   改法   paper 统一成 ENTRY，另开一条对probe的规范化
```


### 🆕 N · v5.0.0 自己引入的（第 0 轮复核新增，原 28 条未覆盖）

```
▸ N1   🔴 [M]   paper/.../haipipe-paper-draft/SKILL.md:5  vs  :153-155      ✅ 已修 v5.0.2
   问题   Step 4a 的全部内容就是三个 Skill() 调用，但 allowed-tools 没有 Skill
   证据   :5   allowed-tools: Bash, Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Agent
          :153 Skill("haipipe-paper-draft-citation", args="<stage-or-section> <paper-path>")
          :154 Skill("haipipe-paper-draft-values",   …)
          :155 Skill("haipipe-paper-draft-display",  …)
          （:230 的 Skill("haipipe-paper-probe" …) 是同一漏洞的旧例，但那在 stage 备注里，
            Step 4a 是必经路径）
   改法   :5 追加 `, Skill`
   ⚡     v5.0.0 的旗舰步骤按声明无法执行 —— 优先级高于原 28 条里的任何一条

▸ N2   🔴 [J]   :158  vs  三条 lane skill                                    执笔权冲突
   问题   问题由谁写进 Q-consumer？两边都说是自己
   证据   hub  :158  「Fold those new questions into the Q-consumer and author
                       their ENTRIES per Step 4」                    ← hub 执笔
          haipipe-paper-draft-citation/SKILL.md:90
                「RAISE a new `## Q-<Stage>-<n>` in the stage doc's Q-consumer,
                  and author its ENTRY in 1-probes/ per haipipe-paper-draft」  ← lane 执笔
          haipipe-paper-draft-values/SKILL.md:78  同
   后果   双向回指 + 双向执笔 → 要么重复写入，要么互相等待
   改法   定一个执笔方。倾向 lane 只 RETURN 洞、hub 统一执笔（单写者，和 QA 文件同理）

▸ N3   🔴 [M]   :126 · :134 · :179 · :264   vs  :33                          自相矛盾
   问题   v5.0.0 的头号规则说「没方括号的占位符就是缺陷」，同一文件四处写裸占位符
   证据   :33  「A placeholder with no bracket is a defect」
          :126 `\citep{key}` … `\cite{TOADD}`           ← 裸
          :134 with `\cite{TOADD}` slots                ← 裸
          :179 gaps use {VAL:?} / \cite{TOADD}          ← 裸（在自检清单里！）
          :264 every {VAL:?}/\cite{TOADD} rolled up     ← 裸
          只有 :34 和 :158 带了 [Q-<Stage>-<n>]
   改法   四处都补 [Q-<Stage>-<n>]。这也是 A9b 的根因

▸ N4   🟡 [M]   :117 · :240 · :258 · :310                                    退役名
   问题   还在用 "Probes section" / "Probes rows"
   证据   probe/haipipe-probe/SKILL.md:70「the `Q-consumer` section in a stage doc (was "Probes")」
   注意   与 C4 / D3 同类；但 display / narrative 两个 stage skill 自己也还没迁移，
          单改这一份会造成不一致 —— 要一起改

▸ N5   🟡 [M]   三条 lane 全中，不是一条                                    ✅ 已修 v1.0.1 ×3
   问题   allowed-tools 都是 Bash, Read, Edit, Grep, Glob —— 没有 Write
   证据   haipipe-paper-draft-display   往 0-lifecycle/4-display/_DISPLAY_REQUEST.md 归档 DR row
          haipipe-paper-draft-citation  :90「RAISE a new `## Q-<Stage>-<n>` … author its ENTRY in 1-probes/」
          haipipe-paper-draft-values    :78「RAISE a new Q-consumer + its ENTRY」
          三个落点（DR inbox / 1-probes/PPNN_<topic>.md）在首次使用时都不存在，Edit 建不出来
          → 恰恰在这条 lane 存在的理由那一刻失败：一篇论文的第一个洞
   改法   三处 :5 各追加 `, Write`

   扫描复核：全 skills/ 扫「正文调用了 Skill(/Agent(/Write 但未声明」，另有 11 处命中，
   逐条验后全是假阳性 —— paper/haipipe-paper 的 Agent( 是文档说明、
   0_utils/haipipe-run-timeline 的 Skill( 在 ASCII 时间线示例里、
   haipipe-paper-draft-citation:24 的 Agent( 是在讲问题稍后去哪。同族已归零。
```


## ⚠️ 跨 console 文件的两个坑

```
1  id 撞车
   260719-PHASE-BOUNDARY-REFACTOR.md 有它自己的 D1–D5，和本文件的 D1–D5 是不同的东西。
   引用时必须带文件名。（要不要在 _console/ 层面统一 id 空间，你定。）

2  主题重叠 —— 这两条该让位，不该两处并行裁
   本文件 D1「四行 PROBE: 归错相位」  ≈  260719-PHASE-BOUNDARY-REFACTOR.md 的整场重构
   本文件 D4「mode 按 per-question 汇报」 ⊂ closed/260719-MODE-RETIREMENT.md（整条 mode 要不要废
   → ✅ 已裁决 A 退役并执行完毕；D4 因此消失，mode 已不是字段）
```


## 🔍 覆盖诚实度

```
方法      三个 fresh-context 只读审计员并行跑，主会话信任门抽查
          抽查抓到 3 个审计员共 4 处需修正，已在上面各条里改过

未审计    调用这两个 worker 的 stage 编排器（1-lifecycle/*）
          PROBE / REVISE / CHECK 三个 worker
          check-probe-cards.sh 本身
          display / narrative 两个 stage skill 自己是否也该迁移退休名「Probes」

顺手发现  1-lifecycle/haipipe-application-venue/ref/venue-template.md
          是 application 九个模板里唯一没有 Q-consumer 段的，与probe :72 冲突

失效      本文件对 haipipe-paper-draft 的所有行号 —— 该文件已升 v5.0.0（307 → 321 行）
          已复核仍成立：A4 B1 B2 B4 C1 D1 D3
          未复核：其余
```


## 📌 review 放哪 —— 已定（R6）

> JL: haipipe-skill-diagnose/SKILL.md:46 please also change this, and make SKILLS to save things to a _console folder?

>> CC0719: ✅ 选 A（`_console/` 取代 bucket 根），已执行：
>>          haipipe-skill-diagnose 的 :46 · [J] thread MIRROR 落点 · RESOLVE 回复扫描 ·
>>          COMMIT 闸 + git add 范围 · return contract · ref/thread-protocol.md ·
>>          ref/finding-taxonomy.md，全部改指 `skills/_console/<YYMMDD>-<SLUG>.md`
>>          新增 MUST NOT：「Write the review ledger into the bucket being reviewed」
>>          新建 `_console/README.md` 定死这个文件夹的合同
>>          现存 4 份已结案的（0_connect/ · task/ · task/1_data/ · task/3_end/）留在原地 ——
>>          有 CHANGELOG 引着它们的路径，搬了就断。只有新 review 走 `_console/`
>>          C7 的 6 个悬空引用另行处理：它们指向的 paper/2-phase/SKILLSET_REVIEW.md
>>          在 faeee359 就被删了，已把悬空路径摘掉、保留出处说明
