# insight/ Skill-Set Review (2026-07-05)

Scope: all 7 skills under `skills/insight/` (orchestrator + data/information/knowledge/wisdom/review/explore), agents/ (4 creators + 5 reviewers + 2 templates + README), ref/ (9), play/ (7), scripts/export_okf.py, root DESIGN.md + CHANGELOG.md, fn/ + feedback/ + PREFERENCES.md.

Status: **EXECUTED 2026-07-05** on JL's go ("我把我的comments都加进去了，你去改改吧。"). Every `[M]` item is applied exactly as its 我改成 line states (deviations listed in Part 3); `[J]` rulings applied per the ✅ notes inside each thread. ALL RESOLVED 2026-07-05: E5=A, D3 relanded caller-based dual-mode, D1-③ ask-session deleted. Awaiting commit order only. Decisions archived with verbatim quotes in the layer CHANGELOG.md 3.2.0 + each skill's CHANGELOG. NOT committed.

Audit method: core files read line-by-line by the main session; 3 read-only subagents deep-audited (1) the 6 sub-skills, (2) the 12 agent files, (3) ref/ + play/ + scripts + fn/. The 9 highest-severity claims were re-checked by hand against the actual files, 9/9 confirmed. Every file in the tree was read.

How to read:

- 🔴 broken: an agent following this text does the WRONG thing (dead path, dead rule, invalid example)
- 🟡 stale: works, but the text lies about disk / schema / itself
- 🟢 cosmetic
- `[M]` mechanical fix, no judgment needed. `[J]` your decision needed, has a `> JL:` slot.
- Tick `[x]` = fix it. Leave `[ ]` = skip. Disagree: write under the item.

---

## 词汇速查 (读下面的 findings 只需要这 6 个词)

- **recut (重切)**: 2026-06-22 的 3.0.0 大改。你把 DIKW 的分界改成: **D/I = 样本内描述** (必须写明 `dataset:`, 不许带 p 值/CI), **K = 样本外概括** (p/CI/confidence 只住这一层, 不需要 probe 把关, 低置信和阴性 K 也照记), **W = 按 K 的 confidence 调风险的行动**。本轮最大一类问题就是: 这次重切改了主干文档, 漏了一批周边文档。
- **claim_type**: 3.1.0 给 K 卡加的必填字段, `associational | causal` 二选一; 写 causal 必须点名识别策略 (RCT / 强 IV / RDD / DiD)。
- **writer / creator / reviewer / auditor**: writer = 四个写卡技能 (`haipipe-insight-{data,information,knowledge,wisdom}`); creator = 包着 writer 跑无人值守的 agent; reviewer = 单卡质检 agent (每层一个); auditor = 查整个引用图一致性的 agent。
- **dual-mode / headless**: 同一个技能两种被调法。人调它, 缺字段就问; agent 调它, 缺字段就返回 `status: blocked`, 绝不挂起等人。
- **--id 预分配**: apply 并发写多张卡之前, 先把 D01/D02... 编号统一分好, 传给每个 writer, 防止两个并发 writer 都给自己编成 D01。
- **dogfood**: ProjB (Opioid 项目) 真实在用的 `insights/`, 有 D/I/K/W 卡各一批 + INDEX + _reviews/。下面凡说"dogfood", 就是拿这个地面真相对照文档。

---

## Part 1: 根因总图 (先看这个)

```
① ✂️ recut 没扫完   3.0.0 重切改了主干, 漏了周边 (A 组, 11 条)
                    最痛的三个: invocation-modes.md 整个没动 · explore 整个没动 ·
                    K writer 缺 claim_type
② 📐 ref 前缀写错层  4 个 writer 的必读清单指向不存在的目录, 24 条死指针 (B 组)
③ 📄 账本失真        7 本 CHANGELOG 顺序乱 · 2 个技能版本号落后正文 ·
                    DESIGN 表头过期 (C 组)
④ 🪝 退役层引用      narrative 当活层引用 ~40 处 · 一个虚构的 console 文件 (D 组)
⑤ ⚔️ 契约内讧        同一条规矩两处各说各话, 5 起 (E 组)
```

骨架本身健康: 7 个 SKILL.md 的 frontmatter 全部合法、名字和文件夹全对上; 9 个 agent 在插件注册表里的 symlink 全部有效; 四个 writer 的 dual-mode 契约齐全; export_okf.py 语法干净, 在 dogfood 上实跑通过 (14 张卡全解析)。

---

## Part 2: findings

### A. recut 没扫完 (旧模型残留)

- [x] **A1** 🔴 `[M]` **`ref/invocation-modes.md` 整个没被重切扫到。** 这个文件是四个 writer 共用的"输入什么才算齐"契约, 每个 writer 的第一步都让 agent 来读它。
  > 它现在说: `:39` "information --scope: **≥ 2 existing D ids**" · `:40` "knowledge: **judged source_ref**" · `:62-64` "**knowledge refuses unjudged claims**, probe claims without confirmed/refuted status ... **information still refuses < 2 D entries**"
  > 现行规矩 (3.0.0): I 只要一个点名的 dataset + 它的 D 卡 (≥1 张就行); K 不需要任何 judged/probe 身份, 只要 claim + generalization basis + confidence。
  > 真实例子: dogfood 里的 I01 是 `sources: [D01]`, 只有一张 D。一个听话的 headless writer 按 `:64` 会返回 blocked, 也就是拒写现实里每一张合法 I 卡。
  > 还漏了: `:38-40` 的"输入齐不齐"表没列 `dataset:` (D/I 必填) 和 `claim_type` (K 必填); `:44-45` "NN is always auto-assigned" 跟 3.1.0 的 --id 预分配唱反调。
  > 我改成: 按现行字段重写那张表; 拒收规则改成 "I: 没点名 dataset 或该 dataset 没有 D 卡才拒; K: 缺 claim / basis / confidence / claim_type 才拒"; 补一句 "--id 预分配时不自动编号"。

- [x] **A2** 🔴 `[J]` **`haipipe-insight-explore/SKILL.md` 整个没被重切扫到, 而且它扫的字段在磁盘上根本不存在。** explore 是"KB 仪表盘"技能: 扫一遍项目, 告诉你已有什么卡、缺什么、什么能升级。
  > 它现在说: `:38` 读 probe.yaml 的 "**result.status** (pending | confirmed | inconclusive | refuted | exploratory)" · `:37` 目录形状 "probes/\<GROUP\>_\<slug\>/\<NN\>_\<slug\>/" (两层) · `:3,19,40,53,75-76,89` 一切分析都以 "probe 是否 CONFIRMED" 为轴 · `:45,54` 用 `source_experiment` 字段和 "P 卡" (都是退役概念)。
  > 磁盘真相: 真 probe.yaml 是顶层一个 `status:` 字段 (值如 `deposited`), 没有 result.status; 真目录是一层平铺 `probes/0605_discretion-gradient/`。
  > 不改会怎样: 照文档执行, 扫描匹配不到任何 probe, 仪表盘永远回答"这个项目没有可归档的东西"。而且"confirmed 才算 ready"正是 3.0.0 明确废掉的那道门。
  > 这不是打补丁, 是重写。给你两个选项:
  > 选项 A: 现在就按现行模型重写 explore (扫平铺 probes/ 读顶层 status; gap 分析改成 "哪些 dataset 有 D 没 I / 哪些 I 有 basis 没 K / 哪些 K 没 W")。
  > 选项 B: 先在文件头挂一条 STALE 横幅 ("本技能未随 3.0.0 重切, 输出不可信, 待重写"), 等下次真要用仪表盘时再重写。
  > 我的倾向: A, 一次清完, 免得横幅一挂半年。
  > JL: 重新写吧
  > ✅ 已重写: explore SKILL.md 2.0.0 整篇按现行模型重写 (per-dataset 链式覆盖 D→I→K→W、未审已定材料检测、读顶层 status:、平铺 probes/ 目录、--out 正式进 argument-hint)。

- [x] **A3** 🔴 `[M]` **K writer (`haipipe-insight-knowledge/SKILL.md`) 缺 `claim_type`, 按它写出来的 K 卡必被质检打回。** 全文 grep `claim_type` = 0 次 (亲手验过), 但 3.1.0 起它是 K 卡必填字段, K reviewer 的 checklist 明确查它。
  > 例子走一遍: 你让 writer 填一张 "LBP 队列的 agreeableness 梯度可推广" 的 K 卡 → writer 按自己的 quick-reminder 只填 claim + confidence → card-reviewer-knowledge-agent 按 checklist 查 "claim_type 在不在" → 不在 → FAIL, 打回。写卡和质检两边的规矩不同步, 卡永远过不了。
  > 同文件还有四处旧模型残留: `:125` "back-links on cited **P/D** entries" (P 卡层早不存在, K 现在引 I 卡); `:169,:177` 同样的 P/D + 一个 D 卡 schema 里没有的 "Cross-references" 正文小节; `:155-157` 教人把 supersede 写进正文某小节, 但 schema 里 `supersedes:` 是 frontmatter 字段; `:84-85` 提到 `contradicts` 字段, schema 没这个字段 (争议用 `status: contested` 表达)。
  > 我改成: Input / quick-reminder / 工作流 / DoD 四处补 claim_type; 反向链接改成"给被引 I 卡的 `ref_by:` 加一行"; supersede 和字段名对齐 schema。

- [x] **A4** 🔴 `[M]` **"probe gate" 这个已废除的门, 还挂在三处花名册里。**
  > 它现在说: `haipipe-insight/SKILL.md:217` "card-reviewer-knowledge-agent.md 🟨 accuracy + K boundary + **probe gate**" · `DESIGN.md:217` "🟨 + the ★ probe gate" · `DESIGN.md:149` "K sources:[probe/lit refs] **MUST be judged**"。
  > 为什么错: K reviewer 的 agent 文件自己都写着 "NO probe is required"。花名册在替一个已拆掉的门站岗。同一份 orchestrator 里 `:433-437` (Review Funnel 段) 说的是对的, 等于一份文件前后互相打架。
  > 我改成: 三处都改成 "confidence + claim_type presence (no probe gate)"。

- [x] **A5** 🔴 `[M]` **I 卡质检员 (card-reviewer-information-agent) 的开场白还是旧规矩, 会错杀合法卡。**
  > 它现在说: description (`:3`) "the pattern is actually visible in the **≥2 cited D cards**"; 开篇格言 (`:23`) "*A pattern earns the name only if **≥2 observations** actually show it.*"
  > 为什么错: 正文 checklist 已经改对了 (单 D 可过), 但 description 和格言是 agent 最先读、印象最深的两行。dogfood 的 I01 (`sources: [D01]`) 送审, 按这两行就是"引用不足, FAIL"。
  > 连带: `agents/creators/_TEMPLATE.md:57-58` 的分层门槛表也还是 "I: at least two D ids; K: judged source", 以后谁用模板造新 creator, 死规矩就跟着复活。
  > 我改成: description 和格言改成"模式在点名 dataset 的 D 卡里真实可见"; 模板的门槛表按现行契约重写。

- [x] **A6** 🔴 `[M]` **新人教材 `play/04_cards_after_apply.md` 里的两张示例卡都不合 schema, 照抄必被打回。**
  > K 示例 (`:11-24`) 的问题: ① 没有 `claim_type:` (必填); ② 用了 `refs:` 字段, 卡片 schema 里没有这个字段 (它是 INSIGHT_REVIEW.yaml 候选清单里的字段, 抄进卡片就是非法字段, auditor 会报)。
  > W 示例 (`:60-71`) 的问题: ① 带着 `confidence:` (那是 K 的字段, W 没有); ② W 的必填三件套 `rec` / `rec_type` / `cost` 一个都没有。
  > 不改会怎样: play/ 的定位就是"新人第一次照着做", 第一次照着做就撞质检。
  > 我改成: 两张示例卡按 schema 重写 (K 补 claim_type、refs 并进 sources 或删; W 换成 rec/rec_type/cost 齐全的样子)。

- [x] **A7** 🔴 `[M]` **教科书自己的旗舰示例不合自家规矩。**
  > `ref/dikw-boundaries.md:290-302`: 这个文件自己定义了 "K 必须有 claim_type", 但它的旗舰 K01 示例卡 frontmatter 里没有 claim_type (正文倒是写了一句 "Associational, not causal", 机器读的字段缺失)。
  > `ref/insight-md-schema.md:345-373`: schema 的 Validation rules 一节逐条列了 K 卡要查什么, 唯独没查 claim_type, 虽然同文件 `:108` 声明它 REQUIRED。reviewer 若按 validation 清单走, 会放行缺 claim_type 的卡, 跟 A3 的 writer 缺口凑成一对。
  > 我改成: K01 示例补 `claim_type: associational`; validation rules 补一条查 claim_type。

- [x] **A8** 🔴 `[M]` **两处示例把"I 该干的事"教成了 D, 正好踩在重切的分界线上。** 重切后的分界: D = 这个数据集长什么样 (几行几列、时间窗、缺失率); I = 数据集内部的模式 (谁比谁高、什么随什么变)。
  > `ref/review-contract.md:117-124` 旗舰例子 C1 把 "OOD split error **by arm**" (按组对比一个指标, 这是模式, 该归 I) 当成 D 卡候选, 还标 "unit: observation" (退役词)。
  > `ref/card-granularity.md:105-113` "Good: D01: FiLM validation **MAE is lower** across 3 seeds": "谁更低"是比较性陈述 = I。同一份文件 `:83` 自己的分层定义 ("D = one named dataset's profile") 是对的, 例子跟定义打架。
  > 我改成: 两处例子换成真正的 D (数据集画像) 和真正的 I (内部模式), 各给一张。

- [x] **A9** 🟡 `[M]` **ref/ 里的零散旧词残留** (每条一行, 都是小改):
  > `ref/index-templates.md:30-31` 示例行 "I02 — pattern across **3 D entries**" + "D01, D02, D03 — **observations**": 多 D 的 I + "observation" 都是旧模型词, dogfood 的 INDEX 已经写成 "cohort dataset profiles"。
  > `ref/insight-context-loading.md:151` 教人读 "I02.sources → D01, D02, D03" (多 D 的 I); `:207-208` 让人把内容收进卡片的 "Notes section", 哪个层的 schema 都没这个小节。
  > `ref/okf-compat.md:35-38` 语义对照表写 "D = observation" (旧词); `:66-69` K 的字段清单漏 claim_type。
  > `ref/insight-md-schema.md:308-339` W 示例缺自己模板要求的 `## Risk posture` 小节; `:322,:325` 教的 probe 命令是退役动词 "design new" / "bridge" (现行是 "plan new", dikw-boundaries `:359` 就是对的)。

- [x] **A10** 🟡 `[M]` **W writer 的三处旧话** (`haipipe-insight-wisdom/SKILL.md`):
  > `:3` "Reads K_knowledge entries (**validated beliefs**)": "validated belief" 是重切前对 K 的叫法, 现在 K 是"带 confidence 的概括判断" (可以低置信、可以阴性), 不是"已验证的信念"。
  > `:76` "invokes **/haipipe-probe design new**": 退役动词, 现行 "plan new"。
  > `:133` DoD 要求检查 "counter-arguments engaged in '**What would change...**'" 小节: W 的 schema 里没有这个小节, 现存的对应物叫 `## Decay condition`。

- [x] **A11** 🟡 `[M]` **agent 文件里的零散旧话** (每条一行):
  > `agents/reviewers/card-reviewer-knowledge-agent.md:94` 结构化返回的枚举结尾还有 "| **no judged source**" (它自己正文 `:85-88` 的失败条件已经改成 "no generalization basis")。
  > `agents/reviewers/card-reviewer-data-agent.md:3` + `agents/creators/card-creator-data-agent.md:62-63` 说数字要"trace to the **probe**": 正文明明允许 task:/probe:/discover:/lit: 四种来源, description 只提 probe, 以偏概全。
  > `agents/README.md:29` K 层边界摘要只写 "confidence present", 漏了 3.1.0 起同样必查的 claim_type。
  > `agents/reviewers/_TEMPLATE.md:44-49` 该读清单漏了 dikw-boundaries.md (真 reviewer 都把它列第一位), `:48` 的来源举例还是旧的。

### B. ref 前缀死路 (系统性, 全部机械修)

- [x] **B1** 🔴 `[M]` **四个 writer 的必读清单, 24 条里 15 条指向不存在的目录。** 病根一张图:
  > ```
  > 从 haipipe-insight-data/SKILL.md 出发:
  >   ../../ref/   → skills/ref/           ❌ 目录不存在
  >   ../ref/      → skills/insight/ref/   ✅ 9 个文件都在这
  > ```
  > 中招的行: `haipipe-insight-data/SKILL.md:22,86,99,121,144` · `haipipe-insight-information/SKILL.md:23,25,114` · `haipipe-insight-knowledge/SKILL.md:23,82,132` (妙的是它 `:111` 用了正确的 `../ref/`, 一份文件两种前缀) · `haipipe-insight-wisdom/SKILL.md:20,38,98`。
  > 为什么会这样: 3.0.0 时修过一次路径, 但只修了 orchestrator 自己 (changelog 原话 "made the orchestrator's ref/ paths consistent"), 四个 writer 没扫。agents/ 下的文件反而全对 (它们多一层目录, `../../ref/` 从那里出发正好落对)。
  > 不改会怎样: writer 第一步就是"去读 schema 和边界文档", 读到的是"文件不存在", agent 要么瞎猜要么带病干活。
  > 我改成: 15 处前缀 `../../ref/` → `../ref/`, 纯 sed。

- [x] **B2** 🔴 `[M]` **review 技能同病, 裸 `ref/` 也落空。** `haipipe-insight-review/SKILL.md:48-53,141-142,220` 写的是裸 `ref/review-contract.md` 等 9 条, 从它自己文件夹出发解析成 `haipipe-insight-review/ref/`, 这个目录不存在 (验过)。而这是全家规矩最重的技能 ("动卡之前必读契约")。修法同上: 加 `../`。

- [x] **B3** 🟡 `[M]` **三个小路径瑕疵**:
  > `haipipe-insight/SKILL.md:43` "read play/README.md": 从 orchestrator 文件夹出发该是 `../play/README.md`。
  > `haipipe-insight/SKILL.md:293` Step 2 说跑 "scripts/export_okf.py", 同文件 `:507` 的文件清单写的是正确的 `../scripts/`, 两处不一致。
  > `ref/okf-compat.md:113-115` 的示例命令一半按 Tools 仓库根写 (`plugins/...`), 一半按工作区根写 (`examples/<project>`), 无论站哪个目录整条命令都跑不通。

### C. 账本失真 (全部机械修)

- [x] **C1** 🟡 `[M]` **7 本 CHANGELOG 自称 "Newest first", 实际顺序是乱的。** 例子: `haipipe-insight/CHANGELOG.md` 的顺序是 2.0.0 → 1.0.0 → 2.6.0 → 3.0.0, 最新的 3.0.0 沉在最底。找最新变更的人 (和 agent) 会把 2.0.0 当最新。
  > 同病文件: `haipipe-insight-data/`、`-information/`、`-wisdom/`、`-review/` (全是旧在上), `-knowledge/` (乱序 1.1.0, 1.0.0, 1.2.0), 外加 `agents/creators/card-creator-knowledge-agent.md` 内嵌的小 changelog (1.2.0, 1.0.0, 1.1.0)。
  > 我改成: 只重排条目, 内容一个字不动 (changelog 是历史, 历史不改写)。

- [x] **C2** 🟡 `[M]` **两个技能的版本号在撒谎。** `haipipe-insight-knowledge/SKILL.md` frontmatter 停在 `1.2.0 / 2026-06-20`, 但正文已经装着 3.0.0 的"无 probe gate"和 3.1.0 的 --id 支持; 它的 CHANGELOG 里这两轮一条记录都没有。`haipipe-insight-review/SKILL.md` 同病: frontmatter `1.1.0`, 正文有 3.1.0 的 PRE-ASSIGN IDS 整段 (`:161-173`)。
  > 不改会怎样: 以后审计拿版本号判断"这文件改没改过", 会做出错误结论 (这次审计差点就上当)。
  > 我改成: 各 bump 一版 + 在各自 CHANGELOG 补一条一句话记录 ("body updated for 3.0.0/3.1.0 recut, version not bumped at the time")。

- [x] **C3** 🟡 `[M]` **DESIGN.md 三处过期**:
  > `:4` 表头 "Status: v2.5.0 (2026-06-20)": 层账本已到 3.1.0 (06-22), 而且 3.0.0 那条 changelog 明说动了 DESIGN.md, 只是没人把表头翻页。
  > `:10` 开篇第一句 "Read **ARCHITECTURE.md + MENTAL_MODEL.md** first": 这两个文件在 insight/ 下都不存在。真身: ARCHITECTURE.md 在插件根目录 (`Tools/plugins/haipipe-toolkit/ARCHITECTURE.md`), MENTAL_MODEL.md 是 probe 层的文档 (`skills/probe/MENTAL_MODEL.md`)。新读者按第一句去找, 直接扑空。
  > `:48` "controlled by review review" 重词。
  > 我改成: 表头翻到 3.1.0 一句话摘要; 必读指路改成真实路径; 重词删一个。

- [x] **C4** 🟡 `[M]` **orchestrator 的 Job 编号自相矛盾**:
  > `haipipe-insight/SKILL.md:104` 小节标题 "**Three Jobs**", 紧接着 `:107` 第一句 "This orchestrator has **five** jobs" (五个也是对的: REVIEW/ROUTE/CHECK/DASHBOARD/EXPORT; 标题是 2.0.0 时代三个 job 的遗物)。
  > `:376` Step 5 自我标注 "(**Job 2**)": 按五 job 表, 归档后的 accumulation check 是 **Job 3** (CHECK), Job 2 是 ROUTE。读者对着表找会找错。
  > 我改成: 标题改 "Five Jobs"; Step 5 标注改 Job 3。

### D. 退役层引用 + 虚构机件 (要你拍板)

- [x] **D1** 🟡 `[J]` **narrative 被当成活的上游层, 全家 ~40 处。** 本轮最大的一个决定。
  > 背景: narrative 层已经退役 (职责并入 paper lifecycle 的 3-narrative 阶段, probe 成了证据侧枢纽)。但 insight 家从 orchestrator 到 ref 到 play 还通篇把它当活人: 说 "narrative review CALLS insight"、给卡片留了 `narrative:N01.C2` 引用命名空间、INDEX 视图里有 `by_narrative.md`。
  > 最实锤的一处: `haipipe-insight-review/SKILL.md:116-119` 教 agent "For narrative scope: Read claims.md, story.md, ignite-log.md": 磁盘上没有任何项目有 narratives/ 目录, 这段一执行就落空。dogfood 的卡片也没有一张带 narrative: 引用。
  > 全部点位: orchestrator `:3,17,21,55,76,141,449,462,478` · review 技能 `:3,62,116-119,126,246,258` · `ref/review-contract.md` 13 处 · `ref/insight-md-schema.md:46,350` · `ref/index-templates.md:5,154,190-200,233` · `ref/card-granularity.md` 4 处 · `ref/card-lifecycle.md:68` · play/ 8 处 · DESIGN.md 5 处。
  > 选项 A: 全局清一遍。caller 一律写成 "paper / application ask / human review"; 引用命名空间 `narrative:` 改成 `paper:`; `by_narrative` 视图删掉; review 技能那段"扫 narrative 文件夹"整段删。动 ~40 处, 一次到位。
  > 选项 B: 只删执行性的段落 (review:116-119 这类"照做会扑空"的), 口头提及先留, 下轮再清。
  > 风险: A 动面大但一致; B 快, 但留着一个死命名空间, 新 agent 学着往卡片里填 narrative: 引用, 图谱里就会长出指向不存在层的边。
  > 我的倾向: A。insight 的 caller 名单本来就该是 "paper / application ask / human"。
  > 问你: A 还是 B? `narrative:` 命名空间是改成 `paper:` 还是直接删掉?
  > JL: 现在已经没有narrative了，insight只会被probe call。直接都删掉。
  > ✅ 已清: ~40 处全删 (orchestrator / review / ref×6 / play×6 / DESIGN / 2 个 K agent)。caller 全家改为 "probe (Deposit step) 或用户直调"; `narrative:` 命名空间从 schema + review-contract 删除; `by_narrative` 视图删除; review 技能的 narrative 扫描段换成 discovery 段。留 2 处: 各 CHANGELOG 的历史条目 + DESIGN "Decisions settled" 史区 (历史不改写)。application 按你的话降为 READ 侧。
  > JL: (chat 2026-07-05, 对 ask-session scope 的追问) delete it.
  > ✅ 已删净: ask-session 从 orchestrator 命令行/路径自动识别/Step 2a、review 技能的命令/映射/扫描块、review-contract 的 kind 枚举里全部移除; scope 现在 = project | probe | task | discovery。连带清掉 "application 可 chain 写卡" ×2 和 creators 的 "ask report phase" 触发词。保留: 问题类输入的出站指路牌 (→ /haipipe-application ask) 和 READ 侧引用 (app:ask: 命名空间合法, 报告引卡是消费不是调用)。

- [x] **D2** 🟡 `[J]` **`.insight-console.yaml` 是虚构机件。** feedback 路由的信号 B 说"看 .insight-console.yaml 里当前活跃的层来猜这条反馈归谁" (`haipipe-insight/SKILL.md:334`, `fn/feedback.md:25,74,98`, 共 4 处)。
  > 问题: 全 insight 树 grep 过, 没有任何技能会创建或写这个文件 (console 机制只有 paper 层有, 那个叫 .paper-console.yaml)。所以信号 B 永远是空的, 路由每次都直接落到下一级 fallback。文档倒是自己打了补丁 ("insight may have no console; that's fine"), 属于"写了个永远不触发的分支"。
  > 选项 A: 删掉信号 B, 路由链短一截, 文档诚实。
  > 选项 B: 留着当占位, 万一将来给 insight 做 console。
  > 我的倾向: A, 真做 console 那天再写回来不迟。
  > JL:删掉吧。
  > ✅ 已删: 4 处信号 B 全移除 (orchestrator Step 4 + fn/feedback.md ×3), 路由链现在是 跨层 guard → 关键词 → orchestrator fallback。

- [x] **D3** 🟡 `[J]` **`views/` 承诺的是"自动生成", 现实是从来没人生成过。**
  > 原文: `haipipe-insight/SKILL.md:55` "views/ (**auto**: topic/source/narrative/status views)"; `ref/index-templates.md` 把 views 当正经导航层写了一节。
  > 现实: dogfood 里没有 views/ 目录; 全家没有任何技能真的去建它 (review 技能只说 apply "**may** write" views)。"auto"是空头支票。
  > 选项 A: 改口不改功能: "views/ (optional, 按需生成)", index-templates 里对应软化。
  > 选项 B: 把 views/ 从契约里删掉, 等真做了再写。
  > 我的倾向: A (改口), 因为 by_topic/by_source 视图这个主意本身没问题, 只是别说"auto"。
  > JL: 我们有两个，一个事auto 模式，就是自动生成，但是在这个之前我们有个co-pilot模式，和人一起走。你懂我意思吗？
  > {CC->JL}: 懂了: views/ 不是"要么 auto 要么删", 而是两档走法, co-pilot 在前 (和你一起挑要哪些视图、看过再落盘), auto 在后 (之后 review/apply --auto 时静默重建已确认过的视图)。我会把 orchestrator :55 的 "views/ (auto: ...)" 改成 "views/ (co-pilot 首建, auto 重建)", index-templates 同步。这么落对吗?
  > ✅ (第一版, 已作废) 落成了 "co-pilot 首建, auto 重建" 的时间先后。
  > JL: (chat 2026-07-05) 不是这个意思，auto是在subagent call这个skill的时候，会走auto，你明白吗
  > {CC->JL}: 明白: 两档按调用方分, 不按时间分。人开的会话 = co-pilot (一起挑视图、确认再写); subagent 调 skill = --auto (静默生成), 和全家 dual-mode 契约同轴。
  > ✅ 已重落: orchestrator :55 = "(topic/source/status views; co-pilot with a human, --auto when agent-called)"; index-templates 改为指向 ref/invocation-modes.md 的 dual-mode 说法。
  > JL:

- [x] **D4** 🟢 `[J]` **"G-ask" 旧字母名残留 2 处**: `agents/creators/card-creator-wisdom-agent.md:47` + `agents/reviewers/card-reviewer-wisdom-agent.md:45` 写 "a user / **G-ask** action"。G 是层字母编号时代对 application 的叫法, 现名 `/haipipe-application ask`。没异议我就顺手改成现名。
  > JL: 改成现在的吧
  > ✅ 已改: 2 处 "G-ask" → application-ask (wisdom creator + wisdom reviewer)。

- [x] **D5** 🟢 `[J]` **四个卡片 reviewer 都写死 "Codex-backed", 但没写 Codex 不在场怎么办。**
  > 现状: 4 个 reviewer 的 description 和正文都说 accuracy 复读那条腿由 Codex 干 (工具单里列着 mcp__codex__codex), 但插件树里没有任何 mcpServers 配置, Codex 掉线时 accuracy 这条腿没有定义的替代动作。
  > 参照系: task 层当年干脆把 Codex 从 reviewer 里去掉了 (fresh-agent 独立复读顶上); illustration 技能则是明写了 gemini fallback。
  > 选项 A: 每个 reviewer 加一句 fallback ("Codex 不可用时自己独立复读一遍, 在质检报告里记 codex: unavailable")。
  > 选项 B: 学 task 层, 把 Codex 从 insight reviewer 里也去掉。
  > 我的倾向: A, 保留双引擎的意图, 但把降级路径写明。
  > JL:okay。没有的话就fallback
  > ✅ 已加: 4 个 reviewer 的 fence 各加一行 codex_fallback (Codex 不在场 → 自己独立复读一遍, 质检报告里记 codex: unavailable); reviewer 模板同步加了占位。

### E. 契约内讧 (同一条规矩两处各说各话)

- [x] **E1** 🔴 `[M]` **图谱审计员 (index-integrity-auditor) 自己抄了一份规则, 抄错了两处。** 这是 agents 里唯一一处不指向 ref 而是自己复述规则的地方, 一复述就漂移, 正好证明"agent 要薄"的道理。
  > 错处 1, status 枚举, 两边对照:
  > ```
  > auditor :60 说合法 status = { active, stale, superseded, deposited }
  > schema  :21 说合法 status =   active | stale | superseded | contested | acted_on
  > ```
  > "deposited" 是 probe 层的词, 卡片根本不用; 反过来 `contested` / `acted_on` 是合法值, auditor 会把用了它们的卡当违规报出来。
  > 错处 2, `:54` 来源合法性一行 "D→task/probe ref · I→D ids · K→I ids · W→K ids": 比 schema 窄。schema 允许 D 来自 `discover:` / `lit:` (数据 reviewer 自己 `:55` 都列了四种), K 也可以带 `probe:` / `lit:` 的 basis 引用。照 auditor 的窄版, 文献来源的 D 卡会被误杀。
  > 我改成: 两处都改成"按 schema 校验"并给出 schema 行号, 不再复述枚举。

- [x] **E2** 🔴 `[M]` **wisdom creator 是四个 creator 里唯一忘了传 `--id` 的, 并发写 W 卡会撞号。**
  > 场景: apply 一次通过 3 张 W 卡, 并发派 3 个 wisdom creator。D/I/K 的 creator 都把 apply 预分配的 --id 转发给 writer; wisdom creator 的调用 (`:56`) 却是 `Skill("haipipe-insight-wisdom", "--scope K03 --project <p> --auto")`, 没有 --id → 3 个 writer 各自数号, 都算出"下一张是 W01" → 三张卡抢同一个文件名。
  > 佐证: D/I/K 三个 creator 都带着同一句"Always forward the apply-assigned --id"的说明, 唯独 wisdom 没有; wisdom writer 本身是支持 --id 的 (argument-hint 里就有)。漏网之鱼。
  > 我改成: 调用串补 `--id W<NN>`, 补那句转发说明, 和其他三个 creator 对齐。

- [x] **E3** 🟡 `[J]` **K 卡的 sources 规则, 两处文档各教一套。**
  > schema 派: `ref/insight-md-schema.md:356` 说 K 卡要"cite the **I card(s)** they generalize"。dogfood 的 K01 就是这么干的: `sources: [I01]`。
  > contract 派: `ref/review-contract.md:229-231` 和 `play/03:16-19` 的示例 K 却是 `sources: [probe:P.0619_film_ood]`, 直接引 probe, 一张 I 都不引。
  > 矛盾后果: auditor 现在按"K→I"校验, contract 派写出来的 K 会被判 dangling; 但"文献直接来的 K"(比如从一篇 paper 学到的可推广结论) 按 schema 派就得先硬造一张 I, 很别扭。
  > 选项 A: K 必须引 ≥1 张 I; probe/lit 只能作为补充 basis 写进 `## Generalization basis` 正文。图谱整齐, 但外部知识入库要先造 I。
  > 选项 B: K 的 sources 允许 I 卡 或 `probe:`/`lit:` 外部引用皆可 (至少一个)。宽容, 符合"lit-only K"的现实; auditor 的校验规则同步放宽。
  > 我的倾向: B。
  > JL: 我也倾向B。
  > ✅ 已落 B: schema 的 K 校验句改为 "cite the I card(s) OR a probe:/lit:/discover: origin (owner decision 2026-07-05)"; auditor 的来源合法性行同步放宽; review-contract 与 play/03 的 probe 直引示例因此转正; K writer 本就兼容, 无需动。

- [x] **E4** 🟡 `[M]` **质检报告该放哪, 五个 reviewer 都没写, review 技能还写错了。**
  > 地面真相 + 3.1.0 定论: 质检报告 (`D_CARD_REVIEW.md` 等 + `INDEX_AUDIT.md`) 的家是 `insights/_reviews/`; dogfood 里 5 份报告都在那。
  > 现状: 5 个 reviewer agent 和 agents/README 只写了交付物文件名, 没写目录 (grep agents/ 里 "_reviews" = 0 次) → 不同 agent 会把报告扔卡片旁边或 insights/ 根下; `haipipe-insight-review/SKILL.md:243,255` 甚至明写 `insights/INDEX_AUDIT.md` (根目录, 错)。
  > 我改成: 5 个 reviewer + README 各加一句 "written to insights/_reviews/"; review 技能两处路径改对。

- [x] **E5** 🟡 `[J]` **"insight 只写 insights/" 这条硬边界, 和实践打架, dogfood 站实践这边。**
  > 边界派: orchestrator `:465-467` "insight NEVER writes to tasks/ or probes/ directly ... ONLY writes to insights/"。
  > 实践派: `haipipe-insight-review/SKILL.md:145-151` 让 review 把 `INSIGHT_REVIEW.yaml` (审阅清单) 写进被审的那个文件夹; dogfood 里 `probes/0605_discretion-gradient/INSIGHT_REVIEW.yaml` 真实存在。
  > 怎么理解: 永久卡片确实只进 insights/; 但"这批材料里什么值得入库"的清单跟着材料走, 像贴在箱子上的验货单。矛盾只在 orchestrator 那句话说得太绝对。
  > 选项 A: 认实践, 软化 orchestrator 措辞: "永久卡片和索引只写 insights/; INSIGHT_REVIEW.yaml 清单落在被审的 scope 文件夹"。
  > 选项 B: 守硬边界, 改实践: 清单统一挪进 insights/_reviews/, review 技能改写目标, dogfood 下次跟进。
  > 我的倾向: A, 清单贴材料更好找, dogfood 已经这么长了。
  > JL: (chat 2026-07-05) 我记得我说了选A
  > ✅ 已落 A: orchestrator 边界句改为 "永久件 (卡/INDEX/_reviews) 只进 insights/; INSIGHT_REVIEW.yaml 清单落被审 scope 文件夹 (唯一例外, owner decision 2026-07-05)"; review 技能与 dogfood 本来就是这么干的, 无需再动。

- [x] **E6** 🟡 `[M]` **七个小抵触** (每条一行, 都是对齐问题):
  > 卡片正文字数预算两处不同: `ref/card-granularity.md:147-150` 说 D 30-70 / I 40-90 / K 60-140 / W 40-90, `ref/insight-md-schema.md` 说 D 30-50 / I 30-60 / K 40-80 / W 30-60。以 schema 为准统一。
  > `ref/index-templates.md:227` + `ref/insight-context-loading.md:194` 让人跑 `/haipipe-insight rebuild-index`: orchestrator 的 Commands 里没有这个动词。改成指向 review 的 apply 步骤重建。
  > `haipipe-insight-review/SKILL.md:210` DoD 枚举漏了 `merge` (它自己 `:212/:216` 都在用 merge)。
  > `haipipe-insight-data/SKILL.md:106-109` + `haipipe-insight-information/SKILL.md:77-80` Step 1 的参数解析清单漏了自家 argument-hint 里就有的 `--dataset` / `--id`。
  > `haipipe-insight-information/SKILL.md:107,148,167` 教人把反向链接写进 D 卡的 "Cross-references" 正文小节: D 的 schema 没这小节, 反向链接是 `ref_by:` frontmatter。
  > `haipipe-insight-data/SKILL.md:55-57` probe 路径还是两层旧形状 (真实是一层平铺 `probes/MMDD_slug/`)。
  > `haipipe-insight-review/SKILL.md:3` description 承诺能审 "discover" 材料, Step 1/3 里却没有 discoveries/ 分支 (dogfood 项目里真有 discoveries/ 目录)。补分支或删承诺, 我倾向补分支。

- [x] **E7** 🟡 `[M]` **export_okf.py 两个实锤 bug** (在 dogfood 上实跑复现过):
  > bug 1 (`:287-289`): 校验 `sources` 时对外部引用 (`probe:xxx`, `lit:xxx`) 有豁免逻辑, 校验 `ref_by` 时忘了同样豁免 → 合法的外部 ref_by 一律报假警 "dangling ref_by"。修法: 把豁免逻辑照抄到 ref_by 分支。
  > bug 2 (`:325-327`): `--out` 指到哪个已存在的目录就整个 `rmtree` 哪个 → 手一抖 `--out .` 会删掉当前目录。而 SKILL.md 的风险声明承诺"只删派生的 insights/okf/"。修法: 目录名不是 okf 且非空就拒绝执行。

### F. cosmetics 🟢 (顺手修, 不用细看)

- [x] **F1** 🟢 `[M]` 批量替换留下的病句 "a **approved by review** settled source_ref" (原来大概是 "a confirmed source", 被全局替换打碎了语法), 4 处: `haipipe-insight-data/SKILL.md:3,18`、`agents/creators/card-creator-data-agent.md:3,26`。改成 "a review-approved ..."。
- [x] **F2** 🟢 `[M]` 示例小瑕疵: wisdom `:152` 示例写 "LHM re-test" (全家其他例子都叫 FiLM); `play/03:49` `unit: run note` 不在枚举 (合法值: observation | pattern | claim | recommendation); `play/02:10-14` probe 文件夹示意还带着时代产物 `CLAIMS_FROM_RESULTS.md`; `play/01:9-14` 文件夹清单写 `discover/` + `narratives/` (真名 `discoveries/`, narratives 是 D1 的事)。
- [x] **F3** 🟢 `[M]` 模板与元数据: 两个 `_TEMPLATE.md` 冻在 1.0.0/05-31 (真 agent 都 1.1.0/1.2.0 了), creator 模板还缺 3.1.0 的 --id 步骤; creator 的工具单带着用不上的 Write+Edit; `ref/insight-md-schema.md:363,367,375` 从 ref/ 内部自引还写 "ref/..." 前缀 (人能懂, 机器解析会差一层, 无害)。
- [x] **F4** 🟢 explore 的 `--out` 尾巴 (`:124` 说 "if --out", argument-hint 里没这个 flag) 并进 A2 的重写一起处理。

---

## Part 3: 执行偏差备注 + 复核记录 + 干净清单

执行偏差 (与账面"我改成"不同之处, 其余全部照账执行):

- F2 的 play/02 `CLAIMS_FROM_RESULTS.md` 一项 **未改**: 磁盘复核发现该文件在真实 probe 文件夹里确实存在 (auditor 之间打架, 磁盘赢), 原文没病。
- 同理 data writer 的 probe 输入清单保留 `CLAIMS_FROM_RESULTS.md`, 只把目录形状改平。
- A2 同病一处扩展: card-reviewer-data-agent 也在读不存在的 `result.status`, 顺手改成读顶层 `status:` (记入其 1.1.0)。
- A10 顺手: wisdom :76 同一行里的退役动词 "/haipipe-task task-folder" 一并改成 "/haipipe-task"。
- B1 实数 14 处 (账面写 15; knowledge 只有 3 处坏前缀, 第 4 处 :111 本来就是对的)。
- 账外发现未动 (等你要不要): `haipipe-insight-data/SKILL.md` 两处 "/haipipe-task task-folder eval" 也是退役动词 (task-folder 已在 task 层 review 中删除), 不在本账清单内, 未改。

主 session 亲手抽查 9 条, 9/9 坐实: A1 (invocation-modes 原文在案) · A2 (explore 的 result.status + 两层目录原文在案) · A3 (claim_type grep = 0) · A5 (≥2-D 在 description 和格言两处) · A6 (play/04 的 refs: 字段 + 无 claim_type) · B1 (../../ref/ 实测不解析) · E1 (两份枚举并排对过) · E2 (调用串里确实没有 --id) · E7 (代码两个分支对过, 豁免只在 sources 侧)。

查过且干净的 (让你知道哪些不用担心): 7 个 frontmatter 全合法、名字全对; data/information/wisdom/explore 四家版本号和账本对得上; 四个 writer 的 dual-mode + blocked-never-hang 契约齐全; `--id` 在四个 writer 侧都支持; 现行文档里没有任何一处还写着字面的 "K requires a confirmed probe"; D/I 不带 p/CI 的规矩在所有现行正文里立住了; agents/ 的相对路径深度全对; 插件注册表 9 个 symlink 全通; K→K 综合边全家口径一致; `ref/card-lifecycle.md`、`play/README.md`、`play/00`、`play/05`、根 `CHANGELOG.md`、`PREFERENCES.md`、`fn/digest.md`、`feedback/README.md` 全干净; export_okf.py 语法过、无硬编码路径、legacy-W 兼容按承诺实现、claim_type 能原样透传到导出副本。

界外观察 (probe 层的事, 只记不动): 插件注册表 `Tools/plugins/haipipe-toolkit/agents/` 里有 3 个 symlink 指向已合并退役的 probe reviewer agent, 目标目录已不存在 (claim-verifier / probe-integrity-auditor / probe-structural-reviewer)。
