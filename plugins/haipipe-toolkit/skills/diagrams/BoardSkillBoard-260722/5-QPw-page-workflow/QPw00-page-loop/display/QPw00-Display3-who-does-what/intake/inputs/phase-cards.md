# The phase job cards · six fields, every phase, the same order

**What this file is for.** Each phase contract states its own authority in its
own words, and no two used the same fields: `haipipe-page-outline` writes
`owns · may do · exits · may not`, `haipipe-page-revise` writes a three-line
same-promise test, and `haipipe-page-check` writes `reads · writes · does not`.
All three are correct and none of them can be read next to the others.

JL asked the question that exposes it (260818 1402): "if I want to work with the
page workflow's each phase, what should each phase do". This file answers it
once, in six fields, identical for every phase.

```text
❓ ASKS     the ONE question the phase answers
📥 READS    what must already exist, or the phase cannot start
📤 WRITES   the exact path it creates or changes
🚪 EXITS    a testable condition
✋ TICK     the person-reserved tick, or none
🔀 ROUTES   where it may go next
```

**The operational rule: you work a phase by satisfying its 🚪 EXITS row.**
Five of the ten exits below are a person's tick. The other five have none, so a
machine may run those end to end without stopping.

## ① 🧭 OUTLINE · `haipipe-page-outline`

```text
❓ ASKS     what will this page say, section by section, and what does each
            bullet still owe?
📥 READS    the Page Type's `outline:` block (fixed | grammar | resolved)
            and the page's current sections
📤 WRITES   <page>/outline/<stem>-outline-v<N>.md
            🚫 nothing in the page itself. The plan and the page are two files.
🚪 EXITS    a person ticks `approved:` on the 🧭 tab
✋ TICK     `approved:`  ← a person. Nothing else ends this phase.
🔀 ROUTES   ② DRAFT · or a v<N+1> here
```

## ② ✏️ DRAFT · `haipipe-page-draft`

```text
❓ ASKS     what does this page promise, and which Aim dies if a hole stays?
📥 READS    the approved outline-v<N>.md
📤 WRITES   <page>/<stem>.md
              the Opening · Content as sentence scaffolds carrying <HOLE>
              the Aims section · the States section · the Log row
🚪 EXITS    every approved Point has a scaffold, and every hole names the Aim
            it would cost
✋ TICK     none
🔀 ROUTES   ③ PROBE · ⑤ REVISE · ⑦ CHECK · ② again
🚫 MAY NOT  open a card. The mark is the proposal; PROBE makes the folder.
```

## ③ 📮 PROBE · `haipipe-page-probe`

```text
❓ ASKS     was this already answered, and if not, who answers it?
📥 READS    the approved plan's marks · this page's existing probe/ and bibex/
            · PageX borrows · the task and discovery QA banks
📤 WRITES   <page>/probe/PP<NN>-<slug>/
              card.md · consumer/ · executor/ · proof/ (manifest only)
            state: planned → commissioned
🚪 EXITS    every marked bullet is served by at least one card, and the receipt
            reports `coverage: <n> of <n>`
✋ TICK     none
🔀 ROUTES   ④ EVIDENCE · HOLD (named) · ① OUTLINE for a v2
🚫 MAY NOT  route to REVISE. A card opened and never landed supports no sentence.
```

## ④ 🃏 EVIDENCE · `haipipe-page-evidence` · THREE LANES, IN PARALLEL

The three lanes are not three steps. Each has its own input, its own tick and
its own finish, and none waits on the others. A page may have a verified
citation, no answered value, and no frozen intake all at the same time, and that
is a normal mid-phase state rather than a defect.

### ④c 📚 the citation lane · board page `QPw4c-citation`

```text
❓ ASKS     which published work says this?
📥 READS    the 📚 mark; plus the bank's answer, only when the key was unknown
📤 WRITES   <page>/bibex/<stem>.bib — one entry
🚪 EXITS    the entry carries `verified = {WHO YYMMDD}`
✋ TICK     `verified`  ← a person
🚫 MAY NOT  a machine may SUBSET or TRANSCRIBE a real record. It may never
            COMPOSE one.
```

### ④v 🔢 the value lane · board page `QPw4v-value`

```text
❓ ASKS     what is the number, and which file proves it?
📥 READS    the QA path the dispatched card came back with
📤 WRITES   card.md `state: answered` · its `target:` path · the files pulled
            into proof/
🚪 EXITS    a person ticks `read:`
✋ TICK     `read:`  ← a person, and it REVERTS when target or proof changes
```

### ④d 🖼 the display intake lane · board page `QPw4d-display`

```text
❓ ASKS     which exact bytes will the figure be drawn from?
📥 READS    a probe card's proof/, which must already exist
📤 WRITES   <page>/display/<unit>/intake/ — frozen, plus its manifest
🚪 EXITS    intake is frozen
✋ TICK     none
🚫 MAY NOT  draw. This lane freezes and nothing else; REVISE renders.
```

## ⑤ 🖊 REVISE · `haipipe-page-revise` · with ⑥ COMPILE folded in

```text
❓ ASKS     does the prose now say only what the landed evidence supports?
📥 READS    answered cards · verified bibex entries · frozen display intake
📤 WRITES   the page prose with each landed hole replaced
            <page>/display/<unit>/recipe/ · assets/ · preview.pdf
            the States rows, updated from visible evidence
            a `> ✎` change record under each rewritten sentence
🚪 EXITS    no hole remains for an answer that landed, and the artifact is
            rebuilt from the current source
✋ TICK     none
🔀 ROUTES   ⑦ CHECK · ④ EVIDENCE when a claim is unsupported · ② DRAFT when the
            promise itself must move
```

⚠️ ⑥ COMPILE has no contract of its own and is folded in here. Whether that
fold is permanent is `QPw5-revise`'s open ruling.

## ⑦ ✅ CHECK · `haipipe-page-check`

```text
❓ ASKS     is this exact version closable, and who must act next?
📥 READS    the RENDERED page and the built artifact, not only the markdown
📤 WRITES   one finding placed at the sentence, section or artifact it concerns
            the check record · the route
🚪 EXITS    CLOSE, or a named route back to any earlier phase
✋ TICK     `accepted: ✅` on each display/<unit>/README.md, and the Page Type's
            declared RULING  ← both a person's
🔀 ROUTES   CLOSE · ⑤ REVISE · ④ EVIDENCE · ③ PROBE · ② DRAFT · ① OUTLINE · HOLD
🚫 MAY NOT  repair a substantive finding inside the same pass, and may not
            judge a version the same actor produced.
```

## 🧾 The five person-reserved ticks, gathered

```text
tick             lives on                          reserved by            phase
────────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<N>.md    haipipe-page-outline     ①
`verified`       each bibex/<stem>.bib entry       haipipe-plugin-bibex     ④c
`read:`          each probe/PP<NN>-<slug>/card.md  haipipe-plugin-probe     ④v
`accepted: ✅`   each display/<unit>/README.md      haipipe-page-check       ⑦
the RULING       the Page Type's declared gate     haipipe-page-check       ⑦
```

Two of them REVERT when their inputs change: `read:` and `accepted:`. The other
three stand until a person moves them.

**The board page that argues this file** is `QPw00-page-loop` on
`BoardSkillBoard-260722`. Each phase's own page (`QPw1` … `QPw6`, plus the three lane faces `QPw4c` ·
`QPw4v` · `QPw4d`) carries what its contract leaves open. The run's three
cross-cutting axes are NOT phases and no longer carry phase numbers:
`QPw00a` who acts · `QPw00r` what proves it ran · `QPw00g` who says yes.
