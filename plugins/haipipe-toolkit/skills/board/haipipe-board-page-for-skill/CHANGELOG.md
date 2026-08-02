haipipe-board-page-for-skill · Changelog
========================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match
SKILL.md frontmatter `version:`. Newest first.

**v0-series rule:** inherited from `haipipe-board`; this skill stays on `0.x.x` and
never reaches `1.0.0` without JL's explicit say-so.

## 0.1.0 - 2026-08-02

- **First cut**, opened on JL's ask: "this is skill page, and it is kind of special,
  how do we deal with it? Like should we have haipipe-board-page-for-skill?"
- **The measurement that opened it.** Five roster pages on `01-boardform-260722` had
  Openings in one shape: `Does <name> <verb> one <noun>?` then own, hard-part,
  depend, healthy. Read alone each was clear; read consecutively they were one letter
  with the nouns swapped. JL caught it by eye before any reviewer ran.
- **Why the base could not have prevented it, which is the reason to ship a variant
  rather than tighten a rule.** `haipipe-board-page` already carries the
  noun-substitution test, so the rule was on the books and five writers broke it
  anyway. The cause is upstream: the base's Opening shape is `the question, what its
  words mean, why that is hard, what this page decides`, and a roster page decides
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
- Carries the roster-page rules that were previously only on the design board's
  `QC3a`: the derived-versus-authored split across the three managed spans, that a
  green `check` covers frontmatter only and not prose, that `state:` is a health
  judgment a person writes while the version rides the title, and that an agent's
  empty tree span is emitted rather than omitted.
- Adds two rules the board learned by doing and had written nowhere: a roster page's
  Aims may be a defect another page ROUTED here because this unit ships the file, and
  the generator's `Page generated <date>. Nothing ruled yet.` stub is a claim that
  nobody has looked, so it may not survive on a page whose unit ships.
- Adds the retirement procedure, proven on `haipipe-board-index` the same day:
  archive the page, deregister it, alias BOTH ids to the archived path, then sweep
  live prose, since a Log line recording what was true stays and a live sentence
  claiming the unit still ships is now false.
