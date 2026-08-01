# What shapes the page: a skeleton to fill, or a spec to parse?
state: 🟡 PARTIAL
owner: JL
method: rule whether a template is a skeleton to copy or a spec to parse, then make it one of them

## Opening
What is `template.md`, and who reads it? Eight of them exist, 754 lines in total, and no page on this board has ever described one. That silence is expensive, because the file is read twice by two different things that believe two different stories about it, and only one of those stories is written down anywhere.

Seven of the eight open with a variant of "TEMPLATE (follow, don't ship)": a skeleton whose `<…>` slots get replaced and whose `<!-- RULE: … -->` comments are guidance to follow then delete. That is the story an agent reads. But `create-page.py` does not copy the file at all. It PARSES it, and it parses THREE different forms of it, in a fixed order: a whole S page whose `### ` headings under `## Content` become the divisions, a Setext file whose `-{3,}` underlines do, or an ATX file whose `## ` headings do. Each division's job line is the first `<!-- RULE -->` in that section, compacted to 220 characters. Under that story the underlines are load-bearing syntax and the RULE comments are machine input.

Both stories are true today, neither file says so, and the eighth template has quietly resolved the argument in one direction: `4-display/template.md` is a whole S page with its own `state:` and its own `## Items to Finish`, meant to be copied. So the two stories are not competing readings of one file. They are two shapes of file, both on disk, both accepted, with nothing declaring which a new template should use. The consequences are also on disk: three of the eight templates instruct the drafter to fill their own `artifact_fallback:` rather than their `artifact:`, and `formatting:` declares `section_rule: "-----"` on the one contract whose template contains no Setext underline at all. What we want is one story, stated in the file, so that changing a template has a predictable effect on both readers.

Scope: This page covers What `template.md` is, both things that read it, and what the contract's `template:` `sections:` and `formatting:` fields mean. Neighbouring pages cover What the contract declares is `QC2`; how the page gets created and named is `QC3b`; what a re-run does to a page already filled is `QC3c`; what DRAFT does with the shape is `QC4a`; what a `<!-- RULE -->` becomes once the prose is real is `QC5`.

## Diagram
```
   📄 stages/<order>-<key>/template.md   is read TWICE, by two readers
      who have been told different things about it.

   ── READER 1 · create-page.py, at PAGE-CREATION time ──────────────

      template_divisions(path)   THREE BRANCHES, tried in order
        │
        ├─① BOARD form   :107  the file has `## Content` +
        │     `## Items to Finish` + `## Where we are`. Its `### `
        │     headings ARE the divisions; Q-consumer is SYNTHESIZED
        │     from a `Q-<X>-<n>` string in the Items block.
        │     ▸ 1 template: 4-display. ZERO Setext underlines.
        │
        ├─② SETEXT form  :122  the `-{3,}` underline scan.
        │     ▸ 6 templates.
        │
        └─③ ATX form     :138  `## ` headings before the Setext
              `Q-consumer` marker, MERGED into ②'s result. The code
              comment names the cases: "Narrative, Resource, and
              section templates deliberately use ATX `##`".
              ▸ 3-narrative has 1 underline and lives here.
        │
        ▼
      ## Content
      ### <Title>
      (job line = that RULE, whitespace-collapsed, cut at 220 chars)
      ## Items to Finish
      (a BOARD-form template's OWN Items block, copied whole, with
       `q_id_pattern`'s id substituted · board_template_items() :174)

      ⛔ zero divisions from all three  ──▶ SystemExit: "no logical
         stage divisions found in template"                    :170
      ⛔ no Q-consumer division         ──▶ SystemExit: "stage
         template has no Q-consumer division"                  :361
      ✅ all 103 templates satisfy both today.
      ⚠️ a template with no Setext section does NOT abort: 4-display
         has none and parses through branch ①.

   ── READER 2 · the DRAFT agent, at RUN time ───────────────────────

      "TEMPLATE (follow, don't ship)"
        replace every  <…>
        follow then DELETE every  <!-- RULE: … -->
        delete the top line too

      ⚠️ under THIS story the RULE is guidance that disappears.
         Under reader 1's story the same RULE is the division's
         permanent job line. Same comment, two fates.

   ── what the CONTRACT says about it ───────────────────────────────
      template:    the filename                     ✅ used by reader 1
      sections:    the artifact's parts, top to bottom
      formatting:  title_rule "=====" · section_rule "-----"
                   line_breaks · headings · comments
                   ⚠️ the parser HARDCODES  -{3,}  at :127 :130 :144
                      and never reads section_rule. Two copies of one
                      rule, and the copy in the contract is WRONG on
                      4-display, which declares it (stage.md:106) with
                      zero Setext underlines in its template.

   ── AND THERE ARE TWO SOURCES, NOT ONE ────────────────────────────
      the eight `stages/*/template.md` are not the only templates.
      `5-section-edit` declares  template: <resolved per (venue, kind)>

        venue pack HAS a template for this (venue, kind)
              venue/playbook-<family>/<VENUE>/<VENUE>-<kind>/template.md
              ──▶ USE IT · AUTHORITATIVE
        no pack template, or a pack-less venue (grant · patent · NEJM)
              ──▶ FALL BACK to stages/5-section-edit/template.md
                  whose own header calls itself the fallback, not the
                  default. `fallback_template:` names it explicitly.

      ⚠️ the resolution is NOT re-run per section. The VENUE stage
         resolves every path ONCE and writes the rows onto the S page:
           "Section Styles (RESOLVED here -- downstream reads
            these rows, never re-derives)"
         so section-edit READS a path; it never resolves one.
         resolve_template() :202 splits each row on `·` and takes the
         `template:` field. A pipe table would not parse.
      ⚠️ 2a-venue/template.md:36 still heads that block "downstream
         reads this TABLE", while 2a-venue/stage.md:126 says one
         RECORD LINE per kind. The parser sides with stage.md.
      📌 the pack is a pinned submodule, and the S page records the
         pin plus the drift diff when it moves. A template path is
         therefore evidence on a page rather than a lookup.

      ➡️ which means whatever is ruled below applies to 8 + 95 = 103
         template.md files, not 8. (venue/ holds 504 files: 245 md,
         254 pdf; only 95 of the md are templates.) The venue 95 were
         written against the same "follow, don't ship" story, are read
         by the same parser, and all 95 carry a Q-consumer division.

   ── what is on disk RIGHT NOW ─────────────────────────────────────
      by FORM, and where each header points the drafter.

      ① BOARD form · a whole S page to COPY
        4-display     "Copy this file to 3-display/
                       S-Display-<N>-<slug>.md"                  ✅
                      ⚠️ AHEAD of its own contract, whose artifact
                         still says 4-display.md            → QC3b

      ② SETEXT form · the `-{3,}` scan
        0-seed        Fill 0-lifecycle/0-seed/0-seed.md          ⚠️
        1b-claims     Fill 0-lifecycle/1-work/1b-claims.md       ⚠️
        2b-pitch      Fill 0-lifecycle/2-venue/2b-pitch.md       ⚠️
        1a-resource   Fill …/1-work/S-Work-0-resources.md        ✅
        2a-venue      Fill …/2-venue/S-Venue-0-venue.md          ✅
        5-section-edit  "copies it to 4-main/{section}.md"       ⚠️

      ③ ATX form
        3-narrative   (no Fill line)

      THREE are stale, not five. 1a-resource and 2a-venue now name
      their contract's `artifact:` byte for byte. And the three that
      remain each name that stage's own `artifact_fallback:`, so they
      point at a REAL file on an unmigrated paper; nothing resolves
      to nothing. That is why they are cheap and why they survived.

   ── WHO READS THESE FIELDS, AND HOW THEY FAIL ────────────────────
      ⚠️ THIS FACE IS SPLIT, and the split IS the bug.
      the template PATH      `template:`
        reader  ② THE CREATOR · create-page.py                  → QC2
        fails   🔊 LOUD, and there are SEVEN refusals, not three:
                :189 no template · :193 dynamic needs --section-kind ·
                :197 venue page absent · :213 no Section Styles record
                for this kind · :232 template not found · :170 no
                logical divisions · :361 no Q-consumer division.
      the template CONTENT   everything inside the file
        reader  ③ THE EXECUTOR · a drafting agent
        fails   🔇 SILENT.
      ⇒ that is EXACTLY why three `Fill` lines survived a restructure:
        the PATH resolved, so nothing raised, while the CONTENT told
        the drafter to write into a filename retired months ago.
      to bind  extend the parse that already fails loud: assert the
               header's declared target matches the contract's
               `artifact:`. One line, in the reader that already exists.
```

## Content
### Two readers, two stories, one file
The file believes it is a skeleton. The creator treats it as a spec. Neither is wrong on its own and the combination has no owner, so a change made for one reader lands on the other unannounced: retitle a section for readability and you have renamed a Content division on every page that stage will ever create; drop a RULE comment as obvious and you have replaced a job line with the fallback string `Complete the <Title> stage output.`

The cost is not hypothetical. It is why the stale `Fill` lines survived the S-face restructure: nothing about the parse path touches that line, so nothing failed, and the only reader who suffers is the drafting agent, which is the reader with no error channel.

### The argument has already been settled once, on one template
`4-display/template.md` is not a skeleton with slots. It is a complete S page carrying its own `state:`, `owner:`, `method:`, `requires:` and `style-from:` lines, its own four `### ` divisions, and its own `## Items to Finish` scaffold. Its header says to copy it. The parser has a branch for exactly that shape, tried before the other two, and it also lifts that Items block onto the new page verbatim with `q_id_pattern`'s id substituted in.

So the template does not supply two things (divisions plus job lines). It supplies four: the division titles, the job line under each, the Q-consumer division, and, in board form, the whole queue. `QC3` states the first two, and stating half of what a compilation step does is how a reader forms a wrong model of it.

### What the template is FOR, once the two stories are separated
The division titles and their job lines are the artifact's SHAPE, and the shape is what a stage guarantees regardless of who runs it. The `<…>` slots and the prose guidance are DRAFTING HELP, and help can be as long as it likes. The 220-character truncation is the seam between them: it only makes sense if the RULE's first sentence is the job and the rest is help, and no template has been written knowing that.

### What is not decided
Which FORM a new template should be written in. Three are accepted, their precedence lives in a code comment, and no contract field records which form a given template uses.

And whether `sections:` in the contract and the divisions in the template must agree, and which one wins if they do not. Today both exist, `check-contracts.py` requires `sections:` to be present, the parser reads only the template, and nothing compares them.

## Items to Finish
- [x] 🔧 Two of five stale `Fill` lines already repaired
      `1a-resource/template.md:1` names `S-Work-0-resources.md` and `2a-venue/template.md:1` names `S-Venue-0-venue.md`, each matching its contract's `artifact:` exactly. The headline count on this face is 3, not 5.
- [ ] 🧠 Rule what a template IS, given three forms
      A: a spec `create-page.py` parses, one form only, with drafting help inside RULE comments and the file saying so. B: a whole S page the drafter copies, which `4-display/template.md` already is, with the divisions declared in the contract's `sections:` and the parse branches deleted. C: all three forms stay and every template's header names its own. The parser accepts all three today (`create-page.py:107` board, `:122` Setext, `:138` ATX merged into Setext) and nothing outside that function's comment says which a new template should use.
- [ ] 🔧 Repair the three stale `Fill` lines
      `0-seed/template.md:1`, `1b-claims/template.md:1` and `2b-pitch/template.md:1` each point the drafter at that stage's `artifact_fallback:` instead of its `artifact:`. Blocked on nothing; it is still the cheapest item here.
- [ ] 🔧 Delete `section_rule` or make the parser read it
      Seven contracts declare `formatting: section_rule: "-----"` and no reader reads it; `create-page.py` hardcodes `-{3,}` at :127, :130 and :144. It is not merely a duplicate: `4-display/stage.md:106` declares the Setext rule while `4-display/template.md` contains zero Setext underlines, so the field is actively wrong on one of eight.
- [ ] 🔍 Assert every template parses and carries a Q-consumer
      `create-page.py:170` raises on zero divisions and `:361` raises on a missing Q-consumer, and neither refusal is exercised until somebody creates a page. Run `template_divisions()` over all 103 templates (8 stage, 95 venue) and require at least one division plus a Q-consumer in each. All 103 pass today; the check locks that in before a ninth template arrives.
- [ ] 📐 Say that the template also supplies the Items scaffold
      `board_template_items()` at `create-page.py:174-182` copies a board-form template's whole `## Items to Finish` block onto the new page with `q_id_pattern`'s id substituted. This face and `QC3`'s Law both describe the template as supplying divisions and job lines only, which is two of the four things it supplies.
- [ ] 📐 State the 220-character contract
      `compact_rule()` at `create-page.py:71-76` collapses whitespace, strips a leading `RULE:`, cuts at the last space before 220 and appends an ellipsis. Either a job line is the RULE's first sentence and the rest is help, or the truncation is arbitrary. Say which, in the header of each template.
- [ ] 🔧 Stop calling the venue resolution a table
      `2a-venue/template.md:36` heads the block "downstream reads this table" while `2a-venue/stage.md:126` says one record line per kind and `resolve_template()` at `create-page.py:202-211` splits each row on `·`. JL banned pipe tables in stage docs, so the word invites the one shape the parser cannot read.
- [ ] 📐 Rule whether `sections:` and the template's divisions must agree
      Both declare the artifact's parts. `sections:` is required by `check-contracts.py:35` and compared to nothing; `create-page.py` reads only the template. Nothing says which wins.
- [ ] 🧪 Add a ninth stage's template, read the result
      The acceptance test for this face: write only `stages/9-<key>/template.md` plus its `stage.md`, run `create-page.py <key> <paper-root>`, and check the divisions, the job lines, the Items scaffold and the Q-consumer without opening `create-page.py`.

## Where we are
Eight stage templates and 95 venue templates exist and are in daily use, and the mechanism works: all 103 parse, all 103 carry a Q-consumer division, and pages get created with the right divisions and job lines. Nothing here is broken in a way that fails loudly, which is exactly why it has gone undescribed for so long.

Nothing is ruled. This face is 🔴 because the central question, what the file IS, has never been asked. Measuring it on 260727 made the question harder rather than easier: there are three accepted forms rather than two competing readings of one form, and `4-display/template.md` has already answered it in the "copy a whole page" direction without any ruling.

## Files
- `stages/*/template.md`
  Eight templates, 754 lines, 46 to 140 lines each. One board form (`4-display`, zero Setext underlines), six Setext, one ATX (`3-narrative`).
- `haipipe-paper-stage/create-page.py`
  `template_divisions()` :89-171 (three branches), `compact_rule()` :71-76, `board_template_items()` :174-182, `resolve_template()` :185-232.
- `stages/CONTRACT.md`
  Declares `template:`, `sections:` and `formatting:` as required fields, and says nothing about how they interact or which form a template may take.
- `stages/2a-venue/template.md`
  Line 36 heads the Section Styles block; the source of the "table" versus "record line" drift.
- `venue/`
  95 `template.md` files under `playbook-<family>/<VENUE>/<VENUE>-<kind>/`, out of 504 files (245 md, 254 pdf). All 95 carry a Q-consumer division.

## Law
_None yet. This face is 🔴 and its first item is the ruling that would produce one._

## Discussion
> CC 260726: I would rule A. The parse path is the one with an error channel, so it is the one that will stay honest; a skeleton nobody parses drifts silently, which is precisely what the five stale `Fill` lines are. Under A the template header changes from "follow, don't ship" to something like "this file's `-----` sections BECOME the page's Content divisions; the first sentence of each RULE becomes its job line; everything after that is help for the drafter."
> The cost of A is that a template stops being freely editable prose, and that cost is real. It is also the cost we are already paying without having agreed to it.

> CC 260727: measuring the parser changed which option is cheap, so the 260726 recommendation above needs a correction rather than a repeat. There are three accepted forms, not one, and the newest template (`4-display`, written 260726) is the one that is furthest from A: it is a complete S page with its own frontmatter and its own queue, i.e. it is option B, shipped without a ruling. A now means converting or grandfathering 7 stage templates plus 95 venue templates onto one form; B means the opposite conversion, on 102 files, and losing the `board_template_items()` path that `4-display` depends on.
> So my recommendation moves to C, with one condition: each template header declares its form in a fixed first line, and `check-contracts.py` asserts the declared form matches what `template_divisions()` actually used. C is normally the weak answer, but here the three forms are not an accident to be tidied away; the board form exists because a per-unit stage wants to hand the drafter a whole page, and the Setext form exists because a single-artifact stage wants to hand it a shape. The cost of C is that the parse function stays three branches long forever, and a reader of any one template still cannot tell which branch will claim it. Declaring the form is what buys that back, and it is one line per file.

## Log
260726 · Created in the QB restructure. Nothing on this board had ever described `template.md`, though five faces referenced one in passing under `## Files`. Reading `create-page.py` to write this face is what surfaced the parse story, the five stale `Fill` lines, and the duplicated `section_rule`.

260726 · The venue half added on JL's ask. `5-section-edit` resolves its template per (venue, section_kind) out of the pinned venue pack and falls back to the generic one, so the ruling on this face governs 253 template files rather than 8.

260727 · Remeasured against `create-page.py` and the 103 files on disk, and six of this face's numbers were wrong. `template_divisions()` has THREE branches, not one: a board form matched first (`## Content` plus `## Items to Finish`, one template, `4-display`, which carries zero Setext underlines), the Setext scan, and an ATX pass merged into it, and the code comment naming the ATX cases is the only place that order is written. So the claim that a template with no Setext section aborts page creation was false, and the error string is "no logical stage divisions found in template", not "no Setext". The stale `Fill` count is 3, not 5: `1a-resource` and `2a-venue` were repaired and now match their `artifact:` exactly, and the three that remain name their own `artifact_fallback:`, which is a real file. The venue template count is 95, not 245 (245 is every md under `venue/`), so the ruling governs 103 files, not 253. The stage templates total 754 lines, not 730. Two verified facts were missing rather than wrong: `create-page.py:361` refuses any template with no Q-consumer division, which all 103 satisfy, and `board_template_items()` copies a board-form template's whole queue onto the new page, so a template supplies four things and this face described two. The `section_rule` defect got sharper on measurement: `4-display/stage.md:106` declares `-----` for a template that has none. Question, Diagram, Content, Where we are and Files corrected; the ruling item rewritten around the three forms, and the 260726 recommendation superseded in Discussion rather than edited.
