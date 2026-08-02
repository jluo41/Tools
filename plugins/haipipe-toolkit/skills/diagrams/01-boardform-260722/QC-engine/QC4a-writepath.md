# The write path: one browser edit, one markdown mutation
state: 🔴 OPEN
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
                                  run below the sentence        (QC6 §9)
                                  discussion: end of the
                                  ## Discussion section
                                     │
                                     ▼
                               ④ write the whole file back  ──▶ last write
                                  no version check              wins, silently
```

```text
   ── where it actually fails, measured on this board 260731 ───────

   4908  prose sentences a write could address
      0  duplicated within their page      the "more than one" refusal is
                                           LATENT here, not a live problem
   2321  carry markdown decoration (47.3%) `edit_sentence` refuses EVERY one
                                           of them: half the board cannot be
                                           edited from the page at all
      2  implementations of the normalizer  _plain_sentence, and a private
                                           plain() inside add_sentence
      0  writes carry a version token       three sessions wrote this board
                                           today with nothing checking
```

## Content
### 1 · The rule that already exists, and the two halves it gets right
The addressing rule is a single exact match on normalized text, and its refusals are loud rather than silent.
`_sentence_line` returns an error string when it finds no match or several, and every caller surfaces that error in the page instead of writing somewhere approximate.
Refusing beats guessing, because a wrong anchor puts a comment under a sentence nobody was discussing and nothing ever flags it.

The insert point is the other half, and it is already correct.
A comment lands at the end of the `>` run below its sentence (`_apparatus_end`), and a discussion line lands at the end of the `## Discussion` section, so both are anchored to a structural boundary rather than to a byte offset.
That is `QC6` §9's law, written after a concurrent session spliced a `### 2 · The source` block into the middle of a sentence on `QB4`.

### 2 · What is actually broken
The normalizer is implemented twice.
`_plain_sentence` serves the comment and edit paths, and `add_sentence` carries its own private `plain()` with the same three substitutions copied out.
Two copies of one rule drift, and when they drift the same click will anchor on one endpoint and refuse on another.
The `QC8` split moved both copies into `live/write.py` unchanged, which is correct for a mechanical move and means this duplication is still open here.

The edit path refuses 47.3% of this board.
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
Its fuzzy layer is the `approx-string-match` library rather than the diff-match-patch described in their 2015 write-up, and an annotation that anchors nowhere is marked an orphan and shown in its own sidebar tab instead of disappearing.
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
The proposal is a fallback ladder for READS of the anchor, and a hard floor under WRITES.

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
Formatting is then never guessed at and never erased, the 47.3% refusal disappears, and the rule stays "the machine never rewrites markdown it did not understand".

## Items to Finish
### Finding the line
- [ ] 🔗 Collapse the two normalizers into one
      `_plain_sentence` and `add_sentence`'s private `plain()` are the same three substitutions written twice; one is the rule and the other is a copy waiting to drift.
- [ ] 🪜 Implement the level 2 anchor
      Carry `prefix` and `suffix` context on the write, in the `TextQuoteSelector` shape, so a repeated sentence stops being unaddressable before this board grows one.

### Writing safely
- [ ] ✂️ Give the edit box the source line
      Return the raw markdown for the matched line so an author edits the source, which ends the 47.3% refusal without ever flattening formatting.
- [ ] 🔒 Put a version token on every write
      Send the hash the page was built from and refuse on mismatch, the `If-Match` and `412` shape, so a concurrent write is reported rather than lost.
      iA's Markdown Annotations does the file-level version of this with a SHA-256 over the annotated range, which is the closest precedent for a format rather than a request.
- [ ] 🧪 Prove the refusals with a test
      A fixture page with a duplicated sentence, a decorated sentence, and a stale version, asserting that each is refused with its own message and that none of them writes anything.

## Where we are
The addressing rule works on this board today and has never written to the wrong line, which is worth saying plainly before changing anything.
What it lacks is a stated contract, a second level for the case it currently refuses, and any protection against a concurrent write.
The measurement above is the argument for ordering: the duplicate case is latent, so the edit refusal and the missing version token are the two that cost something today.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.

- [ ] 🪜 Ratify the ladder and its floor
      Levels 0 to 2 for finding a line, and no approximate matching in the write path ever, on the grounds that a wrong write is invisible while a wrong highlight is not.
      → CC's proposal: yes as drawn; it keeps today's behaviour as level 1 and only adds a level for the case that is refused today.
- [ ] ✂️ Rule how a decorated sentence gets edited
      A · the edit box carries the raw source line, which ends a refusal covering 47.3% of this board without the renderer ever guessing at markdown.
      B · keep refusing and send the author to the file, which is safe and leaves half the board uneditable from the page.
      C · flatten and accept the formatting loss, which is the only option that can destroy an author's work.
      → CC's proposal: A; it ends a refusal that covers 47.3% of this board without ever guessing at markdown, and C is the only option that can destroy an author's work.
- [ ] 🔒 Rule the concurrency token, and where it lives
      A write carries the version it read and is refused on mismatch; the question is whether that belongs here or with `QE4`'s lock.
      → CC's proposal: the token belongs here because it is part of the write's contract, and the lock stays on `QE4`; they compose, since a lock prevents a collision and a token detects the one that got through.
- [ ] 🏷 Decide whether markdown block identifiers are wanted at all
      Level 0 assumes a line can carry a stable `^id` in the Obsidian shape, which is Latin letters, numbers, and dashes appended to the line, and which no markdown standard defines.
      → CC's proposal: defer; levels 1 and 2 cover every case this board has, and an id is only worth its noise once a sentence needs to survive being reworded.

## Files
### Engines
- `../../board/haipipe-board/live/write.py`
  `_plain_sentence`, `_sentence_line`, and `_apparatus_end` are the rule; `add_comment`, `edit_sentence`, `add_sentence`, and `add_discuss` are its four callers.
  They lived in `cli/serve.py` when this face was opened and moved here the same afternoon under `QC8`'s split, which changed no behaviour.
- `../../board/haipipe-board/assets/js/10-drawer/10-comment-dock.js`
  `findAndWrap` holds the approximate fallback that this face rules acceptable for highlights and forbidden for writes.

### The faces this contract borders
- `QC6-subskills.md`
  §9 is the section-boundary law this face's step ③ implements, and the incident that produced it.
- `QE-sharing/QE4-editlock.md`
  The lock around a page, which composes with the version token rather than replacing it.
- `QB-delivery/QB5b-comments.md`
  What a comment is, as opposed to how its line is found.

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
260801 0140 · Full renumber QC7a -> QC4a (JL forced 260801)
260801 0130 · Reindexed QC7 -> QC7a: the write path is now the return-half face of the QC7 round trip (JL 260801)
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · The four write functions this face documents moved from serve.py into live/write.py under QC8's split, verified behaviour-identical by a real comment write; Files and §2 repointed, and the unit-of-change proposal renumbered to QC9
260731 · §3 corrected against the sources after a research pass: Hypothesis uses approx-string-match rather than diff-match-patch, verifies structural hits against the stored quote, and calls a failed anchor an orphan; Obsidian's term is block identifier
260731 · Opened on JL's approval of the QA2 proposal, with the anchor rule measured on this board: 4908 addressable sentences, 0 duplicates, 2321 decorated and therefore uneditable, 2 copies of the normalizer, 0 version tokens
