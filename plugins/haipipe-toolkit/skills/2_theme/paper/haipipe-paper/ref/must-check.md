# Must-check · what JL has already said, checked before he sees it

Every rule below is one JL gave, or a fault his sessions hit, at least once, most of them several times, on more than one paper (the MISQ
replay, 2026-11-08 to 11-14, and the feedback kept in the SPACEs' memories; `said:` counts the times and quotes the
first). A rule here is never said to JL again: the session that writes, revises or delivers a paper runs it.

## The gate

1. **Before JL sees a Section** (a draft version, a Draft Lab round, a reply that shows prose), **before a Section
   closes**, and **before a send**, the session runs every rule whose `when:` matches, `auto` ones by script and
   `read` ones by a fresh reviewer subagent that did not write the text.
2. A failing rule is fixed first, or named in the reply with its id and the reason it stays ("M-A02: P4 has 8
   sentences; the Methods list needs all 8"). Text is never handed over with an unnamed failure.
3. **A correction JL gives, directly or relayed by another session, changes this file in the same change as the fix.**
   If the rule is new, add it here with its check. If it is already here, the gate failed: make its check stronger
   (a script where there was only reading, an earlier `when:`), never only reword the rule. Fixing one view or one
   paper and leaving the rule out is how JL ends up saying it again (M-B03 was fixed in one view on 261113 and said
   twice more on 261115).
4. Rules belong where they are checked: a paper rule here; a page-look rule in the repo's AGENTS.md § Page words; a
   working-style rule in the person's global CLAUDE.md. One paper's own content decisions stay in that paper.

`check:` says how: `auto (…)` is a script test, `read (…)` is what a reviewer reads for. `when:` is the earliest point
it must hold.


## A · Paper writing

M-A01 · Make the smallest edit that fixes a sentence; keep its words, order and paragraph structure.
  check: auto (word similarity per edited sentence, difflib ratio; below 0.6 needs a written reason; sentence count and order unchanged) | read (no rewrite of untouched sentences)
  when: before JL sees a Section
  said: 7× · 261113 MISQ "everytime we nade the chanse, make sure we don't make huge changes."

M-A02 · Keep every paragraph at 4 to 7 sentences; fix by moving or merging, never by filler.
  check: auto (sentences per `### C<n>.P<m>` heading; Abstract, appendix, letters exempt; `reason:` line accepts an exception)
  when: before JL sees a Section
  said: 4× · 261104 JAMA "一个 paragraph 至少是 4~6 句话"

M-A03 · Give each sentence one topic with one or two points, three at most.
  check: auto (flag sentences over 30 words, a colon that chains a second claim, a clause between subject and verb) | read (name each sentence's topic in 2 to 3 words)
  when: before JL sees a Section
  said: 4× · 261113 MISQ "for each sentence, as most two points, but always under one topic"

M-A04 · Make each sentence follow from the one before; cut a sentence that breaks the flow.
  check: read (each sentence read with its neighbours; link carried, weak or broken)
  when: before JL sees a Section
  said: 4× · 261113 MISQ "we can drop them, I feel this is not smooth."

M-A05 · Keep approved, co-author and JL-named wording word for word; propose changes to it as cards.
  check: auto (diff approved or co-author-inserted sentences against the new draft; any change must be a card) | read (no silent edit to a ✓ or co-author sentence)
  when: before JL sees a Section
  said: 3× · 261113 MISQ "wht you changed is very bad"

M-A06 · Remove the AI tells senior co-authors flagged: room metaphors, definition stacks, self-narration, self-praise.
  check: auto (anti_slop.py audit; regex for settle(s), leave(s) open, room to, roadmap lines such as "This section" or "we turn to") | read (ai-tells.md § 5 and the Board's writing-patterns.md)
  when: before JL sees a Section
  said: 3× · 261110 MISQ "ask the agent to read each sentences to see whether it is easier to understand."

M-A07 · Avoid runs of sentences that open with "We" or "Our"; count both as one pattern.
  check: auto (two or more neighbouring sentences opening with We|Our; we/our count per paragraph)
  when: before JL sees a Section
  said: 3× · 261113 MISQ "I think we used too many We We We"

M-A08 · Claim no more than the cited studies or own evidence show; no post-hoc expectations.
  check: read (each claim against its card; causal verbs only with a causal design; "We expected" only with evidence)
  when: before JL sees a Section
  said: 3× · 261113 MISQ "is this really? I don't think so."

M-A09 · Write related work as 3 or 4 streams of close studies; develop theory, never one cited line.
  check: read (number of streams; each theory construct has claim, evidence, fit, prediction)
  when: before JL sees a Section
  said: 3× · 261019 LLMRec "we might have too many related works"

M-A10 · State the research questions together as questions; hypotheses in words, no H1 labels, in an Introduction.
  check: auto (H1/H2 tokens in the Introduction; question marks in the questions paragraph) | read (both questions adjacent)
  when: before JL sees a Section
  said: 3× · 261104 JAMA "why we have the H1 here?"

M-A11 · Say numbers in everyday words; give both halves of a count; size data in its own unit.
  check: auto (flag "tenfold", "per 10x", "cut by"; "only N of M" without the other direction) | read (data size beside people count)
  when: before JL sees a Section
  said: 3× · 261111 ScalingGlucose "what is the tenfold increase? hard to understand."

M-A12 · Never repeat a sentence, a number or a review stream across Sections.
  check: auto (near-duplicate sentence scan across all Sections of the version) | read (Theory does not restate Literature Review)
  when: before closing a Section
  said: 2× · 261114 MISQ "could we just delete this?" (a point already made in three Sections)

M-A13 · Use no semicolons and no transition set off by commas in paper sentences.
  check: auto (anti_slop.py rules `semicolon`, `parenthetical-transition`; statistics in one parenthesis exempt)
  when: before JL sees a Section
  said: 2× · 261016 "if possible, do not use ';'"

M-A14 · Open on why the venue's reader cares; state the contribution first, in plain words.
  check: read (P1's first point is the reader's stake; contribution sentence present and not a result)
  when: before JL sees a Section
  said: 2× · 261021 LLMRec "这个 audience 他是医生"

M-A15 · End the review on the gap; never write a gap that contradicts the team's own papers.
  check: read (gap sentence present; checked against the team's other papers on the topic)
  when: before JL sees a Section
  said: 2× · 261113 MISQ "this is underscored, do you get it? to show that there is a gap here."

M-A16 · Place each citation group beside the words it supports, before the full stop, in the venue's style.
  check: auto (regex for a citation after the full stop; "et al." for 3 or more authors per the venue style)
  when: before JL sees a Section
  said: 2× · 261113 MISQ "what I mean you can put it in different sentences?"

M-A17 · Say a limit once, in Limitations; no over-defensive or procedural-defense lines.
  check: auto (regex for "causation cannot be established", "not causal effects") | read (limits stated once)
  when: before JL sees a Section
  said: 2× · 261104 JAMA "会不会有点过度防御啊"

M-A18 · Use no em-dashes anywhere in paper text.
  check: auto (anti_slop.py rule `em-dash`)
  when: before JL sees a Section
  said: 2× · 260724 "fuck em-dash"

M-A19 · Use one name for each construct in text, figures and captions.
  check: auto (construct names from the Story compared across Sections and display labels)
  when: before closing a Section
  said: 2× · 261113 MISQ "should we say the Clinical Uncertainty or CLinical discretion?"

M-A20 · Make titles and labels academic and clear on first read; no metaphor verbs.
  check: auto (anti_slop.py `title-metaphor`, `in-group-shorthand`) | read (blind title score of 8 or more)
  when: before JL sees a Section
  said: 1× · 261112 ScalingGlucose "I don't know why here we use the word of 'buy'"

M-A21 · Let a person do the verb, and use the exact verb for the method.
  check: read (inanimate subject with an animate verb; "map" where the method scores)
  when: before JL sees a Section
  said: 1× · 261110 MISQ Ritu (co-author) "We introduced three sets of controls in sequence" as the fix (no JL quote)

M-A22 · Open the Abstract with the paper's title; its last sentence does not restate it.
  check: auto (`C1.P0 · Title · S0` present; word limit counted on C1.P1)
  when: before JL sees a Section
  said: 1× · 261111 ScalingGlucose "the abstract should contains the title"


## B · Paper evidence

M-B01 · Print each result as one number everywhere, bound to its Board value or Run.
  check: auto (every number in prose, Abstract and tables matched to the value ledger; same quantity with two values fails)
  when: before closing a Section
  said: 8× · 261113 MISQ "I think it should be 226,999? Are we consistent through the whole draft?"

M-B02 · Check each citation against the paper itself: it exists, and it supports this sentence.
  check: auto (DOI resolves on Crossref; title and abstract fetched) | read (the abstract supports the sentence, fully or partly)
  when: before closing a Section
  said: 5× · 261114 MISQ "I want you to double check this, whether this cititon support this or not."

M-B03 · Show citations to readers as (Author et al. Year); only LaTeX source keeps `\citep` keys.
  check: auto (grep `\\cite[pt]?\{` in cards, replies, web view and Draft view text)
  when: before JL sees a Section
  said: 4× · 261114 MISQ "for the citation, we agreed to not use the latex version, right?"

M-B04 · Point Section evidence and displays at the Block-level source; never copy them.
  check: auto (no `display/` copies in Section folders; every card names a Board Run id)
  when: before closing a Section
  said: 4× · 261113 MISQ "how do you think this to the block level evidence???"

M-B05 · Draw a conceptual model as construct-name boxes and hypothesis arrows only; mechanism goes in text.
  check: read (no statements in boxes; arrows carry only H labels; compared with Figure 1 of venue papers)
  when: before a send
  said: 5× · 261110 MISQ "make the box to be the construct, and the statement."

M-B06 · Link every claim that needs support to a citation or evidence card.
  check: auto (sentences tagged as claims with no card or `\cite`; co-author "needs a citation" comments open)
  when: before closing a Section
  said: 3× · 261114 MISQ "the cusions here are not well linked to the evidences"

M-B07 · Cite only real `.bib` keys; use `\cite{TOADD}` when missing; one work, one key; never edit bank.bib.
  check: auto (every key resolves; duplicate DOI or title under two keys; bank.bib unchanged in git)
  when: before closing a Section
  said: 3× · 260710 MISQ "I think you should use \cite{xxx} from the .bib file"

M-B08 · Plan displays with the authors from meetings and venue rules before Sections write numbers.
  check: read (display plan in the display Job face; venue figure rules and similar journal figures named)
  when: before JL sees a Section
  said: 2× · 261023 LLMRec "this should be a plan, and should be proposed to the author"

M-B09 · Give each display one question, colour named in words, and a blind review of 8 or more.
  check: auto (review/rNN.md score of 8 or more per cited display) | read (legend in every panel; plain-word axis)
  when: before a send
  said: 2× · 261022 LLMRec "display should also have a loop, like the draft"

M-B10 · Never print a data partner's internal cohort names or any identifying rows.
  check: auto (pdftotext of PDF and Word grepped for cohort names; `check_results_phi.py --changed`)
  when: before a send
  said: 2× · 261113 ScalingGlucose "we will not show the name of ALS, CVS, LLY"

M-B11 · Show observed data and the pre-trend in result figures, not only coefficients.
  check: read (raw series beside the model figure; periods before the policy counted)
  when: before a send
  said: 1× · 261104 PDMP "the figures you have here is not exciting, not solid"

M-B12 · Apply a fix JL asks on one figure to that figure only; report the same issue elsewhere.
  check: auto (git diff touches only the named display's Run)
  when: before JL sees a Section
  said: 1× · 261104 ScalingGlucose "Figure 4 我没让你动啊 你动啥呢"


## C · Paper process

M-C01 · Score every sentence with a fresh blind subagent, never the writer; card each one below threshold.
  check: auto (every sentence has a ★ score by a reviewer id that is not the writer; cards exist for scores below 7)
  when: before JL sees a Section
  said: 16× · 261113 MISQ "score, should LLM or agent to judge it, the subagent to judge it."

M-C02 · Apply JL's card choices and comments into draft, page, LaTeX and Word, then confirm each.
  check: auto (each ✓ or accepted sentence compared across draft, Page Content, LaTeX fragment and Word text)
  when: before JL sees a Section
  said: 16× · 261113 MISQ "and check my decision and comments, how d you update them accordingly"

M-C03 · Let one session own one Section and write only there; the main session owns the version build.
  check: auto (a Section session's git diff touches only its tNN folder) | read (cross-page findings sent as messages)
  when: before JL sees a Section
  said: 15× · 260819 "don't cross the pages"

M-C04 · Deliver LaTeX first and Word last: PDF, LaTeX diff against the last round, then Word.
  check: auto (round folder holds the PDF, the diff PDF with margin notes, the Word file; diff base is the previous round)
  when: before a send
  said: 11× · 261113 MISQ "work on the Latex first, and the word will be done for the last step"

M-C05 · Pull the shared OneDrive file and check for others' edits before replacing it in place.
  check: auto (`word_round.py status` clean; size, mtime and content match the copy last placed)
  when: before a send
  said: 5× · 261023 JAMA "just replace the old draft, and make sure others can still work on it"

M-C06 · Read every co-author comment and meeting note; import each as a card on its sentence, then fix it.
  check: auto (every comment id in the pulled Word file has a card or a recorded drop reason)
  when: before JL sees a Section
  said: 4× · 261110 MISQ "could you check the comments from the draft in the onedrive as well?"

M-C07 · Close a Section only after an independent CHECK and the final checks pass.
  check: auto (`page.py health --final` with no FAIL; CHECK verdict by a different actor)
  when: before closing a Section
  said: 4× · 261114 MISQ "we are ready for closing it?"

M-C08 · Put findings, plans, patterns and every proposed edit on the page as cards, never only in chat.
  check: auto (each finding in a reply has a card in `draft/records/<stem>-revise.md`)
  when: before JL sees a Section
  said: 4× · 261113 MISQ "the message should be a card in the sentence or the section name"

M-C09 · Keep the venue format and template settled once; check page limits on the built PDF.
  check: auto (PDF page count against the venue limit; template diff against the official-format file)
  when: before a send
  said: 4× · 261113 MISQ "is this the real MISQ template one?"

M-C10 · Answer story and plan questions with a proposal first; change Structure and Draft together.
  check: read (no edits or rebuilds in the turn a story question is asked; § 1 and § 3 agree)
  when: before JL sees a Section
  said: 4× · 261024 MISQ "等一下，我们先考虑好然后再改"

M-C11 · Make co-author fixes as tracked changes; leave a comment only when no edit can answer.
  check: auto (count `comment:` entries without `new:` in edits.yaml; each needs a reason)
  when: before a send
  said: 3× · 261113 MISQ "for the comments here, why you don't fix them?"

M-C12 · Render the output and review your own changes on it before JL looks.
  check: read (fresh reader on the rendered PDF or Word; each change found where expected)
  when: before JL sees a Section
  said: 3× · 261113 MISQ "I didn;t see it is changed. why you don't review it yourelelf?"

M-C13 · Treat a ✓ checked or approved sentence as final: no reviewer score, notes or proposals.
  check: auto (✓ sentences with open cards or reviewer notes; ✓ on changed words shows ✓?)
  when: before JL sees a Section
  said: 3× · 261114 MISQ "I check this, why???"

M-C14 · Offer 2 to 4 options (A, B, C) for structure or wording choices; JL's named words win.
  check: read (choice cards carry options; JL's exact wording used when he gives it)
  when: before JL sees a Section
  said: 3× · 261022 ScalingGlucose "永远把 propose 这个方法放到首位"

M-C15 · Rescore a sentence whenever its words change.
  check: auto (★ score older than the sentence text is stale)
  when: before JL sees a Section
  said: 2× · 261114 MISQ "I think for the AI rating we should have one for re-eval, right?"

M-C16 · Report prose changes sentence by sentence by UI address, before and after; no bookkeeping.
  check: auto (no quoted paragraph block in a prose reply; each line starts with a `C<n>.P<m>` or `S<n>` address)
  when: before JL sees a Section
  said: 2× · 261113 MISQ "Make it the same to the index in the UI, setnence by sentences"

M-C17 · Read 3 to 4 same-type papers from the target journal, as screenshots, before writing.
  check: auto (`page.py health --final` row `0 · Examples`; `paper_check.py` W6; papers from the target venue only)
  when: before JL sees a Section
  said: 2× · 261104 "This is a must to do when you call the task for the /haipipe-paper-draft"

M-C18 · Move a draft's version number only on JL's OK; edit the current version in place.
  check: auto (no new `-draft-v<N+1>.md` without a recorded ok)
  when: before JL sees a Section
  said: 2× · 261020 LLMRec "until I feel it is ok, and we can upgrade it to v0.5"

M-C19 · Give every edit card its reason.
  check: auto (cards with an empty `Why:`; below 60% similarity needs a named defect)
  when: before JL sees a Section
  said: 2× · 261114 MISQ "for each editing card, we might give some reasons as well."

M-C20 · Run anti_slop.py audit and the readability check on any text you write, before showing it.
  check: auto (anti_slop.py audit and section-stats.py run on the current file; scores no worse than the original)
  when: before JL sees a Section
  said: 2× · 260819 "you should actively call the haipipe-writing to make sure the things are good to read."

M-C21 · Write a Section through /haipipe-draft: plan, sign, then prose; never free prose.
  check: auto (signed plan exists before § 3 sentences)
  when: before JL sees a Section
  said: 2× · 261020 LLMRec "did you used the /haipipe-draft to draft each section"

M-C22 · Between a writing Run's start and end, change content only; records come at the end.
  check: auto (no log, receipt or results/ writes between the Run's start and end marks)
  when: before closing a Section
  said: 2× · 260928 MISQ "don't change the log in the middle way, during the run"

M-C23 · Answer a comment inside the sentence it sits on, in JL's own terms.
  check: auto (card with `Answers: Comment <n>` targets the comment's own S<n>)
  when: before JL sees a Section
  said: 1× · 261022 LLMRec "你这个完全没有按照我的要求来啊！"

M-C24 · Drop co-author comments that point at cut text or ask for nothing.
  check: read (each imported comment anchors to live text and asks something)
  when: before JL sees a Section
  said: 1× · 261113 MISQ "things like this can be discarded."

M-C25 · Keep process text out of a delivered PDF or Word file.
  check: auto (grep text for DRAFT PAGE, NOT READY, not approved, pages ready, built 20xx, scores)
  when: before a send
  said: 1× · 260908 JAMA "the dielvered pdf or word must be clean!!!!!"

M-C26 · Hold a co-author round as a review Job, never in reports/.
  check: auto (no new `reports/qNN_coauthor-*` folder)
  when: before a send
  said: 1× · 261110 MISQ "we will no long using the reports/ plesae use the job or studio"

M-C27 · Keep what a Section must claim in its contract, not in its writing rules.
  check: read (writing rubric holds only size and shape rules)
  when: before JL sees a Section
  said: 1× · 261113 MISQ "this is mode like the decisions to make, right?"

M-C28 · Never rerun evidence scripts when only sentence addresses move; update the ledger.
  check: auto (evidence Run reruns with unchanged inputs and cells)
  when: before closing a Section
  said: 1× · 260928 MISQ "why update this? This waste a lot of resources."

M-C29 · Work evidence markdown-first; defer heavy display rebuilds and agent fan-out until asked.
  check: read (no compiled display rebuild or fan-out in a probe pass without an ask)
  when: before JL sees a Section
  said: 1× · 260709 MISQ "make the probe with the markdown version first"

M-C30 · Bind a paper's existing Board session and Codex threads before creating new ones.
  check: auto (session index searched for the paper's names before `--apply`)
  when: before JL sees a Section
  said: 1× · 260928 TimeEventDM "why we have 18 sessions?"

## D · Added 2026-11-15, from the sessions' relayed corrections

M-D01 · Write sentence ids lowercase and once per Draft: s1, s2 … through the Section, by position.
  check: auto (`page.py health` ids check: an id appears once; `page.py renumber --dry-run` changes nothing; an Abstract's title paragraph C1.P0 keeps s0)
  when: before JL sees a Section
  said: 3× · 261114 AITC "change the sentence label from upper-case S to lower-case s everywhere"; 261115 ScalingGlucose "make them to be small s for all"

M-D02 · Show every citation a reader sees as name-year, in every view and the web export; LaTeX keeps keys.
  check: auto (no `\cite` in the Draft Lab text, cards, replies or delivery/…/web/index.html; a key without a Bib entry shows "not in Bib")
  when: before JL sees a Section
  said: 4× · 261114 MISQ "we agreed to not use the latex version, right?"; 261115 ScalingGlucose "I think we mentioned we convert it to the name year format"

M-D03 · Start every writing lab with a blind sentence review and a paragraph-logic review of each changed Draft.
  check: auto (each Section's newest Draft version has a review Run at that version, sentence and paragraph; an unchanged Draft says "already reviewed at vX")
  when: before JL sees a Section
  said: 2× · 261115 ScalingGlucose "when you start the lab, these sentence level eval should be triggered"; "an AI reviewer to review the paragraph level logics"

M-D04 · Record who made each version: `by:` on a draft version and a display, `By:` on a card.
  check: auto (each file in draft/previous/ and each display version README has `by:`; a session names the person who signed)
  when: before a Section closes
  said: 2× · 261114 AITC "each entry should say WHO made the change"; same for displays

M-D05 · Key every review line, score, check and Flow line by its full address (C2.P1.s3, C2.P1), never a bare id.
  check: auto (a review report line or Flow line names a paragraph that exists; no two sentences share a bare id while one is keyed bare)
  when: before JL sees a Section
  said: 2× · 261115 AITC "a score can sit beside the wrong sentence"; "Flow P3 lands nowhere"

M-D06 · Read the person's marks before adopting, reverting or reviewing; never propose or score a checked sentence.
  check: auto (no proposed card, review score or rewrite on a sentence whose -checked.md line still holds its words; an adopt, revert or review prints the accepts, checks, comments and signs it read first)
  when: before any adopt, revert or review
  said: 3× · 261115 ScalingGlucose: an Abstract session adopted failed rewrites, overwrote accepted cards and reviewed after JL checked every sentence

M-D07 · Adopt a rewrite only when its blind pair says easier AND same meaning; "meaning: no" anywhere blocks it.
  check: auto (adopt refuses a pair with meaning: no, and a later pair that carries that pair's wording)
  when: before any adopt
  said: 1× · 261115 ScalingGlucose: a "meaning: no" keep slipped into unblinded.md and a later pair inherited it

M-D08 · Keep explanations in the Discussion, one meaning per term, claims within their intervals, the test set named in captions.
  check: read (paragraph-logic reviewer: explanation stated as a finding, a term used two ways, a claim stronger than its interval) | auto (each caption names its test set)
  when: before JL sees a Section
  said: 4× · 261115 ScalingGlucose paragraph-logic r01: 45 of 53 paragraphs under 8, these four faults most often

M-D09 · When a Story row changes, each Section that restates it learns it from its own health, not a broadcast.
  check: auto (health names the changed Story row and the Sections whose Drafts restate it)
  when: before JL sees a Section
  said: 2× · 261115 ScalingGlucose: a C6 claim edit failed every Section's narrative check; JL wants the Board not to disturb Sections

M-D10 · Turn a "for all" ruling into one sweep by the tool or the Board; a Section edits only its own Draft.
  check: read (a Section's change list names only its own files)
  when: before a Section closes
  said: 1× · 261115 ScalingGlucose: t01 changed t04's Draft on JL's "for all"

M-D11 · Hold the venue's shared main-text word budget across the Sections that count toward it.
  check: auto (health sums the main-text Sections against the venue cap, e.g. 3,500 for NMI, and names who grew)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose: review fixes added words in each Section (Results +201)

M-D12 · Match every caption's cross-references to the current display numbering.
  check: auto (the display Job's check compares "Figure N", "Table N", "Ext Data Fig. N" in captions with the numbering)
  when: before a send
  said: 1× · 261115 ScalingGlucose: Table 2 still said "Figure 2 and Table 1"; Ext Data Fig. 3 had a blank corner

M-D13 · Fold finished, rejected and superseded cards, fade answered comments, and mark a ★ stale when its words changed.
  check: auto (Draft Lab test: a decided card and an answered comment render folded or faded; a score on other words or an older numbering shows stale)
  when: before JL sees a Section
  said: 3× · 261115 ScalingGlucose "I feel the UI is much harder to use than before"; "are the old comments should be faded alway"

M-D14 · Answer "what is the current section structure" by printing `page.py structure <task>` verbatim, then at most one line.
  check: auto (the reply's first block equals the command's output)
  when: whenever the structure is asked
  said: 1× · 261115 ScalingGlucose: each session improvised a different shape

M-D15 · Accept writes a card into Content even while the plan is unsigned; the page then says so in plain words.
  check: auto (health WARNs, never FAILs, "Content holds text from an unsigned plan (v<N>); sign the plan" while the plan is unsigned and Content has adopted text)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose: an accept put an unsigned v1.4 into print; JL's ruling 261115 "1 A": keep writing, show the warning

## E · JL's method for working a Section (261115; haipipe-paper-draft ref/section-method.md)

M-E01 · S1: check each paragraph's job and each sentence's slot before changing prose.
  check: auto (`page.py structure <task>` printed at the current Draft version before a structure change)
  when: before a structure change
  said: 1× · 261115 ScalingGlucose t01: JL's method, structure loop step 1

M-E02 · S2: compare the structure with the venue's examples of the same article type and note what differs.
  check: read (paragraphs, words, the opening, how questions and results are stated, against 3 or more venue examples)
  when: before a structure change
  said: 1× · 261115 ScalingGlucose t01: structure loop step 2

M-E03 · S3: put a structure change in a new Draft version; a story change goes to JL as 2 to 4 versions.
  check: auto (a structure change bumps the Draft version) | read (a change to the Section's claims or order offers versions, JL picks)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose t01: structure loop step 3

M-E04 · D1: rate every paragraph and sentence by fresh reviewers (paragraph logic; sentence logic, read, ai); pass is 8.
  check: auto (a review Run at the current Draft version scores every paragraph and sentence; its reviewer is not the writer)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose t01: draft loop step 1

M-E05 · D2: rewrite each item under 8, keep only blind-A/B "easier and same meaning", adopt, re-rate what changed.
  check: auto (a blind A/B Run per round; adopted items all say kept; changed items rated again at the new version)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose t01: draft loop step 2

M-E06 · D3: highlight what the loop could not settle (claims, story, missing facts) for the person to read first.
  check: auto (the page lists the highlighted items, each with why the loop could not settle it)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose t01: draft loop step 3

M-E07 · D4: update the text from the person's comments and decisions, each change shown as a card.
  check: auto (every open comment is answered by a card or a Reply; no change applied without a card)
  when: before JL sees a Section
  said: 1× · 261115 ScalingGlucose t01: draft loop step 4

M-E08 · D5: close only when the person has checked every sentence at its current words.
  check: auto (each sentence has a -checked.md line whose words equal its current words)
  when: before a Section closes
  said: 1× · 261115 ScalingGlucose t01: draft loop step 5

M-E09 · Beside both loops: a person verifies each CITE; each VALUE binds by value id to its pinned value Run.
  check: auto (every cite key has a verified mark by a person; every printed number names a value id with a pinned Run)
  when: before a Section closes
  said: 1× · 261115 ScalingGlucose t01: evidence beside the loops
