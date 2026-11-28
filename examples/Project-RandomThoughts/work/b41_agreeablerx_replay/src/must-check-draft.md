# Paper must-check list · draft

A harvest of the rules JL repeats on paper work, drafted as a MUST-CHECK list for the
/hai-paper skill family. Each rule is checked before JL reads the text, so no
session waits for him to say it again.

Sources read (2026-11-15):

- 269 decisions from the MISQ paper week, 2026-11-08 to 2026-11-14 (`decisions-A.md`, `decisions-B.md`).
- 225 `type: feedback` memories: Physician-SPACE 143, WellDoc-SPACE 46, REACH-SPACE 11, Knowledge-SPACE 16, Tools-SPACE 9.
- Skill text: hai-paper (SKILL.md, checklist.md), hai-paper-draft, hai-draft-writing (+ ref/),
  hai-draft-review (+ ref/plain-rules.md, ref/ai-tells.md, ref/anti-slop-rules.json),
  hai-paper-evidence, hai-paper-comments, hai-paper-assemble, hai-paper-related,
  word-track-change, Tools-SPACE AGENTS.md § Page words.

Every source item went to exactly one bucket. Repeats of one rule were merged; the
`source:` count says how often JL had to say it.

| Bucket | Source items | Merged rules |
|---|---|---|
| A · Paper writing | 35 | 22 |
| B · Paper evidence | 35 | 12 |
| C · Paper process | 117 | 30 |
| D · Workbench / page UI | 177 | 24 lines below |
| E · General working style | 80 | 18 lines below |
| X · One paper only (dropped) | 50 | none |

Paper names used below: MISQ = the AgreeableRx MISQ paper (Physician-SPACE);
JAMA = the AgreeableOpioid JAMA paper; LLMRec = the LLMRec JAMA Internal Medicine
paper; PDMP = the PersonalityPDMPMandate paper; ScalingGlucose = the WellDoc-SPACE
Nature Machine Intelligence paper. Dates are yymmdd.

## A · Paper writing

M-A01 · Make the smallest edit that fixes a sentence; keep its words, order and paragraph structure.
  check: auto (word similarity per edited sentence, difflib ratio; below 0.6 needs a written reason; sentence count and order unchanged) | read (no rewrite of untouched sentences)
  when: before JL sees a Section
  source: 7 times · 261113 MISQ "everytime we nade the chanse, make sure we don't make huge changes." ; 260928 MISQ "Did you changed a lot compared to my original writing????" ; 261114 MISQ "why you changed so much in the C2.P3, please review it agian."
  in skill now: hai-draft-writing ref/writing.md § Highest-priority rule · surgical revision; ref/revise.md § Small changes, or a solid reason

M-A02 · Keep every paragraph at 4 to 7 sentences; fix by moving or merging, never by filler.
  check: auto (sentences per `### C<n>.P<m>` heading; Abstract, appendix, letters exempt; `reason:` line accepts an exception)
  when: before JL sees a Section
  source: 4 times (plain-rules.md notes "said more than 4 times" on 261104) · 261104 JAMA "一个 paragraph 至少是 4~6 句话" ; 261112 ScalingGlucose "unless having good reason, we might make sure they are between 4~7 sentences" ; 261113 MISQ "each paragraph is in the sentneces of 4~7? thisone is only three"
  in skill now: hai-paper-draft § Paragraphs of 4 to 7 sentences; hai-draft-review ref/plain-rules.md § 3a Paragraphs

M-A03 · Give each sentence one topic with one or two points, three at most.
  check: auto (flag sentences over 30 words, a colon that chains a second claim, a clause between subject and verb) | read (name each sentence's topic in 2 to 3 words)
  when: before JL sees a Section
  source: 4 times · 261113 MISQ "for each sentence, as most two points, but always under one topic" ; 261111 ScalingGlucose "One sentences, you can have one or two points, but must be one topic" ; 261113 MISQ "this is two long, how could we make it into two sentences?"
  in skill now: hai-draft-review ref/plain-rules.md § 3 Sentences

M-A04 · Make each sentence follow from the one before; cut a sentence that breaks the flow.
  check: read (each sentence read with its neighbours; link carried, weak or broken)
  when: before JL sees a Section
  source: 4 times · 261113 MISQ "we can drop them, I feel this is not smooth." ; 261113 MISQ "the logic here is weird/ can we say it is correct for ritu's comments?" ; 261021 LLMRec "每句话都要看一下上下文，review 它的逻辑关系是否通顺"
  in skill now: hai-draft-review ref/sentence-logic.md

M-A05 · Keep approved, co-author and JL-named wording word for word; propose changes to it as cards.
  check: auto (diff approved or co-author-inserted sentences against the new draft; any change must be a card) | read (no silent edit to a ✓ or co-author sentence)
  when: before JL sees a Section
  source: 3 times · 261113 MISQ "wht you changed is very bad" ; 261028 WellDoc email "I said, patient recruitment!!!!" ; 261114 MISQ approved S55 reverted after a reviewer tweak (no JL quote)
  in skill now: hai-paper-draft § Co-authors' patterns (item 2, their text is theirs); hai-paper-assemble § The final read

M-A06 · Remove the AI tells senior co-authors flagged: room metaphors, definition stacks, self-narration, self-praise.
  check: auto (anti_slop.py audit; regex for settle(s), leave(s) open, room to, roadmap lines such as "This section" or "we turn to") | read (ai-tells.md § 5 and the Board's writing-patterns.md)
  when: before JL sees a Section
  source: 3 times · 261110 MISQ "ask the agent to read each sentences to see whether it is easier to understand." ; 261113 MISQ "did you check the writing patterns" ; 261110 Ritu (co-author) "IT IS CLEAR THAT THIS IS WRITTEN BY AI"
  in skill now: hai-draft-review ref/ai-tells.md § 5 Hard to read; hai-paper-draft § Co-authors' patterns

M-A07 · Avoid runs of sentences that open with "We" or "Our"; count both as one pattern.
  check: auto (two or more neighbouring sentences opening with We|Our; we/our count per paragraph)
  when: before JL sees a Section
  source: 3 times · 261113 MISQ "I think we used too many We We We" ; 261113 MISQ "Yes, I think we and Our they should be the same." ; 261113 MISQ "I think the "we" is used too frequent, so hard."
  in skill now: no (note: ai-tells.md § 5 item 2 asks for a person as subject; both must hold)

M-A08 · Claim no more than the cited studies or own evidence show; no post-hoc expectations.
  check: read (each claim against its card; causal verbs only with a causal design; "We expected" only with evidence)
  when: before JL sees a Section
  source: 3 times · 261113 MISQ "is this really? I don't think so." ; 261111 ScalingGlucose "do we really have evidence for this?" ; 260928 MISQ cold read found causal verbs (no JL quote)
  in skill now: hai-paper-evidence (item 4, claim words fit the design); hai-paper-draft § Writing patterns (item 6)

M-A09 · Write related work as 3 or 4 streams of close studies; develop theory, never one cited line.
  check: read (number of streams; each theory construct has claim, evidence, fit, prediction)
  when: before JL sees a Section
  source: 3 times · 261019 LLMRec "we might have too many related works" ; 261031 PDMP "just categorize them based on the venue; we just need one" ; 261113 MISQ Ritu's lit review vs theory rule (no JL quote)
  in skill now: hai-paper-related (3 or 4 types); hai-draft-review ref/ai-tells.md § 5 (item 7)

M-A10 · State the research questions together as questions; hypotheses in words, no H1 labels, in an Introduction.
  check: auto (H1/H2 tokens in the Introduction; question marks in the questions paragraph) | read (both questions adjacent)
  when: before JL sees a Section
  source: 3 times · 261104 JAMA "why we have the H1 here?" ; 261111 ScalingGlucose "where are the two questions? i didn't see it." ; 261111 ScalingGlucose "do we really have evidence for this?"
  in skill now: hai-paper-draft § No semicolons (H1 labels) and § Writing patterns (items 5, 6)

M-A11 · Say numbers in everyday words; give both halves of a count; size data in its own unit.
  check: auto (flag "tenfold", "per 10x", "cut by"; "only N of M" without the other direction) | read (data size beside people count)
  when: before JL sees a Section
  source: 3 times (one paper, 261111) · 261111 ScalingGlucose "what is the tenfold increase? hard to understand." ; 261111 ScalingGlucose "should say the glucose size as well. not just the human"
  in skill now: hai-draft-review ref/plain-rules.md § 3; ref/ai-tells.md § 5 (items 11, 12)

M-A12 · Never repeat a sentence, a number or a review stream across Sections.
  check: auto (near-duplicate sentence scan across all Sections of the version) | read (Theory does not restate Literature Review)
  when: before closing a Section
  source: 2 times · 261114 MISQ "could we just delete this?" (a point already made in three Sections) ; 261113 MISQ Ritu's Theory: cut repeats of the Lit Review (no JL quote)
  in skill now: hai-draft-review ref/ai-tells.md § 5 (item 4, number said twice); across Sections: no

M-A13 · Use no semicolons and no transition set off by commas in paper sentences.
  check: auto (anti_slop.py rules `semicolon`, `parenthetical-transition`; statistics in one parenthesis exempt)
  when: before JL sees a Section
  source: 2 times · 261016 "if possible, do not use ';'" ; 261104 JAMA "我们尽量不要用分号啊 感觉很奇怪"
  in skill now: hai-paper-draft § No semicolons in the paper's sentences

M-A14 · Open on why the venue's reader cares; state the contribution first, in plain words.
  check: read (P1's first point is the reader's stake; contribution sentence present and not a result)
  when: before JL sees a Section
  source: 2 times · 261021 LLMRec "这个 audience 他是医生" ; 261110 MISQ Ritu (co-author) "Theory, practical, I don't care which."
  in skill now: hai-draft-review ref/ai-tells.md § 5 (item 8, granular openings); the venue reader: no

M-A15 · End the review on the gap; never write a gap that contradicts the team's own papers.
  check: read (gap sentence present; checked against the team's other papers on the topic)
  when: before JL sees a Section
  source: 2 times · 261113 MISQ "this is underscored, do you get it? to show that there is a gap here." ; 261113 MISQ "我们还有一个 Jama paper, 跟这是一样 topic 呢"
  in skill now: no

M-A16 · Place each citation group beside the words it supports, before the full stop, in the venue's style.
  check: auto (regex for a citation after the full stop; "et al." for 3 or more authors per the venue style)
  when: before JL sees a Section
  source: 2 times · 261113 MISQ "what I mean you can put it in different sentences?" ; 260928 MISQ cold read found all 19 Discussion citations after the full stop (no JL quote)
  in skill now: no

M-A17 · Say a limit once, in Limitations; no over-defensive or procedural-defense lines.
  check: auto (regex for "causation cannot be established", "not causal effects") | read (limits stated once)
  when: before JL sees a Section
  source: 2 times · 261104 JAMA "会不会有点过度防御啊" ; 261104 JAMA "this will raise questions"
  in skill now: hai-draft-review ref/plain-rules.md § 3b Say a limit once; ref/ai-tells.md § 5 (item 5)

M-A18 · Use no em-dashes anywhere in paper text.
  check: auto (anti_slop.py rule `em-dash`)
  when: before JL sees a Section
  source: 2 times · 260724 "fuck em-dash" ; global CLAUDE.md (no em-dashes)
  in skill now: hai-draft-review ref/anti-slop-rules.json (`em-dash`)

M-A19 · Use one name for each construct in text, figures and captions.
  check: auto (construct names from the Story compared across Sections and display labels)
  when: before closing a Section
  source: 2 times · 261113 MISQ "should we say the Clinical Uncertainty or CLinical discretion?" ; 261114 MISQ Theory, same question left open (no JL quote)
  in skill now: no

M-A20 · Make titles and labels academic and clear on first read; no metaphor verbs.
  check: auto (anti_slop.py `title-metaphor`, `in-group-shorthand`) | read (blind title score of 8 or more)
  when: before JL sees a Section
  source: 1 time · 261112 ScalingGlucose "I don't know why here we use the word of 'buy'"
  in skill now: hai-paper-draft § Titles read like the text

M-A21 · Let a person do the verb, and use the exact verb for the method.
  check: read (inanimate subject with an animate verb; "map" where the method scores)
  when: before JL sees a Section
  source: 1 time · 261110 MISQ Ritu (co-author) "We introduced three sets of controls in sequence" as the fix (no JL quote)
  in skill now: hai-draft-review ref/ai-tells.md § 5 (items 2, 9)

M-A22 · Open the Abstract with the paper's title; its last sentence does not restate it.
  check: auto (`C1.P0 · Title · S0` present; word limit counted on C1.P1)
  when: before JL sees a Section
  source: 1 time · 261111 ScalingGlucose "the abstract should contains the title"
  in skill now: hai-paper-draft § The Abstract carries the title

## B · Paper evidence

M-B01 · Print each result as one number everywhere, bound to its Board value or Run.
  check: auto (every number in prose, Abstract and tables matched to the value ledger; same quantity with two values fails)
  when: before closing a Section
  source: 8 times · 261113 MISQ "I think it should be 226,999? Are we consistent through the whole draft?" ; 261114 MISQ "the numbers here is not consistent with the abstract" ; 261110 MISQ "I think for the values, you should update it as well?"
  in skill now: hai-paper-evidence § The chain (`chain_check.py`), which says it does not yet read numbers typed in prose

M-B02 · Check each citation against the paper itself: it exists, and it supports this sentence.
  check: auto (DOI resolves on Crossref; title and abstract fetched) | read (the abstract supports the sentence, fully or partly)
  when: before closing a Section
  source: 5 times · 261114 MISQ "I want you to double check this, whether this cititon support this or not." ; 261108 MISQ "at least you show the paper's articile title and abstract" ; 261114 MISQ "do you think the paper from Greenwald is related or not?"
  in skill now: hai-paper-evidence (item 1, citations come from verified CITE Results); "supports this sentence": no

M-B03 · Show citations to readers as (Author et al. Year); only LaTeX source keeps `\citep` keys.
  check: auto (grep `\\cite[pt]?\{` in cards, replies, web view and Draft view text)
  when: before JL sees a Section
  source: 4 times · 261114 MISQ "for the citation, we agreed to not use the latex version, right?" ; 261115 ScalingGlucose "I think we mentioned we convert it to the name year format" ; 261113 MISQ "how about we just make the citaitons to be the readable one?"
  in skill now: no (the ScalingGlucose memory notes no written rule on disk on 261115)

M-B04 · Point Section evidence and displays at the Block-level source; never copy them.
  check: auto (no `display/` copies in Section folders; every card names a Board Run id)
  when: before closing a Section
  source: 4 times · 261113 MISQ "how do you think this to the block level evidence???" ; 261113 MISQ "they will borrow or point it to the block level content, rightt?" ; 261113 MISQ "I think you should update the display, is that available in the blcok level?"
  in skill now: hai-paper-evidence ("One display, one home")

M-B05 · Draw a conceptual model as construct-name boxes and hypothesis arrows only; mechanism goes in text.
  check: read (no statements in boxes; arrows carry only H labels; compared with Figure 1 of venue papers)
  when: before a send
  source: 5 times · 261110 MISQ "make the box to be the construct, and the statement." ; 261114 MISQ "so we don't add the mechenism. or the H1 H2 explanation, right?" ; 261114 MISQ "is this what Ritu be okay with?"
  in skill now: no

M-B06 · Link every claim that needs support to a citation or evidence card.
  check: auto (sentences tagged as claims with no card or `\cite`; co-author "needs a citation" comments open)
  when: before closing a Section
  source: 3 times · 261114 MISQ "the cusions here are not well linked to the evidences" ; 261113 MISQ "we should add the citaiton to RItu;s comments, did we find it or not?"
  in skill now: hai-paper-evidence (item 5, every consequential sentence is one of three)

M-B07 · Cite only real `.bib` keys; use `\cite{TOADD}` when missing; one work, one key; never edit bank.bib.
  check: auto (every key resolves; duplicate DOI or title under two keys; bank.bib unchanged in git)
  when: before closing a Section
  source: 3 times · 260710 MISQ "I think you should use \cite{xxx} from the .bib file" ; 260811 "I want bank.bib to be sealed, don't touch it" ; 261113 MISQ duplicate keys found at the diff build (no JL quote)
  in skill now: hai-paper-evidence (item 1); hai-paper-draft § Closing checks

M-B08 · Plan displays with the authors from meetings and venue rules before Sections write numbers.
  check: read (display plan in the display Job face; venue figure rules and similar journal figures named)
  when: before JL sees a Section
  source: 2 times · 261023 LLMRec "this should be a plan, and should be proposed to the author" ; 261023 LLMRec "if you are the JAMA IM reviewer, will you accept these figures?"
  in skill now: hai-paper-plan (s06 paper displays)

M-B09 · Give each display one question, colour named in words, and a blind review of 8 or more.
  check: auto (review/rNN.md score of 8 or more per cited display) | read (legend in every panel; plain-word axis)
  when: before a send
  source: 2 times · 261022 LLMRec "display should also have a loop, like the draft" ; 261027 WellDoc "I thought blue was low-rate patients and red was high-rate"
  in skill now: hai-paper-evidence (display revise loop; one colour scheme per paper)

M-B10 · Never print a data partner's internal cohort names or any identifying rows.
  check: auto (pdftotext of PDF and Word grepped for cohort names; `check_results_phi.py --changed`)
  when: before a send
  source: 2 times · 261113 ScalingGlucose "we will not show the name of ALS, CVS, LLY" ; 261112 REACH aggregates only, no names or free text (no JL quote)
  in skill now: no

M-B11 · Show observed data and the pre-trend in result figures, not only coefficients.
  check: read (raw series beside the model figure; periods before the policy counted)
  when: before a send
  source: 1 time · 261104 PDMP "the figures you have here is not exciting, not solid"
  in skill now: no

M-B12 · Apply a fix JL asks on one figure to that figure only; report the same issue elsewhere.
  check: auto (git diff touches only the named display's Run)
  when: before JL sees a Section
  source: 1 time · 261104 ScalingGlucose "Figure 4 我没让你动啊 你动啥呢"
  in skill now: no

## C · Paper process

M-C01 · Score every sentence with a fresh blind subagent, never the writer; card each one below threshold.
  check: auto (every sentence has a ★ score by a reviewer id that is not the writer; cards exist for scores below 7)
  when: before JL sees a Section
  source: 16 times · 261113 MISQ "score, should LLM or agent to judge it, the subagent to judge it." ; 261021 LLMRec "for the reviewer, did you call the subagent for it?" ; 261114 MISQ "Where is your sentence level AI-eval?"
  in skill now: hai-draft-review § Highest-priority rule · independence; hai-paper-draft § Co-authors' patterns (item 3)

M-C02 · Apply JL's card choices and comments into draft, page, LaTeX and Word, then confirm each.
  check: auto (each ✓ or accepted sentence compared across draft, Page Content, LaTeX fragment and Word text)
  when: before JL sees a Section
  source: 16 times · 261113 MISQ "and check my decision and comments, how d you update them accordingly" ; 261114 MISQ "I approved the changes, but it is not updated, why?" ; 261114 MISQ "have you apllied or not?"
  in skill now: partly: hai-draft-writing § Adopt · no second draft (accept writes the draft only)

M-C03 · Let one session own one Section and write only there; the main session owns the version build.
  check: auto (a Section session's git diff touches only its tNN folder) | read (cross-page findings sent as messages)
  when: before JL sees a Section
  source: 15 times · 260819 "don't cross the pages" ; 261111 MISQ "Write only inside your own page folder." ; 261113 MISQ "I think for you, you should focus on the [Image #41]"
  in skill now: hai-paper § Section sessions (ref/section-sessions.md)

M-C04 · Deliver LaTeX first and Word last: PDF, LaTeX diff against the last round, then Word.
  check: auto (round folder holds the PDF, the diff PDF with margin notes, the Word file; diff base is the previous round)
  when: before a send
  source: 11 times · 261113 MISQ "work on the Latex first, and the word will be done for the last step" ; 261113 MISQ "could you have the latex version of diff?" ; 261114 MISQ "put the word version and the pdf version, and the pdf version with diff"
  in skill now: hai-paper § Section sessions (web, then LaTeX, then Word); hai-paper-assemble § What changed since the last round · the LaTeX diff

M-C05 · Pull the shared OneDrive file and check for others' edits before replacing it in place.
  check: auto (`word_round.py status` clean; size, mtime and content match the copy last placed)
  when: before a send
  source: 5 times · 261023 JAMA "just replace the old draft, and make sure others can still work on it" ; 261014 "is this one up to date?" ; 261113 MISQ Word opened the old SharePoint copy before AutoSave (no JL quote)
  in skill now: word-track-change § Steps (1 pull, 9 push refuses)

M-C06 · Read every co-author comment and meeting note; import each as a card on its sentence, then fix it.
  check: auto (every comment id in the pulled Word file has a card or a recorded drop reason)
  when: before JL sees a Section
  source: 4 times · 261110 MISQ "could you check the comments from the draft in the onedrive as well?" ; 261113 MISQ "have you read them and fix them? no need to leave the comments." ; 261113 MISQ "did you immigrate Coauthor's comments from the OneDrive?"
  in skill now: hai-paper-comments; hai-paper-draft § Co-authors' patterns

M-C07 · Close a Section only after an independent CHECK and the final checks pass.
  check: auto (`page.py health --final` with no FAIL; CHECK verdict by a different actor)
  when: before closing a Section
  source: 4 times · 261114 MISQ "we are ready for closing it?" ; 261114 MISQ "could we close it now? Do we still have huge errors now?" ; 261104 "must to do before saying such a task session is finished"
  in skill now: hai-paper-draft § Closing checks; § Examples first: a must

M-C08 · Put findings, plans and patterns on the page as cards, never only in chat.
  check: auto (each finding in a reply has a card in `draft/records/<stem>-revise.md`)
  when: before JL sees a Section
  source: 4 times · 261113 MISQ "the message should be a card in the sentence or the section name" ; 261110 MISQ "No, I want you put the plan to somewhere in the workbench UI." ; 261020 LLMRec "I wont read here, just update the results"
  in skill now: partly: hai-paper-draft § Co-authors' patterns (item 1, writing-patterns.md on the Board)

M-C09 · Keep the venue format and template settled once; check page limits on the built PDF.
  check: auto (PDF page count against the venue limit; template diff against the official-format file)
  when: before a send
  source: 4 times · 261113 MISQ "is this the real MISQ template one?" ; 261104 MISQ "我觉得这个东西我们早就做过了 为什么现在把模板给我变了" ; 261113 MISQ "For both word and pdf, they are the same requiremnts of 55 pages?"
  in skill now: hai-paper-assemble § A venue's format is settled once; § The venue template checklist

M-C10 · Answer story and plan questions with a proposal first; change Structure and Draft together.
  check: read (no edits or rebuilds in the turn a story question is asked; § 1 and § 3 agree)
  when: before JL sees a Section
  source: 4 times · 261024 MISQ "等一下，我们先考虑好然后再改" ; 261021 LLMRec "你是一改就把所有的都改完了吗？" ; 261102 WellDoc "please update the structure as well, did you update it?"
  in skill now: hai-paper-draft § Examples first (the Plan gate and sign)

M-C11 · Make co-author fixes as tracked changes; leave a comment only when no edit can answer.
  check: auto (count `comment:` entries without `new:` in edits.yaml; each needs a reason)
  when: before a send
  source: 3 times · 261113 MISQ "for the comments here, why you don't fix them?" ; 261113 MISQ "only leave the comments when you must hve to." ; 261113 MISQ "no need to leave the comments."
  in skill now: conflicts: word-track-change § Steps (3) says a co-author's own sentence gets a comment only

M-C12 · Render the output and review your own changes on it before JL looks.
  check: read (fresh reader on the rendered PDF or Word; each change found where expected)
  when: before JL sees a Section
  source: 3 times · 261113 MISQ "I didn;t see it is changed. why you don't review it yourelelf?" ; 261104 "please work until you update this ready, I will just read this." ; 260928 MISQ cold read of the built PDF (no JL quote)
  in skill now: hai-paper-assemble § The final read

M-C13 · Treat a ✓ checked or approved sentence as final: no reviewer score, notes or proposals.
  check: auto (✓ sentences with open cards or reviewer notes; ✓ on changed words shows ✓?)
  when: before JL sees a Section
  source: 3 times · 261114 MISQ "I check this, why???" ; 261114 MISQ "If I checked, no more comments or edit propossal" ; 261113 MISQ "this sentences passed my judgment, and you can fix that, no need to modify it"
  in skill now: no (workbench code only)

M-C14 · Offer 2 to 4 options (A, B, C) for structure or wording choices; JL's named words win.
  check: read (choice cards carry options; JL's exact wording used when he gives it)
  when: before JL sees a Section
  source: 3 times · 261022 ScalingGlucose "永远把 propose 这个方法放到首位" ; 261021 LLMRec "可以用 A、B、C 几个不同的方法去修改，propose 一些选项" ; 261114 MISQ "what if the two suggestions are not the same?"
  in skill now: partly: hai-draft-writing ref/revise.md (small edit as Option A, larger as Option B)

M-C15 · Rescore a sentence whenever its words change.
  check: auto (★ score older than the sentence text is stale)
  when: before JL sees a Section
  source: 2 times · 261114 MISQ "I think for the AI rating we should have one for re-eval, right?" ; 261114 MISQ "the AI rating is still the old version"
  in skill now: no

M-C16 · Report prose changes sentence by sentence by UI address, before and after; no bookkeeping.
  check: auto (no quoted paragraph block in a prose reply; each line starts with a `C<n>.P<m>` or `S<n>` address)
  when: before JL sees a Section
  source: 2 times · 261113 MISQ "Make it the same to the index in the UI, setnence by sentences" ; 260928 MISQ "why you make things so complicated? I am confused."
  in skill now: hai-paper-draft § Showing prose changes in a reply

M-C17 · Read 3 to 4 same-type papers from the target journal, as screenshots, before writing.
  check: auto (`page.py health --final` row `0 · Examples`; `paper_check.py` W6; papers from the target venue only)
  when: before JL sees a Section
  source: 2 times · 261104 "This is a must to do when you call the task for the /hai-paper-draft" ; 261022 ScalingGlucose "MUST NMI"
  in skill now: hai-paper-draft § Examples first: a must

M-C18 · Move a draft's version number only on JL's OK; edit the current version in place.
  check: auto (no new `-draft-v<N+1>.md` without a recorded ok)
  when: before JL sees a Section
  source: 2 times · 261020 LLMRec "until I feel it is ok, and we can upgrade it to v0.5" ; 261112 MISQ "If I say taht is okay, we can have a new version folder"
  in skill now: hai-draft SKILL.md (the bump is the person's ok)

M-C19 · Give every edit card its reason.
  check: auto (cards with an empty `Why:`; below 60% similarity needs a named defect)
  when: before JL sees a Section
  source: 2 times · 261114 MISQ "for each editing card, we might give some reasons as well." ; 261113 MISQ "you need to provide solid reason, otherwise, don't do it."
  in skill now: hai-draft-writing ref/revise.md § Small changes, or a solid reason

M-C20 · Run anti_slop.py audit and the readability check on any text you write, before showing it.
  check: auto (anti_slop.py audit and section-stats.py run on the current file; scores no worse than the original)
  when: before JL sees a Section
  source: 2 times · 260819 "you should actively call the hai-writing to make sure the things are good to read." ; 261110 MISQ rewrites scored worse and ran 9% longer (no JL quote)
  in skill now: hai-paper-draft § Co-authors' patterns (item 2)

M-C21 · Write a Section through /hai-draft: plan, sign, then prose; never free prose.
  check: auto (signed plan exists before § 3 sentences)
  when: before JL sees a Section
  source: 2 times · 261020 LLMRec "did you used the /hai-draft to draft each section" ; 260805 "the structure is not complete!!!"
  in skill now: hai-paper-draft § Examples first (the Plan gate)

M-C22 · Between a writing Run's start and end, change content only; records come at the end.
  check: auto (no log, receipt or results/ writes between the Run's start and end marks)
  when: before closing a Section
  source: 2 times (both 260928) · 260928 MISQ "don't change the log in the middle way, during the run"
  in skill now: hai-paper § Section sessions (two bookends)

M-C23 · Answer a comment inside the sentence it sits on, in JL's own terms.
  check: auto (card with `Answers: Comment <n>` targets the comment's own S<n>)
  when: before JL sees a Section
  source: 1 time · 261022 LLMRec "你这个完全没有按照我的要求来啊！"
  in skill now: hai-draft-writing ref/revise.md (Answers: Comment <n>)

M-C24 · Drop co-author comments that point at cut text or ask for nothing.
  check: read (each imported comment anchors to live text and asks something)
  when: before JL sees a Section
  source: 1 time · 261113 MISQ "things like this can be discarded."
  in skill now: no

M-C25 · Keep process text out of a delivered PDF or Word file.
  check: auto (grep text for DRAFT PAGE, NOT READY, not approved, pages ready, built 20xx, scores)
  when: before a send
  source: 1 time · 260908 JAMA "the dielvered pdf or word must be clean!!!!!"
  in skill now: hai-paper-assemble § Three behaviors every build must have; word-track-change § Rules

M-C26 · Hold a co-author round as a review Job, never in reports/.
  check: auto (no new `reports/qNN_coauthor-*` folder)
  when: before a send
  source: 1 time · 261110 MISQ "we will no long using the reports/ plesae use the job or studio"
  in skill now: hai-paper-draft § Co-authors' patterns (item 3); word-track-change § Rules

M-C27 · Keep what a Section must claim in its contract, not in its writing rules.
  check: read (writing rubric holds only size and shape rules)
  when: before JL sees a Section
  source: 1 time · 261113 MISQ "this is mode like the decisions to make, right?"
  in skill now: no

M-C28 · Never rerun evidence scripts when only sentence addresses move; update the ledger.
  check: auto (evidence Run reruns with unchanged inputs and cells)
  when: before closing a Section
  source: 1 time · 260928 MISQ "why update this? This waste a lot of resources."
  in skill now: no

M-C29 · Work evidence markdown-first; defer heavy display rebuilds and agent fan-out until asked.
  check: read (no compiled display rebuild or fan-out in a probe pass without an ask)
  when: before JL sees a Section
  source: 1 time · 260709 MISQ "make the probe with the markdown version first"
  in skill now: no

M-C30 · Bind a paper's existing Board session and Codex threads before creating new ones.
  check: auto (session index searched for the paper's names before `--apply`)
  when: before JL sees a Section
  source: 1 time · 260928 TimeEventDM "why we have 18 sessions?"
  in skill now: no

## D · Workbench / page UI (to AGENTS.md or workbench code)

- No check tallies or progress counts on pages or labels · 4
- No status words; marks and layout show state (incl. "Plan: waits for your sign") · 3
- No provenance tags such as "JL 261113" in page content · 2
- Pages minimal: content and controls only, calm colours, no alarming backgrounds or bars · 8
- The sentence is the unit: cards, comments and evidence sit on their sentence or heading · 7
- Draft Lab mark row at sentence end (📎 🕘 ✎ 💬 ✓), ✓ rightmost, 💬 shows and + adds · 9
- Reading typography: Literata, paper background, larger font, aligned numbers and cards · 7
- Paragraph and sentence numbers in reading order, restarting per paragraph, fixed id beneath · 4
- Fold fully ✓ paragraphs, paragraph level only; changed words show ✓? · 5
- The page never reloads or jumps by itself; it returns to the focal sentence · 4
- Each changed sentence shows who and when; history newest first · 3
- Word count and score live inside the ★ card; ★ toggles · 2
- "✓ Use this" writes the sentence; waiting cards show open · 3
- Views: Write and Revise merged as Draft Lab; Structure is the version's main view; extra views dropped · 8
- A display shows under the sentence citing it, only where it first prints, as its full float · 4
- Math is typeset in pages · 1
- Story by Section uses left tabs with the arc first; Displays sit in the design table · 5
- Delivery tabs grouped (LaTeX, Word, portal) with an Open in OneDrive button · 3
- Citation rows show title and abstract with preview links · 2
- Rule tabs list the real rules, one short point each · 4
- One list, the latest version only; one item per row; never a box in a box · 3
- Studio drawings are pictures that teach, not reports: hierarchy, rows, screen-sized frames, real data, fonts · 30
- Names read alone: stranger test, full folder names with ids, typed evidence ids (Ecite, Evalue), display unit names · 7
- Workbench code: files under 600 lines, split by responsibility, reviewed by a fresh subagent · 16

## E · General working style (to global CLAUDE.md)

- Answer first and at the size of the question; short replies · 6
- Reply in Chinese when asked; files, boards and paper text stay English · 6
- Decide it yourself; never end on "say go"; act on a short ask in context · 10
- Verify on the real thing before saying ready; wire green is not UI green · 4
- Explain and propose before changing code or a design; show the shape first · 5
- Use real file and field names; strip subagent vocabulary; full names, no guessed pronouns · 4
- Name a paper by its title first, then authors and year · 1
- Show requested things in the reply; links inside words; no unasked Artifacts, tabs or PDFs · 5
- No mannered prose; emails to colleagues are full, polite sentences · 2
- A rename or consistency fix sweeps every file · 1
- No sha256 hashes in pages, receipts or replies · 2
- Never hand-edit generated files; change the generator and rerun · 4
- Subagent fan-outs run on cheap models · 1
- Let JL press paid, long or shared Runs; run quick local ones yourself · 1
- One session per Project; a theme or Tools session stays in its own scope; work on main · 4
- Log times from the clock; one-line log rows · 2
- Shared spaces carry no personal information; no JL photo · 2
- Machine and server habits (venv, server restarts, remote shells, tickets) · 20

## Already encoded but still repeated

These rules were in a skill (or a memory) before JL had to say them again. They need a
gate that runs by itself, not more rule text.

1. M-A01 small changes: "surgical revision" was the top rule in hai-draft-writing by 260928; JL repeated it on 261113 (t05, t07, t01) and 261114 (t06).
2. M-A02 paragraphs of 4 to 7: in plain-rules.md § 3a (261104) and hai-paper-draft (261112); JL repeated it on 261113 13:17 and 13:21.
3. M-A03 one topic per sentence: in plain-rules.md § 3 on 261111; JL repeated it on 261113 13:34 ("did you check the writing patterns").
4. M-A06 co-author AI tells: in ai-tells.md § 5 on 261110; JL still found them on 261113 and asked if the patterns were checked.
5. M-A13 semicolons: said 261016 and recorded in plain-rules.md; JL said it again on 261104.
6. M-C01 blind sentence review: the independence rule and the 261021 memory existed; JL asked again on 261113 21:49, 261114 01:42 (t06) and for every Appendix sentence; readability scoring after each update was asked again on 261114.
7. M-C17 examples first: encoded 261022; JL had to call it "a must" on 261104.
8. M-C03 one session per Section: in hai-paper § Section sessions since 260928; JL repeated scope on 261113 (t02, t04, t05, main session).
9. M-B01 one number everywhere: chain_check.py existed from 261110; JL caught the count mismatches by eye on 261113 and 261114, because the check does not read numbers typed in prose.
10. M-B03 name-year citations: a Physician memory held it on 261114; on 261115 in WellDoc JL said "I think we mentioned", and no skill held it. Per-folder memories do not travel.
11. M-C02 apply feedback everywhere: Adopt exists in hai-draft-writing, but accept writes only the draft; JL asked "is it updated?" about 16 times on 261113 and 261114.
12. M-C11 tracked changes, not comments: word-track-change (261111) tells a session to comment on a co-author's sentence; JL ruled the other way on 261113. This one is a rule conflict to fix in the skill, not only a missing gate.
13. M-C09 venue format: settled once in hai-paper-assemble since 261104; on 261113 JL had to ask whether the build used the real MISQ template, and page 1 was broken.
