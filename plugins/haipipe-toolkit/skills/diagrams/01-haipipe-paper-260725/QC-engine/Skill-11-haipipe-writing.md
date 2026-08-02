# haipipe-writing · v0.6.0
state: 🟡 PARTIAL
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
haipipe-writing is a shipped unit: what does it still owe, and is it healthy?

This is the roster page for `⑪`, the prose verb, and it is the first roster row on this board for a family whose design record is this board rather than one of its own.
The unit takes prose somebody already wrote and rewrites it so a reader whose English is weak can follow it, then records each edit as a word-level `✎` line under the sentence that changed.
It exists on its own rather than inside `paper/` because its test does not care what file the prose is in: the same pass serves a board page, a manuscript section, and a README, and every rule in it was ruled while rewriting one of this board's own pages.
It would be finished when a caller can run score, rewrite, apply and check end to end without a person placing anything by hand, and when the paper humanizer draws its diffs from `cli/wdiff.py` instead of writing them itself.
`QA10` is where the layer is argued; this page only records what ships and whether it is well.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start ea4202a825457260 writing/haipipe-writing -->

```
haipipe-writing/
  cli/
    agree.py            176 ln  Two statements of one fact, compared. Read-only.
    holes.py             95 ln  Audit the holes in a document: unowned placeholders, and dangling owners.
    score.py            113 ln  Find the prose most likely to fail the weak-English test. Read-only.
    wdiff.py            194 ln  Word-level change records, computed rather than written.
  ref/
    ai-tells.md          55 ln  AI tells: the general catalogue
    change-record.md    113 ln  The change record: `✎`
    holes.md             90 ln  The hole discipline: what to do about what you do not know
    plain-rules.md       91 ln  The plain-English rules, and the ruling behind each one
    weaving.md           59 ln  Weaving: the paragraph-flow pass
  tests/
    test_roundtrip.py    94 ln  What `apply` writes, `check` must accept. Run: python3 tests/test_roundtrip.py
  CHANGELOG.md          164 ln  haipipe-writing
  SKILL.md              173 ln  /haipipe-writing · rewrite prose, and leave a trail
```

<!-- haipipe:skill:tree:end -->

```
WORKFLOW  ── who calls it, and where the judgment sits

  any authored prose in the repo          a board page · a section · a README
        │                                  the host does not change the test
        ▼
  1  score.py        CODE      ranks what is worth rewriting.  READ-ONLY
        ▼
  2  rewrite         JUDGMENT  the ONLY step a model does
        ▼
  3  wdiff.py apply  CODE      computes the diff, anchors the record by POSITION
        ▼
  4  wdiff.py check  CODE      every record well-formed and anchored

  hands off to:
    board/haipipe-board-sentence   owns the lane contract the ✎ record lives in.
                                   This skill owns ONE lane out of ten.
    haipipe-paper-revise           CALLS wdiff.py --host paper. VERIFIED 260802.
    haipipe-paper-revise-humanizer CALLS wdiff.py --host paper. VERIFIED 260802.
                                   Neither keeps a diff of its own, and since
                                   0.5.0 neither converts the marks by hand.
```

## Content
<!-- haipipe:skill:body:start ea4202a825457260 writing/haipipe-writing -->

**haipipe-writing** · `0.6.0` · last shipped 2026-08-02

- folder   `writing/haipipe-writing/`
- tools    not declared
- summary  cli/agree.py compares two statements of one fact, because the three defects of 260802 were all that shape; tests/test_roundtrip.py locks in the apply-versus-check repair, which no grep could have seen.

### SKILL.md




Prose in this repo is written by someone who already knows the subject.
That is the problem this skill exists for: the author cannot see their own jargon, and a long sentence reads as precise to the person who built it.
So the reader who pays is the one who knows least, and nobody in the room is that reader.

**What this skill is FOR**: rewriting authored prose so a person whose English is weak can follow it, and recording each edit next to the sentence it changed.


- 1 · 🧭 1 · What it does, in one picture
      **The loop**: three verbs, and only the middle one needs judgment.
      ```
      📄 authored prose
            |
            | 1️⃣ score.py         🤖 CODE · ranks what is worth rewriting
            v
      📋 a ranked worklist ── a person reads it, nothing has changed yet
            |
            | 2️⃣ rewrite          🧠 JUDGMENT · the only step a model does
            v
      ✍️ new prose + old prose
            |
            | 3️⃣ wdiff.py apply   🤖 CODE · computes the diff, anchors the record
            v
      📝 prose + ✎ record under the sentence it changed
            |
            | 4️⃣ wdiff.py check   🤖 CODE · every record well-formed and anchored
            v
      ✅ readable, and reviewable
      ```
      🔒 the JUDGMENT is step 2, and ONLY step 2
      🚫 a model never writes the diff and never places the record

- 2 · ⚖️ 2 · Why the diff is code
      **The three mistakes**: each was made twice in one evening, by an author who knew the rule.
      ```
      ❌ record appended at the end of a block   ──▶ attaches to the WRONG sentence
      ❌ diff written as one whole sentence      ──▶ shows nothing that survived
      ❌ heading names the MECHANISM             ──▶ reads as jargon

      ✅ wdiff.py apply    anchors under the FIRST new line, by position
      ✅ difflib           marks only the words that moved
      ✅ score.py          flags a heading before anyone reads it
      ```
      This is the whole design argument.
      A model asked to "show the diff" writes a whole-sentence swap, because that is what a diff feels like from the inside.
      It also appends the record wherever it finished writing, which quietly attaches it to a sentence it does not describe.
      Both happened on `QB4` on 260801, twice each.
      So neither is left to judgment: `cli/wdiff.py` computes the diff with `difflib` and inserts the record by position.

- 3 · 📐 3 · The rules it applies
      They are not invented here. They were ruled by JL while rewriting `QB4` and they live in full in `ref/plain-rules.md`; this is the short form.
      **The test**: can a reader who does not read English well follow this? That is harder than "is it correct", and it is the one that catches what correctness misses.
      - A shorter common word always beats a precise rare one. ✅ `settles a decision` ❌ `argues one choice to a close`
      - A heading names its CONSEQUENCE, not its mechanism. ✅ `A blank line decides what people see` ❌ `The opening paragraph ends at the first blank line`
      - One idea per sentence. A sentence past about 30 words is usually two.
      - A word this repo invented is explained where it is used, or it is not used.
      - A good/bad pair gets its own line, marked ✅ and ❌, never buried in a sentence.

- 4 · 🧾 4 · The change record
      **The grammar**: one line, under the sentence it changed. `ref/change-record.md` is the full contract.
      ```
      > ✎ ~removed words~ *added words* · WHO · YYMMDD HHMM

        ~old~     renders struck through      *new*   renders inserted
        plain     words that SURVIVED         ← the reason this is word-level
      ```
      ⚑ it anchors to the SENTENCE its lane run sits under, not to the line directly
         above, because a record joins the END of a run that may already hold lanes
      🔀 a rewrite that splits one sentence into three anchors on the FIRST
      **Two hosts, one computation** (`--host`, 0.5.0): same difflib opcodes, two notations.
      ```
      --host board   (default)  > ✎ ~old~ *new* · WHO · YYMMDD HHMM
      --host paper              > Note: ~~old~~ **new** · WHO · WHEN
      ```
      🚫 the caller never converts the marks by hand. That was the arrangement until
         0.5.0, and it put a hand step inside the one tool built because this exact
         class of hand step gets done wrong.

- 5 · 📎 5 · Files

- 5.1 · Engines
      - `cli/wdiff.py`
        Computes the word-level diff and anchors the record. `record`, `apply`, `check`.
      - `cli/score.py`
        Ranks prose against the weak-English test. Read-only, and it never rewrites.
      - `cli/holes.py`
        Audits placeholders both ways: unowned holes, and holes pointing at an owner that does not exist. Read-only.
      - `cli/agree.py`
        Two statements of one fact, compared: a skill's declared version against its changelog, and every cross-skill path citation against what is on disk. Read-only.
        `python3 cli/agree.py --all --quiet <skills-root>`

- 5.2 · Contracts
      - `ref/plain-rules.md`
        The rules, with the ruling that produced each one.
      - `ref/change-record.md`
        The `✎` grammar, the anchoring law, and how a non-board host records a change.
      - `ref/ai-tells.md`
        How a machine writes, in any register. Migrated 260801 out of the paper humanizer's Layer 1, which no paper owned.
      - `ref/weaving.md`
        Paragraph-to-paragraph arc, hinges, and rhythm. Migrated 260801 out of `haipipe-paper-revise-content`, which still owns when the pass runs.
      - `ref/holes.md`
        What to do about what you do not know: never invent, every hole names an owner, sweep after writing. Migrated 260801 out of the paper DRAFT phase.

- 6 · 🔗 6 · It plugs into an apparatus that already exists
      A `>` line under a sentence belongs to that sentence. `board/haipipe-board-sentence`
      owns that contract, and `QB4 §3.3.3` names its three kinds: eight ⚑ typed lanes, a
      💬 comment, and the ✎ change record this skill writes.
      **This skill owns one lane out of ten, and none of the machinery around it.**
      The lanes, the evidence card, and the archive-and-restore lifecycle are not
      redefined here. Three of their rules bind it directly:
      - a lane is APPENDED, never edited in place
      - a signed `> WHO:` or `> ✎` line is NEVER erased; it is the durable review trail
      - a lane with no signature is not a lane
      `cli/wdiff.py apply` enforces all three. It appends to the end of the lane run,
      it refuses to rewrite a lane, and it refuses to write a result holding fewer `✎`
      lines than it started with.

- 7 · 🧪 7 · Checking it
      **Three checkers, three questions**: none of them rewrites anything.
      ```
      cli/wdiff.py check FILE     is every record well-formed and anchored?
      cli/holes.py       FILE     does every hole in ONE file have a real owner?
      cli/agree.py       DIR...   do TWO files stating one fact agree?
      tests/test_roundtrip.py     does what `apply` writes, `check` accept?
      ```
      `agree.py` exists because three defects surfaced on 260802 in one afternoon and all three were one shape: two halves of a contract, stating one fact, disagreeing, with nothing comparing them. It compares the two that are static, a declared version against its changelog and a cited path against the disk. The third was a round trip, which no grep can see, so it is a test instead.
      ⚠️ It is a FLOOR, not a proof. It checks the two disagreements that have actually bitten, and it stays quiet about path-shaped nouns a skill merely describes, such as `results/` or `1-probes/`, because a checker that cries wolf stops being read.

- 8 · 🚧 8 · What this does NOT own
      `haipipe-paper-revise-humanizer` rewrites ACADEMIC prose for a venue: it keeps scholarly precision, evidence-tied claims, and a journal's voice, and it writes `%%` comments into LaTeX.
      This skill has a different reader (someone whose English is weak) and a different host (any file).
      They share machinery. They do not share judgment.
      So the machinery moved here and the judgment stayed there (JL 260801).
      This skill now holds the general AI-tell catalogue and the weaving method.
      The humanizer calls `cli/wdiff.py` for its diffs instead of writing them by hand.
      What stayed in `paper/` is everything a venue owns.
      How loudly a paper may claim, how it cites, which gates a claim must pass, how a funding proposal sounds, and the `%%` comment grammar LaTeX needs.
      `ref/change-record.md` §3 is where the two host dialects are written down together, so they cannot drift into two ideas.
### The other files

10 files besides `SKILL.md` and `CHANGELOG.md`, each with the purpose it states about itself. They are described here, not reproduced: the folder is the copy.

```
cli/agree.py                176 ln  Two statements of one fact, compared. Read-only.
cli/holes.py                 95 ln  Audit the holes in a document: unowned placeholders, and dangling owners.
cli/score.py                113 ln  Find the prose most likely to fail the weak-English test. Read-only.
cli/wdiff.py                194 ln  Word-level change records, computed rather than written.
ref/ai-tells.md              55 ln  AI tells: the general catalogue
ref/change-record.md        113 ln  The change record: `✎`
ref/holes.md                 90 ln  The hole discipline: what to do about what you do not know
ref/plain-rules.md           91 ln  The plain-English rules, and the ruling behind each one
ref/weaving.md               59 ln  Weaving: the paragraph-flow pass
tests/test_roundtrip.py      94 ln  What `apply` writes, `check` must accept. Run: python3 tests/test_roundtrip.py
```

<!-- haipipe:skill:body:end -->

## Aims
### P · Page-level health ruling
- P1 · Rule this skill's health.
  **Done when:** `state:` records a human judgment: stable, in flux, needs work, or parked.
- P2 · Repair the declared version.
  **Done when:** `SKILL.md` frontmatter and `CHANGELOG.md` agree on one number.
- P3 · Verify the humanizer actually calls `cli/wdiff.py`.
  **Done when:** the call is read in `haipipe-paper-revise-humanizer`, or the claim is withdrawn.
- P4 · Keep the two citing skills agreeing on one path.
  **Done when:** something checks it, rather than a reader noticing.
- P5 · Rule whether `record` grows a host flag.
  **Done when:** the flag ships, or the hand conversion is ruled acceptable and `QA10` says so.
- P6 · `apply` and `check` agree about where a record may sit.
  **Done when:** a record written under a sentence that already carries a lane passes `check`.
- P7 · Something compares two statements of one fact.
  **Done when:** a checker catches the version and path shapes, and a test catches the round trip.
- P8 · The first sweep's findings are cleared, not just recorded.
  **Done when:** the 2 version disagreements and 57 path findings are each repaired or ruled acceptable.
- P9 · Something CALLS the checker.
  **Done when:** `agree.py` runs without a person remembering to run it.

## States
### P · Page-level health ruling
- 🔨 P1 · In flux, and honestly so: five releases in two days. The newest adds `--host` and repairs a contradiction between `apply` and `check` that had stood since the first release.
- ✅ P2 · Repaired 260802. Frontmatter had declared `0.1.0` / 2026-08-01 against a `CHANGELOG.md` that shipped `0.4.0` on 2026-08-02, so this page's derived header understated the unit by three releases. Frontmatter now reads `0.4.0` and its summary describes 0.4.0 rather than the first cut.
- ✅ P3 · Verified 260802, and it held. The call is wired in TWO instructions, `haipipe-paper-revise/SKILL.md:70` and `haipipe-paper-revise-humanizer/SKILL.md:94`, both a `SKILL.md` procedure rather than a changelog note, and `paper/` carries no second diff implementation. `record` was run against this board's own prose to confirm it works.
- 🔨 P4 · Found while verifying P3, repaired in the same pass. The humanizer cited `skills/writing/…`, which resolves from the plugin root and NOT from the repository root where a session starts, while its own hub already wrote `<skills>/writing/…`. It also omitted `--when`, which `record` requires. Both fixed. Nothing checks that two skills citing one path agree.
- ✅ P5 · Ruled and shipped 260802 as 0.5.0. `--host {board,paper}` emits both notations from one `difflib` computation, both paper callers pass `--host paper`, and an unknown host is refused rather than silently defaulted.
- ✅ P7 · Shipped 260802 as 0.6.0. `cli/agree.py` compares a declared version against its changelog and a cross-skill citation against the disk; `tests/test_roundtrip.py` covers the round trip, verified to FAIL against the pre-0.5.0 `check` so it locks the repair in. It got its own job wrong twice before it worked, and both are in the changelog.
- 🧠 P8 · Recorded, not cleared. The sweep over 152 folders returned 2 version disagreements and 57 path findings, one of which is this board's own stale id `QO-delivery-build/QC6-sentence-to-word.md`. Reporting is not repairing.
- 🔨 P9 · Nothing calls it. A checker a person has to remember to run has the same failure mode as the defects it catches.
- ✅ P6 · Repaired 260802, found while testing P5 and present since 0.1.0. `apply` appends a record to the END of the lane run while `check` demanded prose exactly one line above, so any sentence already carrying a `> Citation:` or `> Value:` lane produced a record this tool wrote and then rejected. `check` now walks the run back. The 31-record corpus stays at 0 problems and both negative cases still fail correctly.

## Log
260802 1130 · page generated from `writing/haipipe-writing/` by `skillpage.py new`, admitted under `QC1a`'s rule: it owns four contracts (`plain-rules`, `change-record`, `ai-tells`, `weaving`, `holes`) that were migrated OUT of the paper family and that no other skill may now decide.
260802 1615 · P7 built as 0.6.0: `cli/agree.py` plus `tests/test_roundtrip.py`. Two false starts kept in the changelog rather than tidied away, the second of which is the sharpest evidence the defect class is real: the checker written to catch two halves disagreeing shipped its first draft with a version comparator that missed the bracketed changelog heading, and flagged 35 of 152 folders that agreed perfectly.
260802 1530 · P5 ruled and built as 0.5.0, and P6 opened and closed with it: testing `--host paper` on a sentence that already had a lane exposed `apply` and `check` disagreeing since 0.1.0. Neither defect was visible from the validating corpus, whose 31 records all sit on sentences carrying no other lane.
260802 1400 · P2 and P3 both closed. The version drift was repaired at its source, and the humanizer call was verified rather than assumed: real, wired twice, no second implementation. The verification itself produced P4 and P5.
260802 1130 · Recorded the version drift as P2 rather than repairing it here. The number lives in the skill folder, and a board page that edits its subject to make its own header look right is the wrong direction of travel.

<!-- haipipe:skill:log:start ea4202a825457260 writing/haipipe-writing -->

Converted from the skill's own `CHANGELOG.md`: 6 releases.

260802 · `0.6.0`
      **`cli/agree.py`: two statements of one fact, compared** (JL 260802, from `QA10`
      aim 7). Three defects surfaced that afternoon and all three were one shape, two
      halves of a contract disagreeing with nothing that compares them: a path cited
      one way by a skill and another way by its own hub, a frontmatter version against
      its changelog, and `apply` writing a record `check` rejected. Each was found by a
      person looking. This checks the two that are static.
          version   SKILL.md frontmatter against the newest CHANGELOG.md heading
          path      every cross-skill citation against what is actually on disk,
                    reporting DEAD and, separately, "resolves only from the plugin
                    root", which is the humanizer's defect exactly
      **Two things it got wrong first, both worth recording.** The first sweep skipped
      fenced blocks, on the theory that a checker must not report its own examples.
      That made it blind to its own reason for existing: the instruction it was written
      to catch lives inside an untagged fence holding prose. Unlike a `\cite{TOADD}`
      marker, a path does not become an example by being quoted, so fences are no
      longer skipped.
      The second sweep then returned 1393 path findings, of which the common ones were
      `1-probes/`, `results/`, `QA/`, `runs/<RUN>.sh`: shapes a skill DESCRIBES, not
      files it cites. A path is now checked only when it points into the skills tree.
      152 folders, 57 path findings, 2 version disagreements.
      **And the version comparator was itself an instance of the bug it hunts.** Its
      regex missed `## [0.6.1] — …`, the bracketed Keep-a-Changelog form, so the scan
      fell through to the heading below and reported the wrong number: 35 of 152
      folders flagged, nearly all of them agreeing perfectly. Fixed, and left in the
      docstring, because the checker written to catch two-halves-disagreeing shipped
      its first draft with two halves disagreeing.
      **`tests/test_roundtrip.py`.** What `apply` writes, `check` must accept, over a
      bare sentence, a sentence with one lane, one with three lanes and a comment, one
      already carrying a signed record, and a paper-host call beside a board record. It
      also asserts the three things `check` must still reject. Verified to FAIL against
      the pre-0.5.0 `check`, so it locks the repair in rather than merely passing. A
      round trip is not a grep and `agree.py` could never have seen it.
260802 · `0.5.0`
      **The host is a flag, not an instruction** (JL 260802, from `QA10` aim 5).
      `record` and `apply` take `--host {board,paper}`. One `difflib` computation, two
      notations: `~old~ *new*` behind `> ✎` for a board, `~~old~~ **new**` behind
      `> Note:` for a paper.
      Until now it emitted the board notation only, and `haipipe-paper-revise/SKILL.md`
      told its caller to "double the tildes and turn `*new*` into `**inserted**` for
      this host". That is a hand step inside the one tool whose entire design argument
      is that this class of hand step gets done wrong. The computation was in one
      place and the OUTPUT was not, so the last transformation before marks reached a
      manuscript was performed by the reader the skill exists to protect. Both callers
      now pass `--host paper` and convert nothing.
      **`check` and `apply` had contradicted each other since 0.1.0, and it surfaced
      while testing the flag.** `apply` appends a record to the END of the sentence's
      lane run, which 0.4.0 made explicit and which `QB4`'s Law requires. `check`
      looked exactly one line up and demanded prose there. So every record written
      under a sentence that already carried a `> Citation:`, `> Value:` or any other
      lane was written correctly by one half of the tool and rejected by the other.
      Nothing had caught it because the corpus it was validated against,
      `QB4-overall.md`, happens to carry its 31 records on sentences with no other
      lane.
      `check` now walks the `>` run back to the sentence it hangs under. A record under
      no prose at all is still caught, and a malformed one still is: verified against
      both negative cases and against the 31-record corpus, which stays at 0 problems.
      **Two guards where there was one.** `apply` asserts that the host's own record
      count GREW by one, and separately that the count of signed `> ✎` lines never
      SHRANK. A paper-host call has no more right to destroy a board record than a
      board-host call does, and the single 0.4.0 guard could not express both.
260802 · `0.4.0`
      Aligned with the sentence apparatus, which 0.1.0 through 0.3.0 had ignored
      (JL: "how could you make haipipe-writing consistent with the evidence card and
      comments as well? Did you ever considered about it?"). No, it had not been.
      The gap was that `ref/change-record.md` described `✎` as a standalone grammar,
      creating a SECOND authority on something already owned by
      `board/haipipe-board-sentence` and specified in `QB4 §3.3.3`: eight ⚑ typed
      lanes, a 💬 comment, and the ✎ record, with a badge naming the kind.
      - `ref/change-record.md` rewritten to CITE the owning contract instead of
        restating it. It now carries only what is this skill's: how the diff is
        computed and where the record is placed.
      - `ref/holes.md` §4 rewritten. The "board dialect" had been invented; the real
        one is the typed lanes, and `QB4 §3.3.3` already states the one-to-one map
        `> Citation:` ←→ `\cite{TOADD}`, `> Value:` ←→ `{VAL:? …}`, `> Display:` ←→ a
        display id. That mapping is how the board reaches `/haipipe-paper`.
      - `cli/holes.py` board dialect rebuilt on the eight real lanes. A lane stating
        what it FOUND is no longer counted as a hole; `> Check:` and `> Q-consumer:`
        are holes by definition.
      - `cli/wdiff.py apply` now honours three lane rules it had been breaking:
        it APPENDS to the end of the sentence's lane run rather than splitting it,
        it REFUSES to rewrite a lane, and it REFUSES to write a result containing
        fewer `✎` lines than it started with.
      That last guard exists because the rule was already written, in
      `haipipe-board/ref/writing-rules.md:66` ("do not erase them"), and was broken
      by hand on 260801: eighteen `✎` records were removed with a regex to reposition
      them. Repositioning is the legitimate need; erasing was the wrong way to get it.
260801 · `0.3.0`
      Second look at `paper/2-phase/0-draft`, on JL's ask. The first pass reported
      nothing general there and was wrong: the strongest pattern in the phase is
      general, and it reads as paper machinery only because every rule is written in
      `\cite{TOADD}`, `{VAL:?}` and `Q-<Stage>-<n>`.
      - `ref/holes.md` — the hole discipline. Never invent a fact to close a gap;
        every hole names an owner; sweep after writing, not during; one writer per
        file. Three dialects (paper, board, plain) over one contract.
      - `cli/holes.py` — the checker, both directions. FORWARD catches an unowned
        hole; REVERSE catches a hole pointing at an owner that does not exist, which
        is the worse of the two because it looks owned.
      - `haipipe-paper-draft` Step 4c now RUNS the checker instead of verifying by
        hand. That step already described this exact audit in prose.
260801 · `0.2.0`
      Migration in from `paper/` (JL: "do you think for some skills, we can immigrate
      them out to the haipipe-writing?"). Whole skills did NOT move: every unit in
      `0-draft/` and `2-revise/` is bound to LaTeX, to `%%` comments, to `\cite{TOADD}`
      placeholders, or to venue voice. What moved is the general writing knowledge that
      was only reachable by loading a paper skill.
      - `ref/ai-tells.md` — Layer 1 of the humanizer's pattern catalog. It describes
        how a machine writes in any register; Layers 2 to 6 stayed, because
        over-claiming, citation dumping, venue voice and proposal register do not
        generalize. The humanizer now points here for Layer 1.
      - `ref/weaving.md` — the paragraph-flow pass (arc, hinges, rhythm) from
        `haipipe-paper-revise-content`. Generalized: the recording grammar is now the
        host's, so the same method serves `%% {CC-content}:` and `> ✎`.
        `haipipe-paper-revise-content` still owns WHEN the pass runs.
      - `haipipe-paper-revise-humanizer` now calls `cli/wdiff.py` to compute its
        candidate diffs rather than writing them by hand.
260801 · `0.1.0`
      First cut. Extracted from one evening of hand-rewriting the design board's `QB4`
      page with JL, who asked for the capability after watching the same work be done
      by hand: "I think we need to add it to the skills to make this work."
      - `cli/wdiff.py` — word-level diff and anchored record insertion. `record`,
        `apply`, `check`. The diff is `difflib`, not judgment; the placement is by
        position, not by where the writer stopped typing.
      - `cli/score.py` — read-only ranking against the weak-English test. Counts house
        words, long words, sentence length, and the AI tells this repo has actually
        produced. Reports; never rewrites.
      - `ref/plain-rules.md` — the rules, each with the ruling that produced it.
      - `ref/change-record.md` — the `✎` grammar, the anchoring law, the two host
        dialects, the badge, and what `check` fails on.
      Validated against real prose on the day it was written: `check` passed all 31
      records on `QB4-overall.md`, and `score` independently surfaced the same `### 3`
      sentences that had been flagged by hand, while reporting 0 bad headings on a
      division whose headings had just been repaired.
      Not built yet: a `rewrite` verb that drives the loop end to end. Today step 2 is
      a person or a model reading `score` output and calling `wdiff apply` per sentence.

<!-- haipipe:skill:log:end -->
