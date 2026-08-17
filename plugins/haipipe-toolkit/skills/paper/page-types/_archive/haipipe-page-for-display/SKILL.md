---
name: haipipe-page-for-display
description: >-
  The VARIANT contract for a DISPLAY unit Page: one page per display unit a paper or application ships, such as a figure, table, or diagram, mirroring the unit's folder (float, assets, caption, provenance) and carrying the human acceptance that no file in that folder can hold. It loads haipipe-page for the base frame and adds only what a display page needs: Content that mirrors the unit rather than arguing a question, the acceptance ladder from requested through rendered to accepted-into-prose, the rule that every shown number carries provenance from a Value binding or a named run, and the placement record binding the unit to the sentence that cites it. Use when writing or fixing a display page, when a rendered unit was never accepted by a person, when a figure shows a number nothing traces, or when a unit ships but no sentence points at it. Trigger: display page, display unit, S-Display, figure page, table page, float, preview, caption, acceptance, placement, /haipipe-page-for-display.
metadata:
  version: "0.1.2"
  last_updated: "2026-08-10"
  summary: "Formal Paper Display units remain acceptance-gated, now fed only by Narrative-selected Value or Literature Display candidates."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-display · a unit you can look at, and the acceptance it waits for

**LOAD `haipipe-page` FIRST.** It owns the base frame. What this file guards is ACCEPTANCE: a person says yes to one specific render, and no file in the unit's folder can hold that judgment for them.

**The kind this variant covers**: one page per display UNIT.

```
kind      subject                              closes when
──────────────────────────────────────────────────────────────────────
Display   ONE unit's folder: float · assets ·  a person ACCEPTS the rendered
unit      caption · source recipe               unit into the work
```

**The type key.** A display page declares `page-type: display` in its frontmatter, and the line is REQUIRED: display unit pages wear stage filenames (`S-Display-4c-…`), so without the key the resolver reads them as plain stage pages. The `page-type:` key beats the filename (base, type resolution step ③).

**Where it stands beside the mirror type**: a Skill page and a display page are both mirror-shaped, and they differ in the two facts that matter. A Skill page mirrors a unit maintained ELSEWHERE and closes when that unit ships; a display page mirrors a unit THIS project produces and closes only when a person accepts it. Shipping is an event; acceptance is a judgment. That difference is why display stands alone rather than riding `-for-skill` (JL 260805), and why its `state:` line is a gate position no machine may flip.

## 🧪 Candidate Display before Paper Display

A formal Display unit is not the first place an insight becomes visible. Each Value or Literature probe owns a same-numbered candidate card under `display/<topic>/<n>-<slug>.md`. It records a possible table, figure, matrix, or map; its takeaway; its claim role; and one disposition: `candidate`, `selected`, `paper-bound`, `parked`, or `not-displayable`.

Narrative reads those cards alongside the claim ledger. It may select one only when it has a named claim and a clear rhetorical role. **Only a `selected` card may file the request that opens this formal unit.** This keeps the distinction crisp: candidate display explores and makes evidence legible; Paper Display is the accepted, placed float the manuscript ships.

## 🪜 The acceptance ladder

A display page's state answers one question: how far up this ladder is the unit?

```
① REQUESTED    the need exists · what the unit must show, and for which claim
② SOURCED      the producing run or recipe is named · nothing rendered yet
③ RENDERED     preview exists · a person can LOOK at it
④ ACCEPTED     a person said yes to THIS render · dated, on this page
⑤ PLACED       a sentence cites it · the placement record names the sentence
```

A unit may fall back down: a re-render after acceptance returns to ③, because acceptance was of a specific render, not of the unit's name. The page's Log carries each rung with its date.

## 🎭 The four Page Phases, and the ONE place they are the same act

A display page runs the base's four phases like any other page, and it ALSO carries the ladder above. They are not the same list and must not be collapsed into one, because they govern different objects:

```
  the four phases   govern THIS PAGE, the document      who is writing it, and how far
  the five rungs    govern THE UNIT, the thing on disk  how far the artifact itself got
```

Both can be true at once and neither is wrong: a page sitting in REVISE while someone rewrites its Content can own a unit still at rung ③. Collapsing them would make "an editor fixed a sentence" mean "the figure went back to unrendered", which is absurd and is why the two lists stay two.

They do line up, and the alignment is worth stating because it tells a writer which phase they are actually in:

```
  DRAFT    open the page, state what the unit must show and for which claim   ≈ ①
  EVIDENCE    go and get the evidence: name the producing run, land its data     ≈ ②
  REVISE   draw it, write float.tex, compile preview, ship to displays/       ≈ ③
  CHECK    a person looks at THIS render and says yes                         ═ ④
           ⑤ PLACED falls OUTSIDE the four: it is the next round's REVISE,
           because binding a unit into a sentence is an edit to prose
```

The first three are `≈`, a correspondence. The fourth is `═`, identity: **CHECK and rung ④ are one human act, not two.**

## ⛔ Why THIS type's CHECK may not be delegated

Every other type's CHECK can be run by a fresh reviewer: a cold read plus the mechanical checker is exactly what judging prose needs, and a reviewer who did not write the page is the point.

A display page's CHECK cannot. What it judges is **what a picture looks like**, and no cold read of the markdown reaches it. A reviewer agent asked to CHECK a display page will read the page, find it consistent, and route CLOSE, having never looked at the render at all.

So, binding:

- A display page's CHECK is a HUMAN GATE. `haipipe-page-orchestrator-agent` may run DRAFT, EVIDENCE and REVISE for a display page and must STOP at CHECK, leaving the page at ③ with the reason recorded.
- No agent, reviewer or otherwise, may write rung ④ or move `state:` past ③. This restates the rule already in this file, that the state line is a gate position no machine may flip, and NAMES the phase it belongs to so an automatic loop cannot reach it by another door.
- The failure this prevents is on the record: on 260806 a machine wrote a rung ④ onto `QBt3-for-display`, the specimen page for this very type, and five downstream claims were corrected when the cold read caught it. Nothing in the contract had said which PHASE that gate lived in, so an orchestrator had no rule to obey.

## 🔢 Every shown number carries provenance

A display is where an untraceable number hides best, because a figure asserts without a sentence. The rule is the Value route's rule, applied at the unit:

```
each number the unit shows  →  a Value binding on a Value topic page, BY PATH,
                               or the producing run named on this page
🚫 a rendered number nothing traces is a defect of THIS page, even when
   the figure "looks right"
```

## 🔗 The placement record

A unit that renders well but is cited by no sentence is not finished. The page carries one placement record per consumer: which section, which sentence, and whether the citation landed. An accepted-but-unplaced unit is a visible open row, never a silent success.

**The template.** `template.md`, beside this file. ONE template serves every page of this type: two pages of it differ in what they say, never in what shape they are, so nothing has to be resolved before writing one. Copy it, fill every `<slot>`, and delete each RULE comment as you satisfy it.

## 📥📤 What this page reads, and what it hands on

**A page is a unit of work**: it reads something and hands something out (`QB6` §7). For a display page both sides are folders, and the shipped side is generated.

```text
 📥 INPUT   <stage>/display/<page name>/            ✍️ authored, seven parts
              source/       gen_*.py · the data file · any shared plot style
              candidates/   the renders that LOST, kept with the reason
              assets/       the SELECTED artifact, plus a generated README manifest
              float.tex     the figure/table env, the caption and the \label
              preview.tex   standalone wrapper, compiled from the PAPER ROOT
              preview.pdf · preview.png    the render a person judges at rung ④
              README.md     Reader Takeaway · Claim Supported · Evidence Source ·
                            Placement · Caption Job · Fragility · Status

 📤 OUTPUT  <paper root>/displays/<page name>/      🤖 GENERATED, never hand-edited
              float.tex     asset paths rewritten to point inside displays/
              assets/       the selected artifact only
              ▶ a section then \input{displays/<page name>/float.tex}
```

The unit folder is NAMED FOR THE PAGE THAT OWNS IT. That is what makes the page-to-unit join a lookup instead of a regex guess, and the guess used to fail silently and paint a 🔴 unit green.

**To update a paper's display layer, these four commands are the whole procedure.** `<skill>` is `board/haipipe-board`, and `<stage>` is the stage folder holding `display/`:

```bash
python3 <unit>/source/gen_*.py                              # redraw the artifact
python3 <skill>/cli/build-displays.py <stage>               # ship to displays/
python3 <skill>/cli/build-displays.py <stage> --check       # non-zero if stale
python3 <skill>/cli/asset-manifest.py <stage>               # refresh assets/README.md
python3 <skill>/cli/display-report.py <stage>               # the display -> section map
```

Every one takes the STAGE as its argument and finds the paper root from it. On a real paper that is two levels up; a specimen stage carries its own under `_fixture/`. The tools live in the board engine and nowhere else: a paper that keeps its own copy has a fork that will drift.

⚠️ **`displays/` is a build target.** Editing anything under it is overwritten on the next build. Fix the unit, or fix the generator.

## 📂 Files

```
haipipe-page-for-display/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-page`; the number rule leans on `haipipe-page-for-value`; the paper family's display machinery (renderers, request rows, the displays/ folder shape) stays in the paper and display families, which this contract names but never contains.
