# Patent: the one venue where a single sentence is the deliverable and everything else supports it

state: 🟡 PARTIAL · 3 jurisdictions as README delta tables · no outlet tree · no exemplars
owner: JL
method: state what the word claim means in a filing as against in a paper, record the three jurisdiction deltas, and keep this pack's word collision with the Claims stage from doing damage

## Opening

Every other venue in this tree accepts a document, but a patent office accepts one sentence. What does that change?
> ✎ Every other venue in this tree accepts a ~document. A~ *document, but a* patent office accepts ~a sentence,~ *one sentence. What does that change? That sentence is the patent claim,* and the ~rest of the~ *whole* filing ~exists~ *is written* to support it. ~What does that~ *The trap is the word: a patent claim in a filing and a lifecycle claim in the paper are two different objects sharing one name. This page states what the* inversion ~change?~ *costs, fixes the word so a revision pass cannot soften the wrong object, and gives each office its own division.* · CC · 260802 1542
That sentence is the patent claim, and the whole filing is written to support it.
The trap is the word: a patent claim in a filing and a lifecycle claim in the paper are two different objects sharing one name.
This page states what the inversion costs, fixes the word so a revision pass cannot soften the wrong object, and then takes the three offices one at a time.
> ✎ This page states what the inversion costs, fixes the word so a revision pass cannot soften the wrong object, and ~gives each office its own division.~ *then takes the three offices one at a time.* · CC · 260802 1542

**The word collision, and the only defence against it**: spell the word out every time.
The lifecycle has a Claims stage, and a filing has patent claims.
> ✎ ~It also produces the most dangerous word collision in the paper system.~ The lifecycle has a Claims ~stage. A~ *stage, and a* filing has *patent* claims. They are ~not the same object~ *different objects that share one word,* and the pack's `-> Claims` map runs ~straight through~ *from one to* the ~ambiguity.~ *other without warning anybody.* · CC · 260802 1542
They are different objects that share one word, and the pack's `-> Claims` map runs from one to the other without warning anybody.

**Where this page sits**: it is one venue target in `QBv`, and the only one in its pack.
This page owns only what is true of `playbook-patent`.

**Why this pack has no outlet tree**: jurisdictions are not journals.
CNIPA, USPTO, and EPO each prescribe their own specification order, their own patent claim form, and their own abstract limit.
> ✎ CNIPA, USPTO, and EPO *each* prescribe ~different~ *their own* specification ~orders, different~ *order, their own patent* claim ~forms,~ *form,* and ~different~ *their own* abstract ~limits, and the~ *limit. The* pack encodes ~them~ *those differences* as delta tables in ~`README.md`. That is~ *`README.md`,* the same declared exception `QBv15` carries. · CC · 260802 1542
The pack encodes those differences as delta tables in `README.md`, the same declared exception `QBv15` carries.

**What is unusual about its lifecycle**: the pack documents a drafting process, which no journal pack does.
A filing is prosecuted over years rather than submitted once.

## Writing Style

How this page must be written. Read it before editing, and edit to it.

**Inherited from `QB4`**: the page grammar, the section order, and the sentence rules come from `QB4-overall.md` and are not restated here.

**Never transcribe the jurisdiction table**: it lives in `playbook-patent/README.md` and is cited, never copied.

**Always disambiguate the word claim on this page**: write `patent claim` or `lifecycle claim`, never a bare one.
The collision is the single most likely source of a wrong action anywhere in this group.

✅ `a patent claim is the deliverable`  ❌ `the claim is the deliverable`

**Say the jurisdiction office, not the country**: CNIPA, USPTO, EPO, because the deltas are the offices' rules.

## Diagram

**One sentence, three jurisdictions**: and a word that means two different things.

```text
  ⚖️ THE INVERSION
     journal ── the DOCUMENT is the deliverable
     patent  ── the PATENT CLAIM is the deliverable,
                the specification exists to support it

  🌍 THREE JURISDICTIONS
  ┌──────────────┬──────────────┬─────────────┬──────────────┐
  │              │ CN · CNIPA   │ US · USPTO  │ EP · EPO     │
  ├──────────────┼──────────────┼─────────────┼──────────────┤
  │ patent claim │ two-part,    │ single-     │ two-part     │
  │              │ character-   │ clause      │ "character-  │
  │              │ izing clause │ "compris-   │ ised in      │
  │              │              │ ing"        │ that", Rule  │
  │              │              │             │ 43(1), where │
  │              │              │             │ appropriate  │
  │ abstract     │ <=300 chars  │ <=150 words │ ~150 words   │
  │              │              │ 15 lines    │ no merits    │
  │ drawings     │ "Figure 1"   │ FIG. 1      │ FIG./Figure 1│
  │ ref signs    │ in the       │ inline      │ separate list│
  │              │ drawings     │             │              │
  │              │ description  │             │              │
  │ utility mdl  │ 10 yr, avail │ none        │ none         │
  └──────────────┴──────────────┴─────────────┴──────────────┘

  ⚠️ WORD COLLISION
     lifecycle "Claims" stage  ≠  patent claims
     and the pack's  ->Claims  map crosses exactly here

  🚫 no outlet tree · 🚫 no exemplars · taste.md at FAMILY level
```

## Content

### 1 · The inversion, and what it does to the lifecycle

**The specification supports the patent claim**: every artifact the paper system produces changes role.

```text
  📄 journal            📑 filing
  ──────────            ─────────
  the document IS   ▶   the PATENT CLAIM is the deliverable
  the deliverable       the specification SUPPORTS it

  ── a figure is not illustration, it is support for a
     limitation, and its reference signs are load-bearing
  ── background is not motivation, it is what the patent
     claim must be distinguished FROM
  ── the abstract is a length-capped formality, and the
     EPO forbids stating merits in it
```

⚖️ Establishes the inversion as the pack's core content, so every stage map here reads differently from a journal pack's.
> ✎ ⚖️ Establishes the inversion as the pack's core content, ~which is why~ *so* every stage map here reads differently from a journal pack's. · CC · 260802 1542

#### 1.1 · Prosecution is a lifecycle no journal pack has
(so this pack documents a drafting process rather than a submission)
The pack's README carries a drafting process under its Write/Edit map.
A filing is amended against office actions over years, which makes the closest paper analogue `QB10` Round rather than a submission.

### 2 · The word collision, and how to survive it

**Two objects, one word, and a stage map that crosses between them**: this is the pack's real hazard.

```text
  🧩 LIFECYCLE CLAIM        🧩 PATENT CLAIM
     an assertion the           a legally construed sentence
     paper argues and           defining the boundary of the
     evidence supports          monopoly
     lives in 1b-claims         lives in the filing itself
     can be softened            cannot be softened without
     during revision            narrowing the right

  💥 the pack's  ->Claims  map points the lifecycle stage at
     the filing's patent claim set, and nothing in the
     wording of either says they are different objects

  🛡 the mitigation is vocabulary, not structure:
     write "patent claim" or "lifecycle claim", always
```

⚠️ Establishes the collision as a naming hazard with a naming fix, rather than a structural problem to re-architect.

#### 2.1 · Softening is safe on one side and destructive on the other
(which is why the two must never share a revision pass)
A revise pass that hedges a lifecycle claim improves it.
The same pass applied to a patent claim narrows the granted right, and the pack has no guard that would stop it.

### 3 · Three jurisdictions, no exemplars

**The deltas are precise and there is nothing granted on disk to imitate**: the same hole `QBv15` carries.

```text
  ✅ the jurisdiction table is specific and correct
     patent claim form · spec order · reference signs ·
     abstract limits · drawing labels · utility model
     availability · term

  📭 0 exemplars
     ── no granted CNIPA specification, no USPTO Detailed
        Description, no EPO Reference Signs List
     ── and the README again calls Write/Edit "the main
        purpose"

  🔀 taste.md at FAMILY level ── the same placement as
     playbook-grant and playbook-pnas, undeclared
```

⚠️ Establishes the pack as structurally correct and linguistically ungrounded.

### 4 · CNIPA, and the only route that is not an invention patent

**One office, two filing routes, and a prescribed order that stops before the patent claims**: CNIPA is the only row in the pack that offers a second kind of right.

```text
  📜 CNIPA · the delta table in playbook-patent/README.md
  ┌──────────────────────────────────────────────────────────┐
  │ spec order    Title · Field · Background · Disclosure ·   │
  │               Drawings · Embodiments                      │
  │ patent claim  two-part, with a characterizing clause      │
  │ abstract cap  300 Chinese characters                      │
  │ drawing label Figure 1                                    │
  │ ref signs     inside the Brief Description of Drawings    │
  │ utility model available · 10 years · formal examination   │
  │               · apparatus patent claims only              │
  │ invention     20 years · substantive examination          │
  └──────────────────────────────────────────────────────────┘

  ⚖️ the patentability bar · the drafting process, step 2
     novelty and inventive step assessed under Art 22

  🔀 the utility model · the pack's ->Claims map
     apparatus and device patent claims ONLY, no method
     patent claims, and a lower inventive-step bar

  ✍️ language rules the table does not carry · style-profile.md
     the filing language is Chinese
     a dependent patent claim recites its parent explicitly
     title concise, typically under 25 characters
```

📜 Establishes CNIPA's prescribed order and the utility model as a route choice that has to be made before any patent claim is drafted.

#### 4.1 · The order in the table is shorter than the order in the same README
(so a CNIPA draft built from the table alone ships without two required parts)
The delta table's CNIPA spec order runs Title, Field, Background, Disclosure, Drawings, Embodiments, and stops there.
The filing-order list under the same README's `-> Minimap` map carries the patent claims and the Abstract after the Detailed Description.
> ✎ The filing-order list under the same README's `-> Minimap` map carries ~Claims~ *the patent claims* and *the* Abstract after the Detailed Description. · CC · 260802 1542
Nothing states that the short row is an elision of the long list, so the two missing parts read as an absence.
The USPTO row on the same table does name the Abstract, so the CNIPA row looks deliberate rather than truncated.
> ✎ The USPTO row on the same table does name the Abstract, ~which is what makes~ *so* the CNIPA row ~look~ *looks* deliberate rather than truncated. · CC · 260802 1542

#### 4.2 · The utility model is a patent-claim decision, not a formatting one
(which is why it cannot be deferred to the compile step)
The pack's `-> Claims` map bars method patent claims from a utility model outright.
A patent claim set drafted around a method therefore cannot be refiled as a utility model without being redrafted from the concept up.
The README places the invention-versus-utility-model choice in the filing's STATUS.md venue field, which is read when the venue is pinned, one stage before patent claims exist.

#### 4.3 · Format values
(two of the four metrics are recorded for this office, and the other two are absences the pack never fills)

```text
  📏 WORDS            abstract 300 Chinese characters · title typically under 25
                      characters · specification length not recorded by the pack,
                      here or at any other office
                      [README.md, per-jurisdiction delta table under the
                      -> Minimap map, Abstract limit row; style-profile.md,
                      Title and Abstract]
  📚 CITATION DENSITY not recorded by the pack
                      a filing cites prior art, not literature, and the pack sets
                      only what the Background DOES with it: the closest prior
                      art's specific technical deficiencies, never a review
                      [style-profile.md, Specification]
  🔢 VALUE DENSITY    not recorded by the pack, and absent by construction
                      this pack has no style.md, and none of the venue tree's 95
                      style.md files records the metric either
                      a filing's numerals are mostly reference signs tying a
                      drawing element to the text, which is a different object
                      from a result value [README.md, -> Display]
  📊 DISPLAYS         "Figure 1", rendered in English on this board · reference
                      signs inside the Brief Description of Drawings
                      [README.md delta table, Drawings label and Reference signs
                      list rows]
                      block diagrams, flowcharts, schematics · every component and
                      step carries a reference numeral consistent across every
                      figure and every mention [README.md, -> Display]

  ⚠️ blueprint-only bites here: stages/section-kinds.yml declares no kinds for
     playbook-patent, so a stage resolving packs: gets zero hits, while the CNIPA
     rules style-profile.md does carry, the two-part form, the 300-character cap
     and the 25-character title, are loaded by nothing.
```

#### 4.4 · The language, in the filings' own words
(the pack stores no granted CNIPA specification, so what follows is its own formulation, rendered in English)
The pack's CNIPA cells are written in Chinese and this board is English-only, so every phrase below is a rendering rather than a quotation from a filing.
The two-part connector renders as "characterized in that".
> ✎ The two-part connector renders as "characterized in ~that", and it~ *that". It* is what makes a CNIPA patent claim two-part: preamble, *then* connector, *then* characterizing clause [style-profile.md, Per-jurisdiction language notes]. · CC · 260802 1542
It is what makes a CNIPA patent claim two-part: preamble, then connector, then characterizing clause [style-profile.md, Per-jurisdiction language notes].
The dependent recital is given as a fixed pattern: it names its parent patent claim by number, then repeats the connector.
> ✎ The dependent recital is given as a fixed ~frame that~ *pattern: it* names its parent *patent claim* by ~number and~ *number,* then repeats the ~connector, rather than as~ *connector. It is not* a sentence lifted from a ~grant~ *granted filing* [style-profile.md, Claims]. · CC · 260802 1542
It is not a sentence lifted from a granted filing [style-profile.md, Claims].
The Summary states an advantage as "because the [structure] is adopted, the [effect] is obtained".
> ✎ The ~Summary's advantages frame renders~ *Summary states an advantage* as "because the [structure] is adopted, the [effect] is ~obtained", which~ *obtained". That* is the pack's one worked sentence ~shape~ *shape,* and ~the reason~ *it is why* a CNIPA advantage is structural rather than measured [style-profile.md, Specification]. · CC · 260802 1542
That is the pack's one worked sentence shape, and it is why a CNIPA advantage is structural rather than measured [style-profile.md, Specification].
None of this comes from a granted CNIPA specification.
> ✎ None of this comes from a granted CNIPA ~specification: the~ *specification. The* pack's own enrichment checklist asks for three to five real ~granted-patent patent-claim-1~ *patent claim 1* sentences *out of granted patents,* and none has been ~pulled, while~ *pulled. Meanwhile* the README calls the Write / Edit map "the main purpose". · CC · 260802 1542
The pack's own enrichment checklist asks for three to five real patent claim 1 sentences out of granted patents, and none has been pulled.
Meanwhile the README calls the Write / Edit map "the main purpose".

### 5 · USPTO, and the one order that ends on the abstract

**A single-clause patent claim, an inline reference sign, and caps that can actually be counted**: USPTO is the only prescribed order in the pack that names the abstract.

```text
  🗂 USPTO · the delta table in playbook-patent/README.md
  ┌──────────────────────────────────────────────────────────┐
  │ spec order    Title · Field · Background · Summary ·      │
  │               Drawings · Detailed · Abstract              │
  │ patent claim  single clause, "comprising"                 │
  │ abstract cap  150 words, 15 lines, both "preferably"      │
  │ drawing label FIG. 1                                      │
  │ ref signs     inline, in the specification text           │
  │ utility model not available                               │
  │ invention     20 years · substantive examination          │
  └──────────────────────────────────────────────────────────┘

  ⚖️ the patentability bar · the drafting process, step 2
     novelty under 102, obviousness under 103

  ✍️ language rules the table does not carry · style-profile.md
     antecedent basis strict: "a" or "an" first, "the" after
     no legal phrases in the abstract
     title under 500 characters
     means-plus-function invokes narrow interpretation
```

🗂 Establishes USPTO as the pack's most fully specified jurisdiction, and the only one where the abstract has a place in the prescribed order.

#### 5.1 · Three of this row's limits are enforceable by counting
(so a USPTO draft is the one a machine can gate without judgment)
150 words and 15 lines are both countable, as is the 500-character title cap in style-profile.md.
> ✎ 150 words and 15 lines are both countable, as is the 500-character title cap in style-profile.md. Corrected 260802: the 2500-character figure the pack paired with the 150 words has no source in 37 CFR 1.72 or MPEP Chapter ~600, and both~ *600. Both* surviving limits are stated as preferences rather than caps. · CC · 260802 1542
Corrected 260802: the 2500-character figure the pack paired with the 150 words has no source in 37 CFR 1.72 or MPEP Chapter 600.
Both surviving limits are stated as preferences rather than caps.
Antecedent basis is countable too: every "the X" needs an earlier "a X" inside the same patent claim.
No equivalent count exists for the merits ban at the EPO.
> ✎ No equivalent count exists for the merits ban at the ~EPO or~ *EPO. None exists* for the CNIPA character cap *either,* once a filing is drafted in English and translated ~later, and the~ *later. The* pack does not say which side of *the* translation the cap is measured on. · CC · 260802 1542
None exists for the CNIPA character cap either, once a filing is drafted in English and translated later.
The pack does not say which side of the translation the cap is measured on.

#### 5.2 · Format values
(the office with the most countable limits records the same two absences as the other two)

```text
  📏 WORDS            abstract preferably <=150 words and <=15 lines
                      [37 CFR 1.72(b), MPEP 608.01(b), 260802]
                      title under 500 characters
                      characters · specification length not recorded by the pack
                      [README.md, per-jurisdiction delta table under the
                      -> Minimap map, Abstract limit row; style-profile.md,
                      Title and Abstract]
  📚 CITATION DENSITY not recorded by the pack
                      the prior art a filing cites positions the Background and
                      bounds the patent claims, and the README files it as a
                      SECONDARY use behind style imitation, with no count and no
                      per-sentence figure [README.md, Prior-art candidates]
  🔢 VALUE DENSITY    not recorded by the pack
                      the office whose limits ARE countable records no count of
                      values, because the specification is meant to carry none:
                      no experimental result, no accuracy metric, no numerical
                      performance figure anywhere [style-profile.md, Tone and
                      preferences; taste.md, No]
  📊 DISPLAYS         "FIG. 1" · reference signs inline in the specification text,
                      with no list part at all
                      [README.md delta table, Drawings label and Reference signs
                      list rows] · no experimental plots, no result charts
                      [README.md, -> Display]

  ⚠️ blueprint-only bites hardest here: the three USPTO limits a checker could
     count sit in a pack stages/section-kinds.yml never resolves, so the one
     jurisdiction a machine could gate without judgment is gated by nothing.
```

#### 5.3 · The language, in the filings' own words
(the only office whose phrasings the pack states in English, and not one of them from a granted filing)
"comprising" is the open transition: it keeps a patent claim open to elements the patent claim does not recite.
> ✎ "comprising" is the open ~transition that~ *transition: it* keeps a patent claim open to ~unrecited elements, against~ *elements the patent claim does not recite.* "consisting of" ~which~ closes ~it~ *it,* and "consisting essentially of" ~which~ sits ~between, and~ *between* the *two. The* pack's default is the open ~one~ *one,* for breadth [style-profile.md, Claims]. · CC · 260802 1542
"consisting of" closes it, and "consisting essentially of" sits between the two.
The pack's default is the open one, for breadth [style-profile.md, Claims].
Antecedent basis arrives as a two-word pattern rather than a sentence: "a" or "an" on first use, then "the" or "said" thereafter [style-profile.md, Claims].
"means for ..." is the one phrase the pack quotes in order to warn against it.
> ✎ "means for ..." is the one phrase the pack quotes in order to warn against ~it, because functional~ *it. Functional* language invokes a narrow statutory ~interpretation~ *interpretation,* tied to the structure ~in~ the specification *describes* [style-profile.md, Claims; taste.md, No]. · CC · 260802 1542
Functional language invokes a narrow statutory interpretation, tied to the structure the specification describes [style-profile.md, Claims; taste.md, No].
The banned Title words are literal: "improved", "new", "novel", plus trademarks.
> ✎ The banned Title words are literal: "improved", "new", "novel", plus ~trademarks, and the~ *trademarks. The* pack states them once for every ~office~ *office,* even though the 500-character cap beside them is USPTO's alone [style-profile.md, Title and Abstract]. · CC · 260802 1542
The pack states them once for every office, even though the 500-character cap beside them is USPTO's alone [style-profile.md, Title and Abstract].
The banned relative terms are literal too, "rapid", "efficient" and "substantially", each barred unless the specification defines it [style-profile.md, Claims; taste.md, No].
All five are the pack's own formulation, and none is lifted from a granted filing.
> ✎ All five are the pack's own ~formulation~ *formulation,* and none is lifted from a ~grant: no~ *granted filing. No* USPTO Detailed Description is stored, *and* the dependent recital is given as a ~template frame, and the~ *template. The* README calls the Write / Edit map "the main purpose" of a pack whose examples/ folder does not exist. · CC · 260802 1542
No USPTO Detailed Description is stored, and the dependent recital is given as a template.
The README calls the Write / Edit map "the main purpose" of a pack whose examples/ folder does not exist.

### 6 · EPO, and the reference-signs list as a separate part

**The only order that ends on a list, and the only rule in the table that is conditional**: EPO asks for a part no other office asks for.

```text
  🔖 EPO · the delta table in playbook-patent/README.md
  ┌──────────────────────────────────────────────────────────┐
  │ spec order    Title · Field · Background Art ·            │
  │               Disclosure · Embodiments · Drawings ·       │
  │               Reference Signs List                        │
  │ patent claim  two-part, "characterised in that",          │
  │               wherever appropriate, Rule 43(1),           │
  │               NOT every independent patent claim          │
  │ abstract cap  about 150 words, no statements on merits    │
  │ drawing label FIG. 1 or Figure 1                          │
  │ ref signs     a separate list, recommended by the EPO     │
  │               Guidelines, strongly expected for grant     │
  │ utility model not available                               │
  │ invention     20 years · substantive examination          │
  └──────────────────────────────────────────────────────────┘

  ⚖️ the patentability bar · the drafting process, step 2
     novelty under Art 54, inventive step under Art 56

  🔁 the drawings sit in a different place here
     US   Drawings BEFORE the Detailed Description
     EP   Drawings AFTER the Embodiments
     CN   Drawings BEFORE the Embodiments
```

🔖 Establishes the Reference Signs List as an EPO-only part, and the two-part form as the pack's one conditional rule.

#### 6.1 · Wherever appropriate is the only cell a drafter has to judge
(and the pack gives no test for applying it)
Every other cell in the delta table is a fact: a cap, a label, a route, a term of years.
Rule 43(1) makes the two-part form conditional.
> ✎ Rule 43(1) makes the two-part form ~conditional, the~ *conditional. The* README repeats the condition in ~both~ its table and *in* its per-jurisdiction notes, and neither says which independent patent claims meet it. · CC · 260802 1542
The README repeats the condition in its table and in its per-jurisdiction notes, and neither says which independent patent claims meet it.
The taste.md examiner test does not reach patent claim form at all, so the one judgment call in the table has no source in the pack that could settle it.

#### 6.2 · Format values
(the only office whose abstract rule is a ban rather than a number, and the only one whose reference signs are a part)

```text
  📏 WORDS            abstract about 150 words, and no statements on merits inside
                      it · no title cap recorded for this office · specification
                      length not recorded by the pack
                      [README.md, per-jurisdiction delta table under the
                      -> Minimap map, Abstract limit row; style-profile.md,
                      Per-jurisdiction language notes]
  📚 CITATION DENSITY not recorded by the pack
                      nothing per-sentence at any office, and nothing EPO-specific
                      beyond the Art 54 and Art 56 bars the Background has to
                      clear [README.md, drafting process step 2]
  🔢 VALUE DENSITY    not recorded by the pack, and this is the office that bans
                      the place a value would land: the abstract may state no
                      merits [README.md delta table, Abstract limit row]
                      the reference signs that fill an EPO filing with numerals
                      are addresses into the drawings, not results
  📊 DISPLAYS         "FIG. 1" or "Figure 1", the pack's only office accepting
                      either · reference signs as a separate Reference Signs List,
                      the last part of the prescribed order, recommended by the
                      EPO Guidelines and strongly expected for grant
                      [README.md delta table, Drawings label, Reference signs list
                      and Spec order rows]

  ⚠️ blueprint-only bites oddly here: the Reference Signs List is a part the pack
     names and no stage produces, because stages/section-kinds.yml declares no
     kinds for playbook-patent and the -> Display map stops at the drawings.
```

#### 6.3 · The language, in the filings' own words
(one connector, one condition, and no EPO filing behind either)
"characterised in that" is the EPO two-part connector, spelled the British way here while the CNIPA rendering takes the American spelling.
> ✎ "characterised in that" is the EPO two-part connector, spelled the British way ~for this office where~ *here while* the CNIPA rendering takes the American ~spelling, and the~ *spelling. The* difference is the pack's own ~inconsistency rather than~ *inconsistency, not* an office rule [README.md delta table, Claim form row; style-profile.md, Per-jurisdiction language notes]. · CC · 260802 1542
The difference is the pack's own inconsistency, not an office rule [README.md delta table, Claim form row; style-profile.md, Per-jurisdiction language notes].
"wherever appropriate" is quoted from Rule 43(1), and it is the pack's only conditional phrasing.
> ✎ "wherever appropriate" is quoted from Rule ~43(1)~ *43(1),* and *it* is the pack's only conditional ~phrasing, which is why~ *phrasing.* §6.1 records it as the one cell *in the table* with no test behind it. · CC · 260802 1542
§6.1 records it as the one cell in the table with no test behind it.
The abstract rule is stated as a ban and not as a phrasing, so the pack offers no EPO abstract sentence to imitate, only the merits it must not state.
Beyond those two phrases the pack holds nothing.
> ✎ Beyond those two phrases the pack holds ~nothing: no~ *nothing. No* EPO Reference Signs List is stored, so the part this jurisdiction is defined by has no example of its own line format ~anywhere, and the~ *anywhere. The* README's Write / Edit map, ~which~ *the one* it calls "the main purpose", points at an examples/ folder that was never built. · CC · 260802 1542
No EPO Reference Signs List is stored, so the part this jurisdiction is defined by has no example of its own line format anywhere.
The README's Write / Edit map, the one it calls "the main purpose", points at an examples/ folder that was never built.

### 7 · The drafting process, which is a Round and not a submission

**Six steps, prosecuted over years, filed under a map that fits only three of them**: this is the process no journal pack in the tree documents.

```text
  🔁 THE DRAFTING PROCESS · playbook-patent/README.md, written
     as a subsection of the -> Write / Edit map
  ① prior-art search   Google Patents · Espacenet · IPC/CPC
                       overlap risk · freedom to operate
  ② patentability      anticipation first, then obviousness
                       US 102/103 · CN Art 22 · EP Art 54/56
  ③ patent claims      one primary independent patent claim,
                       then the dependent hierarchy
  ④ specification      every patent claim element gets
                       written-description support
  ⑤ examiner review    an office action, issued in-house,
                       CRITICAL and MAJOR fixed before ⑥
  ⑥ jurisdiction fmt   one office per compile, never mixed;
                       patent claim CONTENT identical across
                       offices, only the format differs

  🔗 WHERE EACH STEP LANDS
     ③ ④ ⑥   writing       ── the -> Write / Edit map fits
     ① ② ⑤   not writing   ── no lifecycle stage named
     ⑤ ▶ ⑥   repeated once per office action  ── QB10 Round

  📦 it also replaces six legacy procedure skills, which is why
     the whole process is inside a knowledge pack at all
```

🔁 Establishes the six-step process as the pack's own lifecycle, and its home under a writing map as a misplacement rather than a statement about what the steps are.

#### 7.1 · An office action is a Round, and the fit is exact
(which makes QB10 the only page in this repo that already describes what prosecution does)
QB10 defines a Round as one externally triggered batch of review, rebuttal, revision, and resubmission, held as one dated S-Round page per batch.
An office action is externally triggered, answered by a written response, applied as a patent claim amendment, and refiled, so each one is a batch on exactly that definition.
QB10's gate asks a human to verify two things: that every response is applied or explicitly declined, and that the resubmission matches the round record.
> ✎ QB10's ~gate, that~ *gate asks* a human ~verifies~ *to verify two things: that* every response is applied or explicitly ~declined~ *declined,* and that the resubmission matches the round ~record, is the same verification a~ *record. A* response to an office action ~needs.~ *needs the same verification.* · CC · 260802 1542
A response to an office action needs the same verification.
The gap QB10 records as still open, that Round is not yet resolvable as a first-class family in the board tooling, is therefore open for filings too.

#### 7.2 · A submission is the wrong analogue, and step 6 says why
(because the filing is compiled once per office, not sent once)
A journal submission is one document to one desk, and the pack's step 6 compiles the same patent claim content into a different format for each office.
So a filing has a fan-out a submission does not have, and a round per office on top of it.
Nothing in the pack says whether the offices share one round record or keep one each, and the four stage maps do not reach the question.

#### 7.3 · Steps 1, 2 and 5 have no owner in the paper lifecycle
(so the process is documented and unroutable at the same time)
Prior-art search, patentability analysis, and examiner-style review are not writing.
> ✎ Prior-art search, patentability analysis, and examiner-style review are not ~writing, and the~ *writing. The* README carries all three under `-> Write / ~Edit`~ *Edit`,* because that is where the drafting-process subsection sits. · CC · 260802 1542
The README carries all three under `-> Write / Edit`, because that is where the drafting-process subsection sits.
The pack's other three maps each name a lifecycle folder; the drafting process names none.
A reader following the maps reaches steps 3, 4 and 6, and never reaches the three that decide whether a filing is worth drafting at all.

### 8 · What an appendix becomes in a filing

**No section kinds declared, so the question has to be answered from the parts a filing actually has**: and what a paper appendix usually carries is banned from every one of them.

```text
  🧳 THE APPENDIX QUESTION, ASKED OF THIS VENUE
     a journal page reads its answer off stages/section-kinds.yml
     playbook-patent declares NO kinds there, blueprint-only by
     design, so there is no appendix row to read

  📦 THE PARTS A FILING HAS
     specification   Detailed Description: at least one complete
                     embodiment plus alternatives that support
                     broader patent claim interpretation
     drawings        FIG. 1 .. FIG. n, structure and steps only,
                     every element carrying a reference numeral
     ref signs list  EP a separate part · CN inside the Brief
                     Description of Drawings · US inline

  🚫 WHAT A PAPER APPENDIX USUALLY CARRIES
     experimental results · accuracy metrics · empirical
     evaluations · numerical advantages
     barred from the whole specification by style-profile.md,
     and named office-action bait by taste.md
```

🧳 Establishes that a filing has no optional part, so the appendix question resolves into three named homes rather than one.
> ✎ 🧳 Establishes that a filing has no optional part, ~which is why~ *so* the appendix question resolves into three named homes rather than one. · CC · 260802 1542

#### 8.1 · By shape the nearest thing is the EPO Reference Signs List
(the only part of a filing that is a separate, list-shaped document)
An appendix is separate matter appended after the main text, and the EPO order is the only one that ends on a separate part rather than on prose.
CNIPA puts the same content inside the Brief Description of Drawings, and USPTO puts it inline.
> ✎ CNIPA ~folds~ *puts* the same content ~into~ *inside* the Brief Description of ~Drawings~ *Drawings,* and USPTO puts it ~inline, so at~ *inline. At* those two offices the *separate-list* shape does not exist at all. · CC · 260802 1542
At those two offices the separate-list shape does not exist at all.
The closest structural analogue is therefore jurisdiction-specific, which no journal outlet's appendix answer is.

#### 8.2 · By function the nearest thing is not optional
(so calling it an appendix would license exactly the wrong edit)
The Detailed Description's alternatives are what a paper would push into an appendix: extra cases, kept out of the main argument.
In a filing they are what supports the breadth of the patent claim.
> ✎ In a filing they are what supports the breadth of the patent ~claim, and~ *claim.* taste.md names a broad patent claim resting on a single narrow embodiment as a defect the examiner acts on. · CC · 260802 1542
taste.md names a broad patent claim resting on a single narrow embodiment as a defect the examiner acts on.
Cutting them shortens the specification and narrows the granted right, which is the same asymmetry division 2 records for softening a patent claim.

#### 8.3 · The drawings are the one part a display stage already produces
(and the pack refuses most of what that stage makes)
The `-> Display` map says a drawing shows what a patent claim covers, not how well the invention performs.
> ✎ The `-> Display` map says ~drawings show~ *a drawing shows* what ~is claimed,~ *a patent claim covers,* not how well ~it performs, and~ *the invention performs. It* rules out experimental plots and result charts. · CC · 260802 1542
It rules out experimental plots and result charts.
A paper's display set is largely those plots, so converting a paper into a filing discards most of the display layer rather than relocating it.
What survives is the block diagram and the flowchart, each element carrying a reference numeral consistent across every figure and every mention in the specification.

## Aims

### A1 · ⚖️ The inversion, and what it does to the lifecycle
- A1.1 · The role change for figures, background, and abstract is stated where a paper is converted into a filing.
  **Done when:** converting a display into a supporting figure records the limitation it supports.

### A2 · ⚠️ The word collision, and how to survive it
- A2.1 · The vocabulary rule is written where either stage reads, not only on this page.
  **Done when:** no skill can act on the word claim in a patent context without meeting the disambiguation.
- A2.2 · A revise pass cannot silently soften a patent claim.
  **Done when:** the humanizer and content workers are barred from a filing's patent claim set, or the bar is written and checkable.

### A3 · ⚠️ Three jurisdictions, no exemplars
- A3.1 · At least one granted filing per jurisdiction this repo actually targets lands in the pack.
  **Done when:** the language guidance the README calls its main purpose has a source on disk.

### A4 · 📜 CNIPA, and the only route that is not an invention patent
- A4.1 · A CNIPA draft can be built from this board without anyone reading the pack's Chinese-language cells.
  **Done when:** the six specification blocks, the two-part form, and the abstract cap are all readable in English at the point a filing is drafted.
- A4.2 · The invention-versus-utility-model choice is made before patent claims are drafted.
  **Done when:** a CN target that pairs method patent claims with a utility model route is refused rather than compiled.

### A5 · 🗂 USPTO, and the one order that ends on the abstract
- A5.1 · The countable USPTO limits are counted rather than trusted.
  **Done when:** a check reports an abstract over 150 words, a title over 500 characters, and the first "the X" with no earlier "a X" inside the same patent claim.

### A6 · 🔖 EPO, and the reference-signs list as a separate part
- A6.1 · An EP compile carries a Reference Signs List.
  **Done when:** the list's absence is reported before the filing is packaged rather than after.
- A6.2 · The Rule 43(1) condition has a test a drafter can apply.
  **Done when:** the pack states which independent patent claims take the two-part form at the EPO, instead of repeating the condition.

### A7 · 🔁 The drafting process, which is a Round and not a submission
- A7.1 · Each office action is held as one Round record.
  **Done when:** an office action opens a dated Round page carrying the action, the amendment made, and anything explicitly declined.
- A7.2 · The three non-writing steps are routed somewhere other than Write / Edit.
  **Done when:** prior-art search, patentability, and examiner-style review each name an owning stage in the pack.

### A8 · 🧳 What an appendix becomes in a filing
- A8.1 · The appendix question has a per-jurisdiction answer for this venue.
  **Done when:** a filing names where its supporting matter lives at each office, and the material a paper appendix carries is refused where it is written rather than at review.

## States

### A1 · ⚖️ The inversion, and what it does to the lifecycle
- ⬜ A1.1 · Not started. The stage maps carry the roles; the conversion is unwritten.

### A2 · ⚠️ The word collision, and how to survive it
- ⬜ A2.1 · Not started. The collision is recorded here for the first time.
- ⬜ A2.2 · Not started, and unguarded. Nothing prevents a revise worker from hedging a patent claim.

### A3 · ⚠️ Three jurisdictions, no exemplars
- ⬜ A3.1 · Not started. Zero exemplars, same as `playbook-grant`.

### A4 · 📜 CNIPA, and the only route that is not an invention patent
- ⬜ A4.1 · Not started. This page carries the English rendering, and nothing downstream reads it yet.
- ⬜ A4.2 · Not started. The route is set in the filing's STATUS.md venue field, and no stage checks it against the patent claim kinds.

### A5 · 🗂 USPTO, and the one order that ends on the abstract
- ⬜ A5.1 · Not started. The limits are recorded in the pack and counted nowhere.

### A6 · 🔖 EPO, and the reference-signs list as a separate part
- ⬜ A6.1 · Not started. The list is recommended by the pack and produced by no stage.
- ⬜ A6.2 · Not started, and unanswerable from the pack as it stands. Neither the README nor style-profile.md resolves the condition.

### A7 · 🔁 The drafting process, which is a Round and not a submission
- ⬜ A7.1 · Not started, and blocked upstream. `QB10` records that Round is not yet a first-class family in the board tooling.
- ⬜ A7.2 · Not started. All six steps sit under the Write / Edit map, including the three that are not writing.

### A8 · 🧳 What an appendix becomes in a filing
- ⬜ A8.1 · Not started. `stages/section-kinds.yml` declares no kinds for this pack, so there is no appendix row to answer from.

## Files

- `../../paper/venue/playbook-patent/README.md` · the jurisdiction delta table, the drafting process, the four stage maps
- `../../paper/venue/playbook-patent/taste.md` · the examiner's test, at family level
- `QBv15-grant.md` · the other non-journal pack, same shape exception and same exemplar hole

<!-- exemplars:begin -->

📚 **Exemplars** · 0 papers on disk, regenerated by `_tools/sync-exemplars.py`

Filed at FAMILY level under `../../paper/venue/playbook-patent/examples/`, not under the outlet (the group intro on the Index).

- none. No `examples/` folder under `../../paper/venue/playbook-patent/`, so this outlet states section norms with no exemplar behind them.

<!-- exemplars:end -->

<!-- kinds:begin -->

📐 **Section kinds** · none declared in `stages/section-kinds.yml`, so this venue is blueprint-only: the S-Venue-0 blueprint is binding and no per-section pack is resolved.

<!-- kinds:end -->

🔗 **Authority** · the office's own rules, fetched and verified 260802

- [USPTO Manual of Patent Examining Procedure](https://www.uspto.gov/web/offices/pac/mpep/index.html) · the office's own reference on the practice and procedure of prosecuting an application before the USPTO. Ninth Edition, Revision 01.2024, published November 2024 and up to date as of 31 January 2024, which is also the date after which nothing has been incorporated. [Chapter 600, Parts, Form and Content of Application](https://www.uspto.gov/web/offices/pac/mpep/mpep-0600.html) carries 37 CFR 1.77(b) on the order of the specification, 37 CFR 1.72(b) with MPEP 608.01(b) on the abstract, and 37 CFR 1.72(a) with MPEP 606 on the title.
- [EPO Guidelines for Examination](https://www.epo.org/en/legal/guidelines-epc) · April 2026 edition, in force from 1 April 2026 and superseding the April 2025 edition, with its main updates listed in OJ EPO 2026, A4. [Part F, Chapter IV, 2.2 Two-part form](https://www.epo.org/en/legal/guidelines-epc/2026/f_iv_2_2.html) governs the two-part patent claim, [Part F, Chapter II, 2.3 Content of the abstract](https://www.epo.org/en/legal/guidelines-epc/2026/f_ii_2_3.html) governs the abstract, and [Part F, Chapter II, 4.8 Reference signs](https://www.epo.org/en/legal/guidelines-epc/2026/f_ii_4_8.html) governs reference signs. [Rule 42 EPC](https://www.epo.org/en/legal/epc/2020/r42.html) is the regulation prescribing what a description contains.
- [CNIPA Patent Examination Guidelines, 2023](https://www.cnipa.gov.cn/attach/0/%E4%B8%93%E5%88%A9%E5%AE%A1%E6%9F%A5%E6%8C%87%E5%8D%97.pdf) · the office's own examination authority, a 613-page document in Chinese only, issued by CNIPA and in force from 20 January 2024. [The Implementing Regulations of the Patent Law, 2023 revision](https://www.cnipa.gov.cn/art/2023/12/21/art_98_189197.html) sit above it, decided 11 December 2023 and published on the office site, also in Chinese only.
- CONFIRMS the CNIPA 300-character abstract cap at 4 and 4.3, and moves where it lives. The Guidelines state that the abstract text including punctuation may not exceed 300 characters, and add four rules the pack does not carry: no heading inside the abstract text, chemical or mathematical formulae permitted, an abstract drawing chosen from the specification drawings and named in the request, and no advertising or purely functional product description. The 2023 Implementing Regulations no longer state the number anywhere, so the cap is a Guidelines rule and citing the Regulations for it now fails.
- CONFIRMS the CNIPA specification order at 4 and the two-part patent claim form at 4 and 4.4. Article 20 of the Implementing Regulations prescribes technical field, background art, disclosure of the invention, brief description of the drawings, and specific embodiments, which is the pack's order once the title is added. Article 24 requires an independent patent claim to carry a preamble part and a characterising part introduced by "characterized by" or a similar term, which is the connector 4.4 renders in English.
- CONFIRMS the EPO abstract rule at 6 and 6.2, and names the instruments behind it. The abstract must "not contain statements on the alleged merits or value of the invention or its speculative application" under Rule 47(2), and must "preferably not contain more than one hundred and fifty words" under Rule 47(3). So the pack's "about 150 words" is the rule's own softness, while the merits ban is absolute, which makes them two different kinds of limit sitting in one cell.
- CONFIRMS Rule 43(1) and its conditional at 6 and 6.1, and leaves A6.2 open against the office too. The Guidelines state that Rule 43(1)(a) and (b) define the two-part form an independent patent claim must take "wherever appropriate", the first part naming the subject-matter plus the prior-art features and the second, the "characterising portion", stating what the invention adds. The requirement reaches independent patent claims only, never dependent ones. No test for when the form is appropriate is given beyond a neighbouring section listing when it is unsuitable, so the judgment 6.1 records as unsourced in the pack is unsourced at the office as well.
- CORRECTS the USPTO abstract cap at 5, 5.1, 5.2 and the Diagram. 37 CFR 1.72(b) reads "preferably not exceeding 150 words in length", and MPEP 608.01(b) adds that the abstract is "generally limited to a single paragraph preferably within the range of 50 to 150 words" and "should not exceed 15 lines of text". The 2500 characters this page pairs with the 150 words appears nowhere in MPEP Chapter 600, nowhere in 37 CFR 1.72, and on no uspto.gov page fetched, so it has no USPTO source and should be dropped. What survives is a 15-line ceiling the pack never recorded, and 5.1's countable set is really 150 words, 15 lines, and the title cap.
- CONFIRMS the USPTO title cap at 5 and 5.2, and ADDS the gap in its prescribed order. MPEP 606 states the title "may not contain more than 500 characters", so the 500 the pack carries is the office's own number. But 37 CFR 1.77(b) runs title, cross-references, federally sponsored research statement, joint research agreement parties, incorporation by reference, prior-disclosure statement, background, brief summary, brief description of the drawings, detailed description, the patent claims at (11), and only then the abstract at (12). The pack's USPTO row drops the patent claims from its own order, which is the same elision 4.1 records at CNIPA rather than a CNIPA-only truncation.
- CORRECTS the EPO Reference Signs List at 6, 6.2, 8.1 and A6.1, which is this page's EPO headline. The office prescribes no such part. Rule 42(1) EPC lists six description contents, technical field, background art, disclosure of the invention, brief description of the figures, at least one detailed way of carrying out the invention, and industrial applicability, and stops there. Guidelines F-II, 4.8 asks only that description and drawings be consistent, that each sign be explained, and that no sign used in the description or in the patent claims be missing from the drawings. So a separate list is a drafting convention, "recommended by the EPO Guidelines" is not accurate, and "strongly expected for grant" is not something the office states anywhere fetched. A6.1 remains a sensible house rule and stops being an office requirement.

## Law

- In a filing the patent claim is the deliverable and the specification supports it, which inverts the role of every artifact the paper lifecycle produces.
  A patent claim and a lifecycle claim are different objects that share a word: softening one improves a paper and narrows a granted right, so no revision pass may treat them alike.

## Glossary

- **Patent claim**: the legally construed sentence defining the boundary of the monopoly, the filing's actual deliverable.
- **Lifecycle claim**: an assertion the paper argues, owned by the `1b-claims` stage, which may be softened during revision.
- **Reference sign**: a numeral tying a drawing element to the specification text, load-bearing in a filing and placed differently in each jurisdiction.

## Log

260802 · The USPTO abstract cap is corrected in the body, not only in the Authority block.
  `2500 characters` appears in no USPTO instrument, and is dropped from the Diagram, from 5, 5.1 and 5.2.
  What replaces it is 15 lines from MPEP 608.01(b).
  Both that and the 150 words are stated as preferences.
  Verified independently at source: 37 CFR 1.72(b) reads "preferably not exceeding 150 words in length" and carries no character count.
260802 · Authority block added at the end of Files, from the three offices' own rules rather than the pack.
  It corrects this page's EPO headline.
  The EPO prescribes no Reference Signs List: Rule 42(1) EPC gives six description contents and stops.
  Guidelines F-II, 4.8 asks only for consistency and for every sign to be explained.
  So the separate list is a drafting convention, and "recommended by the EPO Guidelines, strongly expected for grant" is unsupported.
  That reaches 6, 6.2, 8.1 and A6.1.
  The USPTO 2500-character abstract figure has no source in MPEP Chapter 600 or 37 CFR 1.72, and is dropped.
  The real companion to the 150 words is a 15-line ceiling the pack never recorded, and both are "preferably" rather than hard.
  Confirmed at source:
  the CNIPA 300-character cap, though it now lives in the Guidelines and not in the 2023 Implementing Regulations;
  the CNIPA specification order and two-part patent claim form at Articles 20 and 24;
  the EPO abstract's soft 150 words under Rule 47(3) beside an absolute merits ban under Rule 47(2);
  Rule 43(1)'s two-part form for independent patent claims only, with no test for "wherever appropriate" at the office either, which leaves A6.2 open on both sides;
  and the USPTO 500-character title.
  One addition: 37 CFR 1.77(b) puts the patent claims at (11) before the abstract at (12), so the pack's USPTO order drops them the same way 4.1 records for CNIPA.
260802 · Added a Format values block and a language subsubsection to each jurisdiction division: 4.3 and 4.4 for CNIPA, 5.2 and 5.3 for USPTO, 6.2 and 6.3 for EPO.
  Of the four format metrics only WORDS and DISPLAYS are recorded by `playbook-patent`, and both differ per office.
  CITATION DENSITY is absent because a filing cites prior art rather than literature, and the pack records no count of either.
  VALUE DENSITY is absent by construction: the pack has no `style.md`, and none of the venue tree's 95 `style.md` files records the metric anywhere.
  No granted filing is stored at any office, so the language subsubsections quote `style-profile.md`'s own formulations, with the CNIPA ones rendered into English, and say so.
260802 · Expanded Content from three divisions to eight.
  One division per jurisdiction: CNIPA, USPTO, EPO.
  Each division carries that office's prescribed specification order, patent claim form, abstract cap, drawing label, reference-sign placement and utility-model availability, all from the delta table in `playbook-patent/README.md`.
  Plus the six-step drafting process mapped onto `QB10` Round.
  Plus the appendix question, answered from the parts a filing actually has.
  The CNIPA cells are rendered in English because this board is English-only and the pack states them in Chinese.
260802 · Opened with the QBv group, from `playbook-patent` at `Venue-Paper@fe25a88`.
