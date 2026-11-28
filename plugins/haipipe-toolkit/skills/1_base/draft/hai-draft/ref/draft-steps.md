This file holds a draft Task's seven steps (the seven Work tabs) and the Plan gate, moved from `SKILL.md`.

## 🪜 A draft Task's seven steps (b32 s41, on screen 2026-10-20)

A draft Task is worked in seven steps, the seven tabs of its Work (JL 261015: "So it is the Studio, 1, Plan,
..... and Delivery as the last one"). Each tab gives its prompt; this table says what the prompt's verb
does. Only a person signs, ticks, accepts or sends.

| Step (tab) | Its prompt | Owner it loads | Writes | Waits for you |
|---|---|---|---|---|
| 🎨 Studio | `/hai-studio <block> <sNN>` | hai-studio | the Block's `sNN-<topic>/`; what you settle goes into §1 (s41-D25) | optional |
| 📐 1 · Plan | `/hai-draft <task> structure` | hai-draft-logic `ref/context.md`, `ref/structure.md`, `ref/scratch.md` | `draft/records/<stem>-context.md`; `## 1 · Structure`; you type `## 2 · Scratch` here, a note per paragraph (JL 261020: "I think we should move the scratch here") | ✍ Sign: your word in chat ("go with B"); the agent writes it with `page.py sign --quote` |
| ✍️ 2 · Write | `/hai-draft <task> write` | hai-draft-writing `ref/writing.md` | `## 3 · Draft` from §1 and its Scratch (one sentence per Bullet, ⟦pending⟧ where a value waits), keeping the sentences you typed, in a new `-draft-v<N>.md`; the old one to `previous/` | none: a first draft, no rules yet (s41-D26) |
| 🔎 3 · Evidence | `/hai-evidence <task>` | hai-evidence `cards.py` | `evidence/cards.yaml`, `evidence/proposals.md`; cards are CITE and VALUE, one topic (a Task) each, items CITE 1.2 | ☐ you tick each ask |
| 🖼 4 · Display | `/hai-display <task>` | hai-display (its five renderers) | `display/Display<n>-<slug>/`: README (claim, kind, `label: Table 1`, built_on its cards), recipe, assets, preview; shown beside the sentence that calls it | ✍ you write `accepted:` in its README |
| 🔁 5 · Revise | `/hai-draft <task> revise` + your notes (your own sentences are typed in 2 · Write) | hai-draft-writing `ref/revise.md`; hai-draw draft `section_canvas.py` when the Section has a canvas | `draft/records/<stem>-revise.md` rewritten as one pass, the latest (`## Pass <k> · <date> · on draft v<N>`; undecided cards still true carry over, older passes stay in git), first as the venue's reviewer, structure before sentences; one `### <Edit · Review · Section question> · s<n> · <what>` card each: Why, Original, Expected, State; accepted cards into §3 as the next version | ✍ on each card ✓ Accept, ✗ Reject or ✎ Edit its words (the cards file only); then `/hai-draft <task> apply` writes the accepted ones as the next version |
| 📤 Delivery | `/hai-draft <task> deliver`, `check`; `/hai-delivery` render, pull | hai-delivery (`page.py export`, `word_round.py`), hai-draft-review | the Block's `delivery/<jNN>/<tNN>/`; `render/<name>-v<N>/p-<k>.png` | ✍ you send; another round? |

### 🚦 The Plan gate (JL 261111)

The steps run in order, Plan → Write → Evidence → Display → Revise → Delivery, and the sign on the plan is a gate,
not a note (the case: `t01_introduction` of Paper-ScalingGlucose-NatSeries2026 was written, rebound and revised
twice on a plan never signed, then its structure came into question).

1. **Every later step reads the plan state first.** Write, Evidence, Display and Revise open the current Draft
   Markdown; if `approved:` does not start with ✅, the reply starts at 1 · Plan whatever the prompt named ("revise
   in a loop", "make v0.11"): show the `## 1 · Structure` map, propose 2 to 4 structure versions with one lean
   (hai-draft-logic, Propose first), and wait.
2. **The sign is the person's word in chat** ("go with B", "this structure"). The agent writes it, never decides it:
   `page.py sign <task> --quote "<their words>"` sets `approved: ✅ <who> <yymmdd> · in chat: "<quote>"` and keeps the
   row that governs the Task (its Job's `## Narrative` row; only an older Board whose Story § 8 still holds Section
   rows uses that row) as text in `draft/records/<stem>-sign.md`; no hash, health compares the text. No button, no
   second loop.
3. **Written before the sign is out of order.** `page.py health` gives `order` WARN when `## 3 · Draft` exists on an
   unsigned plan; `health --final` makes it FAIL. The plain "plan not signed" line stays a WARN at the final gate
   while no § 3 exists, because the sign is the person's.
4. **A moved row sends the Section back to Plan.** When the governing row changes after the sign, `health` gives
   `row` WARN (FAIL at `--final`): re-propose against the new row, then sign again.
5. **A version's Narrative is signed first.** In a Job whose face has `## Narrative` (a paper version: that venue's
   layout, one row per Section), the person signs that Narrative before any Section's plan: `page.py sign-narrative
   <job> --quote "…"` writes `narrative-approved: ✅ JL <yymmdd> · in chat: "…"` and a readable `story-at-sign:` on the
   face's header and keeps the Story's § 8 (the shared narrative: title, story, claims) as text in
   `<job>/records/narrative-sign.md`. Then each Section's `page.py sign`. Section health gives `narrative` WARN while
   the version's Narrative is unsigned or the Story's § 8 has moved since (FAIL at `--final`).
6. **Revise checks the structure before sentences.** If the structure fails, the pass holds Section question cards
   only and returns to Plan (hai-draft-writing `ref/revise.md`).

The old controller operations still answer and map onto the steps: CONTEXT and OUTLINE are 1 · Plan,
EVIDENCE is 3 · Evidence and 4 · Display, CONTENT is 2 · Write and 5 · Revise, CHECK is Delivery's `check`. The screen reads
the files above on every open and writes none of them (`servers/workbench/workbench-task-draft/page_shell/draft_steps.py`);
its chips are the state: Plan `✍ sign` until `approved:` starts with ✅, Revise `🔁 pass k` by
`draft/previous/`, Evidence `🔶 asked` while an item or a proposal waits, Display `✍ sign` while a built unit waits for
your `accepted:` (`· optional` when the text calls no Table or Figure). A Job's Work shows each Task's
seven chips, a click each into that tab. Your own words go straight in: 2 · Write and 5 · Revise open, in Work and
Report, with the Page's paragraph boxes (`outline_revise.py`), and 1 · Plan with its Scratch boxes
(`outline_scratch.py`); a paragraph box shows one sentence a row, typed freely, each sentence matched back to the
Bullet it reads like, and it
saves into the draft when you leave it or press Cmd+Enter; Esc puts back what it held.
