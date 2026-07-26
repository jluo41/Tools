# The stage template: the shape DRAFT fills
state: 🔴 OPEN
owner: JL
method: rule whether a template is a skeleton to copy or a spec to parse, then make it one of them

## Question
What is `template.md`, and who reads it? Eight of them exist, 730 lines in total, and no page on this board has ever described one. That silence is expensive, because the file is read twice by two different things that believe two different stories about it, and only one of those stories is written down anywhere.

Its own first line says "TEMPLATE (follow, don't ship)": a skeleton whose `<…>` slots get replaced and whose `<!-- RULE: … -->` comments are guidance to follow then delete. That is the story an agent reads. But `create-page.py` does not copy the file at all. It PARSES it: every Setext `-----` heading becomes a `## Content` division on the new S page, and each division's job line is that section's RULE comment, compacted to 220 characters. Under that story the `-----` underlines are load-bearing syntax and the RULE comments are machine input.

Both stories are true today, and neither file says so. The consequences are already on disk: five of the eight templates instruct the drafter to fill a path that no longer exists, a template with no Setext section would abort page creation with an error nobody has documented, and `formatting:` declares `section_rule: "-----"` in the contract while the parser hardcodes the same rule separately. What we want is one story, stated in the file, so that changing a template has a predictable effect on both readers.

## Boundary
- ✅ Covered here
  What `template.md` is, both things that read it, and what the contract's `template:` `sections:` and `formatting:` fields mean.
- ↪ Covered elsewhere
  What the contract declares is `QB1`; how the page gets created and named is `QB4`; what a re-run does to a page already filled is `QB5`; what DRAFT does with the shape is `QB8`; what a `<!-- RULE -->` becomes once the prose is real is `QC0`.

## Diagram
```
   📄 stages/<order>-<key>/template.md   is read TWICE, by two readers
      who have been told different things about it.

   ── READER 1 · create-page.py, at PAGE-CREATION time ──────────────

      template_divisions(path)
        │
        │  finds every SETEXT heading:   Title
        │                                -----
        │  and for each, the first       <!-- RULE: … -->
        │
        ▼
      ## Content
      ### <Title>
      (job line = that RULE, whitespace-collapsed, cut at 220 chars)

      ⛔ no Setext section  ──▶  SystemExit: "no Setext stage
                                 divisions found in template"
      ⚠️ the `-----` is SYNTAX here, not formatting.

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
                   ⚠️ the parser HARDCODES  -{3,}  and never reads
                      section_rule. Two copies of one rule.

   ── what is on disk RIGHT NOW ─────────────────────────────────────
      0-seed          Fill 0-lifecycle/0-seed/0-seed.md          ⚠️ stale
      1a-resource     Fill 0-lifecycle/1-work/1a-resource.md     ⚠️ stale
      1b-claims       Fill 0-lifecycle/1-work/1b-claims.md       ⚠️ stale
      2a-venue        Fill 0-lifecycle/2-venue/2a-venue.md       ⚠️ stale
      2b-pitch        Fill 0-lifecycle/2-venue/2b-pitch.md       ⚠️ stale
      3-narrative     (no Fill line)
      4-display       (no Fill line)
      5-section-edit  (no Fill line)

      half-migrated: the FOLDERS are the new ones (1-work, 2-venue),
      the FILENAMES are the pre-S-face ones. The artifact is really
      0-lifecycle/0-seed/S-Seed-0-seed.md, which no template names.
```

## Content
### Two readers, two stories, one file
The file believes it is a skeleton. The creator treats it as a spec. Neither is wrong on its own and the combination has no owner, so a change made for one reader lands on the other unannounced: retitle a section for readability and you have renamed a Content division on every page that stage will ever create; drop a RULE comment as obvious and you have replaced a job line with the fallback string `Complete the <Title> stage output.`

The cost is not hypothetical. It is why the stale `Fill` lines survived the S-face restructure: nothing about the parse path touches that line, so nothing failed, and the only reader who suffers is the drafting agent, which is the reader with no error channel.

### What the template is FOR, once the two stories are separated
The division titles and their job lines are the artifact's SHAPE, and the shape is what a stage guarantees regardless of who runs it. The `<…>` slots and the prose guidance are DRAFTING HELP, and help can be as long as it likes. The 220-character truncation is the seam between them: it only makes sense if the RULE's first sentence is the job and the rest is help, and no template has been written knowing that.

### What is not decided
Whether `sections:` in the contract and the Setext headings in the template must agree, and which one wins if they do not. Today both exist, the parser reads only the template, and nothing compares them.

## Items to Finish
- [ ] 🧠 Rule what a template IS
      A: a spec that `create-page.py` parses, with drafting help allowed inside RULE comments and the file saying so. B: a skeleton the drafter copies, with the Content divisions declared in the contract's `sections:` instead and the parser deleted. C: both, with the dual role stated in every template's header. A is what the code does; B is what the file says.
- [ ] 📐 Rule whether `sections:` and the template's headings must agree
      Both declare the artifact's parts. Nothing compares them and nothing says which wins.
- [ ] 🔧 Repair the five stale `Fill` lines
      Five templates point the drafter at a pre-S-face filename inside a correctly renamed folder. Blocked on nothing; it is the cheapest item here.
- [ ] 📐 State the 220-character contract
      A job line is the RULE's first sentence and the rest is help, or the truncation is arbitrary. Say which.
- [ ] 🔍 Stop declaring `section_rule` twice
      The contract declares `-----` and `template_divisions()` hardcodes `-{3,}`. Either the parser reads the field or the field goes.
- [ ] 🧪 Add a template that a stranger can follow
      The acceptance test for this face: someone adds a ninth stage, writes only its template, and gets a correctly divided page without reading `create-page.py`.

## Where we are
Eight templates exist and are in daily use, and the mechanism works: pages get created with the right divisions and job lines. Nothing here is broken in a way that fails loudly, which is exactly why it has gone undescribed for so long.

Nothing is ruled. This face is 🔴 because the central question, what the file IS, has never been asked, and the three defects below it are consequences of not asking rather than separate problems.

## Files
- `stages/*/template.md`
  Eight templates, 730 lines, 43 to 140 lines each.
- `haipipe-paper-stage/create-page.py`
  `template_divisions()` and `compact_rule()`: the parse story, in about thirty lines.
- `stages/CONTRACT.md`
  Declares `template:`, `sections:` and `formatting:` as required fields, and says nothing about how they interact.

## Law
_None yet. This face is 🔴 and its first item is the ruling that would produce one._

## Discussion
> CC 260726: I would rule A. The parse path is the one with an error channel, so it is the one that will stay honest; a skeleton nobody parses drifts silently, which is precisely what the five stale `Fill` lines are. Under A the template header changes from "follow, don't ship" to something like "this file's `-----` sections BECOME the page's Content divisions; the first sentence of each RULE becomes its job line; everything after that is help for the drafter."
> The cost of A is that a template stops being freely editable prose, and that cost is real. It is also the cost we are already paying without having agreed to it.

## Log
260726 · Created in the QB restructure. Nothing on this board had ever described `template.md`, though five faces referenced one in passing under `## Files`. Reading `create-page.py` to write this face is what surfaced the parse story, the five stale `Fill` lines, and the duplicated `section_rule`.
