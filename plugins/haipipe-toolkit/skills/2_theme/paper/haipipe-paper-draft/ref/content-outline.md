How a Section's Content outline resolves from the venue's Sec- division, its kind maps, and its sentence-slot plan; moved from SKILL.md.

## 🧱 Content outline

**Outline mode (also in this file's frontmatter, which the Skill tool strips):**
`mode: resolved` · source = the bound QBv desk division (`structure-source:` +
`structure-division:`, via `cli/resolve-structure.py`) · fallback =
`generic-template.md` · one `## C<n>` per Content division of the page, so a
flat section is `C1` with one paragraph group per move · one bullet per
sentence slot.

Resolve paragraph or move divisions from the QBv Venue Page named by the
version face (its venue; an older Board: the Story §8 row's `target` column). **Address the division by grep, never by a
remembered name or number** (0.5.0):

```bash
grep -n '^### [0-9]* · Sec-' <venue-bank>/QBv<n>-<desk>/QBv<n>-<desk>.md
```

The heading is `### <n> · Sec-<n>-<Kind>: <tagline>`, so the token is followed
by a colon and prose; match the token, never the whole line. Its NUMBER moves
between desks: MISQ's abstract is §4, Nature Communications' is §3, and PNAS §3
is Sec-0-Significance with the abstract at §4. Cite the whole address in
`structure-source`, both the number and the `Sec-` token, so a re-read can
prove it.

**`cli/resolve-structure.py` does this and prints the verdict**, so no page has
to trust a remembered mapping:

```bash
python3 <skill>/cli/resolve-structure.py <QBv page>.md <section page>.md
python3 <skill>/cli/resolve-structure.py <QBv page>.md --all <group>/   # a board
```

### The kind-to-token map · not derivable by casing

Two of the nine differ from their kind by more than capitalization, which is
why an agent must read this table and never transform the string itself:

```text
section_kind        Sec- token              note
────────────────────────────────────────────────────────────────────────────
abstract            Sec-0-Abstract
introduction        Sec-1-Introduction
literature-review   Sec-2-Related-Work      ⚠️ different word · absent at MISQ,
                                            present at QBv9/10/12
theory              Sec-2-Theory            shares the number 2 with
                                            Related-Work across desks
methods             Sec-3-Methods
results             Sec-4-Results
discussion          Sec-5-Discussion
conclusion          Sec-6-Conclusion
appendix            Sec-A-Appendix          ⚠️ letter, not a digit
```

Raw pack `style.md` files and stage-era playbook material stay informative: they
may feed a typed PACK OBSERVATION on the QBv page, but they may not become
`structure-source`.

### The kind-to-division map · four relations, not one

`section_kind` does not equal a `Sec-` token, and the mismatch has four
different remedies. Naming only one of them is what made every Section fall
silently to the fallback:

```text
relation            what it looks like                     what to do
──────────────────────────────────────────────────────────────────────────────
EXACT               one kind, one Sec- division            resolve · cite the
                    abstract → Sec-0-Abstract              address
SHARED              one division serves several Pages      resolve · SPLIT the
                    methods → Sec-3-Methods (2 Pages)      division's word and
                    appendix → Sec-A-Appendix (6 Pages)    move budget on the
                                                           version's Narrative row, never
                                                           give each Page the
                                                           whole budget
ABSENT BY DESIGN    the desk HAS no such unit and the      fallback · record the
                    paper keeps the section anyway         DEVIATION on the
                    literature-review at MISQ              Narrative row · do NOT
                                                           raise a QBv gap
MISSING             the desk should have the division      fallback · raise the
                    but the page has not been written      gap on the QBv page
                    8 of 17 desks carry zero Sec- rows     · the desk owes it
```

**The ABSENT BY DESIGN row is the one 0.4.0 lacked.** MISQ publishes no
related-work unit, and a paper may still keep one as a deliberate deviation a
person ruled. Raising that as a gap tells the venue bank to invent a division
the desk does not have, which corrupts a consumer-neutral asset to suit one
paper. The deviation belongs on the Section's row in the version's `## Narrative`, where the target decision lives.

**Eight desks resolve to nothing today** (QBv5-jama, QBv7-jama-network-open,
QBv8-npj-digital-medicine, QBv9 partially, QBv11-nature-human-behaviour,
QBv14-diabetes-care, QBv15-grant, QBv16-patent, QBv17-wise carry zero `Sec-`
divisions). For those, `mode: resolved` is aspirational: every Section takes the
generic fallback and the gap is real. Say so in `structure-source` rather than
letting the page read as venue-resolved.

Each Content division states:

```text
reader move
claim ids advanced
evidence/citation/value/display bindings
expected prose or display placement
transition to the next move
known limitation or unresolved need
```

**A Section quotes, it never computes (0.20.0, JL 261110).** Every number in its prose is a value id of the value
Job, bound by id, and the Section names the value Run it quotes (its VALUE card or binding says the Run, never "the
newest"). A number with no id gets one in the value Job first; a binding goes stale when an id it quotes moves or leaves
in a newer value Run, and stays current when that Run only adds ids (haipipe-paper-evidence, The chain; `chain_check.py` says where it breaks).

**The plan is a list of sentence slots (0.5.3, JL 260831).** One bullet is one
sentence slot, `s<n> · <what the sentence does>` in 4 to 11 plain words;
paragraphs group by move (`### C2.P1 · Problem and question · s1 to s3`); a
finding carries its claim id plus a word (`s6 · C1: <the number and its unit>,
comparison owed`); one `Cut:` bullet names what leaves the section and where it
goes; a Note is one line and never the drafted sentence, which lives on the
page. The approved specimen is quoted in `workbench-task-draft` §✂️.

**Structure and Draft move together (JL 261102: "when you update the draft, you should also udpate teh structure as
well")**. A Draft Markdown's `## 1 · Structure` is the plan of its `## 3 · Draft`, so every edit to the sentences
makes the same change to the plan in that edit: a sentence added or cut adds or cuts its Bullet (`- B<k> · s<n> ·
[Role] what it does`, with its `Evidence:` line), a sentence moved moves its Bullet, a paragraph added, split, merged
or renamed changes its `### C<n>.P<m> · <title> · s<a> to s<b>` heading in sections 1, 2 and 3 and its entry in the
Structure Overview, and the S numbers and spans are renumbered to match. A new structure is a new draft version
(`draft-v<G>.<S+1>`, the older one moved to `draft/previous/`), never a section 3 rewritten under the old plan; its
Evidence Items and the face's `evidence-allowlist:` follow their sentences. `page.py health <Task>` checks it
(`structure`: `plan_layout.structure_draft_mismatches`, the paragraphs, titles, sentences and Overview spans of
sections 1 and 3) and fails until both agree.
