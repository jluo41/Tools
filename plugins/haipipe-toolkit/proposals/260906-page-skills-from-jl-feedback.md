# Proposal · absorb JL's feedback into the Page skills

date: 260906 · author: Claude B (session Paper-PhyTraitOpioid-MISQ) · status: ✅ reviewed by JL in Codex chat
source: 375 of JL's own messages across 9 Codex sessions (main MISQ session 260824–260906 + 8 `Paper-MISQ-*` branches)
skills applied: haipipe-page-outline 0.32.0 · haipipe-page-evidence 0.22.0 · haipipe-page-content 0.8.0 · haipipe-page 0.59.0 · haipipe-plugin-outline 0.46.0

decision record: ✅ D1 D2 P01 P02 P03 P04 P05 P07 P08 P09 P10 P11 P12 P14 P15 P16 P17 P18 P19 P21 P22 P24
keep current: D3 (retain the existing Feedback column and format)
skip: P06 P13 P20 P23
unchanged by default: N1–N6

## How to answer

Every row ends with `Your call: ⬜`. Replace ⬜ with one of:

- ✅ agree, do it as written
- ❌ disagree, do not do it
- ✎ change, and write one line after it saying what to change

Or just reply in chat, for example: `D1 B · P03 ✅ · P07 ❌ · P11 ✎ only at assembly`.
Nothing is patched until you answer. Rows you leave ⬜ are treated as "not yet", never as yes.

## Words used below

- **Page** = one section's folder on the paper board (for example S-MISQ-Main-Theory).
- **Bullet** = one planned sentence in the outline (address like C2.P1.B5).
- **Evidence Item** = the typed thing a Bullet owes: VALUE (a number), CITE (a reference), DISPLAY (a figure or table).
- **SHAPE / SURVEY** = the two outline cycles: agree the plan, then map which Runs feed each Evidence Item.
- **LAND / EMBED** = the two evidence cycles: execute the Runs and get a Result, then fold that Result into the outline.
- **v0.x / v1.0** = outline versions before and after your approval.
- **Round** = one batch of external feedback (RD01 = Gordon and Ritu, 260825).

---

## Part 0 · Three decisions only you can make

### D1 · When may an outline become v1.0?
- **You said (two different things)**: 260906 21:01 you approved Abstract v1.0 while 2 of 5 items were still open (one needs the secure server, one needs your citation check). 260906 21:25 (Empirical): "我让你冻结成 V1.0，是意思是说你得先把 survey、land、embed 做完。不做完不能成为 V1.0。"
- **Today the skill**: v1.0 on shape approval alone; content release is a separate second gate.
- **Option A (strict)**: v1.0 only when every Evidence Item is ready and folded. The Abstract would go back to v0.x.
- **Option B (recommended)**: v1.0 when the shape is approved AND every item the machine can finish is finished; the only open items are secure-server or person gates, and they are named in the `approved:` line. Matches what you did with the Abstract.
- **Your call: ⬜**

### D2 · May a draft contain a placeholder where no number exists yet?
- **You said**: 260905 01:08 "用 placeholder 把它 place 下，我们大不了再改" · 260906 22:19 "先用 V06-18 的结果当作真正的结果，不要在正文里面说…在 outline 或 discussion 里加个记号" · 260906 22:45 "先把最好的版本弄出来，我现在先要一个 PDF".
- **Today the skill**: content may not contain any missing support; the page must stop and go back to EVIDENCE.
- **Option A (recommended)**: if an old value exists, write it plainly (no "historical" wording; the caveat goes in the evidence record). If no value exists at all, one visible marker `[E## pending]` is allowed; the assembler already has a draft mode that shows these and a final mode that rejects them.
- **Option B**: never a placeholder; the page waits for the number.
- **Your call: ⬜**

### D3 · Should feedback state appear inside the Outline table?
- **You said (two directions)**: 260902 15:23 "越简洁越好，就跟 Apple 一样" and you had the item-progress block removed · 260906 01:49 "这个 outline table 是不是也要加一个 feedback 这个东西，我觉得可能也需要加一下".
- **Option A (recommended)**: one small chip per Bullet, `fb 2·1` = 2 feedback rows routed here, 1 landed; clicking opens the feedback record. No new text column.
- **Option B**: no change; feedback stays in its own record under the Context tab.
- **Option C**: a full feedback text column in the table.
- **Your call: ⬜**

---

## Part 1 · haipipe-page-outline (the SHAPE and SURVEY skill)

### P01 · SHAPE starts from your brief, the advisors' feedback, and the sibling pages' settled decisions. The log is history, never an input.
- **You said**: 260905 04:26 "这个 log 什么都不重要…看完他们的 feedback 之后，我们再想想该怎么写" · 260906 13:19 "我们这个文章已经不再讲 dual eligibility 了，你仔细看看 abstract 和 introduction 做的决定，为啥还在犯一样的错误".
- **Today the skill**: step 2 PROPOSE uses "brief + owning phase policy + venue". Feedback records and sibling pages are not named as inputs.
- **Change**: §SHAPE step 2 lists four inputs: brief · feedback record · sibling pages' `approved:` arcs and the Narrative page · venue. Adds one line: "the log is read for history only".
- **Your call: ⬜**

### P02 · The over-protection check keeps both halves: keep a boundary that explains something; cut a hedge that only defends. Applies to every section.
- **You said**: 260904 12:56 kept the pressure-and-discretion Bullet "it is okay to state the boundary here, it is talking about the theories" · 260906 13:57 "这个 outline 是不是太过于 overprotect 自己了，一看就知道是 AI 写的" · 20:40 "are you doing the overprotection here again?"
- **Today the skill**: one sentence, only about the Introduction ("route a real limitation to Discussion instead of giving defensive prose its own Introduction paragraph").
- **Change**: a named check in the five checks: for each hedging Bullet ask "what does it explain?"; no answer = cut or move to Limitations. Section-independent.
- **Your call: ⬜**

### P03 · The review packet you read before approving gains four things: a diff versus the last version with reasons, counts in paper terms, the display count, and my own verdict.
- **You said**: 260905 02:09 "之前的 version 跟现在这个 version 的区别是什么，为什么我们要这样改" · 260906 21:03 "Tell me the numbers of subsection, sub-subsection, paragraphs, sentence" · 21:58 "先给我说 results 里面我们要有多少个 display" · 21:51 "你自己感觉这些 evidence 怎么样?"
- **Today the skill**: packet = link, arc, C/P map, form audit, evidence counts, feedback routed, human decision. No diff, no paper-level counts, no display count, no verdict.
- **Change**: ref/review-packet.md part 1 adds "changed since v<prev>: what · why"; part 1 form audit reports subsection / sub-subsection / paragraph / sentence counts; part 2 adds a display line; part 4 opens with "My verdict: would I approve this? yes/no because…".
- **Your call: ⬜**

### P04 · Every count and density target is measured from named MISQ exemplar PDFs, never recalled from memory; the exemplar is named in the packet.
- **You said**: 260906 13:43 "你这个数字怎么来的呀？你可能需要 double check 一下人家的 PDF" · 14:06 "reference 的 density…跟其他 MISQ 相比正常吗" · 21:05 "你看看别的 MISQ paper，它们的 results 的 structure 一般是什么样子".
- **Today the skill**: "benchmarked when available"; the content skill says "never invent a venue rule". Nobody says where the benchmark must come from.
- **Change**: §Prepare adds: run `section-stats.py` on 2–3 named exemplar PDFs for this section type and record the numbers with the exemplar names; a target without a named exemplar is reported as `not specified`.
- **Your call: ⬜**

### P05 · Displays are planned in SHAPE: how many, and which Bullets each one serves. One display may serve several Bullets; the first display covers all cohorts; overlapping figures are merged.
- **You said**: 260906 16:57 "我们现在只保留一个 display 就行了" · 22:01 "一的话要一个表格把四五个 cohort 都过一下" · 22:02 "一个 display 可以被几个一起用，对吧" · 22:41 "第三个图其实可以被嵌到第一个图里面".
- **Today the skill**: "displays optional; owed only when a visual is necessary". No display plan step.
- **Change**: §SHAPE gains a display plan line (count · purpose · Bullets served); the five checks flag two displays with the same purpose; the evidence-items grammar allows one DISPLAY item to list several `serves:` Bullets.
- **Your call: ⬜**

### P06 · An unfamiliar construct word in a dictated brief is confirmed before it becomes a Bullet.
- **You said**: 260906 00:46 "我发现这个语音转文字效果非常差…以后遇到这种问题，先给我确认一下这个词汇是不是转译错了" (after "prior" had replaced "pressure" in a whole outline version).
- **Today the skill**: nothing.
- **Change**: §Brief adds: a term not in the Narrative, the requirement record, or the sibling pages is echoed back as a question before it is used.
- **Your call: ⬜**

### P07 · Paragraph lines in the plan stay in order and roughly balanced; a division with one paragraph beside divisions with five is flagged.
- **You said**: 260906 17:17 "为什么 C3 这里就只有一个 paragraph，其他的都是好几个，这个分布是不是不太均匀" (the real cause was paragraphs out of order in the file).
- **Change**: five checks ① adds an ordering tooth and a balance warning (not a blocker).
- **Your call: ⬜**

### P08 · Every version report states the active version, whether it licenses content, and what the next change would be called (bounded v1.1 or major v2.0).
- **You said**: 260906 19:06 "现在还不能做 V2.0，就是现在还是 V1.0，现在已经可以去写作了吗" · 19:59 "So this will become the big changes compared to previous versions?"
- **Change**: packet part 4 gets a fixed first line: `version v1.0 · content: licensed / not yet · next change would be v1.1 (bounded) / v2.0 (major)`.
- **Your call: ⬜**

---

## Part 2 · haipipe-page-evidence (the LAND and EMBED skill)

### P09 · Before saying a value is missing, search the old result store. Recovered material is registered as a provisional Supporting Result with its hash and is replaced automatically when the canonical Result lands.
- **You said**: 260906 16:25 "你可以再确认一下旧的里面真的没有 results 吗…去 workspace 的 0-CMS-Store 找找" · 16:29 "找到最原始的那个 log 文件，把它当作 old results 放到对应的 run 里面" · 260905 01:02 "能用的话尽量都用，之后我会更新成新的 Run，我们会 cover 它".
- **Today the skill**: actions are `reuse / rerun / registered`; there is no provisional state and no "search first" step.
- **Change**: §LAND step 2 adds "search `_WorkSpace` stores and `old/` dirs before declaring missing"; new binding state `provisional` (hash recorded, marked stale when a newer Result with the same target arrives).
- **Your call: ⬜**

### P10 · LAND runs everything that can run on this machine before it returns. Only a secure-server route or a person gate may stop it, and the receipt says "as far as I could go".
- **You said**: 260904 23:35 "除了不能跑的，其他可以跑的你是不是先可以跑起来了" · 260906 17:44 "as far as you can go" · 21:35 "那你开始做呀，等我干嘛？你去把它都做完啊".
- **Today the skill**: item graphs may run in parallel; nothing says "exhaust local work before HOLD".
- **Change**: §LAND preamble adds the rule; receipt gains a `stopped-by:` line (server · person · nothing left).
- **Your call: ⬜**

### P11 · EMBED writes each verified citation's bib entry into the paper's room bibliography, so a strict build resolves every key.
- **You said**: 260906 22:29 "为什么我们现在还有 citation 没有解析呢？evidence 不是都已经做好了吗" · 22:35 "所有的 citation 一定要都 work，不能给我 hallucination，要不然我就 GG 了" (the master build had 23 unresolved keys).
- **Today the skill**: the CITE item is verified on the page; nothing moves the entry into `reference.bib`.
- **Change**: §EMBED step: append the verified entry to the room bibliography under the same key; a key already present with a different body is a conflict to report, not overwrite.
- **Your call: ⬜**

### P12 · A DISPLAY Result is reported with its rendered picture or PDF link, never described in words.
- **You said**: 260906 22:42 "你能不能让我看看这三个 table 现在长什么样子" · 22:44 "我们现在是不是已经有了这些图了？".
- **Change**: typed local Results table: the DISPLAY row requires `preview:` (image or PDF path) and the receipt prints its viewer link.
- **Your call: ⬜**

### P13 · A VALUE Result names the population layer it reports.
- **You said**: 260905 00:00 "我们实际上用的是整个 coverage 的数据呢，还是最终 data content 的数据呢，还是 online review 里面有多少医生".
- **Change**: typed local Results table: the VALUE row carries `population:` (for example coverage corpus · analytic cohort · linked LBP sample).
- **Your call: ⬜**

### P14 · Evidence status is reported per item as decided · landed · folded · ready, grouped by type and by how easy each is to get.
- **You said**: 260906 15:36 "evidence 是不是都已经 ready to use 了，都已经做好 landing 和 embedding 了吗" · 13:54 "有没有图啊、表啊，是不是都现在比较容易拿到了".
- **Change**: §Receipt replaces the bare counts with the four-state table by type; adds an `attainability` column (local · server · person).
- **Your call: ⬜**

---

## Part 3 · haipipe-page-content (the writing skill)

### P15 · Process words never enter the prose. "Historical", "provisional", "pending", "will be replaced" live in the evidence record, not the paragraph.
- **You said**: 260906 18:17 "你不要加这个 history，也不要加这个 pending，这些我们自己记录就行了，正文不要显示这些东西" · 22:19 "不要在正文里面列上有这样的一个区别".
- **Today the skill**: says "preserve calibrated hedging"; no ban on bookkeeping vocabulary.
- **Change**: §① Draft adds a short banned list and the rule "the caveat belongs on the Local Result / discussion record".
- **Your call: ⬜**

### P16 · The Revise step is a real pass: the humanizer skill, then a fresh-context style check against MISQ exemplars, before the build.
- **You said**: 260906 21:43 "在写之前是不是要自己审阅一下？我们有一个专门的 revise…避免写得太 AI" · 22:21 "content 写完之后没有做 revise 呀？" · 18:05 "像不像一个 MISQ paper style？读起来很 AI 吗？double check 一下".
- **Today the skill**: §② Revise is five lines of intent with no named pass.
- **Change**: §② Revise = run `haipipe-paper-revise-humanizer`, then a fresh subagent reads two exemplar paragraphs and ours and returns a style verdict; both receipts required before ③ Build.
- **Your call: ⬜**

### P17 · A paragraph has 4 to 6 sentences; a paragraph grows by adding sentences, never by lengthening them; median about 21 words.
- **You said**: 260906 15:56 "一个句子只能表达一个点…一个自然段五到六个句子是 OK 的，但不要使一个句子变得太长" · 17:57 "每个自然段都是四句会不会太少，变成四到五句" · 16:38 "21 是不是没什么问题".
- **Today the skill**: 18–24 word median, 30+ words flagged. No paragraph rule.
- **Change**: §① Draft adds the paragraph range; the entry check reports sentences per paragraph.
- **Your call: ⬜**

### P18 · Build delivers what you asked to see: LaTeX/PDF and Word on "complete version", page count reported, the best available PDF first when something is blocked, figure PDFs trimmed to their margins, and the viewer link returned.
- **You said**: 260906 19:07 "把它转成 LaTeX，还有 Word 文件，我想看一个 complete 的版本" · 22:45 "先把最好的版本弄出来，我现在先要一个 PDF" · 13:53 "PDF 的话可不可以把 margins 变得小一些".
- **Today the skill**: "regenerate only the declared projections".
- **Change**: §③ Build lists the deliverables above and the two lines every build report carries: pages · link.
- **Your call: ⬜**

### P19 · A writing-only review is allowed: judge the prose while unresolved numbers stay bracketed.
- **You said**: 260906 19:33 "先不考虑 values，writing 的地方还有什么需要更改的".
- **Change**: §② Revise adds the mode `writing-only`; VALUE gaps are shown as brackets and excluded from the style verdict.
- **Your call: ⬜**

---

## Part 4 · haipipe-page (the page contract and router)

### P20 · A `status` verb prints one row per page: Outline (version · approved?) · Evidence (decided / landed / folded / blocked) · Content (written to which version · built? · PDF pages · citations resolve?) · Check. A group prints every page and never drops one.
- **You said**: 260905 22:26 "其中一个 column 应该说是 outline，然后 evidence，还有 content，这三个 column" · 260906 21:38 "bullets 没问题了是吧？evidence 做完了？content 也 OK 了？" · 21:39 "那我们的 introduction 呢？在哪里啊？"
- **Today the skill**: `preview` prints title, opening, aims, divisions, last log line. No phase-state row.
- **Change**: new `cli/status.py` + §Preview·create·work on·run documents the four columns.
- **Your call: ⬜**

### P21 · Every reply that changes a page ends with the verified board URL. A reply may not end with a file path, `localhost`, or `127.0.0.1`.
- **You said**: 260906 13:21 "我们的页面不能用 127.0，这我说很多次了，为什么还在犯一样错误" · 13:51 "每个 response 的末尾，把 webpage 的链接给我一下" · 20:41 "At the end you should give me the board page link".
- **Today the skill**: the URL rule exists; "end every reply with it" and "verify it opens first" do not.
- **Change**: §Open the rendered Page adds the closing-line rule and a `curl` check before the link is written.
- **Your call: ⬜**

### P22 · An accepted process ruling lands in the skill text first, then in the affected pages, in the same pass.
- **You said**: 260906 14:20 "在做 content writing 之前，先想办法更新我们的 skills…更新完之后再推进 introduction" · 15:13 "一边是更新我们的 skills，一个是更新我们的 outline" · 20:56 "Could you update the skills accordingly? And then update the outline accordingly".
- **Change**: §What a write may touch adds the rule; the receipt names the skill version the page was written under.
- **Your call: ⬜**

### P23 · When a phase ends, the receipt names the next owed thing: which Runs remain, which gate is next, who holds it.
- **You said**: 260905 22:34 "假如说这个 shape 没问题的话，那我还需要额外跑什么 runs 呢" · 260906 00:23 "abstract ready 的话，那 abstract 里面的 run 还有 evidence 我该怎么办呢".
- **Change**: outline and evidence receipts gain a `next:` block (runs · gate · holder).
- **Your call: ⬜**

---

## Part 5 · haipipe-plugin-outline (the Outline tab)

### P24 · The Outline table is regenerated and the board rebuilt right after any plan change, and the rendered tab is checked before the reply.
- **You said**: 260906 20:26 "Is the outline table updated or not?" · 20:28 "Do it. Go and update."
- **Change**: §Generation adds "regenerate + rebuild + open the tab" as one step at the end of SHAPE, SURVEY, and EMBED.
- **Your call: ⬜**

### P25 · Feedback state in the table = decision D3 above.

---

## Part 6 · Not changing, because it is already in the skill (veto if you disagree)

- **N1** version law: v0.x until your approval, v1.0 then v1.1; evidence folds v1.0.1; wrong integers demoted (outline skill, plus a checker tooth).
- **N2** chat approval is transcribed as `approved: ✅ JL <date> · in chat: "…"`; a machine never writes it.
- **N3** evidence binds to one Bullet; no paragraph or sibling inheritance; `Evidence: none` is explicit.
- **N4** CITE verification is your signature; a machine never signs it.
- **N5** entry checklist before writing: names · paragraph and sentence counts · word target · citation density; 18–24 word median.
- **N6** Outline table first and open; the other blocks collapsed; the four cycle names shown bare.
- **Your call on N1–N6: ⬜** (blank = keep all)

---

## Part 7 · Order of work after your answers

1. Patch the five skill texts and `review-packet.md` for every ✅ row; ✎ rows patched as you wrote them; ❌ rows untouched.
2. Re-apply to the MISQ paper: run `status` on the 8 Main pages; re-issue the review packet for the 4 approved pages; no version number changes without your tick.
3. Field test: a fresh subagent runs SHAPE→SURVEY on S-MISQ-Main-Empirical-Strategy under the patched skills; I check it hits P01, P03, P05, P10, P21 without being told.
4. One version bump per skill and one CHANGELOG entry each, at the end.
5. Reply with the board link and the field-test result.

Estimated: one working session after your answers.
