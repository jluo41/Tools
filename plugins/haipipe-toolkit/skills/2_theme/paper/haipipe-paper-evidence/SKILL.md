---
name: haipipe-paper-evidence
description: >-
  What backs a paper, the paper's rules on top of the base haipipe-evidence (cards: CITE from discovery Runs, WORK
  from work Runs) and haipipe-display (figures and tables). A paper Section is a draft Task: its draft/ is
  haipipe-paper-draft's, its evidence/ and display/ follow this skill. The rules: a citation comes from a verified
  CITE Result and never from bank.bib; one result gives one number in every Section; displays are numbered for the
  paper and kept within the venue's limit; claim words fit the design. It also reads one whole version (a Job
  jNN_v<MMDD>_<desk>) as one evidence ledger, every Section side by side, and flags what disagrees across Sections:
  one value read from two Runs, one label bound to different estimates, too many displays, a display shown twice
  (scripts/evidence_ledger.py). Use to check a Section's or a version's evidence, citations, numbers or displays
  before a build or a send. Trigger: paper evidence, evidence ledger, check the evidence of this version, same number
  everywhere, numbers disagree, verify citations, display numbering, display limit, /haipipe-paper-evidence.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.0"
  last_updated: "2026-10-19"
  # version history: ./CHANGELOG.md
---

# /haipipe-paper-evidence · what backs the paper, Section by Section and as one version

JL 261019: "should we chagne this to haipipe-paper-draft? and also have a haipipe-paper-evidence? ... it is like we
have the paper to combine the evidence and draft together to make a draft task, right?"; then "okay, please go ahead
and do it". A paper Section is a draft Task (b32_draft s03, s41-D06), three folders side by side, one writer each:

```text
base (every theme)      paper adds                  one Section Task
haipipe-draft      ─▶   haipipe-paper-draft    ─┐   tNN_<section>/
haipipe-evidence   ─▶   haipipe-paper-evidence ─┼─▶ ├── draft/      plan and sentences
haipipe-display    ─▶   (this skill too)       ─┘   ├── evidence/   cards.yaml · proposals.md
                                                    └── display/    Display<n>-<slug>/
```

The base finds and shows evidence for any page; this skill adds what only a paper needs. A base skill sees one Task
at a time, so the one thing no base skill can do is read a whole version and say where its Sections disagree: that
is the ledger below.

| base skill | does, for any page | this skill adds, for a paper |
|---|---|---|
| `haipipe-evidence` | the card format, CITE and WORK, `cards.py check · propose` | the citation and number rules; the version ledger |
| `haipipe-evidence-cite` | a discovery Run's `.bib` and `facts.md` | verified before a Section closes; never `bank.bib` |
| `haipipe-evidence-work` | a work Run's value at `file` + `key` | the same Run for the same value in every Section |
| `haipipe-display` | `Display<n>-<slug>/`, built on cards | numbered for the paper; within the venue's limit |


The rules
---------

1. **Citations come from verified CITE Results.** A CITE card names a discovery Run; its one-entry BibTeX is the
   citation. The Page export freezes `delivery/latex/selected-bibliography/<page>.bib` from the selected, verified
   CITE Results, and `haipipe-paper-assemble` merges them; both are generated, never edited. Never touch
   `bank.bib` or the paper's `delivery/reference.bib`. A source with no Result yet is `\citep{TOADD}` and a red
   card with `need`. Check every entry against Google Scholar or its DOI record before the Section closes. Never cite
   one paper in back-to-back sentences.
2. **One result, one number.** A number in prose comes from a WORK card (`file` + `key` in a Run's `result/`), best
   through the research question's report (`reports/qNN_<question>/`). The same result reads from the same Run, and
   shows the same number, in the Abstract, the Results, the Discussion and the letters.
3. **Displays are the paper's.** Each `Display<n>-<slug>/` is built on cards (haipipe-display). The paper numbers them
   in Section order: the main text Display 1, 2 …, the appendix (`t2N_`) eDisplay 1, 2 …; each is cited in its
   Section's text; the main text stays within the venue's limit (its call, or what the person says).
4. **Claim words fit the design.** An observational design says "association", never a causal verb; a claim
   never outruns the evidence card under it.
5. **Every consequential sentence is one of three**: backed by a card (an older Page: a typed Evidence Item and
   its accepted local Result), framed as interpretation and bounded by its evidence, or a visible open need that
   keeps the Section from closing. haipipe-paper-draft writes the sentence; this skill checks which of the three it is.


The version ledger
------------------

```bash
L=Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-evidence/scripts/evidence_ledger.py
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/                    every Section of one version, side by side
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/ --max-displays 7   with the venue's limit on main-text displays
.venv/bin/python -B $L <paper>/jNN_v<MMDD>_<desk>/ --json             for a builder or a workbench
```

It reads each Task in either shape: `evidence/cards.yaml` (haipipe-evidence, since 261016) or an older Page's
`draft/<stem>-evidence-items.md` (read by haipipe-draft's `item_table`, the parser the Page workbench uses), its
`display/Display<n>-*/`, and its `.bib` files (`draft/evidence/bibex/` on an older Page, else each CITE card's Run).
Parts by Task number: `t00` the Abstract, `t01`-`t19` the main text, `t2N` the appendix, `t3N` the letters. Only the
Sections in the version face's `haipipe:compile-order` block are numbered, counted and compared; the rest show
`⏸ off`.

```text
❗ one value, two Runs            the same WORK value (source, file, key) read from different Runs in two Sections
❗ one label, different estimates  an older VALUE label whose Results report different estimates, compared in
                                  one unit (a key with pp or percentage_point is in percentage points)
❗ one citation key, two entries   the same key with another year or title in two Sections' .bib files
❗ too many displays              main-text displays over --max-displays
❗ a card does not resolve        haipipe-evidence's cards.check, per Section
⚠️ one label, the same estimates  two Results that hold the same estimates (one copies the other: point both at one)
⚠️ one display twice              the same display name in two Sections
⬜ open                           citations not yet verified, values not yet landed, needs not yet filled
```

**What it does not read yet**: numbers typed into table bodies or prose, and wording that drifts between Sections
("no association" in one, "close to zero" in another). Those stay a person's read of the built PDF
(haipipe-paper-assemble's cold read). **The venue's limit** is passed by hand: a venue's call (`venues/<venue>/call.md`)
or the person says it; a QBv desk record may not hold it.

It changes no file of the paper: the ledger is a view of the Tasks' own files, so nothing generated is tracked (`-B`
keeps Python from writing its bytecode cache beside the script). Exit 1 on a ❗. A ❗ is fixed in the Section that is
wrong (its card, its Evidence Item, its `.bib`, or the Run it reads), never by editing a built file.


Where it sits on the ladder
---------------------------

```text
Board     💡 s01 idea · 📖 s02 story (§7 allots evidence to Sections) · 🔍 s10-s19 related · ❓ reports/qNN_
  └─ Job  jNN_v<MMDD>_<desk>: the Narrative order · 🧾 this ledger, once per send
      └─ Task tNN_<section>: draft/ ✎ (haipipe-paper-draft) · evidence/ 🧾 · display/ 📊 (this skill)
```

Who calls it: a Section's CHECK (haipipe-paper-draft's closing checks), `haipipe-paper-assemble` before a build (gate
G4), and a person before a send. It proposes nothing itself: a missing piece is a card with `need`, and
`cards.py propose` (haipipe-evidence) flags what to make.


Files
-----

```text
haipipe-paper-evidence/
├── SKILL.md                      this contract
├── CHANGELOG.md
├── scripts/evidence_ledger.py    the version ledger
└── tests/test_evidence_ledger.py a made-up version: two Runs, two estimates, too many displays
```
