# The write path: one browser edit, one markdown mutation
state: 🟡 PARTIAL · one Aim met silently, 3 rulings waiting on JL, remeasured 260802
owner: JL
method: name the addressing contract every write endpoint already shares, measure where it fails on this board, then rule the ladder and the version token

## Opening
How should a browser action find the exact Markdown line to change and refuse the write when certainty is lost?

A wrong anchor can place a comment or edit under a sentence nobody selected.
Rendered text also hides Markdown formatting, and concurrent sessions can make an apparently valid target stale.
This contract protects every comment, edit, and future sentence-level write that returns to the source file.
It succeeds when one shared matcher handles decorated and repeated text and rejects stale writes without mutation.


## Diagram

```text
   ── one click, from browser to markdown ──────────────────────────

   browser                     serve.py                      the .md
   ────────────────────────    ─────────────────────────     ──────────────
   visible sentence text   ──▶ ① normalize                   4908 prose
   (textContent, no md)        strip ` ` ** ** [ ]( )        lines are
                               collapse whitespace           addressable
                                     │
                                     ▼
                               ② scan for an exact match
                                  0 hits  -> refuse, visibly
                                  2+ hits -> refuse, visibly
                                  1 hit   -> that is the line
                                     │
                                     ▼
                               ③ walk to the insert point   ◀── never a
                                  comment: end of the `>`       byte offset
                                  run below the sentence        (QC1b §4.2)
                                  discussion: end of the
                                  ## Discussion section
                                     │
                                     ▼
                               ④ write the whole file back  ──▶ last write
                                  no version check              wins, silently
```

```text
   ── where it fails · measured 260731, REMEASURED 260802 ──────────

              260731    260802
   lines       4908      7752   prose lines a write could address
                                the board grew 58% in two days
   duplicated     0         0   the "more than one" refusal is still
                                LATENT here, not a live problem
   decorated   2321      3474   `edit_sentence` refuses EVERY one of them
              47.3%     44.8%   the share barely moved: still ~half the
                                board cannot be edited from the page
   normalizers    2         1   ✅ FIXED, and nobody wrote it back.
                                `add_sentence`'s private plain() is gone;
                                one `_plain_sentence` serves every caller
   version        0         0   no If-Match, no ETag, no 412, no hash
   tokens                       anywhere in live/write.py
```

```text
   ── what changed AROUND this face on 260802, after it was written ─

   ✍️ a THIRD writer is coming. haipipe-board-routing 0.9.0 names as its
      next step: "the write path moves behind serve.py's anchored-append
      endpoint, so a routed write and a clicked comment share one code
      path." This face's title says ONE BROWSER EDIT. That scope is now
      too narrow: an agent's routed write wants the same anchor contract.

   ✒️ the law is now RESTATED in a shipped skill. haipipe-sentence
      0.3.0 carries "the anchor is an EXACT match on the source line; a
      miss FAILS VISIBLY" and "a write needs serve.py" under its own
      heading. That is this face's rule, written a second time, which is
      the duplication disease that cost the family two days on QC1b.

   🈶 the refusal a reader actually meets is in CHINESE.
      edit_sentence returns 这句话带有 Markdown 格式；为避免丢格式，请先在
      源文件编辑, the one message 44.8% of this board's sentences produce,
      on boards JL ruled English-only on 260724.
```

## Content
### 1 · The rule that already exists, and the two halves it gets right
The addressing rule is a single exact match on normalized text, and its refusals are loud rather than silent.
`_sentence_line` returns an error string when it finds no match or several, and every caller surfaces that error in the page instead of writing somewhere approximate.
Refusing beats guessing, because a wrong anchor puts a comment under a sentence nobody was discussing and nothing ever flags it.

The insert point is the other half, and it is already correct.
A comment lands at the end of the `>` run below its sentence (`_apparatus_end`), and a discussion line lands at the end of the `## Discussion` section, so both are anchored to a structural boundary rather than to a byte offset.
That is `QC1b` §4.2's law, written after a concurrent session spliced a `### 2 · The source` block into the middle of a sentence on `QB4d`.

### 2 · What is actually broken
The normalizer was implemented twice, and that defect is now closed.
`add_sentence` carried its own private `plain()` with the same three substitutions copied out, and the `QC2c` split moved both copies into `live/write.py` unchanged.
Two copies of one rule drift, and when they drift the same click will anchor on one endpoint and refuse on another.
The private copy is gone: one `_plain_sentence` serves every caller, verified against `live/write.py` on 260806, so the two defects still live below are the decoration refusal and the missing version token.

The edit path refuses 44.8% of this board, 3474 of its 7752 addressable lines at the 260802 remeasure.
`edit_sentence` finds the line by normalized match, then insists the raw source equals the browser's text before it will write, so any sentence containing code, bold, or a link is rejected with a message telling the author to open the file by hand.
The intent is right, since replacing a decorated sentence with its flattened text would erase the formatting.
The mechanism is wrong, because it protects the file by refusing half the board rather than by handing the author the real source line.

No write carries a version.
Each endpoint reads the file, mutates a list of lines, and writes the whole file back, so a write that started before a concurrent write finished silently discards it.
`HOLD` exists but guards the drawer and the terminal, not the write path.

### 3 · What the standards and the production systems actually do
The W3C Web Annotation Data Model, a Recommendation since 2017, is the specification for this exact problem.
Its `TextQuoteSelector` carries `exact` plus a `prefix` and a `suffix` of surrounding context, which is precisely what disambiguates a repeated sentence, and its `TextPositionSelector` carries `start` and `end` character offsets, which is precisely what this board already refuses to trust.
The specification sets no length for the context, and Hypothesis in practice stores 32 characters on each side.

Hypothesis is the largest production answer, and two details of its behaviour matter more here than the ladder itself.
It tries `RangeAnchor`, then `TextPositionAnchor`, then the fuzzy `TextQuoteAnchor`, but a structural hit is only accepted after the text it lands on is compared against the stored quote, and a mismatch throws and falls through rather than winning.
Its quote matcher then scans for an exact hit first and only runs approximate search when there is none, which is the same order this face proposes.
Its fuzzy layer is the `approx-string-match` library rather than the diff-match-patch described in their 2015 write-up, and an annotation that anchors nowhere is marked an orphan and shown in its own page list tab instead of disappearing.
A published study of their corpus found 27% of annotations already orphaned and 61% at risk, which is the number to keep in mind before trusting any anchor to survive an edit.

Markdown has a native stable anchor as well, though not a standard one.
Obsidian's block identifier is a `^id` of Latin letters, numbers, and dashes appended to the end of a line, linked as `[[file#^id]]`, and it survives rewording completely because the id rather than the text is the identity.
Logseq and Roam have equivalents and none of the three is CommonMark, so an id is a local convention rather than a portable one.

The plain-text alternative is to put the annotation IN the text instead of anchoring to it.
CriticMarkup does this with `{==highlighted text==}{>>the comment<<}`, so the markup is its own anchor and nothing can drift.
This board already uses that idea at line granularity, since a `> WHO:` row sits adjacent to its sentence in the source, and the open question is only whether it is ever needed at span granularity inside a line.

For the lost update, the standard answer is HTTP's own.
The server returns a strong `ETag`, the client sends it back as `If-Match`, and RFC 9110 says the server MUST answer `412 Precondition Failed` when it no longer matches; RFC 6585's `428 Precondition Required` is the companion for refusing a write that carries no precondition at all.
A retried POST is made safe with an `Idempotency-Key`, which is Stripe's long-standing pattern and has been an IETF draft since 2025, where a repeat of the same key returns the first result and a reuse with a different payload is an error rather than a second write.
iA's Markdown Annotations format is the closest precedent for a file rather than a request, and it stores a SHA-256 over the annotated range so that the annotation invalidates itself when the text drifts.

Conflict-free replicated data types are the answer one tier up, and the reason they do not apply here is scope rather than capability.
Yjs and Automerge both ship a stable-position primitive that names comment anchoring as its use case, but the position lives inside a document stored and synced as a CRDT.
These pages are plain files on disk edited by people, by agents, and by hand, so there is no CRDT holding the position and the anchor falls back to quote or hash matching regardless, which is what `QE4` already says when it rules against reaching for one first.

### 4 · The ladder this board should adopt
**The anchor ladder**: how a written line is found, level by level.
```text
   level   how the line is found                      when it is used
   ─────   ────────────────────────────────────────   ────────────────────
   0       an explicit `^id` on the line              once ids exist
   1       exact match on normalized text             today's rule, kept
   2       normalized text + prefix and suffix        only when level 1
           context, the TextQuoteSelector shape       finds several
   ─────   ────────────────────────────────────────   ────────────────────
   none    approximate or fuzzy matching              FORBIDDEN for writes
```
The proposal is a fallback ladder for READS of the anchor, and a hard floor under WRITES.


Fuzzy matching is right for the highlight layer and wrong for the write layer, and the difference is what a mistake costs.
`board.js` already falls back to the first twelve characters when it re-finds a quote to highlight, and a wrong highlight is visible and harmless.
A wrong write mutates a file that nobody re-reads, so the write layer stops at level 2 and fails visibly instead.
Hypothesis can afford four levels because it is drawing on a page; this board is editing the source, and the 27% orphan rate is what tolerance looks like from the other side.

A line number is absent from that ladder deliberately, and the reason generalizes.
An anchor whose position is INCIDENTAL, such as an offset, an XPath, or a line number, must be verified against the text it lands on before it is trusted, which is exactly what Hypothesis does when it compares a structural hit against the stored quote and falls through on mismatch.
An anchor whose identity is INTENTIONAL, such as a block identifier someone wrote, is trusted without that check, because surviving a rewording is the whole reason it exists.
Levels 1 and 2 are text, so they verify themselves.

### 5 · Ending the decoration refusal
The edit box should carry the SOURCE line rather than the rendered text.
The server already knows the line, since it just found it, so the response that opens the editor can return the raw markdown for the author to edit directly.
Formatting is then never guessed at and never erased, the 44.8% refusal disappears, and the rule stays "the machine never rewrites markdown it did not understand".

## Aims
### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🪜 Ratify the ladder and its floor
      Levels 0 to 2 for finding a line, and no approximate matching in the write path ever, on the grounds that a wrong write is invisible while a wrong highlight is not.
      → CC's proposal: yes as drawn; it keeps today's behaviour as level 1 and only adds a level for the case that is refused today.
- [x] ✂️ Rule how a decorated sentence gets edited
      MOVED to `QB8`'s Decision Now on 260802, at JL's direction: "I think it should be the QB8 question, right?"
      He is right. `QB8` `### 8` claims "the sentence, and everything written onto it · §6 the edit", so what an author experiences when editing one sentence is that page's, and this face owns only how any write FINDS its line and refuses safely.
      It was written here because CC was measuring `live/write.py` and anchored the ruling to the file it was reading rather than to the page that owns the gesture, which is what routing's step 3 forbids.
- [ ] 🔒 Rule the concurrency token, and where it lives
      A write carries the version it read and is refused on mismatch; the question is whether that belongs here or with `QE4`'s lock.
      → CC's proposal: the token belongs here because it is part of the write's contract, and the lock stays on `QE4`; they compose, since a lock prevents a collision and a token detects the one that got through.
- [ ] 🏷 Decide whether markdown block identifiers are wanted at all
      Level 0 assumes a line can carry a stable `^id` in the Obsidian shape, which is Latin letters, numbers, and dashes appended to the line, and which no markdown standard defines.
      → CC's proposal: defer; levels 1 and 2 cover every case this board has, and an id is only worth its noise once a sentence needs to survive being reworded.


### Finding the line
- [x] 🔗 Collapse the two normalizers into one
      Met, and met SILENTLY: `grep -rn "def plain("` across `live/`, `cli/` and `src/` now returns nothing, and every caller goes through the single `_plain_sentence`.
      Nobody wrote it back, so this page claimed an open defect that had already been fixed, which is the "stale pretty thing" the sync verb exists to prevent.
      Remeasured 260802.
- [ ] 🈶 The refusal a reader meets is in English
      (kept here rather than on `QB8`: the STRING is emitted by `live/write.py`, which this face owns, while WHETHER the refusal should exist at all is `QB8`'s)
      `edit_sentence` returns `这句话带有 Markdown 格式；为避免丢格式，请先在源文件编辑`, and it is the single most-produced message in the write path because 44.8% of this board's lines trigger it.
      JL ruled boards and artifacts English-only on 260724; a UI string a reader hits daily is squarely inside that rule.
      It is one line and it is not the same work as the fix below, which is why it is its own row: even if the refusal stays, it should be readable.
- [ ] 🪜 Implement the level 2 anchor
      Carry `prefix` and `suffix` context on the write, in the `TextQuoteSelector` shape, so a repeated sentence stops being unaddressable before this board grows one.

### Writing safely
- [ ] ✂️ Give the edit box the source line
      Return the raw markdown for the matched line so an author edits the source, which ends the 44.8% refusal without ever flattening formatting.
- [ ] 🔒 Put a version token on every write
      Send the hash the page was built from and refuse on mismatch, the `If-Match` and `412` shape, so a concurrent write is reported rather than lost.
      iA's Markdown Annotations does the file-level version of this with a SHA-256 over the annotated range, which is the closest precedent for a format rather than a request.
- [ ] 🌐 Widen the contract past the browser
      This face is titled "one browser edit" and `haipipe-board-routing` (0.9.1 today) still names moving the write path behind one anchored-append endpoint so a routed agent write and a clicked comment share it.
      An agent write has no rendered `textContent` to normalize, so it enters the ladder at a different rung, and nothing states which.
- [ ] 🔁 Take the law back from `haipipe-sentence`
      That skill's 0.3.1 still restates "the anchor is an EXACT match on the source line; a miss FAILS VISIBLY" and "a write needs serve.py" in its own words.
      This face owns the rule, so the skill should cite it rather than carry a second copy, which is the same defect `QC1b` spent two days finding in the index.
- [ ] 🧪 Prove the refusals with a test
      A fixture page with a duplicated sentence, a decorated sentence, and a stale version, asserting that each is refused with its own message and that none of them writes anything.

## Discussion

### From the retired States section (merged 260831)
The addressing rule works on this board today and has never written to the wrong line, which is worth saying plainly before changing anything.
What it lacks is a stated contract, a second level for the case it currently refuses, and any protection against a concurrent write.
The measurement above is the argument for ordering: the duplicate case is latent, so the edit refusal and the missing version token are the two that cost something today.
Remeasured on 260802, two days after the figures this page was opened with, and three things moved.
The normalizer duplication is FIXED and this page did not know, which is the reverse of the usual staleness and the more embarrassing direction.
The edit refusal did not improve: the board grew 58% to 7752 addressable lines and the decorated share only fell from 47.3% to 44.8%, so the absolute count of uneditable sentences rose from 2321 to 3474.
And the face's own scope aged, because `haipipe-board-routing` 0.9.0 now wants to send agent writes down this same path while the title still says one browser edit.
- 260802 CC · ✅ An Aim was met and nobody claimed it
  The private `plain()` inside `add_sentence` is gone and one `_plain_sentence` serves every caller.
  It most likely went during the `QC2c` live-layer split, which this page records as having moved both copies unchanged, so either that record or the code was wrong for two days and no check compares them.
  This is the failure mode `check.py`'s `open-with-met-aims` was written for, and it cannot see a defect stated only in prose.
- 260802 CC · 🈶 The most-produced message in the write path is in Chinese
  44.8% of this board's addressable lines produce it, and `haipipe-board`'s own assets carry several more Chinese docstrings and comments from the same period.
  Only the user-facing refusal is proposed as an Aim here; the internal comments are a different sweep and belong to whoever owns `live/`.
- 260802 CC · 🌐 A second consumer arrived before the contract was ratified
  `haipipe-board-routing` absorbed the board altitude and named the shared endpoint as its next step, and `cli/sentencerun.py` already calls `_sentence_line` outside the browser path.
  So the four rulings below are now blocking two consumers rather than one, which raises what they cost to leave open.

## Files
### Engines
- `../../board/haipipe-board/live/write.py`
  `_plain_sentence`, `_sentence_line`, and `_apparatus_end` are the rule; `add_comment`, `edit_sentence`, `add_sentence`, and `add_discuss` are its four callers.
  They lived in `cli/serve.py` when this face was opened and moved here the same afternoon under `QC2c`'s split, which changed no behaviour.
- `../../board/haipipe-board/assets/js/10-drawer/10-comment/00-highlight.js`
  `findAndWrap` holds the approximate fallback that this face rules acceptable for highlights and forbidden for writes.

### The faces this contract borders
- `6-QS-sentence/QS1-overview/QS1-overview.md`
  `### 6` owns the edit as an author meets it, and `### 8` claims "everything written onto" a sentence. The decorated-sentence ruling moved there on 260802. This face owns the addressing mechanism every writer shares, not any one writer's gesture.
- `1-QA-constitution/QA6-skillfamily/QA6-skillfamily.md`
  §4.2 is the section-boundary law this face's step ③ implements, and the incident that produced it.
- `8-QO-operating/QO7-editlock/QO7-editlock.md`
  The lock around a page, which composes with the version token rather than replacing it.

## Glossary
The sources behind §3, so every claim there is checkable.
- W3C Web Annotation Data Model, Recommendation 2017: https://www.w3.org/TR/annotation-model/#selectors
- Hypothesis anchoring, current client: https://github.com/hypothesis/client/blob/main/src/annotator/anchoring/match-quote.ts
- The orphan study, 27% orphaned and 61% at risk: https://arxiv.org/abs/1512.06195
- Obsidian block identifiers: https://obsidian.md/help/links
- CriticMarkup: https://fletcher.github.io/MultiMarkdown-6/syntax/critic.html
- RFC 9110 on If-Match and 412: https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match
- iA Markdown Annotations, the SHA-256 over the annotated range: https://github.com/iainc/Markdown-Annotations

## Log
- 260806 2135 · [REVISE-CC] swept to the 260806 architecture; retired ids repointed (`QC6` §9 -> `QC1b` §4.2, `QC8` -> `QC2c`), §2 stopped claiming the fixed normalizer duplication as open, live figures moved to the 260802 remeasure (44.8%), `findAndWrap` repointed to `10-drawer/10-comment/00-highlight.js`, sentence/routing versions verified at 0.3.1/0.9.1, state line's ruling count corrected to 3
260802 2200 · The decorated-sentence ruling moved to `QB8`, its real owner (JL: "I think it should be the QB8 question, right?"). It had been written here because CC anchored to `live/write.py` rather than to the page owning the gesture. What stays here is the shared mechanism: the normalizer, the ladder, the version token, and widening past the browser; what left is one writer's reader-facing behaviour
260802 2130 · Remeasured against disk and the numbers all moved: 4908 to 7752 addressable lines, decorated 47.3% to 44.8% but 2321 to 3474 in absolute count, and the two normalizers are now ONE, so that Aim was met silently and is ticked. Three new Aims: the Chinese refusal message, widening the contract past the browser now that routing wants the same endpoint, and taking the law back from `haipipe-sentence` 0.3.0 which restates it. `state:` 🔴 to 🟡 PARTIAL
260801 0140 · Full renumber QC7a -> QC4a (JL forced 260801)
260801 0130 · Reindexed QC7 -> QC7a: the write path is now the return-half face of the QC7 round trip (JL 260801)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The four write functions this face documents moved from serve.py into live/write.py under QC8's split, verified behaviour-identical by a real comment write; Files and §2 repointed, and the unit-of-change proposal renumbered to QC9
260731 · §3 corrected against the sources after a research pass: Hypothesis uses approx-string-match rather than diff-match-patch, verifies structural hits against the stored quote, and calls a failed anchor an orphan; Obsidian's term is block identifier
260731 · Opened on JL's approval of the QA2 proposal, with the anchor rule measured on this board: 4908 addressable sentences, 0 duplicates, 2321 decorated and therefore uneditable, 2 copies of the normalizer, 0 version tokens

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0