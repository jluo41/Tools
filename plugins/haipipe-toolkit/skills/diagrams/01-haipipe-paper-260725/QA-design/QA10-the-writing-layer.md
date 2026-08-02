# ⑪ The PROSE verb: /haipipe-writing

state: 🟡 PARTIAL · placed and ruled; the two seam questions are open in Aims
owner: JL
method: rule the paper-side half of a family that owns no artifact kind, and keep its record here because it has nowhere else to go

## Opening

A paper's prose is written by someone who already knows the subject, so who makes it readable to someone who does not, and where is that decision recorded?

This is the fourth shared family on the map and the first one whose board is this board. `①` writes the paper, `③` renders and runs its boards, `⑤` owns the crossing where evidence enters, `⑨` makes the floats, and `⑪` rewrites prose that already exists. The pattern is the same in all five cases: this family depends on a contract it does not own and rules only its own half. What is different here is where the other half is argued, because `⑪` has no board of its own.

That is not an oversight, and the skill's own README gives the reason: every other family owns a KIND of artifact, `paper` owns manuscripts, `board` owns pages, `application` owns reports, and this one owns none. Its consumer is any authored prose in the repo and its test does not care what file the prose is in. A family with no artifact has no separate subject to argue, so JL placed its record here on 260802 rather than opening a board for it.

The prose that produced it was this board's. Every rule in `ref/plain-rules.md` was ruled while rewriting `QB4` on `④`, the `✎` record grammar was built because the same two mistakes were made twice by hand in one evening, and `ref/ai-tells.md`, `ref/weaving.md` and `ref/holes.md` were all migrated OUT of `①` because no paper owned them. The skill exists because a design board needed it first.

Scope: This page covers Where the prose verb sits, what it owns against `①` and `③`, why it has no board of its own, and what is still owed at the seam. Neighbouring pages cover Which folder this is among the eleven is `QA1`; what ships and whether it is well is `Skill-11`; the lane contract the `✎` record lives inside is `Skill-9`; the paper's own venue-bound revision chain is `Skill-5`.

## Diagram

```
   ── one verb, three owners, and the line between them ─────────────

   ⑪ /haipipe-writing            ① paper/                ③ board/
   the PROSE verb                the VENUE owner         the LANE owner
   ┌────────────────────┐        ┌──────────────────┐    ┌──────────────────┐
   │ can a weak-English │        │ how loudly may a │    │ a > line under a │
   │ reader follow it?  │        │ paper claim?     │    │ sentence belongs │
   │                    │        │ how does it cite?│    │ to that sentence │
   │ plain-rules        │        │ which gate must  │    │ 8 ⚑ typed lanes  │
   │ ai-tells           │        │ a claim pass?    │    │ 1 💬 comment     │
   │ weaving            │        │ %% in LaTeX      │    │ 1 ✎ record ◀─────┼─┐
   │ holes              │        │                  │    │                  │ │
   └─────────┬──────────┘        └──────────────────┘    └──────────────────┘ │
             │ writes ONE lane out of ten ─────────────────────────────────────┘
             │
             ▼
   ANY authored prose      a board page · a manuscript section · a README
                           the host changes the dialect, never the test

   ── the split JL made on 260801 ───────────────────────────────────
      the MACHINERY moved here      wdiff.py, and the general catalogues
      the JUDGMENT stayed there     venue voice, claim strength, citation
      "They share machinery. They do not share judgment."
```

```
   ── why it has no board, stated as a test ─────────────────────────

      does the family own a KIND of artifact?
            │
      ┌─────┴─────┐
     YES          NO
      │            │
      ▼            ▼
   it has a     it is argued where its prose already lives
   subject to
   argue        ⑪ writing/  → ②, this board, at QA10
                ⑨ display/  → ⑩, its own board  (owns the float)
                ⑤ probe/    → ⑥, its own board  (owns the QA file)
                ③ board/    → ④, its own board  (owns the page)
```

## Content

### What `⑪` owns, and what we own

```
 ⑪ /haipipe-writing   the plain-English rules and the ruling behind each ·
   v0.4.0 · 143 ln    the ✎ diff computation and its anchoring by POSITION ·
                      the general AI-tell catalogue · the weaving method ·
                      the hole discipline, both directions
                      consumer: ANY authored prose in the repo

 ① the paper side     everything a VENUE owns. How loudly a paper may claim,
                      how it cites, which gates a claim must pass, and the
                      `%%` comment grammar LaTeX needs.
                      `haipipe-paper-revise-humanizer` keeps all of it.
```

The division is the skill's own and it is stated in one line there: they share machinery, they do not share judgment. `ref/change-record.md` §3 holds both host dialects side by side so they cannot drift into two ideas.

### It owns one lane out of ten, and none of the machinery around it

The `✎` record is not a grammar this family invented. `③` owns the lane contract, `Skill-9` mirrors it here, and `QB4@boardform §3.3.3` names the ten kinds: eight `⚑` typed lanes, one `💬` comment, and the `✎` change record `⑪` writes. Three of those rules bind it directly and `cli/wdiff.py apply` enforces all three: a lane is appended and never edited in place, a signed `> WHO:` or `> ✎` line is never erased, and a lane with no signature is not a lane.

That is the healthy shape of a dependency, and it was got wrong first. Releases 0.1.0 through 0.3.0 described `✎` as a standalone grammar, which created a second authority on something `③` already owned. JL caught it on 260802 and 0.4.0 rewrote the reference to CITE the owning contract rather than restate it.

### Why the record lives here and not in a board of its own

```
                        a board of its own          this board
 has an artifact kind?  required                    not required
 where the rules came   its own subject             THIS board's QB4 page
 from
 who reads the record   that family's owner         whoever writes prose here
 cost of a board        one more thing to keep      none
                        current
```

Opening a board for `⑪` would create a record with no subject of its own to argue, kept current by nobody, at the moment when every rule in it was produced by working on pages that live here. JL ruled it directly (260802): "for the skill folder, its skill board will be in the paper skill board itself."

This makes `②` the board of two things, which `QA1`'s Law now states, and it is the only case on the map.

### The seam, verified 260802

The call is real, and it is wired in two places rather than the one that was claimed. Both are instructions in a `SKILL.md`, not notes in a changelog, so a worker following either one reaches `cli/wdiff.py`.

```
 haipipe-paper-revise/SKILL.md:70            "COMPUTE those marks, do not write
   the candidate-diff hub                     them: wdiff.py record …"
 haipipe-paper-revise-humanizer/SKILL.md:94  "COMPUTE the diff, never write it
   the pass that emits candidates             by hand: wdiff.py record …"
```

There is no second diff implementation anywhere in `paper/`, so the 0.2.0 migration was carried and not merely declared. `wdiff.py record` was run against this board's own prose to confirm it works: `The map has ~three~ *five* reusable skills, not two.`

Two defects surfaced in the check and both are repaired.

The humanizer cited `skills/writing/haipipe-writing/cli/wdiff.py`, a bare relative path that resolves only when the working directory is the plugin root and fails from the repository root, where a session actually starts. Its own hub two files away already wrote `<skills>/writing/…`, so the two halves of one instruction disagreed. The humanizer now matches the hub, and gained the `--when` argument, which `record` requires and the instruction omitted.

`SKILL.md` declared `0.1.0` against a `CHANGELOG.md` that had shipped `0.4.0`, so `Skill-11`'s derived header understated the unit by three releases. The frontmatter now reads `0.4.0`.

### The host became a flag, 0.5.0

The verification found one hand step nobody had asked about, and JL ruled it out the same day. `wdiff.py record` emitted the board notation only, so `haipipe-paper-revise/SKILL.md:70` had instructed its caller to "double the tildes and turn `*new*` into `**inserted**` for this host". That put a hand step inside the one tool whose whole design case is that this class of hand step gets done wrong: the computation was in one place and the OUTPUT was not, so the last transformation before marks reached a manuscript was performed by the reader the skill exists to protect.

`--host` now selects the notation, from one set of `difflib` opcodes.

```
 --host board   (default)   > ✎ ~old~ *new* · WHO · YYMMDD HHMM
 --host paper               > Note: ~~old~~ **new** · WHO · WHEN
```

Both paper callers pass `--host paper` and convert nothing. An unknown host is refused by `argparse` rather than silently defaulting, so a third notation has to be added deliberately.

### The flag uncovered an older contradiction

Testing `--host paper` on a sentence that already carried a lane exposed a defect present since 0.1.0, in code this change never touched.

```
 apply   appends the record to the END of the sentence's lane run
         0.4.0 made this explicit, and QB4's Law requires it
 check   looked exactly ONE line up and demanded prose there
 ────────────────────────────────────────────────────────────────
 result  every record under a sentence already carrying a
         > Citation: or > Value: lane was written correctly by one
         half of the tool and rejected by the other
```

Nothing had caught it because the corpus it was validated against, `QB4-overall.md` on `④`, happens to carry all 31 of its records on sentences with no other lane. `check` now walks the `>` run back to the sentence it hangs under. A record under no prose at all is still caught, a malformed one still is, and the 31-record corpus stays at 0 problems.

This is the third instance today of one shape: two halves of one contract disagreeing, with nothing that compares them. The humanizer's path against its hub's path, the frontmatter version against the changelog, and now `apply` against `check`.

### Something now compares them, 0.6.0

`cli/agree.py` checks the two disagreements that are STATIC, and `tests/test_roundtrip.py` covers the one that is not.

```
 version   SKILL.md frontmatter  ⟷  the newest CHANGELOG.md heading
 path      a cross-skill citation ⟷  what is on disk, reporting DEAD and,
                                      separately, "resolves only from the
                                      plugin root", the humanizer's case
 round     what `apply` writes    ⟷  what `check` accepts
   trip    a test, because no grep can see a round trip
```

Swept over all 152 skill folders: 2 version disagreements and 57 path findings, and it still reports the humanizer defect the moment it is reintroduced. Among the 57 is a stale reference to this board's own pre-260802 naming, `skills/diagrams/01-haipipe-paper-260725/QO-delivery-build/QC6-sentence-to-word.md`, which no longer exists in any form.

The checker got its own job wrong twice before it worked, and both are recorded in `0.6.0` rather than tidied away. It first skipped fenced blocks, which made it blind to the instruction it was written for, because that instruction lives inside a fence. Its version comparator then missed the bracketed `## [0.6.1]` heading form, fell through to the heading below, and flagged 35 of 152 folders that agreed perfectly. A checker built to catch two halves disagreeing shipped its first draft with two halves disagreeing, which is the strongest evidence available that the class is real and that noticing is not a reliable defence.

⚠️ It is a floor and not a proof. It checks two disagreements, both of which have actually bitten, and it stays silent about the path-shaped nouns a skill merely describes.

## Aims

- [x] 🗺 Place the prose verb on the map
      `⑪` on `QA1`, the fourth shared family, and the first whose board is `②` (JL 260802).
- [x] 📐 State the test that decides whether a family needs its own board
      Does it own a KIND of artifact? `⑨` does and keeps `⑩`; `⑪` does not and is argued here.
- [x] 🧾 Record that it owns one lane out of ten
      `③` owns the lane contract; `⑪` writes the `✎` record inside it and redefines none of the machinery.
- [x] 🔍 Verify the humanizer actually calls `cli/wdiff.py`
      Verified 260802. Wired in TWO SKILL.md instructions, `haipipe-paper-revise:70` and `haipipe-paper-revise-humanizer:94`, and no second diff implementation exists in `paper/`. Two defects repaired in the same pass: the humanizer's path was unresolvable from the repository root, and it omitted the required `--when`.
- [x] 🎚 Give `wdiff.py record` a host flag, or rule that the hand conversion stays
      JL ruled it built (260802). `--host {board,paper}` ships in 0.5.0, both paper callers pass `--host paper`, and no caller converts marks by hand.
- [x] 🧯 Make `apply` and `check` agree about where a record may sit
      Found while testing the flag and present since 0.1.0: `apply` appends after the lane run, `check` demanded prose one line up, so any sentence with an existing lane produced a record the tool wrote and then rejected. `check` now walks the run back.
- [x] 🔁 Find the next disagreeing pair before a reader does
      `cli/agree.py` and `tests/test_roundtrip.py` ship in 0.6.0 and cover all three shapes that bit today. The sweep over 152 skill folders returns 2 version disagreements and 57 path findings.
- [ ] 🧾 Clear what the first sweep found
      57 path findings and 2 version disagreements are recorded and not repaired. One of them is this board's own stale id, `QO-delivery-build/QC6-sentence-to-word.md`. Reporting them is not fixing them.
- [ ] 🚦 Decide whether `agree.py` runs on its own
      Nothing calls it. A checker a person has to remember to run is a checker with the same failure mode as the defects it catches.
- [ ] 🧠 Rule which prose on a PAPER is `⑪`'s and which is `①`'s
      The machinery/judgment split is stated and is not yet checkable. A section draft that is merely unreadable, with no venue question in it, has no ruled owner today.
- [ ] 🔗 Rule what happens when `③`'s lane contract changes
      `⑪` binds to it and `QA8` has the same open question for the Board grammar. Nothing says who migrates the writer when the lane spec moves.

## States

The layer ships, is in daily use on this board's own pages, and is now on the map. What is new here is placement, not mechanism: `cli/wdiff.py` wrote 31 records on `QB4@boardform` on 260801 and nothing on this board said where the skill that wrote them belonged.

The seam with `①` is the part that is only argued. The machinery moved and the judgment stayed, which is the right split, and there is still no test that tells a writer which of the two they are doing when a manuscript paragraph is simply hard to read.

Both unverified claims were closed on 260802 and both moved in the direction the page did not assume: the humanizer call is real and wired twice, and the version drift was repaired at its source rather than annotated here.

The check then turned up a question nobody had asked, JL ruled on it, and `--host` shipped as 0.5.0 the same day. Testing that flag exposed an older defect underneath it: `apply` and `check` had disagreed about where a record may sit since 0.1.0, invisibly, because the corpus that validated the tool has no sentence carrying two lanes.

The pattern worth keeping is not any of the three defects. It is that all three are one shape, two halves of a contract that nobody compares, and that each was found by a person looking rather than by anything that checks.

Something checks now, and the honest reading of it is narrow. `agree.py` covers the two static shapes and a test covers the round trip, so a fourth instance of any of those three should surface without a person noticing. Nothing yet RUNS it, so the tool has the same failure mode as the defects until something calls it, and its first sweep produced 59 findings that are recorded rather than repaired.

## Files

- `writing/haipipe-writing/`
  `⑪` itself: the rules, the diff engine, the hole checker, the catalogues.
- `writing/README.md`
  Where the no-artifact-kind argument is stated by the family in its own words.
- `board/haipipe-board-sentence/`
  `③`'s lane contract, which owns the shape the `✎` record lives in.
- `paper/2-phase/2-revise/haipipe-paper-revise-humanizer/`
  The venue half, and the unverified call to `cli/wdiff.py`.

## Law

The prose verb is the fourth reusable family this board's paper depends on and does not own, and the first whose board is `②`. A family that owns a KIND of artifact earns a board of its own; a family that owns none is argued where its prose already lives.

`⑪` owns whether a reader whose English is weak can follow a sentence, and `①` owns everything a venue decides: how loudly a paper may claim, how it cites, which gates a claim must pass, and the `%%` grammar LaTeX needs. They share machinery and never share judgment.

`⑪` writes ONE lane out of the ten `③` defines. It never redefines the lane, the evidence card, or the archive lifecycle, and a reference here that restates `③`'s contract instead of citing it is a defect, which is exactly what `0.4.0` repaired.

A change record is APPENDED, is never erased once signed, and is placed by position rather than by where the writer stopped typing.

## Glossary

- **Prose verb**: a family whose product is a rewrite of prose that already exists, rather than a new artifact of its own kind.
- **Artifact kind**: the class of thing a family produces and owns, which is the test for whether it needs its own board.

## Log

260802 · Opened when JL placed `writing/` on the map and ruled that its skill board is this board. The face exists because that ruling makes this board the family's owner, which is the one condition under which `QA1`'s no-face rule permits a page about a shared family. Two unverified claims recorded rather than repeated: the humanizer's call to `cli/wdiff.py`, and the `0.1.0` frontmatter against a `0.4.0` changelog.

260802 · Aim 4 verified rather than assumed, and it held: the call is wired in two SKILL.md instructions and `paper/` carries no second diff implementation. Repaired the humanizer's unresolvable path and its missing `--when`, and the `0.1.0` frontmatter against a `0.4.0` changelog. Opened one new aim the verification produced: `record` has no host flag, so the paper's marks are converted by hand.

260802 · Aim 5 ruled and built: `--host {board,paper}` ships in `haipipe-writing` 0.5.0 and both paper callers convert nothing by hand. Testing it exposed a 0.1.0 contradiction between `apply` and `check` about where a record may sit, now repaired. Opened one aim that is not about any of the three defects but about the shape they share.

260802 · Aim 7 built: `cli/agree.py` compares a declared version against its changelog and a cross-skill citation against the disk, and `tests/test_roundtrip.py` covers the round trip no grep can see. Both shipped in 0.6.0. The checker got its own job wrong twice first, and both wrong turns are in the changelog rather than tidied away. Two aims opened in its wake: the 59 findings are recorded and not cleared, and nothing calls the checker.
