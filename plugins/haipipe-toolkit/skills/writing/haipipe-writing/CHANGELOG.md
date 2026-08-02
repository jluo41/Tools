# haipipe-writing
## 0.6.0 — 2026-08-02

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

## 0.5.0 — 2026-08-02

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

## 0.4.0 — 2026-08-02

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

## 0.3.0 — 2026-08-01

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

## 0.2.0 — 2026-08-01

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

## 0.1.0 — 2026-08-01

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