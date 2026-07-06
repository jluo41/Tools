Thread protocol: `> {CC->JL}:` judgment-point comments
=======================================================

How [J] findings get decided: the agent applies its best reading, then opens ONE thread AT the judgment point in the file, and the user replies inline with `> JL:`.
Threads open AT REPORT TIME (Phase 3), together with SKILLSET_REVIEW.md, not deferred to FIX: the user answers them in the same pass as the report eyeball (JL 2026-07-05: "我觉得这个comment 必须要先生成好"). Each finding records its thread's `path:line`, and the FULL block is MIRRORED under the finding in SKILLSET_REVIEW.md so the user replies in one file without hopping (JL: "我在哪里加入我的comments呀"). Either copy's `> JL:` slot counts, first reply wins; the RESOLVE sweep greps BOTH places and removes both copies together. Opening a thread is a question, not a fix; nothing else changes before the go.
This protocol exists because terse threads failed twice in the field: JL replied "I think I need more context here" (2026-07-05, src2input) and later "inline 的你的每个comments 都很难understand，try to provide more information and examples" (2026-07-05).
Write every thread for a reader who has NOT followed the session.


Block format (all fields, in this order)
-----------------------------------------

```
> {CC->JL}: <one-line headline: what was changed or decided here>
> 背景: what this file/section controls, in plain words. NO session shorthand: if a LESSON or doc is cited, restate its claim inline ("L16 说 xxx"), never bare "L16 胜".
> 原文: "<exact quote of the text BEFORE the change>"
> 现文: "<exact quote of the text AFTER the change>"        (use 提议: instead when nothing is applied yet)
> 例子: a concrete worked example showing the difference in BEHAVIOR, not in wording. MANDATORY, see below.
> 证据: why this reading won (what beats what, with file paths).
> 风险: what breaks if this judgment is wrong. Omit only when genuinely nothing.
> 问你: ONE crisp question, answerable with yes/no or A/B. Spell both options out.
> JL: 
```

The trailing `> JL: ` line is the user's reply slot; always leave it.


例子 is mandatory, and DRAWN when drawable
--------------------------------------------

An abstract description without a worked example is a DEFECTIVE thread.
The example shows what actually happens under each side of the decision, with real values.

DEFAULT FORM IS A DIAGRAM (JL 2026-07-05: "你的comments，如果可以用diagram-ascii，就用这个来explain"): whenever the decision is two options with different behaviors, a flow, or a before/after, draw it as a compact emoji-rich ASCII block (diagram-ascii style, side-by-side option boxes or a branch) inside the 例子 field, each line prefixed `> `. Prose one-liners are the fallback for cases a diagram cannot carry (e.g. a pure wording choice). The other fields (背景/原文/提议/证据/风险/问你) stay one line each; only 例子 spans multiple lines.

Good (option comparison, drawn):

```
> 例子:  你输入: /haipipe-probe file "tasks/R02_Reg_TraitDiabetesNDC"
>
>        B 现状 (legacy 别名)              A 提议 (正式命令)
>        ┌────────────────────────┐       ┌──────────────────────────────┐
>        │ 路由器先猜:            │       │ 第一跳直读 probe-attach.md   │
>        │ gather link? 还是 plan?│       │ 分类→claim门→STRONG 匹配     │
>        │ ⚠ 三分支判决不保证触发 │       │ ✅ "NEW P.T0622_… (confirm?)"│
>        └────────────────────────┘       └──────────────────────────────┘
```

Good (values-only case, prose is enough):

```
> 例子: 同一条 record 发两个平台。SageMaker 收 {"patient_id": "559", "cgm_seq": [...]};Databricks 收 {"dataframe_records": [{"patient_id": "559", ...}]}。争议就是: 这层信封由谁解。
```

Bad (what NOT to write):

```
> 例子: 按 L16 收敛后行为更一致。          ← 没有值,没有场景,没讲行为差异
```


Placement and scale
--------------------

- ONE thread per judgment point, placed AT the point in the file (next to the changed block), not collected at the top.
- A file-wide rewrite gets one thread at the top summarizing what changed and what to read first.
- Threads in the review ledger (SKILLSET_REVIEW.md) follow the same format, indented to match the item.


Lifecycle
----------

```
🤖 open thread (full block + empty > JL: slot)
      │
🧑 replies inline under > JL:
      │
      ├── ✅ decision → execute it → archive the verbatim quote into the owning
      │    skill's CHANGELOG as `### Changed (JL: "...")` → REMOVE the thread
      │
      ├── ❓ confused ("没讲清楚" / "need more context")
      │    → do NOT pile more prose; draw it with /diagram-ascii in chat
      │      (concrete payloads, both options, incident history, one question)
      │
      └── 🔁 counter-proposal → apply, add one short {CC->JL} reply under his
           line confirming what was done, leave a fresh > JL: slot
```

- The user's decision can overturn a recorded LESSON: keep the lesson text as history, add a `⚠️ SUPERSEDED <date> by owner decision ("<quote>")` banner on top.
- Process feedback in a reply (how to work, not what to change) goes to agent memory, not to any CHANGELOG.
- Chat closes each turn with a clickable eyeball list: bare `path:line` in backticks pointing at each open `> JL:` slot; never markdown links with `#L` anchors.


Scope note
-----------

This is the skill-review protocol.
It does not change the paper-workflow rule that replies to JL's own `%% Comments:` in prose/outline files stay ONE line; there the file is a manuscript and long blocks wreck readability.
Here the file is a contract doc under review and the thread IS the work product.
