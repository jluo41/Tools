haipipe-board-page-for-skill · Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.4.1 - 2026-08-03

**Board bucket review, 260803** (JL: "go ahead to solve yourself, dont ask me"). Ledger: `skills/_console/260803-board-bucket-review.md`.

- Drops "the seven sections" from the line describing what the base owns; the base no longer claims a count.

## 0.4.0 - 2026-08-03

**Opens with the whole page in one picture** (JL: "could you show what is the expected outline for the skill-page?").

Ten sections and 240 lines said what every slot must contain and never once showed the page. A writer had to assemble the shape in their head from prose spread across the file, which is the same defect this contract was opened to fix one level down. The figure now marks every slot 🤖 machine-written or 🧑 person-written, so the split a reader most needs is the first thing they see.

- **Merges two `## 🎯 Aims and States` sections that had drifted apart.** 0.1.0 wrote one and 0.3.0 added a second without noticing, so the contract carried two headings on one subject: one saying what Aims hold, the other claiming the form override. Found by grepping this file's own headings while answering the outline question, which is a reminder that a contract needs its own table of contents read as often as its prose.
- `## Files` now says OMITTED in the figure rather than only in prose, since that was the one section a reader could not tell was deliberately absent.

## 0.3.0 - 2026-08-02

**Every item here came from `haipipe-board-reviewer-agent`'s first real dispatch**, which reviewed the eight pages written to 0.1.0 and reported as this contract's first independent consumer.

**The pass this contract exists for WORKED.** All eight Openings survive noun substitution: swap in a sibling and each paragraph goes false on a named, dated or measured fact. The reviewer named slot ❷, "name the sibling you would otherwise pick", as the single rule that did it, because a paragraph naming its real neighbour cannot be swapped with that neighbour.

- **🔴 The contract contradicted the shipped checker, and this contract lost.** `check.py` warned `opening-lead-not-a-question` on any lead not ending in `?`, with no page-kind exemption, so the seven pages that OBEYED this contract each carried a warning telling them to put the question back, while the one page that satisfied the checker was the one that broke this contract. A writer working the checker's list would have regressed all seven. `check.py` now exempts `Skill-` and `Agent-` pages and warns `skillpage-opening-is-a-question` in the opposite direction. The conflict is recorded here so the next contradiction is reported rather than worked around.
- **🚫 The no-question rule is now MECHANICAL.** It read "open with a rhetorical question", which is a judgment call; six writers read it as "no question" and one did not. It now reads: the lead sentence never ends in `?`. A rule a checker can enforce is a rule nobody has to interpret.
- **⚠️ ❶❷❸ is content, not a template, and this file now says so.** The reviewer's sharpest finding: the base forbids a reusable scaffold, and naming three slots is one keystroke from becoming the next form letter. The first batch already showed the pull, with 7 of 8 putting a second-person pick-me line second and 6 of 8 closing on what has not happened yet. It survived only because each slot carried a DIFFERENT checkable fact. Stated explicitly, with that measurement, as the thing to watch.
- **🎯 The Aims-form override is claimed in writing.** The base wants `A<n>` ids, a testable `Done when`, and one State row per Aim; `writing-rules.md` forbids a checkbox on a canonical Aim; all eight skill and agent pages do none of that. The reviewer correctly refused to judge the Aim-to-State map because three contracts disagreed and none claimed the override. New `## 🎯` section claims it and gives the reason: base Aim ids key to CONTENT DIVISIONS, and a skill page's Content is the unit's own bytes in a managed span, so there are no divisions of ours to key to.

## 0.2.0 - 2026-08-02

**Everything here was found by a blind door test**, an agent given one bare task, no skill name and no path, asked only how it WOULD add a skill page.

- **🔌 The registration gap, and it made this skill unusable for a day.** The agent could not invoke this skill: the folder shipped on 260802 and was never linked into `~/.claude/skills/`, so `Skill(haipipe-board-page-for-skill)` failed while the folder sat on disk. It read the file directly and warned that anyone else "will conclude the skill does not exist and fall back to the base contract, which is exactly the failure the variant was written to prevent." New `## 🔌` section: shipping is not the last step, and a running session keeps its old roster either way.
- **🏗 Two contradictory CREATE procedures, with nothing routing between them.** The base says copy `ref/page-template.md` and register the page in `board.md` yourself; `skillpage.py new` uses its own stub and writes `board.md` itself. Following the base literally produces a hand-typed page with no managed spans, which `check` then reports as `no managed block` forever. New `## 🏗` section states the generator path, and `haipipe-board-page` 0.11.1 routes the two skill and agent page kinds to it.
- **📎 `Files` is omitted on purpose, and now says so.** No skill page carries one, the base marks it "allowed, advised against", and the reason was unwritten: the derived Diagram tree already lists every file the unit ships, so a Files section would be a second and staler copy. `Writing Style` is recorded as optional, since the two newest pages carry it and the older ones do not, and "copy the sibling page's shape" was returning different answers.
- **🔢 The `<n>` collision is named.** It is the PAGE NUMBER, while the base writes the same slot as `Skill-<unit>-<slug>` and "unit" means the shipped thing everywhere else in the family. Also records that `new` takes `max + 1` and that an archived page in `_archive/` does not count, so a retired number is spent rather than free.
- Records that `--group` takes the KEY (`QC`) and not the full heading, which the tool's own error message implies the opposite of.

## 0.1.0 - 2026-08-02

- **First cut**, opened on JL's ask: "this is skill page, and it is kind of special,
  how do we deal with it? Like should we have haipipe-board-page-for-skill?"
- **The measurement that opened it.** Five skill and agent pages on `01-boardform-260722` had
  Openings in one shape: `Does <name> <verb> one <noun>?` then own, hard-part,
  depend, healthy. Read alone each was clear; read consecutively they were one letter
  with the nouns swapped. JL caught it by eye before any reviewer ran.
- **Why the base could not have prevented it, which is the reason to ship a variant
  rather than tighten a rule.** `haipipe-board-page` already carries the
  noun-substitution test, so the rule was on the books and five writers broke it
  anyway. The cause is upstream: the base's Opening shape is `the question, what its
  words mean, why that is hard, what this page decides`, and a skill page decides
  nothing. A writer obliged to ask a question about a unit that decides nothing can
  only manufacture a rhetorical one, and "Does X do X well?" has one answer that
  carries no information. The slot was the defect, not the writers.
- Replaces that slot with three ordered questions the visible paragraph answers:
  what the unit is and is for; when you reach for it rather than its named sibling;
  and where it stands, meaning the one thing to know before trusting it. The base's
  physical shape is unchanged: one visible paragraph, first blank line is the split.
- Names four things a roster Opening may never do, each traced to the measurement:
  a rhetorical question, a paraphrase of the unit's own `description:` (Content
  already carries those bytes), the four-slot scaffold, and a health claim the page
  cannot show.
- States that the consecutive read is the test and that it is NOT the author's to
  pass, because the writer knows which unit they meant and therefore cannot see the
  substitution failure.
- Carries the skill-page rules that were previously only on the design board's
  `QC3a`: the derived-versus-authored split across the three managed spans, that a
  green `check` covers frontmatter only and not prose, that `state:` is a health
  judgment a person writes while the version rides the title, and that an agent's
  empty tree span is emitted rather than omitted.
- Adds two rules the board learned by doing and had written nowhere: a skill page's
  Aims may be a defect another page ROUTED here because this unit ships the file, and
  the generator's `Page generated <date>. Nothing ruled yet.` stub is a claim that
  nobody has looked, so it may not survive on a page whose unit ships.
- Adds the retirement procedure, proven on `haipipe-board-index` the same day:
  archive the page, deregister it, alias BOTH ids to the archived path, then sweep
  live prose, since a Log line recording what was true stays and a live sentence
  claiming the unit still ships is now false.
