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
## 🔁 The loop has TWO parts, and the first one CONVERGES (260819)

Ruled by JL: "outline 之后就直接 probe 准备证据，基于证据我们再改 outline，直到
outline 自己是自洽的 … until outline is self-consistent and together with all the
evidence cards, then we are good to go ahead to draft."

```text
  ┌── PREPARE · repeat until self-consistent ──────────────────┐
  │                                                            │
  │   🧭 OUTLINE ─▶ 🧑 LOOK ─▶ 📮 PROBE ──▶ 🃏 EVIDENCE        │
  │       ▲      (a person reads the plan       │              │
  │       │       after every ① pass,           │              │
  │       │       before ②③ dispatch)           │              │
  │       └──── the answer changes the plan ────┘              │
  │                                                            │
  └────────────────────────┬───────────────────────────────────┘
                           │ 🚧 ONE gate: the plan AND its evidence
                           ▼
                       ✏️ DRAFT      writes REAL numbers, not holes
                           ▼
                       🖊 REVISE     prose · captions · the rebuild
                           ▼
                       ✅ CHECK      may return to ANY phase above
```

**Why the first part loops.** Evidence does not confirm a plan; it changes it.
Two worked cases from 260819, both on `QPw00-page-loop`:

```text
  the plan said   COMPILE deserves its own division
  the evidence    0 contracts · 0 receipts · 0 ticks, and 0 of 4 split tests
  the plan now    14 divisions, COMPILE folded into §6.4

  the plan said   17 probe cards still at `planned`
  the evidence    checks/values.py recomputed it: 13
  the plan now    13
```

Neither was a defect in the plan. Both are the loop working: a plan written
before its evidence is a guess, and a plan rewritten after it is a plan.

**Why DRAFT moved after it.** DRAFT used to write `<VALUE HOLE>` and wait. With
the evidence already landed it writes the number, so a hole becomes the EXCEPTION
rather than the normal case: it is what a genuinely BLOCKED question leaves
behind, named, with the input that is missing.

## 🧑 A person's attention belongs to the PREPARE loop (260819)

Ruled by JL: "for the user, we will mainly check the outline and the evidences if
we want. But if not, you can just go ahead for the draft and revise and the
compile."

```text
  ┌ ① OUTLINE ⇄ ② PROBE ⇄ ③ EVIDENCE ┐   🧑 ATTENDED · stop here for a person
  └──────────────┬────────────────────┘
                 ▼
     ④ DRAFT → ⑤ REVISE (⑥ COMPILE)      🤖 UNATTENDED · run end to end
                 ▼
     ⑦ CHECK                              🧑 judges, and may return to any above
```

**Why the attention sits there and not later.** The PREPARE loop is where the
page decides WHAT IS TRUE and what it will therefore say. Everything from ④ on is
execution against a plan already agreed: a wrong sentence is cheap to fix, and a
wrong plan has already been paid for in evidence.

**So ④⑤⑥ ask for nothing.** A run that stops between DRAFT and CHECK for a person
is stopping in the wrong place. The ticks that remain are ① `approved:`, the two
③ lane ticks (③c `verified` · ③v `read:`), and ⑦'s two, `accepted:` and the
RULING. ③d leaves no tick behind: its `accepted:` is ⑦'s, per the gathered
table below.

**Every phase says which phase it is, out loud.** JL 260819: "could you then tell
me which phase you are in every time you do it?" A receipt already carries
`phase:`; the same word belongs in whatever a person is shown, because work that
does not name its phase cannot be routed or audited.

Five of the exits below are a person's tick. The others have none, so a machine
may run those end to end without stopping.

## ① 🧭 OUTLINE · `haipipe-page-outline`

```text
❓ ASKS     what will this page say, section by section, and what does each
            bullet still owe?
📥 READS    the Page Type's `outline:` block (fixed | grammar | resolved)
            and the page's current sections
📤 WRITES   <page>/outline/<stem>-outline-v<N>.md
            🚫 nothing in the page itself. The plan and the page are two files.
🚪 EXITS    FOUR machine checks, then a person ticks `approved:`
              ① COVERAGE, both directions: every mark is served by at least
                one card, AND every display unit on disk is cited by some
                bullet's mark or carries `retired:`
              ② every card's `serves:` names a real address in this plan
              ③ every recomputable value matches the repo  (checks/values.py)
              ④ the plan's shape matches its Page Type      (plan-shape-off-type)
✋ TICK     `approved:`  ← a person, and only after the four pass. What the
            person judges is the plan's DIRECTION, never its arithmetic.
🔀 ROUTES   the 🧑 LOOK first, after EVERY pass: a person reads the plan
            before ② or ③ dispatch (haipipe-page-workflow §🧭) · then ② PROBE
            and ③ EVIDENCE, in parallel where their inputs allow (the
            OUTLINE→EVIDENCE edge is legal since 260819) · or a v<N+1> here
            when the evidence that came back changed the plan
```

## ② 📮 PROBE · `haipipe-page-probe`

```text
❓ ASKS     was this already answered, and if not, who answers it?
📥 READS    the plan's marks, once its ① pass has had its 🧑 LOOK
            (`approved:` closes the round, later) · this page's existing
            probe/ and bibex/ · PageX borrows · the task and discovery QA banks
📤 WRITES   <page>/probe/PP<NN>-<slug>/
              card.md · consumer/ · executor/ · proof/ (manifest only)
            state: planned → commissioned
🚪 EXITS    every marked bullet is served by at least one card, and the receipt
            reports `coverage: <n> of <n>`
✋ TICK     none
🔀 ROUTES   ③ EVIDENCE · HOLD (named) · ① OUTLINE for a v2
🚫 MAY NOT  route to REVISE. A card opened and never landed supports no sentence.
```

## ③ 🃏 EVIDENCE · `haipipe-page-evidence` · THREE LANES, IN PARALLEL

The three lanes are not three steps. Each has its own input, its own tick and
its own finish, and none waits on the others. A page may have a verified
citation, no answered value, and no frozen intake all at the same time, and that
is a normal mid-phase state rather than a defect.

### ③c 📚 the citation lane · board page `QPw4c-citation`

```text
❓ ASKS     which published work says this?
📥 READS    the 📚 mark; plus the bank's answer, only when the key was unknown
📤 WRITES   <page>/bibex/<stem>.bib — one entry
🚪 EXITS    the entry carries `verified = {WHO YYMMDD}`
✋ TICK     `verified`  ← a person
🚫 MAY NOT  a machine may SUBSET or TRANSCRIBE a real record. It may never
            COMPOSE one.
```

### ③v 🧮 the value lane · board page `QPw4v-value`

```text
❓ ASKS     what is the number, and which file proves it?
📥 READS    the QA path the dispatched card came back with
📤 WRITES   card.md `state: answered` · its `target:` path · the files pulled
            into proof/
🚪 EXITS    a person ticks `read:`
✋ TICK     `read:`  ← a person, and it REVERTS when target or proof changes
```

### ③d 🖼 the display lane · board page `QPw4d-display`

```text
❓ ASKS     what will a reader SEE, and is it drawn?
📥 READS    a data unit's answered probe card and its proof/, or a concept
            unit's source files, which need not wait for anything
📤 WRITES   <page>/display/<stem>-Display<N>-<slug>/
              intake/manifest.yaml + inputs   ① INTAKE
              recipe/                          ② RENDER
              candidates/ when there are any   ③ PICK
              assets/ · float.tex · preview.pdf ④ BUILD
              README.md with `claim:` `kind:` `accepted: ⬜`
🚪 EXITS    the unit is DRAWN and previewable, and its intake is frozen
✋ TICK     `accepted: ✅` ← a person, and it is CHECK's, not this phase's
🔀 ROUTES   ① OUTLINE, always: the answer either confirms the plan or changes
            it, and only the plan's own gate ends the PREPARE loop
```

⚠️ Steps ② to ④ were REVISE's until 260819. They moved because this lane
returned an intake folder while its two sibling lanes returned a bib key and a
bound number: one lane of three landed nothing a page could use.

## ④ ✏️ DRAFT · `haipipe-page-draft`

```text
❓ ASKS     what does this page promise, and which Aim dies if a hole stays?
📥 READS    the approved outline-v<N>.md
📤 WRITES   <page>/<stem>.md
              the Opening · Content as sentence scaffolds carrying <HOLE>
              the Aims section · the States section · the Log row
🚪 EXITS    every approved Point has a scaffold, and every hole names the Aim
            it would cost
✋ TICK     none
🔀 ROUTES   ② PROBE · ⑤ REVISE · ⑦ CHECK · ④ again
🚫 MAY NOT  open a card. The mark is the proposal; PROBE makes the folder.
```

## ⑤ 🖊 REVISE · `haipipe-page-revise` · with ⑥ COMPILE folded in

```text
❓ ASKS     does the prose now say only what the landed evidence supports?
📥 READS    answered cards · verified bibex entries · frozen display intake
📤 WRITES   the page prose with each landed hole replaced
            the sentence citing each drawn unit, and its caption
            the States rows, updated from visible evidence
            a `> ✎` change record under each rewritten sentence
🚪 EXITS    no hole remains for an answer that landed, and the artifact is
            rebuilt from the current source
✋ TICK     none
🔀 ROUTES   ⑦ CHECK · ③ EVIDENCE when a claim is unsupported · ④ DRAFT when the
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
🔀 ROUTES   CLOSE · ⑤ REVISE · ④ DRAFT · ③ EVIDENCE · ② PROBE · ① OUTLINE · HOLD
🚫 MAY NOT  repair a substantive finding inside the same pass, and may not
            judge a version the same actor produced.
```

## 🧾 The five person-reserved ticks, gathered

```text
tick             lives on                          reserved by            phase
────────────────────────────────────────────────────────────────────────────────
`approved:`      outline/<stem>-outline-v<N>.md    haipipe-page-outline     ①
`verified`       each bibex/<stem>.bib entry       haipipe-plugin-bibex     ③c
`read:`          each probe/PP<NN>-<slug>/card.md  haipipe-plugin-probe     ③v
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
