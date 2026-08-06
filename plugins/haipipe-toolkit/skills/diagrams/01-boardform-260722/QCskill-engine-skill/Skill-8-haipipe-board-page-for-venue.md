# haipipe-board-page-for-venue · v0.1.2
state: 🟡 in flux · lifted 260803 · 13 of 16 venue pages conform · the 0.1.0 contradictions fixed at 0.1.1
owner: JL
method: three managed spans sync from the skill folder; everything else is written by hand

## Opening
`haipipe-board-page-for-venue` is the contract for a venue page, which is one page per place a paper is submitted to.
That place is a journal, a funder, or a patent office.
Its sibling `haipipe-board-page-for-skill` governs the other page kind that describes rather than decides.
What splits them: a skill page mirrors a folder in this repo, a venue page records an outside desk.
It was lifted off `QBv1-misq.md` on 260803, and the same day's fan-out took it to fourteen more desks.

**The pages it governs, and where they live**: a venue page is named `QBv<n>-<slug>.md` and every one of them sits on the paper board `01-haipipe-paper-260725`, not here.
Sixteen exist.
Re-measured 260806, thirteen carry the three figures and the section index this contract requires; the grant and patent pages have no journal resolver to index, and `QBv11` has not been brought up.

**What binds on a venue page and what does not**: this is the rule the skill puts above all the others, and it is a rule about how the PAGE IS READ rather than about how it is written.
Nearly everything on a venue page is a measurement of what published papers at that desk actually did, so a drafter may depart from any of it on purpose.
Only the desk's own published rules bind, because only those get a manuscript returned unreviewed.
The distinction was paid for: `QBv1-misq.md` printed `120-160 words, do NOT exceed ~185` for its abstract.
That was the pack's measurement of eight papers, at a desk publishing no abstract cap at all, and JL read it as a limit and ruled ~250 words fine.

**The two sources it arbitrates**: a venue page is written from the venue pack under `paper/venue/playbook-<family>/`, which is its own repository and is read but never written here, and from the desk's own published instructions.
When they disagree the desk wins and the disagreement is written onto the page rather than quietly resolved.
`QBv1-misq.md` records three of them, including a pack that observed "40-50 published pages" where the desk sets a 55-page ceiling.
Every desk fact also carries HOW it was read, which was added the day `misq.umn.edu` began answering a direct fetch with HTTP 403 and a fact could only be re-checked through search summaries.

**Why its placement was worth a second look**: it shipped in `skills/board/`, beside the base, while `haipipe-board-page` then stated that a variant ships under its CONSUMER and never beside the base.
`haipipe-board-page-for-skill` was allowed there because its consumer is the board family itself.
This variant's consumer is the paper family: every page it governs lives on `01-haipipe-paper-260725`, and the generator it names lives in that board's `_tools/`.
The conflict resolved by changing the law rather than the folder: the base now rules that a variant ships WHERE THE BOARD FAMILY MAINTAINS IT (JL 260803), and at 0.1.2 this file moved under the base's `page-types/` with the other nine variants.

**Covered elsewhere**: `haipipe-board-page` owns the frame both variants extend and this file never repeats a rule from it.
`Skill-6` mirrors `haipipe-board-page-for-skill`, the variant this one is most often confused with, and the two disagree on purpose about Aim form: the skill-page variant drops the base's `A<n>` ids and `Done when`, and this one keeps them, which its changelog says out loud so a reader arriving from the roster does not assume every variant drops them.
`QBv1-misq.md` on the paper board is the reference implementation and the contract tells a new writer to copy it rather than the base template.
`_tools/sync-exemplars.py` on that same board owns the two marker blocks inside a venue page's `## Files`, and is the only generator involved; nothing on THIS board writes a venue page.

**Where it stands**: it is registered, which the sibling variant was not, so the failure that made `haipipe-board-page-for-skill` unloadable for a day did not repeat here.
The 260803 fan-out wrote from it at scale: fourteen agents took it to fourteen desks the day it shipped, and thirteen of sixteen `QBv` pages now carry its shapes.
The two contradictions this page found inside the shipped file were fixed at 0.1.1, and their Aims below are closed with the evidence.

## Writing Style
English only. One sentence per source line. Describe the shipped unit factually and keep generated inventory separate from human health judgment.

## Diagram
<!-- haipipe:skill:tree:start 700d0f9ae07e31fd board/page-types/haipipe-board-page-for-venue -->

**What `haipipe-board-page-for-venue` ships**: every file in the folder, with the one-line purpose each one states for itself.

```
haipipe-board-page-for-venue/
  CHANGELOG.md          50 ln  haipipe-board-page-for-venue · Changelog
  SKILL.md             361 ln  /haipipe-board-page-for-venue · a venue page records a desk it cannot argue with
```

<!-- haipipe:skill:tree:end -->

**How `haipipe-board-page-for-venue` is used**: the two sources it merges, the one that wins, and the board it writes onto, which is not this one.

```text
WORKFLOW  writing or fixing ONE QBv page

   📄 haipipe-board-page              the BASE · every page kind
      five on-stage sections, fixed order · the Opening split · numbering
        │
        │  loaded FIRST, never repeated below
        ▼
   🏛 haipipe-board-page-for-venue           ONLY the delta
      ┌──────────────────────────────────────────────────────────┐
      │ 🖼 Diagram   THREE figures, fixed order:                  │
      │              ① desk taste    would it look at my paper?  │
      │              ② Venue-Structure  what am I writing?       │
      │              ③ Submission-Rules what does the portal ask?│
      │ 🔢 Content   divisions carry the venue's reading index    │
      │              Sec-0-Abstract … Sec-A-Appendix             │
      │ 📎 Files     five groups, ending Authority + Generated    │
      │ 🎯 Aims      base form KEPT: A<n> ids · Done when         │
      │              (this is where it splits from Skill-6)      │
      └──────────────────────────────────────────────────────────┘
        │
        │  reads TWO sources, and they are not equal
        ▼
   📦 THE PACK                        🏛 THE DESK
      paper/venue/playbook-*/            the venue's own published rules
      taste · style · template           categories · caps · policies
      ⚖️ read, NEVER written here        ⚖️ fetched, and the METHOD is stamped
        │                                  │
        └──────────────┬───────────────────┘
                       ▼
              ⚔️ THEY DISAGREE
              the DESK wins, and the gap is PRINTED on the page
              a slot neither can fill is printed too, never deleted
                       │
                       ▼
   📋 QBv<n>-<slug>.md   on 01-haipipe-paper-260725, NOT on this board
      QBv1-misq is the reference implementation: copy IT, not the template
                       │
                       ▼
   🤖 _tools/sync-exemplars.py   owns 2 marker blocks inside ## Files
      exemplars = one row per paper · kinds = the S-page roster
      --check before calling the page done

   📖 REFERENCE vs ⚖️ BINDING is the reading rule over all of it:
      arcs, budgets, moves and word counts are MEASUREMENTS a drafter
      may depart from; only the desk's published rules cost a submission
```

## Content
<!-- haipipe:skill:body:start 700d0f9ae07e31fd board/page-types/haipipe-board-page-for-venue -->

**haipipe-board-page-for-venue** · `0.1.2` · last shipped 2026-08-04

- folder   `board/page-types/haipipe-board-page-for-venue/`
- tools    not declared
- summary  Now lives under page-types/ and composes the venue-page contract with the current Page Phase.

### SKILL.md




**LOAD `haipipe-board-page` FIRST.** It owns the base: the sections and their fixed order, the five rows that define each one, the title rule, the Opening split, the numbering, and the evaluation contract.
This file adds only what a venue page needs and an ordinary decision page does not.
It never repeats a base rule, because a copied rule goes a night out of date while the contract moves.
After resolving this Page Type, load the current contract from `page-phases/`; this file determines the persistent venue shape, not whether the current work is DRAFT, PROBE, REVISE, or CHECK.

**The kind this variant covers**: one page per submission TARGET, and nothing above it.

```
kind    filename              subject                        closes when
────────────────────────────────────────────────────────────────────────────
Venue   QBv<n>-<slug>.md      ONE desk: a journal, a         its Aims are met
                              funder, a patent office        like any Q page
```

`QBv1-misq.md` is the reference implementation. Read it before writing a new one.
There is no pack-head page above the outlets (JL 260802): four outlets in one pack get four pages, and what they share is stated on each page that needs it, never in a fifth page nobody opens.


- 1 · 🏛 What makes a venue page different
      A normal Q page settles something the team gets to decide. **A venue page settles nothing.** Its subject is a desk outside this repo that publishes its own rules, changes them without telling anyone, and rejects papers that ignore them. The page's job is to make that desk legible before a paper is written for it, not to have an opinion about it.
      Three consequences, and every rule below comes from one of them:
      ```
      1  the subject is EXTERNAL      →  every fact carries where it came from and when
      2  there are TWO sources        →  the desk outranks the pack, and the gap is written down
      3  a paper is BUILT from it     →  the page owes structure and mechanics, not just taste
      ```
      **What a venue page does NOT own**: which venue this paper picks. That decision lives in the paper board's Opening concern (`QB1` on the paper board). This group is the catalog that decision reads.

- 2 · 📖 A venue page is a REFERENCE, not a rulebook
      **The principle (JL 260803), and it governs everything below.** A venue page is read while writing a paper, and almost everything on it is a suggestion: the arcs, the budgets, the moves, the anti-patterns are all measurements of what published papers at that desk actually did. A drafter may depart from any of them on purpose, and doing so is off-pattern rather than wrong.
      **One part of the page binds.** The desk's own published rules, which live in the `Submission-Rules` figure and the `Authority` group, are enforced by the desk itself: break one and the manuscript is returned unreviewed. Nothing else on the page has that force.
      ```
      📖 REFERENCE   arcs · budgets · shapes · moves · the pack's refusals ·
                     format values · exemplar language
                     ↳ measured from papers · departing is a choice

      ⚖️ BINDING     category cap · manuscript format · reference style ·
                     anonymity · required disclosures · the portal
                     ↳ published by the desk · breaking one costs the submission
      ```
      **Why it has to be written down.** A page full of measured numbers reads as a specification. `QBv1` printed `120-160 words, do NOT exceed ~185` for the abstract, which is the pack's measurement of eight papers, while the desk publishes no abstract cap at all. Read as a rule, it makes a drafter write to the middle of a distribution instead of to the paper. Found by JL 260803, who ruled ~250 words fine.
      **So every length says whose it is**, and the page says it in the row itself:
      ```
      ✅  120-160w observed, no desk cap · ~250w ruled acceptable JL 260803
      ✅  55 pp Research Article · the DESK's cap, counting everything
      🚫  120-160 words, do NOT exceed ~185        ← reads as a rule, is not one
      ```
      **A binding rule also has a WHEN, and it is not always submission.** Nature Communications requires no particular structure or format at first submission and says style and length "will not directly influence consideration"; its caps are enforced at REVISION. A page that files those caps beside JAMA's tells a drafter to spend weeks on a gate that is not there yet, and a page that omits them lets a revision arrive over the limit. So a binding row carries the moment it bites:
      ```
      ⚖️ AT SUBMISSION    the desk checks it before an editor reads · JAMA's 3,000 words
      ⏳ AT REVISION      free at first submission, enforced later · Nature Communications
      🎯 AT ACCEPTANCE    priced or demanded once accepted · every Nature-family APC,
                          and npj's waiver, which must be REQUESTED at submission anyway
      ```
      **Write the pack's refusals as the pack's.** `the pack refuses more than ~160 words` rather than `do not exceed ~160 words`, so the page never sounds like it is the one doing the refusing.

- 3 · 📚 The two sources, and which one wins
      ```
      📦 THE PACK          paper/venue/playbook-<family>/<OUTLET>/
                           taste.md · <OUTLET>-<section>/style.md + template.md · examples/
                           ⚖️ READ and NEVER written by this plugin: the packs are their
                              own repository, jluo41/Venue-Paper, pinned as a submodule

      🏛 THE DESK          the venue's own published instructions, on its own site
                           submission guidelines · categories and lengths · policies ·
                           review process · the manuscript templates it publishes

      ⚔️ WHEN THEY DISAGREE   the DESK wins, and the disagreement is WRITTEN DOWN on the
                              page, naming both readings. A correction never goes into
                              paper/venue/, because this plugin does not write there.
      ```
      The disagreement is the most valuable thing on the page, so it is never quietly resolved. `QBv1` records three of them: the pack observed "40-50 published pages" where the desk sets a 55-page submission ceiling, the pack records no reference style where the desk requires APA 7th, and the pack records none of the submission mechanics at all.
      **Provenance is stamped, and HOW it was read is part of it.** A desk fact carries the date and the method, because these two are not equally strong:
      ```
      ✅  fetched and verified 260802
      ✅  re-checked 260803 through search summaries only, the site answers a direct
          fetch with HTTP 403 · re-read before submitting
      🚫  "MISQ requires APA 7th"            ← true, and unciteable, and unmaintainable
      ```

- 4 · 🖼 Three figures, in this order, in `## Diagram`
      The base allows any number of figures and requires a caption line above each. A venue page carries these three, and a page missing one is incomplete rather than short:
      ```
      ① DESK TASTE        what COUNTS as the contribution · what is DESK-REJECTED ·
                          the desk's own test, quoted · the exemplar count
                          answers: would this desk even look at my paper?

      ② VENUE-STRUCTURE   the sections in the venue's READING ORDER, each with its
                          budget and what it owes · the one ceiling over all of them ·
                          whether a kind is a floor a real paper may exceed
                          answers: what am I actually writing?

      ③ SUBMISSION-RULES  category and cap · manuscript format · reference style ·
                          the submission system · anonymity · required disclosures ·
                          the odds, the clock and the money · an open row for what is
                          NOT on record · the desk's own URLs
                          answers: what does the portal demand on the day I upload,
                                   and what am I signing up for by choosing this desk?
      ```
      **When the desk publishes a TOTAL, add the pack's parts up and print the sum against it.** This is a required row in `Venue-Structure`, not an optional nicety, because it went 3 for 3 the first time anyone checked:
      ```
      JAMA IM         desk 3,000 w body   ·  pack floors sum to 3,350   ·  over before you start
      PNAS            desk ~4,000 w       ·  pack floors sum to ~6,970  ·  74% over
      Diabetes Care   desk 4,000 w body   ·  pack floors sum to 3,950   ·  the cap IS the floor
      MISQ            desk 55 pp counting everything · no per-section desk limit at all
      ```
      The arithmetic is systematic rather than unlucky. A pack measures PUBLISHED papers section by section, and a published page is not a submission budget, so the parts were never fitted to the whole. Neither source is wrong and the page resolves nothing: it prints both, names the cap as the binding one, and opens an Aim on how the body gets allocated. A drafter who writes to the middle of every per-section budget is over the cap at every desk that has one.
      **The odds and the clock belong on the page.** Acceptance rate, how many review rounds a paper takes, how long a cycle runs, whether submission or open access costs anything: these decide whether a desk is worth a year, and none of them are in any pack. They are the desk's reported statistics rather than promises, and the row says so.
      **A venue page ends with the gate as a runnable list.** The last Content division turns the binding figure into an ordered checklist run once on the final file, because a rule remembered while drafting is a rule half-applied. `QBv1` runs seven steps: count the pages, pick the category, strip the author out, fix the references, move nothing outside the limit, write the disclosures, upload. The division also names the ONE step a finished paper cannot fix in an afternoon, which at every desk with a hard cap is the page count.
      **Embed the desk's links twice, on purpose.** A row inside a fenced figure is plain text: the renderer runs `esc()` and the figure linker over a fence, never the inline markdown pass, so a URL written in a figure will not be clickable. Put the bare hosts in the figure so it stays readable when copied, and repeat them as real markdown links in a line directly under the fence.
      **Never put a bare URL alone on its own line inside `## Diagram`.** That is the Excalidraw canvas slot. A desk URL alone on a line is safe only because the renderer matches the excalidraw host specifically; do not rely on it, and keep desk links inline in prose.

- 5 · 🔢 A section division carries the venue's index
      **The rule (JL 260803, "I want to see the index").** A Content division that describes one section of the paper is named with the venue's own reading position in front of the section name:
      ```
      ### 4 · Sec-0-Abstract: one unstructured paragraph, question forward
          ▲       ▲
          │       └── Sec-<n> from ZERO, so the index IS the S-Main page number ·
          │           only the appendix takes a letter, Sec-A
          └── the Content division number, which counts the judgment divisions too

      ### A4 · 📝 Sec-0-Abstract: one unstructured paragraph, question forward
               ▲   the emoji lives on the Aims and States group and on the division's
                   closing line. NOT on the division heading, however tempting the
                   symmetry: check.py strips it from a group name and not from a
                   division, so ten divisions produce twenty group-name-drift
                   warnings at once. Written, built, reverted, 260803.
      ```
      **The index counts from ZERO and carries the `Sec-` prefix** (JL 260803, arrived at in three tries). A 1-based index sat one off the `S-Main-<n>` page forever, so every reader converted; 0-based fixes that, and `Sec-` is what keeps `Sec-0-Abstract` from reading as a typo where a bare `0-Abstract` would. Letters were tried and dropped: a journal that letters its own appendix sections, as MISQ does with Appendix A and Table A1, gives a lettered section index two meanings at once. Only the appendix keeps a letter, `Sec-A`, precisely because it matches the desk's own lettering.
      ```
      Sec-0-Abstract → S-Main-0     Sec-3-Methods → S-Main-3
      Sec-1-Introduction → S-Main-1  Sec-4-Results → S-Main-4
      Sec-2-Theory → S-Main-2        Sec-5-Discussion → S-Main-5   Sec-A-Appendix → S-Appendix-A
      ```
      **`Sec-<i>` = `S-Main-<i>` is a PROPERTY, not a law, and a page must check it rather than assume it.** The identity holds only where the desk's reading order matches the order `section-kinds.yml` resolves, and three of the first four venue pages written to this contract broke it in a different way:
      ```
      PNAS       reading order is Significance ▸ Abstract ▸ … ▸ Methods LAST, while the
                 resolver has abstract=0, significance=1, methods=3 · the two columns
                 genuinely disagree, so QBv13 prints BOTH and explains why
      JAMA NO    no theory kind at this outlet, so Methods is Sec-2 where MISQ has Sec-3 ·
                 the index is the DESK's order, never a shared numbering across venues
      JAMA IM    a Research Letter is a whole article type with no reading position, so
                 QBv6 gave it Sec-L rather than claiming a slot in the sequence
      ```
      **When the two disagree, `Sec-<n>` follows the RESOLVER and the desk's printed order gets its own row.** The fan-out split 2-2 on this before anyone ruled: `QBv12` and `QBv10` bound the index to `section-kinds.yml`, `QBv9` and `QBv13` bound it to the desk's reading order. Both printed both numbers, so nothing was lost either way, but a board cannot carry two conventions. The resolver wins for one reason: `Sec-<n>` exists to JOIN the `S-Main` page a paper actually writes, and an index that tracks the desk stops being a join key the moment the two differ. Describing the desk is `Venue-Structure`'s job, and it has a column for it.
      **The desk's own section list can be longer than the resolver's, and that gap is a finding.** `section-kinds.yml` declaring seven kinds is not evidence that the desk asks for seven blocks: MISQ expects Concluding Remarks that the resolver does not declare, Management Science requires a ≤250-word nontechnical executive summary that no pack folder covers, and JAMA Network Open publishes a Research Letter the resolver withholds. A draft built from the resolver alone reaches the portal with a required field empty. Print the block in `Venue-Structure` with the gap named, and open an Aim on it.
      **A section has three numbers, and only one pair agrees**, so `Venue-Structure` prints all three: the venue index counts from 0 and the lifecycle page `S-Main-<n>` counts from 0, so those two LINE UP, which is the whole reason 0-based was chosen; the Content division is the one that differs, because it counts the judgment divisions ahead of it. State this in the figure; do not make a reader work it out.

- 6 · 📐 The division shape a section division repeats
      Divisions `§1` to `§3` are the desk's judgment layer. Every division after them describes ONE section kind and repeats the same five parts, which is what makes the sections comparable across venues:
      ```
      ### <n> · <index>-<Kind>: <what this section is, in the desk's terms>
          **Caption**: the one thing that is true of it here and not elsewhere.
          ```text fence: 📐 ARC · 📏 BUDGET · 🧱 SHAPE · 🔀 VARIANT or 🖼 DISPLAYS OWED
          <emoji> Establishes ...        one line, what this division settles
      **<n>.1 · The moves, as slots        fill the shape; never lift the sentence**
      **<n>.2 · What the pack refuses      each a named anti-pattern, not a preference**
      **<n>.3 · Format values              words · citation density · value density · displays**
      **<n>.4 · The language, in the papers' own words   5-6 attributed sentences, one move each**
      ```

      The judgment divisions are not fixed in number, and `QBv1` runs three: what the desk buys and refuses, what arriving here costs, and which sibling outlet a paper leans to with the tie-break that pins it here.

      **Every number states its source inline.** A word budget, a paragraph count, or a citation density may appear only with the line that records it: a `style.md` line number, an exemplar name, or the desk's own page. Never as the page's own claim.

      **A slot the sources cannot fill is PRINTED.** `🔢 VALUE DENSITY  not recorded by the pack` is a finding; deleting the row is a silent gap. The same holds in `Submission-Rules`, which carries an open `❓ NOT ON RECORD YET` row.

      **Say what the desk REFUSES, not what it prefers**, because a preference does not decide a submission:

      ```
      ✅  a better classifier is not a MISQ paper
      🚫  MISQ values theory highly
      ```

      ## 🏛 When the target is NOT a journal

      A funder and a patent office are venue targets, and four of this contract's rules break on them. All four were found on 260803, by the agents that wrote `QBv15-grant` and `QBv16-patent`, and each is a real adaptation rather than a licence to skip the section.

      ```
      1  Sec-<n> HAS NO RESOLVER      section-kinds.yml declares ZERO kinds for grant and
                                      for patent, so no S-Main page exists and the index
                                      cannot be "the S-Main number"
                                      → grant used Row-<i>-<AGENCY>, the pack's own unit
                                      → patent read its index off 37 CFR 1.77(b), with
                                        HOLES: conditional items take a figure row and no
                                        division, so the index is not contiguous
      2  ONE TARGET, MANY DESKS       playbook-grant covers 8 agencies, playbook-patent
                                      covers CNIPA + USPTO + EPO, each with its own
                                      prescribed order
                                      → Venue-Structure becomes a MATRIX, one lane per
                                        agency; or PIN one, say so in three places, and
                                        keep the others' deltas as their own divisions
      3  "PACK OBSERVATION" IS EMPTY  the label means measured from published work, and
                                      these packs hold ZERO funded proposals and ZERO
                                      filings
                                      → use AGENCY RULE vs PACK RECORD, and say on the
                                        page why the measured tier is missing
      4  A RULE NEEDS ITS CYCLE       a journal's guidelines stand until changed; a
                                      funder's expire every round and an office's fees
                                      are dated
                                      → provenance says when it was READ · a non-journal
                                        row also says which CYCLE it binds
      ```

      **The unfixable step is not the page count.** At a journal it usually is. At a funder it is CHOOSING THE AGENCY, because a 15-page NSF description, a 5-page ERC Part I and a 7-page ARC description are three documents rather than three formats of one. At a patent office it is what the specification failed to disclose, because `35 U.S.C. 132(a)` bars new matter after the filing date. Verify the claim at source before writing it, as `QBv16` did.

      **A blueprint-only pack has no exemplar language, and the page says so.** The per-section shape (`n.1` moves, `n.2` refusals, `n.3` format values, `n.4` the papers' own words) presumes measured work. Fill only what the pack or the office actually says, and never print four subsubsections with empty rows to satisfy the shape.

      ## 📎 Files: five groups, and two of them are this kind's own

      The base offers a menu of action groups. A venue page takes these five, in this order:

      ```
      ⚙️ Engines       what REGENERATES this page       _tools/sync-exemplars.py
      📋 Contracts     THIS FILE, and the base it        haipipe-board-page-for-venue ·
                       extends                           haipipe-board-page
      📥 Input files   the pack files this page READS   taste.md · style.md · README.md ·
                                                        stages/section-kinds.yml
      🔗 Authority     what the DESK itself PUBLISHES, read directly and never through
                       the pack · opens with the provenance stamp · carries the desk's
                       links AND every place the desk contradicts the pack
      📤 Generated     what a tool WRITES into this page, between markers
      ```

      `Authority` and `Generated` are this variant's additions; the other three are the base menu's own names. Both additions state an action, which is the base's test for a group name.

      **This contract goes in `Contracts`, never in `Engines`** (JL 260803 asked which). The base's split is what decides it: an Engine is something you RUN and open to change behavior, while a Contract is what CARRIES a rule to other pages, and a loadable spec that never executes is named there. The row also has to say the link runs both ways: the page is this contract's reference implementation, so a rule changed on the page is changed in this file in the same pass, and a sibling outlet page reads this file rather than reading the reference page.

      ## 🤖 The generated spans

      `_tools/sync-exemplars.py` on the paper board owns two marker blocks inside `## Files`, and nothing else:

      ```
      <!-- exemplars:begin --> … <!-- exemplars:end -->    one row per exemplar PAPER,
                                                           keyed by filename stem
      <!-- kinds:begin -->     … <!-- kinds:end -->        the S-page roster, resolved
                                                           from stages/section-kinds.yml
      ```

      ```bash
      python3 <board>/_tools/sync-exemplars.py            # rewrite every outlet page
      python3 <board>/_tools/sync-exemplars.py --check    # exit 1 if any block is stale
      ```

      Never hand-edit between the markers: the next run overwrites it. The blocks are replaced by a marker regex, so they may sit under any heading, but keep the kinds block after the exemplars block. Run `--check` before calling a page finished; a stale block is a count that disagrees with the folder.

      ## 🩺 `state:` on a venue page

      The page keeps the base's four values, and the readable note answers one question: **how much of this desk is actually recorded, and how much is still prose nobody reads?**

      ```
      ✅  🟡 PARTIAL · 15 exemplars · 7 sections · taste ✓ · the one-sentence test is
                       unread by any skill
      🚫  🟡 PARTIAL                              ← says nothing a reader can check
      🚫  🟡 PARTIAL · pack looks good            ← a mood, not a count
      ```

      The desk being well documented is not the same as the desk being wired in. A page whose facts are complete and whose Aims are all `⬜` is honest, and common: the pack is a library until a lifecycle stage reads it.

      ## 🎯 Aims and States

      **This variant does NOT override the base's Aim form.** Ids, `Done when`, and one State row per Aim id all apply, unlike the skill-page variant, which drops them. Use `### A<n> · <emoji> <index>-<Kind>: <name>` to mirror the Content division, and `### P` for a target belonging to no single section, such as the submission mechanics or propagating a template to sibling pages.

      An Aim on a venue page is almost always the same shape: **something the pack records and nothing reads.** `Done when` names the run that would prove it, not the reading.

      ```
      ✅  A4.1 · The abstract variant is chosen before drafting, since it decides
                whether a number may appear.
          Done when: an abstract draft records its variant and its measured word
                     count against the 120-160 budget.
      🚫  A4.1 · Understand the abstract norms.        ← no run can close this
      ```

      **Keep States honest against the folds.** A Log line that says a question was settled and a State row that still says `⬜ Not started, and the pack cannot answer it` is the drift this board exists to catch; it happened on `QBv1` between 260802 and 260803.

      ## 🚪 The two verbs

      ### 📄 create a venue page

      1. Confirm the pack family and outlet folder exist under `paper/venue/`. A missing file at either level is a missing ANSWER to record, not a reason to stop.
      2. Copy `QBv1-misq.md` as the shape, never `ref/page-template.md` alone: the base template has no three-figure Diagram, no Authority group, and no section-division pattern.
      3. Take the next free `QBv<n>` and register the page in `board.md`'s `## Pages` under `QBv`.
      4. Fill `§1`-`§3` from `taste.md` and the family `README.md`, then one division per section kind from that kind's `style.md` and `template.md`.
      5. Fetch the DESK itself. Write `Submission-Rules` and the `Authority` group from it, with the provenance stamp, and record every contradiction with the pack.
      6. Run `sync-exemplars.py`, then build, check, and read the RENDER.

      ### 🔧 work on a venue page

      1. Read the whole page first, including the folds.
      2. Run the checker and clear the mechanical findings.
      3. Then check the three things no checker reaches: does every number name its source, is every desk fact stamped with how it was read, and does any State contradict a Log line.
      4. Re-read the desk when a fact is older than the last issue. A page limit or a reference style changes without a changelog.

      ```bash
      python3 <toolkit>/skills/board/haipipe-board/cli/build.py <board-folder>
      python3 <toolkit>/skills/board/haipipe-board/cli/check.py <board-folder> | grep '^QBv'
      python3 <board-folder>/_tools/sync-exemplars.py --check
      ```

      ## 📂 Files

      ```
      page-types/haipipe-board-page-for-venue/
      ├── SKILL.md            this variant contract
      └── CHANGELOG.md        version history
      ```

      Owns no scripts. The base frame is `haipipe-board-page`; the engine is `haipipe-board`; the generator for the marked spans is the paper board's `_tools/sync-exemplars.py`; the group's own law lives in that board's `board.md` under `### QBv · Delivery Venue`; the reference implementation is `QBv1-misq.md`.

<!-- haipipe:skill:body:end -->

## Aims
- [x] 🧪 It is used to write a venue page it was not lifted from
      Every rule in it was read off `QBv1-misq.md`, which is also the only page that satisfies it: of sixteen venue pages, one carries `Venue-Structure`, `Submission-Rules` and the `Sec-` index, and fifteen carry none of the three.
      A contract measured against the single page it was derived from has not been tested, only restated.
      Closed 260803 by the fourteen-desk fan-out its own 0.1.1 changelog records; re-measured 260806, thirteen of sixteen `QBv` pages carry the three shapes, with the grant and patent pages outside the journal index by design.
- [x] 🩹 Its own section-index rule stops contradicting itself
      The shipped `SKILL.md` rules that the index counts from ZERO so that `Sec-<n>` lines up with the lifecycle page `S-Main-<n>`, and then eight lines later says a section carries "three numbers that disagree on purpose", listing "the venue index counts from 1".
      The mapping table printed between those two passages shows the two indexes AGREEING, which is the whole reason 0-based was chosen after three tries.
      The 1-based sentence is leftover text from the superseded rule, and a writer who reaches it first will number every division wrong.
      Closed at 0.1.1 (260803): the shipped `SKILL.md` no longer contains the 1-based sentence, verified by grep on 260806.
- [x] 📓 The changelog stops teaching the rule the skill abandoned
      `CHANGELOG.md` 0.1.0 records the index rule as `### 4 · 1-Abstract` and repeats "venue index from 1", while `SKILL.md` of the same release rules `Sec-0-Abstract`, which is what `QBv1-misq.md` actually uses in all eleven of its section divisions.
      Both documents ship in the same folder at the same version, so the reader who checks the history is the one who gets misled.
      Closed at 0.1.1 (260803): the changelog now names the 1-based form only as the corrected defect, verified by grep on 260806.
- [x] 🔌 A writer who loads only the base is routed here
      `haipipe-board-page` 0.11.1 names `haipipe-board-page-for-skill` as its variant and never mentions this one, so nothing sends the author of a `QBv` page from the base to this contract.
      That is the same discoverability failure the sibling variant hit on 260802 in its other form, where the file existed and could not be reached.
      The fix lands in the base's own `SKILL.md`, which `Skill-3` mirrors, so this Aim closes on a change to that unit rather than this one.
      Closed by the base's one resolution table (0.20.0, 260805): a `QBv<n>` filename resolves to this contract at step ①, and the ten-variant list names it.
- [x] 🗺 Where this variant BELONGS is ruled
      It ships beside the base while its consumer is the paper family, and `haipipe-board-page` states that a variant ships under its consumer and never beside the base.
      Routed from `QC3a`, which already carries the open scope row for what the roster admits, widened once on 260802 when `Skill-7` landed for a unit outside `skills/board/`.
      Closed by the maintainer rule (JL 260803, "a variant ships WHERE THE BOARD FAMILY MAINTAINS IT") and the 0.1.2 move under the base's `page-types/` on 260804.

## States
The contract was lifted 260803 and describes a page kind that has sixteen instances, thirteen of which now carry its shapes after the same day's fourteen-desk fan-out.
Its health is `🟡 in flux` because the rules moved fast: the two shipped contradictions this page found were fixed at 0.1.1, and the folder moved under the base's `page-types/` at 0.1.2.
Nothing about it is unreachable, which is the one thing its sibling got wrong: the folder was linked into the skill roster on 260803 at 0026 and loads by name.

- 260803 CC · 🔎 Mirroring the unit found two contradictions inside one release
  The section index is ruled 0-based and then described as 1-based eight lines later, and the changelog documents only the 1-based form.
  Neither is reachable by any checker, because both halves are prose inside the skill's own file and the board's checks read the PAGE.
  Recorded here as the first evidence for something `QC1a` has argued generally: a `SKILL.md` needs its own headings read against each other, which is how the sibling variant found two `## 🎯 Aims and States` sections on 260803.
- 260803 CC · 📄 Page opened for a unit that shipped without one
  Generated with `skillpage.py new --group QC` and written to `haipipe-board-page-for-venue`, the eighth Skill row on the roster and the second variant of `Skill-3`.
  The roster's prose and the `QC · Engine` lane figure were updated in the same pass, which `QC1b` requires and which no script enforces.
- 260803 JL · 🏛 The rule was lifted OUT of the page that carried it
  JL ruled `QBv1-misq.md` the template for the other fifteen venue pages and then asked for the rule to be written down as a skill, rather than left as one page other pages are told to copy.
  That is the same move that produced `Skill-6` the day before, and the roster now carries two variants born the same way, which is an argument that the base's variant list is the thing that keeps going stale.

## Log
- 260806 2115 · [REVISE-CC] swept to the 260806 architecture; the WORKFLOW figure's "seven sections" corrected to the base's five on-stage sections (board-form.md §4, Files after, folds last), the count the venue skill's own 0.1.1 changelog already dropped
- 260806 0140 · [REVISE-CC] card synced to disk truth after 260805 (ten types · thin-paper phase 2 · first live RUN); the "1 of 16 conforms, never used, still contradicting itself" picture is replaced by the measured one, 13 of 16 conform after the 260803 fan-out, the 0.1.1 fixes landed, the base's resolution table routes QBv writers here, and the placement was ruled by the maintainer rule with the folder now under page-types/.
260803 0043 · authored half written: Opening, the WORKFLOW figure, Aims, States; `state:` ruled 🟡 in flux from 🔴 OPEN; Aims and States converted from the generator's base-form stub to the checkbox and dated-record form `haipipe-board-page-for-skill` overrides to
260803 0043 · page generated from `board/page-types/haipipe-board-page-for-venue/` by `skillpage.py new`

<!-- haipipe:skill:log:start 700d0f9ae07e31fd board/page-types/haipipe-board-page-for-venue -->

Converted from the skill's own `CHANGELOG.md`: 4 releases.

260804 · `0.1.2`
      - Moved under `page-types/` with the other stable Page Type variants.
      - Separates the venue Page's persistent structure from its current DRAFT, PROBE, REVISE, or CHECK authority.
260803 · `0.1.1`
      **Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.
      - **The section index contradicted itself eight lines apart.** `:149` ruled the index counts from ZERO so it lines up with `S-Main-<n>`; `:157` then said "the venue index counts from 1", which is the superseded rule left standing. A writer reaching `:157` first numbered every division wrong.
      - The 0.1.0 changelog entry taught that same abandoned 1-based form, in the same folder at the same version, so the reader who checked the history was the one who got misled. Corrected.
      - Drops "the seven sections" from the base description.
260803 · `0.1.1`
      Written from the fan-out: fourteen agents took this contract to fourteen desks the same day it shipped, and every item below is something a real desk broke rather than something anyone predicted. That is the point of releasing a contract and then running it at scale immediately.
      - **🧮 Add the pack's parts up against the desk's total.** Now a required row in `Venue-Structure`, because it went 3 for 3 the first time anyone checked: JAMA IM 3,350 against 3,000, PNAS ~6,970 against ~4,000, Diabetes Care 3,950 against 4,000, and JAMA where an RCT at the pack's floor lands within 50 words of the cap. The arithmetic is systematic: a pack measures published papers section by section, and a published page is not a submission budget, so the parts were never fitted to the whole.
      - **⏳ A binding rule has a WHEN.** Nature Communications is format-free at first submission and enforces its caps at revision; every Nature-family APC bites at acceptance, and npj's waiver must be requested at submission anyway. A binding row now carries at-submission, at-revision or at-acceptance.
      - **🔢 `Sec-<n>` = `S-Main-<n>` is a property, not a law, and the resolver wins when they part.** Five Nature-family desks print Methods last and PNAS reads Significance first, none of which `section-kinds.yml` orders that way. The fan-out split 2-2 on which side the index should follow; ruled for the resolver, because the index exists to JOIN the S page and an index tracking the desk stops being a join key the moment the two differ.
      - **🚨 The desk's section list can be longer than the resolver's, and the gap is a finding.** MISQ expects Concluding Remarks, Management Science requires a 250-word nontechnical executive summary, JAMA Network Open publishes a Research Letter: none is a declared kind, and a draft built from the resolver alone reaches the portal with a required field empty.
      - **🏛 A whole section on non-journal targets**, from `QBv15-grant` and `QBv16-patent`: no resolver means no `Sec-<n>`, one target can be many desks (8 agencies, 3 patent offices), `PACK OBSERVATION` is empty where a pack holds zero funded proposals, and a non-journal rule carries its CYCLE and not just its read date. Also that the unfixable step is choosing the agency, or what the specification failed to disclose, rather than a page count.
      - **🕶 Same-family rules are not the same desk's rules.** Nature Medicine's page carries neither superscript numbering, nor the et-al threshold, nor double spacing; those are *Nature*'s. A sibling rule inherited by proximity is the mirror of the pack-versus-desk error, one level in.
      - **📌 nature.com does not 403.** It 303s to its SSO host and WebFetch refuses the cross-host hop; `curl -L` with a cookie jar and a desktop UA returns 200. Four Nature pages were read live because one agent worked that out. INFORMS, PNAS and ADA genuinely do 403, and Wayback snapshots of the desk's OWN url are the next-best read, stamped as such.
      - **⚔️ Desks contradict THEMSELVES, and the page prints both.** ISR on anonymity and on its open-access fee, Management Science on single-blind against double-anonymous, JAMA on a 400-word against a 300-word Narrative Review abstract, Nature Communications on three separate pairs, Nature Medicine and NMI on Extended Data figures against items.
260803 · `0.1.0`
      First release. JL ruled `QBv1-misq.md` the template for the other fifteen venue pages, then asked for the rule to be written down as a skill rather than left as one page other pages are told to copy. Everything here was established on that page the same day and is lifted, not invented.
      - **📖 The governing principle: a venue page is a reference, not a rulebook** (JL 260803). Almost everything on it is a measurement of what published papers did, and departing from it is a choice rather than a violation; only the desk's own published rules bind. Found through a real misreading: `QBv1` printed "120-160 words, do NOT exceed ~185" for the abstract, which is the pack's measurement of eight papers, where the desk publishes no abstract cap at all. JL ruled ~250 words fine. Every length now says whose it is, and the pack's refusals are written as the pack's.
      - **🏛 The variant's reason: a venue page settles nothing.** Its subject is a desk outside the repo that publishes its own rules and rejects papers that ignore them. Three consequences drive every rule in the file: the subject is external, so facts carry provenance; there are two sources, so one has to outrank the other; and a paper is built from the page, so it owes structure and mechanics rather than taste alone.
      - **⚔️ The two-source rule, and the disagreement is the asset.** The pack (`paper/venue/playbook-*/`, its own repository, READ and never written) against the desk's own published instructions. The desk wins, and the gap is written down on the page naming both readings. `QBv1` carries three: the pack's observed "40-50 published pages" against the desk's 55-page submission ceiling, no reference style recorded where the desk requires APA 7th, and none of the submission mechanics recorded at all.
      - **📌 Provenance records HOW a fact was read, not just when.** Added after `misq.umn.edu` answered a direct fetch with HTTP 403 on 260803, one day after the same pages had been fetched successfully. A fact re-checked through search summaries is weaker than a fetched one and now says so on the page.
      - **🖼 Three figures, in a fixed order.** Desk taste (would this desk look at my paper), Venue-Structure (what am I writing), Submission-Rules (what the portal demands). Figures ② and ③ were written on 260803 at JL's request; ① already existed on every outlet page.
      - **🔗 Links are embedded twice on purpose.** Verified against `src/body.py`: a fenced block is rendered with `esc()` plus the figure linker and never the inline markdown pass, so a URL inside a figure is plain text. Bare hosts go in the figure, real markdown links go directly under it. Also records that a bare URL alone on a line in `## Diagram` is the Excalidraw canvas slot.
      - **🔢 The section index rule** (JL 260803, "I want to see the index"): `### 4 · Sec-0-Abstract: ...`, with the Aims and States groups repeating the name behind their emoji. A section carries three numbers that disagree on purpose (venue index from 0, so it lines up with `S-Main-<n>`; Content division counting the judgment divisions, `S-Main-<n>` from 0), so `Venue-Structure` prints all three rather than making a reader work it out.
      - **📋 This contract is filed under Contracts, not Engines** (JL 260803 asked which). The base menu's split decides it: an Engine is run and opened to change behavior, a Contract carries a rule to other pages, and a loadable spec that never executes is the second. The reference page lists this file, this file names that page, and a rule changed in one is changed in the other in the same pass.
      - **📎 Two Files groups this kind adds**: `🔗 Authority`, what the desk itself publishes, and `📤 Generated`, what a tool writes between markers. Both state an action, which is the base's test for a group name. Recorded after `QBv1`'s Files section was found flat, against `QB4-overall.md` §6's action menu.
      - **🎯 States the NON-override explicitly.** Unlike `haipipe-board-page-for-skill`, this variant keeps the base's Aim ids, `Done when`, and one State row per Aim. Said out loud because a reader arriving from the roster variant would otherwise assume every variant drops them.
      - **❓ An unfillable slot is printed, never deleted.** `not recorded by the pack` is a finding; a missing row is a silent gap. Applies to the format-values fences and to `Submission-Rules`, which carries an open `NOT ON RECORD YET` row.

<!-- haipipe:skill:log:end -->
