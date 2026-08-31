# Page · the kinds: Q, stage, design, and what admits one
state: 🟡 WORKING · two-kind roster ruled, both specimens exist · open: the engine reads no `page-type:`
owner: JL
method: the admission law first, one division per surviving kind, and one table saying where every reduced kind lives now; the pre-sweep record is archived whole

## Opening
Which page KINDS exist on a board, and what admits a new one?

Three: the base Q page, and two kinds that change what closing means, `stage` and `design`.
The admission law is that one sentence: a kind survives only if it changes what CLOSING means, because a kind that only changes what a page looks like is a template, and a kind that only holds material is a plugin.
Five kinds reduced to two on 260815 under that law, and this page's table says where each one's job lives now.
The hub succeeds when a writer with a new page knows in one read whether it is a Q, a stage, a design, or just material for a plugin.

**Covered elsewhere**: `QPs1` owns the sections every kind shares; `QPs3` and `QPs4` are the two living specimens; `QPf1` owns the plugin law the reduced kinds fell into; the `haipipe-page` unit (plugged on `QPs1`) owns type resolution across all families, including the paper dialect's own variants.

## Diagram
**Three kinds, three meanings of closed**: what a page must be measured against.
```text
  📋 Q · the base          closed = the QUESTION is settled
                           and its Law has a home
  🪜 stage                 closed = a HUMAN GATE passed in a
                           lifecycle chain (QPs3 the specimen)
  🧩 design                closed = a SELECTION record: candidates,
                           the ruling, the loser kept (QPs4)
  ─────────────────────────────────────────────────────────────
  everything else that once wore a kind is a PLUGIN or a
  design page now, and the table in Content says which
```

## Content
### 1 · The admission law
**One test**: a kind must change what closing means.
```text
  ✅ admits    a new definition of CLOSED, with a specimen page
  ❌ refuses   a look, a template, a folder shape, a material home
```
The law is enforced specimen-first: a kind is admitted by building one real page and then writing the contract that page taught, which is how `QPs3` and `QPs4` were born.
A kind that decides nothing has no question to ask, so its pages converge on one prose, and that measured disease is what reduced the roster.

### 2 · The two kinds beyond base
**Stage and design**: the survivors, one sentence of contract each.
```text
  🪜 stage    S-<Family>-<unit> · one lifecycle stage of a paper or
              application · a chain with a managed span and a human
              gate at its end · specimen QPs3
  🧩 design   Design-<n> or page-type: design · candidates side by
              side, closing on a SELECTION record · the loser is
              recorded, never silently deleted · specimen QPs4
```
A design page may relate to several shipped units, and its title carries each unit's version, refreshed by `skillpage.py plug` rather than typed.
The paper family ships its own dialect of variants (venue, section, display, literature, value, narrative, dash, view); those are `haipipe-page`'s to route and this board's roster does not list them.

### 3 · Where the reduced kinds live now
**The table of departures**: every job survived, no kind did.
```text
  was a kind        now                              ruled
  mirror (Skill-n)  a design page + skill/ plugin    260815 · QPs1 §11.2
  for-skill         the skill/ plugin                260815
  for-meeting       the meeting/ plugin              260815
  for-slide         the slide/ plugin + ✨ autodeck   260815 · QPf3
  (chat pages)      the chat/ plugin                 260815 · QPf4
```
Each departure's full story is on the page that ruled it, and each pre-reduction record is archived whole.
The shipped units followed the ruling: `haipipe-page` 0.26.0 dropped the `page-type: slide` resolution key and `page-types/haipipe-page-for-slide/` left the family; `for-skill` and `for-meeting` still ship and their retirement rides the family reorg.

## Aims
- [ ] ⚙️ The engine reads the `page-type:` key
      Today `parse.py` resolves kind from the FILENAME alone, so `page-type: design` on a Q-named page decorates and decides nothing; either the key becomes load-bearing or the contract says filename is the only resolver.
- [ ] 🗑 for-skill and for-meeting leave `page-types/`
      The last two shipped variants that contradict this roster; they ride the family reorg.
- [ ] 🧪 A checker rule polices the roster
      Nothing today flags a page wearing a retired kind key; one rule in `check.py` closes the door the reductions opened.

## Discussion

### From the retired States section (merged 260831)
The roster is ruled and lived: both surviving kinds have specimens, ten mirror pages converted on 260815, and the slide reduction completed the same day through to the shipped unit.
What remains is enforcement, which is the first and third aim, and the two stragglers in the second.

## Files
- `3-QPs-page-structure/QPs3-for-stage/QPs3-for-stage.md`
  The stage specimen.
- `3-QPs-page-structure/QPs4-for-design/QPs4-for-design.md`
  The design specimen.
- `../../board/haipipe-page/SKILL.md`
  Type resolution across all families; its plugged snapshot sits on `QPs1`.
- `_archive/QPs2-page-types-260815-pre-sweep.md`
  This page's full pre-sweep record: the ten-type world, the QBt specimen lane, and the application-step findings.

## Log
- 260815 2050 · [REVISE-CC, JL delegated] swept to the two-kind world ("keep the things with slides like the plugin"): the ten-type roster, the QBt specimen lane, and the 260807 application findings moved whole to `_archive/QPs2-page-types-260815-pre-sweep.md`; this page now states the admission law, the two survivors, and the departure table only.
- 260815 1730 · [REVISE-CC, JL ruled] for-slide left the roster: a deck is plugin material at `<page>/slide/`, ruled on `QPf3`; third kind reduced after for-skill and for-meeting.

- 260831 0113 · `## States` merged into `## Aims` (tick + `Now:` per Aim; asks and threads kept verbatim), skill 0.148.0