# The page a stage works on, and who owns which part of it
state: 🟡 PARTIAL
owner: JL
method: one markdown file, four regions, four owners, and no two of them writing the same bytes

## Opening
You hand the skill a stage page and it modifies that page. So before anything else in this group can be settled, the page has to be understood as an object: what it is, where each part of it came from, and who is allowed to write where. It is one markdown file, and four different things have a claim on it. That sounds like a recipe for collision and is not, because of a design decision that is easy to miss.

The four are the BOARD, which supplies the generic shell and a machine-managed block; the STAGE TEMPLATE, which supplies the Paper divisions inside `## Content` and the job line under each; the PAPER SKILL, which writes the prose and the queue; and the SENTENCE LAYER, which carries the Paper Board's sentence and evidence requirements. They never contend because each writes at a different moment and into a different region: `stage.py new` lays the shell, `create-page.py` compiles the stage template into `### divisions`, and only then does a phase worker write prose. By the time anything is drafted there is one file with one grammar.

This face is the anchor for four questions that are all about this same object, and are otherwise easy to mistake for each other. What SHAPES the page is `QC3a`. What it is CALLED, and how many of it exist, is `QC3b`. What a SECOND run does to it is `QC3c`. What is generated OUT of it is `QC3d`.

What is unsettled sits at the seams rather than in the middle. One rule is declared twice, in a stage's `formatting:` and again by `QC5`. One region is machine-managed and sha256-digested, and nothing tells a writer to stay out of it. And when the venue's Structural Blueprint, the stage template and the page's own `style_from:` all describe one paragraph, only a single stage's contract says which wins.

Scope: This page covers What a stage page is, its four regions and their owners, why the contracts layer instead of competing, and the seams where they can still disagree. Neighbouring pages cover What the contract declares is `QC2`; the four sub-questions are `QC3a` to `QC3d`; the flow that modifies the page is `QC4`; the board's own face grammar and the ①/③ ownership line are `QA8`; what a line inside a division may be is `QC5` to `QBe1 §7`.

## Diagram
```
   📄 A STAGE PAGE.  one markdown file · four regions · four owners.

   ┌──────────────────────────────────────────────────────────────┐
   │ state: · owner: · method: · requires: · style-from:          │
   │ provides: · contract-source-hash:  ③ THE BOARD, at create    │
   ├──────────────────────────────────────────────────────────────┤
   │ ## Question · ## Boundary          ③ shell · ① fills         │
   ├──────────────────────────────────────────────────────────────┤
   │ ## Stage Contract         🔒 MACHINE-MANAGED · DO NOT TOUCH  │
   │   ### Required Inputs   ◀ generated from `requires:`         │
   │   ### Writing Style     ◀ generated from `style-from:`       │
   │   sha256 over its SOURCES, never itself · stage.py sync      │
   │   "build.py never edits Markdown"                            │
   ├──────────────────────────────────────────────────────────────┤
   │ ## Content                         ① THE PHASES WRITE HERE   │
   │   ### <division>  ◀ from the STAGE TEMPLATE's Setext section │
   │       (job line)  ◀ from that section's <!-- RULE -->        │
   │       the prose   ◀ at 🅲's sentence formats                  │
   ├──────────────────────────────────────────────────────────────┤
   │ ## Items to Finish                 ① THE PHASES WRITE HERE   │
   │   - [ ] 🔎 Q-<Stage>-<n>   one per hole DRAFT could not fill │
   ├──────────────────────────────────────────────────────────────┤
   │ ## Where we are · ## Files         ①                         │
   └──────────────────────────────────────────────────────────────┘

   ── WHY FOUR CLAIMS DO NOT COLLIDE ───────────────────────────────
      because each is compiled in at a DIFFERENT MOMENT:

      ③ board template  ──▶ stage.py new
                            the SHELL: which `##` sections exist
                                │
      ① stage template  ──▶ create-page.py :: template_divisions()
                            a Setext `-----` section ──▶ `### division`
                            its `<!-- RULE -->`      ──▶ the job line
                                │                             → QC3a
      ①③ style-from:    ──▶ stage.py :: render_block()
                            a Writing Style block generated FROM
                            another page, sha256-digested
                                │
                                ▼
      🅲 the sentence layer ▶ what a LINE inside a division may be
                                              → QC5 QBe1 §4 QBe1 §5 QBe1 §6 QBe1 §7

      ⇒ the stage template is NOT a file a phase opens and copies.
        It was already turned into this page's skeleton before any
        phase ran. That is why nothing has to arbitrate.
      ⚖️ the same disjoint-region discipline QA8 states between ① and
        ③, applied one level down, inside a single file.

   ── THE FOUR QUESTIONS ABOUT THIS OBJECT ─────────────────────────
      QC3a  what SHAPES it     skeleton to fill, or spec to parse
      QC3b  what it is CALLED  identity ▸ filename, and HOW MANY
                               pages exist (`runs:`)
      QC3c  a SECOND run       what happens to a page you edited
      QC3d  what comes OUT     md ▸ tex, one way, never back

   ── WHERE THE FOUR CAN STILL DISAGREE ────────────────────────────
      ⚠️ ONE SENTENCE PER LINE is declared THREE TIMES: every stage's
         `formatting: line_breaks:`, QC5, and the Board's own
         `ref/writing-rules.md:35`, which is the one that BINDS the
         rendering. Three homes for one rule is how three drift apart.
      ⚠️ the MANAGED BLOCK's digest covers its SOURCES, never itself,
         so nothing detects a hand-edit and nothing tells a writer it
         is off limits. The next `stage.py sync` reverts it in silence.
      ⚠️ PARAGRAPH COUNTS have three claimants: the venue Structural
         Blueprint (BINDING), the stage template, and `style-from:`.
         Only section-edit's contract states an order.

   ── WHO READS THIS, AND HOW IT FAILS ─────────────────────────────
      fields   template · sections · formatting, plus the page's own
               `requires:` and `style-from:`
      reader   ② THE CREATOR lays the regions       fails 🔊 LOUD
               ③ THE EXECUTOR writes inside them    fails 🔇 SILENT
                                                            → QC2
      to bind  the region boundary is the checkable part: RE-RENDER
               `## Stage Contract` and compare bytes. The stored
               sha256 cannot do it, because it hashes the SOURCES.
               Anything that drifted was written by something that
               should not have been writing there.
      ⛔ and the frontmatter is a CLOSED whitelist, not a free map:
         src/parse.py:145 keeps state owner method session requires
         style-from provides contract-source-hash. Any other key is
         dropped in silence, which is why CONTRACT.md had to rule out
         a `venue:` key on the page that pins the venue.
```

## Content
### Four owners, and the moment that separates them
No two of the four ever write the same bytes, and that is a consequence of ordering rather than of etiquette. The board writes the shell first, the creator compiles the stage template into divisions second, and a phase writes prose third. Each step finds the previous step's output already in place and adds only what is missing.

The compilation is the part that becomes invisible afterwards. `create-page.py` reads the stage's `template.md`, finds every Setext `-----` heading, emits it as a `### division` under `## Content`, and takes the first `<!-- RULE -->` in that section as the division's job line, truncated at 220 characters. Afterwards the page shows no sign that a template was involved, which is why a reader can mistake the divisions for something a phase invented.

### The region nobody may write
`## Stage Contract` is generated by `stage.py` from the page's own `requires:` and `style-from:`, and is refreshed by `stage.py sync`. `build.py` never edits markdown, so nothing rewrites it during a build. Anything written there gets no error and is lost at the next sync, which makes it the quietest failure mode on the page and the one most worth a check.

The sha256 that sits on the block is not that check, and it is easy to assume otherwise. `contract_digest()` in `src/stage_contract.py` hashes the pages named by `requires:` and `style-from:` and says so in one line of its own docstring: hash only the sources, never the destination page. So the digest detects a source that has MOVED ON, which is what `stage.py check` reports, and it is blind by construction to a hand-edit inside the block it is printed on.

### Generic Board page, Paper-specific writing dialect
The Board contracts define a generic working record: the Q/S shell, where `## Content` begins, how a heading or source line receives an address, and how a comment or routed record is attached. They do not say what a manuscript section, paragraph, or sentence has to accomplish.

This Paper Board supplies that second layer without changing Board grammar.

| Level | Generic Board contract | Paper Board requirement |
|---|---|---|
| Section | a `###` division and its page boundary | a reader-facing purpose, stage/venue constraints, and a declared contribution to the paper's argument |
| Paragraph | a `####` heading and addressable sibling prose | a paragraph job plus an intelligible claim → evidence → warrant → implication progression where applicable |
| Sentence | one addressable source line with attachable lanes | a local claim or rhetorical job, traceable citation/value/display/owed evidence, and a sibling-aware revision check |

`QC5` is the authority for this Paper overlay. `haipipe-page` and `haipipe-sentence` remain the reusable substrate; they must not inherit Paper's rhetoric, evidence states, or human gates.

### Why this is the anchor rather than four unrelated faces
`QC3a` to `QC3d` were four separate faces until 260726 and read as interchangeable, because each opened by describing the same file from a different angle. Naming the object once, here, lets each of them ask only its own question: what shapes it, what it is called, what a re-run does, what comes out.

## Aims
- [x] 📐 The four contracts are layered, not arbitrated
      Shell at `stage.py new`, divisions at `create-page.py`, prose in a phase. Each writes a different region at a different moment, and the layering is live rather than proposed: 40 S pages on the MISQ paper, 39 of them carrying a generated `## Stage Contract` block.
- [ ] 🧠 Rule where `style-from:` ranks against the venue blueprint
      Three sources describe one paragraph and only one stage says anything about order. `5-section-edit/stage.md:76` declares the Structural Blueprint BINDING and its lines 184-186 say the blueprint wins on numbers; the stage template carries its own `<K> paragraphs` and `<n> sentences · ~<m> words` slots; and `style-from:` generates a Writing Style block on 32 of the 40 live MISQ pages. Two options: blueprint then template then style-from, as a page-level rule; or style-from second, because it is generated from a page a human pinned while a template is a generic skeleton.
- [ ] 📐 Say which sentence-format contract is authoritative
      One sentence per line has three homes, not two: `formatting: line_breaks:` in all eight stage contracts, `QC5` (state ✅ SETTLED, "the approach is one sentence per source line"), and `haipipe-board/ref/writing-rules.md:35`, which is the one the renderer actually depends on. Name that third one as the owner and make the other two cite it.
- [ ] 📐 Tell a writer the managed block is off limits
      `## Stage Contract` exists on 39 of the 40 live MISQ S pages, is regenerated by `stage.py sync`, and no phase contract under `paper/2-phase/` names it. The one line that says so today is printed INSIDE the generated block, at `stage.py:142`, so it is only visible to someone already reading what they should not be editing.
- [ ] 🔍 Assert the managed block still matches its generated form
      The existing digest cannot do this. `src/stage_contract.py`'s `contract_digest()` hashes only the pages named by `requires:` and `style-from:`, and its docstring says so: never the destination page. So `stage.py check` reports a stale SOURCE and is blind to a hand-edit. The assertion is to re-render the block for each page and compare bytes, over 39 pages that already exist.
- [ ] 📐 Name the frontmatter whitelist as a closed set
      `haipipe-board/src/parse.py:145` accepts exactly `state owner method session requires style-from provides contract-source-hash` and drops everything else in silence. `../../paper/haipipe-paper-stage/stages/CONTRACT.md` already had to rule out a `venue:` key for this reason. This face draws the frontmatter as one region of the page and never says the set of legal keys is fixed.
- [ ] 🧪 Hand-edit a managed block, then run `stage.py sync`
      The acceptance test for the protected region. Copy one of the 39 pages, write a line inside the block, sync, and confirm the line is gone and nothing warned. The reversion is stated in `stage.py:142` and has never been watched happen.

## States
The layering works and is in daily use on the MISQ paper, which carries 40 S pages, 39 of them with a generated `## Stage Contract`. A stage is called, the page already exists with its shell and its divisions, and the phases fill them; nobody has had to arbitrate, because the four owners never touch the same bytes. The one page without a managed block is `S-Seed-0-seed.md`, and that is correct: seed has no upstream, so it declares no `requires:` and no `style-from:`, and the generator has nothing to render.

The boundary is now explicit: Board owns generic page mechanics; this Paper Board owns the manuscript-specific requirements that live in those mechanics. The detailed sentence and evidence rules remain on `QC5`.

What is open is all at the seams. One rule has two homes, one region is protected only by nobody having tried to write in it, and one precedence order is stated on a single stage's contract rather than for the page.

## Files
- `board/haipipe-board/stage.py`
  `stage.py new` writes the shell; `render_block()` generates the managed `## Stage Contract` from `requires:` and `style-from:`. Line 142 is the only place that says the block may not be hand-edited.
- `board/haipipe-board/src/stage_contract.py`
  Where the digest rule actually lives. `contract_digest()` hashes the SOURCE pages and never the destination, and `contract_status()` is what turns that into the one warning `stage.py check` prints.
- `board/haipipe-board/src/parse.py`
  Line 145 is the closed frontmatter whitelist. A key outside it is dropped without a word.
- `create-page.py`
  `template_divisions()`: where a stage template becomes this page's Content divisions and job lines, with `compact_rule()` truncating each job line at 220 characters.
- `../../paper/S06-main/section-edit/stage.md`
  The one contract that states a precedence when the blueprint and the pack disagree: line 76 declares the blueprint BINDING, lines 89-91 make a pack row REFERENCE ONLY, and lines 184-186 say the blueprint wins on numbers.

## Law

- A stage page is one markdown file with four owners, and they never contend because each writes at a different moment and into a different region: the Board lays the shell, the creator compiles the stage template into `## Content` divisions, the phases write prose and the queue, and the sentence layer governs what a line inside a division may be.
- `## Stage Contract` is machine-managed. It is generated by `stage.py` from the page's own `requires:` and `style_from:`, it carries a sha256 digest, and nothing else may write there.
- The stage template is not a file a phase opens and copies. It is compiled into the page before any phase runs, and survives inside it as division titles and job lines.

## Discussion
> CC 260727: the paragraph-count precedence is worth JL's ruling now rather than later, because it is the only one of this face's seams that a wrong answer makes VISIBLE in the manuscript. My recommendation is blueprint, then `style-from:`, then the stage template, in that order, and to state it on this face rather than on `5-section-edit`. The reason to put `style-from:` above the template is that it is generated from a page a human pinned and can be traced back to it, while a template is a generic skeleton nobody signed.
> The cost is that it changes the order `5-section-edit/stage.md` already implies, where the blueprint is BINDING and everything else is undifferentiated reference, so that contract needs an edit rather than just a citation. The cheaper option is to lift section-edit's two-level order (blueprint BINDING, everything else reference) to the page and leave `style-from:` unranked, which settles nothing about the 32 pages that carry a generated Writing Style block and will be asked again the first time one of them disagrees with a blueprint.

## Log
260726 · Created as the anchor of the page half of QB, on JL's restructure: the group's mental model is "hand the skill a stage page and it modifies it in a predefined flow", so QB is now the stage (`QC2`), the page (`QC3`) and the flow (`QC4`). The four-region ownership map and the layering argument moved here out of `QC4a`, where they had been written as if they were DRAFT's business; DRAFT now points here and keeps only what it itself adds and refuses.

260727 · Verified against the two programs and the live paper, which corrected three things and added one region. The frontmatter key is `style-from:` on the page, not `style_from:`; the underscore form is only the parsed dict, so every diagram and prose mention here was spelling a key that no page carries. The sha256 on `## Stage Contract` does NOT protect the block: `src/stage_contract.py`'s `contract_digest()` hashes the pages named by `requires:` and `style-from:` and its docstring says never the destination page, so `stage.py check` catches a moved source and is blind by construction to a hand-edit. That makes the digest item sharper rather than redundant, because the check it asks for is a re-render and byte compare, and it can run today over the 39 live pages that carry a block. One sentence per line turned out to have three homes, not two, the third and binding one being `haipipe-board/ref/writing-rules.md:35`. And a fifth thing the page owns surfaced while reading `src/parse.py`: the frontmatter is a closed whitelist of eight keys, so a writer who invents one gets silence, which is the same failure mode as writing in the managed block and had no item. The precedence question was rewritten from a 📐 into a 🧠 with its two options named, because the third claimant's rank is genuinely unruled and `5-section-edit` decides only that the blueprint beats the pack.
260801 · Distinguished generic Board page mechanics from the Paper-specific section, paragraph, sentence, and evidence dialect. QC5 now owns the latter rather than Board's reusable page specs.
