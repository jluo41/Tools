# 260719 · 两份 PREFERENCES.md 编码了已退役的模型

**话题**:`paper/haipipe-paper/PREFERENCES.md` 和 `application/haipipe-application/PREFERENCES.md`
里的偏好条文,写的还是旧 probe 模型。agent 照着做,写出来的文件会被 checker 判 FAIL。
**你的偏好在教它写不合法的文件。**
D1 裁「直接退役 preferences.md」之后,本板的题目变成:**5 份 PREFERENCES.md + digest fan-out 怎么退役**。
本板**不**执行拆搬(那要新板);本板只出实测和形状选项。

来源:`260719-02-PHASE-BOUNDARY-REFACTOR.md` 第 ④ 行(JL 在该板 D4 裁「再开一个吧」)。

**为什么单独成板**:PREFERENCES.md 是你对 agent 说过的原话,是 agent 的行为约束。
agent 改它 = 自己改自己的约束。所以我全程只读不写,只在这里起草、由你粘贴。

```
  D<n>         DECISION  等你在 `> JL:` 里拍板
  ENTRY        probe 文件里的一条 `## QX<n>`,底下挂四个 `###` 子节(旧称 SECTION)
  ①ORGANIZE ②MATCH  已移到 DRAFT 相;③DISPATCH ④POINT ⑤INTERPRET 才是 PROBE 相
  ### a-executor    probe 条目里抄回来的答案(旧称 probe 文件字段 `a-consumer:`)
  a-consumer   仍然活着,但它现在住 stage doc(站②),不是 probe 文件
```

---

## 🔴 病灶

```
  paper/haipipe-paper/PREFERENCES.md:11
    ✗ 「⑤ INTERPRET (`a-consumer:` + the 1b-claims.md flip)」
       → `a-consumer:` 作为 probe 文件字段已退役 → 现在是 `### a-executor`
    ✗ 「Raise each question as a SECTION in 1-probes/」
       → 现在是 ENTRY(`## QX<n>` + 四个 `###` 子节)
    ✗ 「② MATCH it against the bank's QA corpus」写在 PROBE 相的步骤里
       → ②MATCH 已移到 DRAFT;PROBE 只跑 ③④⑤,不再 re-match
    ✗ 「the section's `q-executor:` block」
       → 现在是 `### q-executor` 子节

  application/haipipe-application/PREFERENCES.md:17
    ✗ 「raise the questions as SECTIONS in the flat pool」          同上
    ✗ 「then run the five-step loop (ORGANIZE → MATCH → …) through
        haipipe-application-probe」                                同上,①②不在 PROBE
    ✗ 「a section that never bound to a QA file」                   同上

  ⚠️ 后果是实测的,不是推理:照这两条写出的 probe 文件,
     会被 check-probe-cards.sh 的 stale-old-format 规则直接 FAIL
     → 那个 stage 的 PROBE 相永远过不了闸。
```

## 🎯 现在在哪

```
  D1 已裁「直接退役 preferences.md」 → 下面两段英文起草作废(不删,留痕:板子未入 git)
  退役范围从 2 份涨到 5 份 + 一套 fan-out 机制 → 形状要你在 D3 定
  ⚠️ 阻断:20 条规矩里有 14 条只活在这 5 个文件里,直接 rm 就是丢你的原话
```

## ✍️ ~~改好的英文原文~~(⛔ 作废 · D1 裁退役,条目不再修补而是死掉)

> 保留原文仅为留痕。只改**机制描述**,你那句原话引文(JL, 2026-07-07 "you need to always run the real
> probes in the probe phase")和整条偏好的**意图**一字不动。

**paper/haipipe-paper/PREFERENCES.md:11 — 建议替换为:**

```
- **Always run the REAL probe in the PROBE phase — never substitute an inline scan.** Evidence work has exactly ONE exit: the PROBE phase worker (`Skill("haipipe-paper-probe")`). DRAFT authors the plan — ① ORGANIZE each question into a `## QX<n>` ENTRY in `1-probes/PPNN_<topic>.md` (writing its `### q-executor`, its `### q-consumer` bullets, and its `### bank binding`), and ② MATCH it against the bank's QA corpus so most entries close on T2 REUSE. PROBE then runs that plan FORWARD: ③ DISPATCH only what the bank still owes — the entry's `### q-executor` block, VERBATIM, through `Agent(haipipe-probe-q-executor-agent)` — then ④ POINT (`target` → the answering QA file) and ⑤ INTERPRET (`### a-executor` + each Q-consumer's a-consumer in its stage doc + the 1b-claims.md flip). A light web scan woven into the stage prose is a DRAFT-phase scoping aid, NOT a probe. A stage whose probe file has no entry with a RESOLVING `target` has not run its PROBE phase, and must not be promoted past it. MATCH comes before DISPATCH: most entries should close on T2 REUSE, so a fresh q-executor is the exception, not the norm — but "the bank already answered it" is a MATCH result you must SHOW (the QA file you read), never an excuse to skip the loop. JL, 2026-07-07 (Paper-CGMtoCyclePhase seed): caught the empty probe folder and said "you need to always run the real probes in the probe phase." (also in auto-memory: feedback_always_run_real_probes)
```

**application/haipipe-application/PREFERENCES.md:17 — 建议替换为:**

```
- **Always run the REAL probe in the PROBE phase — never substitute an inline scan.** In any stage's PROBE phase, the evidence work MUST go through the ledgered worker path. DRAFT authors the plan: raise each question as a `## QX<n>` ENTRY in the flat pool `1-probes/PPNN_<topic>.md` (① ORGANIZE) and root it against the bank (② MATCH). PROBE then runs it forward — ③ DISPATCH → ④ POINT → ⑤ INTERPRET — through `haipipe-application-probe`, the ONLY door to the bank. A light web scan woven into the stage prose is a DRAFT-phase scoping aid, not a probe; an entry that never bound to a QA file (still `state: planned`, no resolving `target`) leaves the PROBE phase INCOMPLETE. Do not promote a stage past PROBE on an inline scan. JL, 2026-07-07 (paper-side origin, Paper-CGMtoCyclePhase seed: "you need to always run the real probes in the probe phase"); family-generic — applies verbatim to every application stage. (also in auto-memory: feedback_always_run_real_probes)
```

## ⚖️ 裁决账本(append-only · 你的原话逐字保留)

```
D1 · 上面两段英文,你认吗?
     我只改了机制描述(SECTION→ENTRY · ①②归 DRAFT · a-consumer:→### a-executor),
     你的原话引文和意图一字未动。认的话你自己粘贴进去 —— 我不碰 PREFERENCES.md。
     要我改措辞就直接在这行说。
> JL:要不然直接把preferences.md 直接退役吧。
     >> CC0719:方向我认,而且比修条文更对 —— 但**退役范围比你我原以为的大**,而且直接 rm 会丢你的原话。
     实测(命令在 D2 里):PREFERENCES.md 不是 2 份,是 5 份;不是几条偏好,是 35 条 bullet、
     去重后 20 条规矩;还挂着一套 `digest` fan-out 机制在往里写。
     🔴 阻断项:这 5 个文件自称「auto-memory 里有镜像」,但那些镜像**已经没了** ——
        文件里引用的 9 个 `feedback_*` 记忆,现在只剩 2 个还有对应(名字也换成 kebab 了)。
        `ls ~/.claude/projects/-Users-jluo41-Desktop-Physician-SPACE/memory/` → 9 个文件,
        没有 `feedback_always_run_real_probes` / `_commit_each_tex_edit` / `_manuscript_pn_sn_indexing` 等 7 个。
        而且 auto-memory 不只是「换机器会丢」,它是**按项目路径分家**的:
        `find ~/.claude -maxdepth 3 -type d -name memory` → 这台机器上 14 个独立 memory 目录,
        Physician-SPACE 自己就占了 2 个(`-Physician-SPACE` 和 `-OpenClawServer-...-Physician-SPACE`)。
        所以「全搬去 auto-memory」不成立,它接不住。
     ✅ 我的结论:**退役 = 搬完再删,不是直接删**。20 条规矩本来就是三种东西被塞在一个文件里,
        拆开之后,你那句「直接退役」对其中 6 条是**直接删**(它们本来就是复述契约,checker 才是执法者)。
        三桶怎么分见 D3。

D2 · 还有别的偏好条也带病吗?要不要我全量体检一遍?
     我只查了这两条(因为它们在 ③⑩ 的 grep 里撞出来)。
     两份文件各有 5-6 条偏好,其余的我没逐条对过当前契约。
     要我全查一遍、把带病的都起草出来吗?
> JL:
     >> CC0719:D1 一裁,这题的答案就从「逐条修」变成「逐条定去向」,我按后者做了一遍分诊。
     实测命令 + 结果:
       find . -name PREFERENCES.md                                  → 5 份
       grep -h '^- \*\*' */haipipe-*/PREFERENCES.md | wc -l          → 35 条 bullet
       …| sed 提取标题 | sort | uniq -c                              → 23 个不同标题
       再合并同义异文(见下)                                        → 20 条真规矩
     ⚠️ fan-out 本身就已经坏了,不是「同步得不好」,是**同一条规矩存在互相打架的两种写法**:
       diagram-ascii        5 份 · 2 种写法:paper/discovery/probe/task 写「keep prose to a one-line ask」,
                            application 写「THE default mode」—— 强度不同,agent 读哪份行为就不同
       不留墓碑            2 种写法:paper「NO TOMBSTONES」 vs probe「Keep skills CLEAN / 不是垃圾桶」
       正文一句一行        2 种写法:task「In doc BODY prose」 vs probe「Body prose: one sentence, one line」
     ⚠️ 文件和挂钩也早就对不上(逐个 SKILL.md 数 PREFERENCES 提及):
       paper ✅  application ✅  discovery ✅  |  probe 有文件·SKILL.md 0 提及
       task 有文件·SKILL.md 0 提及            |  project 有挂钩(SKILL.md:146)·**根本没有这个文件**
     分诊结果 —— 20 条按「它到底是什么东西」分三桶:
       A 机制复述 6 条 → 直接删。契约在别处,这里只是会烂的第二份拷贝
          真 probe(2 份,就是本板病灶) · 走 task agents · RELEASE MENU · alignment watch
          · Pn.Sn 索引 · Q-consumer 粗体标签
          (RELEASE MENU 尤其典型:它自己写着「Enforced twice: draft worker step 5 + probe STEP 1.5」——
           已经有两处执法了,偏好条是第三份拷贝,只会烂)
       B 写技能的规矩 9 条 → 归 `skills/STRUCTURE.md`(或新开 AUTHORING.md)。这不是「你的偏好」,
          是这套 toolkit 的作文法,住在 5 个 orchestrator 文件夹里本来就是错位
          不留墓碑 · metadata 要小 · description ≤55 词 · SKILL.md 只 ROUTE 不复述 · 正文一句一行
          · markdown 不手动折行 · `> JL:` 回复协议 · 已解决线程移 `_LOG` · 核对「已完成」声明
          (末三条已经和 `_console/README.md` 的 hard rules 重叠)
       C 真·个人偏好 5 条 → auto-memory + 仓库 CLAUDE.md。这些是永久的、不复述任何机制的
          diagram-ascii 默认 · 无理解不写字 · 最简分组 · 短句优先 · 每次 tex 编辑单独提交
     全量逐条对契约(B/C 桶还有没有暗病)我没做 —— 要不要做取决于 D3 选哪个形状。

D3 · 退役的形状选哪个?(D1 已裁「退役」,这里只定怎么退)
     甲 · 全删:5 个文件 rm + 4 处 SKILL.md 挂钩拆掉 + digest fan-out 退役。
          最干净,但 B 桶 9 条 / C 桶 5 条无处可去 → 丢你的原话。我不推荐。
     乙 · **拆三桶归位,再删文件**(我选这个)。A 桶 6 条删掉(含本板 PF-1/PF-2)、
          B 桶 9 条合进 `skills/STRUCTURE.md`、C 桶 5 条进 auto-memory + CLAUDE.md,
          搬空之后 5 个文件 + fan-out 一起退役。
          理由:你「直接退役」的直觉针对的是 A 桶那种「复述契约、没人执法、会烂」的条文,
          而这个文件之所以会烂,正是因为它把三种东西塞在一起 —— 拆开就没有会烂的部分了。
          代价:一次性工作量最大(约 5+4+1 处文件改动),但之后没有 fan-out 要维护。
     丙 · 只留一份:5 份合成 `skills/PREFERENCES.md` 单一来源,fan-out 退役,
          立一条新法「偏好只写规则 + 你的原话,不准复述机制」。改动最小、跨机器可移植性保住,
          但 B 桶那 9 条仍住在错的地方。
> JL:
     >> CC:
```

## 🧾 清账表(**闭集**:全部来自这一次审计,不再新增编号)

```
  编号  项目                                  规模    等谁   状态
  ──────────────────────────────────────────────────────────────
  PF-1  paper/haipipe-paper/PREFERENCES.md:11  4 处错  D3     ⬜ D1 裁退役 → 起草作废,改判「A 桶·删」
  PF-2  application/…/PREFERENCES.md:17        3 处错  D3     ⬜ 同上,改判「A 桶·删」
  PF-3  其余偏好条全量体检                     20 条   D3     ✅ 已分诊(A 6 / B 9 / C 5,见 D2 回复)
  ──────────────────────────────────────────────────────────────
  1 / 3     PF-1·PF-2 的执行归 D3 选定的形状;真动手拆搬另开新板(闭集不吃退役工程量)
```
