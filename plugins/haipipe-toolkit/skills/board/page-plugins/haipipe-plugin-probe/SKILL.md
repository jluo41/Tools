---
name: haipipe-plugin-probe
description: >-
  The Task/Discovery QA lane of a Board Page's Probe family: one evidence
  question per folder at <page>/evidence/probe/PP<NN>-<slug>/ — consumer/ holds the
  stake-bearing question, executor/ the stripped one, proof/ the evidence,
  card.md the reader-facing head. Trigger: probe plugin, QA probe, probe card,
  Task evidence, Q-consumer, Q-executor, /haipipe-plugin-probe.
metadata:
  version: "0.9.3"
  last_updated: "2026-08-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---
# /haipipe-plugin-probe · Probe's Task/Discovery QA lane

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
**LOAD `haipipe-probe` for the crossing itself**: stake stripping, the five-step loop, MATCH-before-DISPATCH, bank independence. This file owns the page-side delta only: where each of those pieces lands on disk, and how a sentence cites the result.

PageX is the other lane inside the Probe family. It binds accepted Page files in
OUTLINE; this plugin creates QA cards only for `source: task|discovery`.

## 🗂 Storage · one question per folder, and the stake wall is a PATH

```text
<page>/evidence/probe/
└── PP<NN>-<slug>/          one evidence question, numbered per page (QPf9 §1)
    ├── card.md             🧑 the head, one screen, all fields (§🪪)
    ├── consumer/           🧱 STAKE ALLOWED · never crosses
    │   ├── q-consumer.md     one block per consumer question this reduces to
    │   └── a-consumer.md     Page-specific interpretation · not Page prose
    ├── executor/           🧱 STAKE FORBIDDEN · all of it may cross
    │   ├── q-executor.md     the stripped question · THE ONLY THING DISPATCHED
    │   └── a-executor.md     the bank's answer, verbatim
    └── proof/              the FILES behind that answer  (§🧾)
```

`haipipe-probe` LAW 2 forbids stake outside the review-only Q-consumer copy. Two folders make that law checkable: a walk of `executor/**` for claim ids, `our` / `this paper` / `we`, and PP numbers returns a file and a line. The same walk over one mixed file is impossible, because stake is legitimately present twelve lines above.

**The folder name is a NOUN, and every word in it is already on disk.** `PP<NN>-` plus two or three words naming WHAT THE CARD IS ABOUT; the question lives in `card.md`'s `question:` line.

```text
  ✅ PP01-ols-headline-coef · PP02-ols-spec1-5 · PP03-ols-sample-n · PP04-ols-script
  ❌ PP01-ols-which-spec        a question wearing a folder's clothes
  ❌ PP02-control-rung-ladder   "rung" and "ladder" grep to zero in the repo

  ① the slug may not contain  which · what · why · how · whether · is · does
  ② for each word w:  grep -ril "<w>" <task-folder>/  must hit, or w is in the
     short plain list:  n · coef · sample · script · run · table · log · gap ·
     commit · spec
```

Read the real words off disk before naming anything: run directory names, table file stems, column headers. The same rule governs the page's `###` division headings, so a card and the division citing it use one word for one thing.

## 🪪 `card.md` · the head, and every field it may carry

The whole head is `key: value` lines above the first `##`. Nothing else parses, and a field this table does not list does not exist.

```text
field       required when        value
──────────────────────────────────────────────────────────────────────────
# <id>      always               the folder name, exactly
state:      always               planned | commissioned | answered | read |
                                 answered-local | deferred | failed | concern
read:       always               ⬜ <why not yet>   or   ✅ <who> · <date>
serves:     once the plan is     C<n>.P<n>.B<n>, ` · ` separated (§↩)
            approved
question:   always               ONE line, neutral words, no page id
route:      after ① ORGANIZE     task | discovery | none
bank:       after ② MATCH        reuse | run | code | new · the folder judged
                                 = the COST TIER, named twice: reuse is T2,
                                 run/code are T3, new is T4, and a card that
                                 never needed the bank at all carries no `bank:`
                                 because it closed at T0/T1 (`haipipe-probe` §💰)
dispatch:   after ③ DISPATCH     who · when
target:     after ④ POINT        the path of the answering QA file
```

⚠️ **`binding:` is the legacy name of `bank:`** and is not written on new cards. A head carrying prose where `bank:` belongs ("not opened; requires a secure-server run") is that legacy shape: the verdict word is missing, so `② MATCH` cannot be checked as done.

Everything else in `card.md` is a pointer, not content: the body is the four-line map of `consumer/`, `executor/` and `proof/`, and nothing more. A card that starts explaining its own answer has crossed back over its own wall.

## ↩ `serves:` · the card names the bullet, never the reverse

**Ruled 260817.** A card is created at PROBE, long after OUTLINE froze the page's plan. So the plan cannot name the card: at the moment it was written, the id did not exist. The link runs BACKWARD, and `card.md` carries it, right under `state:`:

```text
  serves: C4.P1.B4                        one bullet
  serves: C3.P1.B3 · C3.P3.B3 · C7.P2.B1  three — PP04 on QC1-visitlbp really does
```

```text
  ✍️ authored   the bullet names PP01      illegal at WRITING time: the plan is
                at OUTLINE                 authored bare, because the id does
                                           not exist yet
  ✅ folded     the ① fold appends         legal: `📮 PP<NN>` lands in the
                `📮 PP<NN>` in place        bullet once the card SERVES it
  ✅ backward   the card names the bullet  the LIVE join, and the one the 🧭
                                           tab reads
```

So a forward id in a bullet is a fold-appended CITATION, never an authored one; `serves:` remains the live join.

The address is the plan's own (`C<n>.P<n>.B<n>`, `haipipe-plugin-outline` §📐), and the relation is MANY-TO-MANY: one card may answer several bullets, and one bullet may need two cards, typically a number and the script that produced it. `serves:` is therefore a list.

**A bullet is satisfied when EVERY card serving it is answered**, never when any one is. `any` would let a claim with one landed number and one open question read as finished, which is the failure the counts exist to prevent. The 🧭 tab prints `↩ PP04 serve this bullet · 2 of 3 answered` until they all are.

A card whose `serves:` is empty is not an error while the plan is still being written. Once the plan is approved it is one, and the 🧭 tab shows it as 🎈: evidence nobody is using.

## ✍️ Writer · the loop lands each piece, and the state is checkable by FILE

The lifecycle is `haipipe-probe`'s five-step loop, split across TWO phases since 260819: PROBE runs ① ORGANIZE ② MATCH ③ DISPATCH, and EVIDENCE runs ④ POINT ⑤ INTERPRET, landing and binding what came back. No board route writes a card; this plugin only says where each step lands.

```text
step                                  where it lands
──────────────────────────────────────────────────────────────────────
① ORGANIZE  strip the stake           consumer/q-consumer.md ✚ executor/q-executor.md
② MATCH     the bank verdict          card.md · bank: reuse|run|code|new
③ DISPATCH  send it out               card.md · dispatch: who · when
④ POINT     bind to the QA file       card.md · target: <path> ✚ proof/
⑤ INTERPRET the answer, verbatim      executor/a-executor.md
            what it MEANS here        consumer/a-consumer.md · stake allowed
```

The one obligation this plugin adds: **write into the right side of the wall.** A question arriving with stake is copied into `consumer/` and stripped into `executor/`; the stripped copy is what any dispatch reads, and nothing edits `executor/` to add context back.

**The state vocabulary is `haipipe-probe`'s, adopted verbatim** (its §🧾 Return contract `state:` row), never a page-local set of words. ⚠️ This line named "its entry record, §`state`" until 260821; that section does not exist, and the list it did point at was missing `answered-local` — so the plugin was the de-facto source for a word it claimed to be borrowing. Both files now carry all eight. What this plugin adds is the DISK TEST beside each one, so the word is checkable:

```text
card.md state     and on disk                                     hand
────────────────────────────────────────────────────────────────────────
planned           executor/q-executor.md exists · target empty     🧑
commissioned      target names a QA file claimed `working`         ⚙️
answered          target names an `answered` QA file ✚ a non-empty ⚙️
                  a-executor.md ✚ proof/ with files or a why_empty
read       answered ✚ non-empty consumer/a-consumer.md ✚           🧑
           read: ✅ <who> · <date> in card.md
answered-local    answered from our own registries, no bank run    🧑
deferred          parked on purpose; card names until what         🧑
failed            the bank ran and could not answer                ⚙️
concern           route: none · no bank can close it · stops at ①  🧑
```

⚠️ **`answered` is the machine's finish, `read` is the page's.** `answered`
means the bank returned something; `read` means a person read `a-executor.md`,
accepted the interpretation in `consumer/a-consumer.md`, and ticked `read:` in
`card.md`. DRAFT may then use that accepted interpretation in Page prose. Only
a person may tick it, and a changed `target`, proof, or A-consumer drops the tick
back. A Page quoting a number from a card that is not `read` is quoting an
unread answer.

A card claiming `answered` with an empty `a-executor.md` is a defect, not a nearly-finished card. `PRIMARY` material is `card.md`, both `q-*.md` and `proof/manifest.yaml`; `a-executor.md` is a verbatim copy. A question is asked ONCE: a second folder for the same unknown is the failure the id exists to prevent, and one `q-executor.md` may serve several consumer questions, which is why `q-consumer.md` holds a block per consumer.

## 🧮 One card, many values: `PP<NN>.v<n>`

A card is ONE question and its answer usually holds SEVERAL numbers. A sentence
uses one of them. Citing the card alone is therefore not precise enough, and
nothing caught it until JL asked on 260819: "probe 是一个大 folder，里面放了所有
的 value，而有的时候我们在正文里面只会用到一个具体的 value".

```text
  probe/PP01-phase-contract-count/
    the question   how many phases, contracts, ticks, runs?
    the answer     7 · 6 · 5 · 2          ← four values, one card

  §1  cites PP01.v1     the phase count
  §13 cites PP01.v4     the run count
```

**The id is allocated in `card.md`, in a `## Values` block, and nowhere else.**
It is written when the answer LANDS, at EVIDENCE, because a value that does not
exist yet cannot be numbered:

```text
## Values
- v1 · phases the loop declares · 7 · proof/phase-census.json `.phases`
- v2 · contracts that ship      · 6 · proof/phase-census.json `.contracts`
- v3 · person-reserved ticks    · 5 · proof/phase-census.json `.ticks`
- v4 · runs executed            · 2 · proof/run-index.json `.runs | length`
```

Each row is one line: the id, what the number IS in plain words, the number, and
the exact place in `proof/` it was read from. A row whose last field names no
file is not a value; it is a number somebody typed.

**Why this is not a new plugin.** The number already lives in `proof/` with its
source, run and sha256. A `value/` folder would be a second home for one thing,
which is the rule that retired the proof mark on 260819 (its glyph 🧮 now means value). What was missing was never a
folder; it was one more level of ADDRESS, and the same grammar already handles
that everywhere else: `C3.P1.B4` splits one bullet into sentences, `PP01.v2`
splits one card into values.

**A `bank: code` value is RECOMPUTED, not re-read by eye** (JL 260819: "I think
the machine should check these numbers"). `checks/values.py` re-runs each value's
own recipe against the repo and compares:

```text
  🤖 the machine owns   is the number still true?
  🧑 the person owns    is this the right number to be asking for?
```

That splits what `read: ✅` means. It stops being "I checked the arithmetic" and
becomes "I agree with the judgment inside the question". `PP01.v1` is the worked
example: counting the contract folders is mechanical, and whether COMPILE counts
as a phase at all is not, which is why the count is 7 and not 6.

The check earned itself on its first run: `PP03.v2` quoted 17 cards at `planned`,
which was true when it was written and became 13 four cards later. A person
re-reading by eye does not catch that, because the page still looks right.

A value with no recipe reports `unchecked`, never as passing.

**What it makes checkable, in both directions:**

```text
  🕳 a sentence carries a number and cites no `PP<NN>.v<n>`   ← unsourced
  🎈 a card holds a value no sentence uses                    ← unused answer
```

## 🧾 `proof/` · the files behind the answer

`a-executor.md` holds the answer IN WORDS; `proof/` holds the files that back it, so a reader who doubts the sentence can look at the numbers without leaving the page (JL 260817).

```text
proof/
├── manifest.yaml                    🧑 the only authored file · one block per file
├── main-ols_trait_l5_mme_ttl.csv    ⚙️ the SOURCE FILENAME, unchanged
└── versions/260814/                 the whole previous proof/, manifest included
```

**Three shape rules, and each one is a decision that could have gone the other way:**

```text
Ⓐ FLAT · no sub-folder by kind
  A card holds one to three files. `tables/ logs/ numbers/` would leave two of
  three empty on every card, so the kind is a manifest field, not a directory.

Ⓑ THE FILENAME IS THE SOURCE'S FILENAME, unchanged
  `ls proof/` and the manifest's `source:` must read as the same thing at a
  glance. Renaming to a friendly slug breaks that match and re-opens the
  question of which file this actually is.
  Collision only: prefix with the run — `af14d__main-ols_trait_l5_mme_ttl.csv`.

Ⓒ versions/<YYMMDD>/ HOLDS THE WHOLE FOLDER, not one file
  A rerun moves several numbers together. Per-file history answers "did this
  cell change"; whole-folder history answers "what did the last pull say",
  which is the question a stale proof actually raises.
```

**Three kinds land here, and nothing else:**

```text
  📊 table    .csv    an esttab coefficient table, a frequency table
  🧮 numbers  .json   a handful of scalars: N, a cutoff, a date range
  📄 excerpt  .txt    the few lines cut out of a log, with their line numbers

  ⛔ never: a whole log · a .dta or .parquet · any row-level record · any id
```

**`manifest.yaml`, one block per file.** The file alone is a number with no history; the block is what makes it evidence:

```yaml
card: PP02-ols-spec1-5
files:
  - name: main-ols_trait_l5_mme_ttl.csv   # as it sits in proof/
    kind: table                           # table | numbers | excerpt
    source: <full path inside the task folder or its shipped results>
    run: run_reg_visitlbp_1stpair_af14d_ols
    pulled: 2026-08-17
    rows: 13
    bytes: 472
    sha256: <of the file as pulled>
    why: the five SPEC coefficients this card was raised to get
    aggregate: true          # 🚨 required · false may not be committed
```

```text
① PULLED VERBATIM, NEVER EDITED   an edited cell stops being proof and becomes
                                  an assertion; a wrong number is a new pull
② SMALL                           ≤ ~200 rows and ≤ ~50 KB per file; bigger stays
                                  in the task folder and is cited by source: alone
③ AGGREGATE ONLY · 🚨 PHI         counts, coefficients, rates — no row-level
                                  record, no beneficiary id, no physician id
④ source: NAMES THE TASK PATH     without it the CSV is a number nobody can
                                  re-derive, the defect the card was raised to close
⑤ sha256 MAKES STALENESS COMPUTE  re-hash the source; a difference means the run
                                  moved and this proof is stale
```

```text
  task folder results/  ──pull──▶  probe/PP<NN>/proof/  ──freeze──▶  display/<unit>/intake/
  the AUTHORITY                    the page's frozen copy            the approved extract
```

When the two disagree the TASK FOLDER wins and the proof is stale; a display freezes `intake/` FROM `proof/` and never by hand.

⚙️ **A pull is a SCRIPT, never a hand copy** (JL 260817 asked how the CSV got there; the honest answer was `cp` plus a hand-typed hash, and a hand-typed hash proves nothing):

```bash
python3 ref/pull-proof.py <card-dir> <source-file> \
        --why "<one line>" --date $(date +%F) --repo-root .
```

One run copies the bytes AND writes the manifest block, so `sha256`, `rows` and `bytes` describe the bytes that actually landed. It REFUSES rather than warns: over ~200 rows or ~50 KB, a name already present with different bytes (unless `--replace`, which first moves the whole `proof/` into `versions/<YYMMDD>/`), and a kind it cannot infer. Any `pending:` or `why_empty:` line is removed as the first real file lands.

**`proof/manifest.yaml` exists from the moment the card is raised**, so the folder shape is the same at every state and an unexplained empty is impossible. `files: []` is legal in exactly two forms, and they are not the same thing:

```text
  files: []
  pending: the SPEC1..SPEC5 row, once the run that produced it is named
                                      ← not answered YET · normal on a planned card

  files: []
  why_empty: the answer is a definition; there is no file to pull
                                      ← answered, and there was never a file
```

An `answered` card whose manifest has neither is a defect.

## 🚪 Surface · the strip, in wall order

The right-pane 🚪 tab is `live/plugview.py`'s `plug_probe`, taking the display split's structure whole (JL 260816): a horizontal strip, one card filling the pane, a chip row naming every PP id, per-card anchors so a citation lands on the card it names. The filling is probe's own and reads the folder in wall order, so the reader sees the crossing:

```text
  🏷 head        card.md            state · bank verdict · target
  🧱 asked       q-executor.md      what actually crossed
  📥 came back   a-executor.md      the bank's own words
  🧮 proof       proof/             THE FILE'S OWN CONTENT, rendered
  🗂 audit       q-consumer.md      folded: who wanted it, and why
```

⚠️ **The proof step EMBEDS the file; it never re-renders it as HTML** (JL 260817).
A `.pdf` is framed with `<object>`, exactly as a display unit frames
`preview.pdf`; everything else is framed with `<iframe>` and a link to open it
alone. The manifest's fields are the label above the frame (`name`, then
`kind · rows · bytes · from run` as chips, then `why:`); `source:`, `pulled:`
and `sha256:` fold under `▸ provenance`.

**Embedding is a correctness decision, not a look.** Every proof bug so far came
from PARSING: `15.3332***` lost its stars to the bold rule, a folded yaml scalar
printed `>-`, and esttab's `="…"` armour needed its own splitter. An embedded
file IS the file, so there is nothing left to get wrong. It also holds the
board's no-script invariant, since a frame is not a script.

⚙️ The server must serve a proof file so it RENDERS rather than downloads:
`cli/serve.py`'s `guess_type` maps `.csv .tsv .log .do .yaml` to `text/plain`.
Under `text/csv` some browsers offer a download and the frame comes up blank.

**And the card follows the display unit's shape** (JL 260817: "让这个 layout 跟
display layout 长得像一些"), which is the same order a display card uses:

```text
  the question, in body type
  ┌ STATE ─ ROUTE ─ BANK ─ SERVES ─ TARGET ─────┐  a definition grid
  └ 🕳 the one next step, or ✅ read ────────────┘  amber / green

  ┏━ 🧮 PROOF · the files behind the answer ━━━━┓  the LEAD panel, heavier border
  ┃ ┌ main-ols_trait_l5_mme_ttl.csv (table)(13 rows)┐ one figure PER FILE
  ┃ │ ▓▓▓ the embedded file itself ▓▓▓             │
  ┃ │ ▸ provenance                                 │
  ┃ └──────────────────────────────────────────────┘
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  ┌─ 🧱 ASKED · executor/q-executor.md ──────────┐
  ┌─ 📥 CAME BACK · executor/a-executor.md ──────┐
  ▸ 🗂 AUDIT · consumer/q-consumer.md   (folded)
  ▸ 📂 FILES · the folder tree          (folded)
```

**Each step is its own panel, and each proof file its own figure.** JL read the
run-together version as 乱糟糟 (260817): five steps in one column separated by a
hairline gave the eye nothing to hold, so the dispatched question and the answer
that came back ran into each other. A panel has a header strip naming the step
and the file it comes from, so the card can be scanned without being read.

The header reports four independently computed counts, each from disk and not from the `state:` word: **planned** means a folder exists, **commissioned** means `target` names a claimed QA file, **answered** means an answered QA file plus a non-empty `a-executor.md` plus a settled `proof/`, and **read** means a human tick. A folder count is never presented as an answered question, and the strip's one-line verdict is the `read` count: `3 / 4 read` is what "done or not done" means on this page.

Every card that is not `read` shows a 🕳 notice naming the FIRST missing step, evidence-driven the way display's no-render notice is:

```text
  🕳 q-executor written, target empty          → nobody has been asked yet
  🕳 target claimed 2026-08-14, no answer      → dispatched, still working
  🕳 answered, proof/ empty and no why_empty   → the answer has no files behind it
  🕳 answered, no read: tick                   → nobody has read it
```

It must not claim a step exists merely because the folder does. The tab renders and never dispatches, because sending a question out is a deliberate act, not a button reflex.

## 📎 Citation · a card is evidence, and the citation lives in the sentence

A page's prose CITES a card by id and never restates what the card holds; a sentence carrying `state: raised` in words duplicates a field the card owns and will contradict it (`haipipe-page-workflow` §🪞).

```text
  The 7,865-row gap between the table and the estimation sample is PP03's.
                                                                  └─🚪 chip─┘
```

On a `dialect: paper` board the join key from a sentence to the question that owes it is the bracket `[Q-<Sec>-<n>]`, resolved at BUILD time by `src/dialect_paper.py`, which reports `unowned` when no probe entry declares that id. ⬜ **A board page has no equivalent chip yet**: `PP03` in a board sentence renders as plain text, and a backticked `` `PP03` `` is a code span, which QUOTES instead of chipping. Until that index exists, cite the bare id and let the 🚪 anchor carry the reader.


> Since 260831 this lane lives under the page's category folder (`evidence/` or `delivery/`, haipipe-page 0.47.0 §📁); a flat lane name on an unmigrated page, or a flat SYMLINK STUB on a migrated one, is the same lane during the migration.

## 📂 Files

- `ref/check-probe.py`
  The checker for everything above, no dependencies, never writes:
  `python3 ref/check-probe.py <page-dir> --task-folder <path>`. It verifies the
  state word against the protocol list, the two required `q-*.md`, the naming
  rule, the stake wall (a grep of `executor/**`), every manifest block and its
  `sha256`, the size ceiling, `aggregate: true`, and prints the four counts and
  the `read` verdict. On its first run against `QC1-visitlbp` it found two real
  wall leaks: each `q-executor.md` titled itself with its own PP id, and one
  dispatched question told the bank to match "whatever `PP01` finds".
- `../../../probe/haipipe-probe/SKILL.md`
  The crossing protocol this plugin defers to whole: stake stripping, the loop, LAW 2.
- `../../haipipe-board/live/plugview.py`
  The 🚪 strip, current as of 0.6.0: `plug_probe` reads the folder in wall order,
  computes the four counts from disk, prints the 🕳 first-missing-step notice, and
  renders every `proof/` file's content (`_render_proof_file`, `_csv_cells`).
  ✅ `_STATE_BADGE` keys on the protocol's own ladder since 260817, with the
  three retired words kept as aliases; `planned` and `commissioned` used to fall
  back to ⬜, which is how two ANSWERED cards read as untouched.
- `../../haipipe-board/src/dialect_paper.py`
  The `[Q-…]` join key, and the state a bracket resolves to.
- `../haipipe-plugin-display/SKILL.md`
  The unit whose folder shape this one mirrors, and the consumer of `proof/` through `intake/`.
- `../../haipipe-plugin/ref/roster.md`
  The row this skill expands.
