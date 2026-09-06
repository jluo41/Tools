# Outline human review packet

Use this packet only when a person asks to **review**, **check**, **read**, or
**approve** a Page outline.  It turns the existing Outline records into a
decision-ready conversation; it neither rewrites the plan nor grants a human
approval on the person's behalf.

## 1 · Current Shape

- Link the latest `outline/<stem>-outline-v<G>.<S>[.<E>].md` and state its version and
  `approved:` value.
- Give its one-line `arc:` and a compact reader path: `C1 → C2 → …`; add
  decisive P/B labels when that helps the person inspect sequencing.
- On a revision, identify what changed since the prior version and why.  Do
  not recite every bullet when a division map is enough.
- For a Section, include a compact form audit: paragraph count; one reader job
  per paragraph; sentence-slot count; word target; implied words per sentence;
  transitions; and any paragraph whose job is merely defensive, cautionary, or
  meta-commentary. Compare paragraph, sentence, and citation expectations to
  the resolved venue source when one exists.

## 2 · Evidence owed

- Link `outline/<stem>-evidence-items.md` and report its item count by type
  and derived status from `outline/<stem>-evidence.md` when present. Also
  report `typed-item Bullets · explicit-none Bullets · missing decisions`; the
  last number must be zero before approval.
- Keep citation units explicit: `CITE Items · verified source entries · citation
  placements · citation-key mentions · cited sentences / total sentences`.
  Before CONTENT exists, label placements, key mentions, and realized density
  as planned or not yet measurable. Never call the number of CITE Evidence
  Items “the number of citations.”
- For every item material to the page's headline, show: `target → expected
  payload → acceptance → Supporting Runs → Local Input → Local Run`.
- Confirm that each citation/value/display-bearing Bullet owns the matching
  type at that exact address. An explicit `none` is valid only for a realization
  with no citation, empirical value, figure, or table.
- Group routine items as a count with a link.  A missing, deferred, or
  unbound item is stated plainly; no future result is described as a finding.

## 3 · What shaped the plan

- Link `feedback`, `requirement`, and `discussion` records when they exist.
- List each open feedback row that changes the plan's order, claim, evidence,
  or display.  Give `row id → Routed: C.P.B → effect on the Shape`.
- Name only requirements that constrain the proposed shape (for example, a
  fixed venue division or refused move), and only discussion threads that
  still require a human ruling.
- If a record has no material row, say so.  Reading feedback is not landing
  feedback; an open row stays open until its Landed field is bound.

## 4 · Human decision

- State whether the mechanical plan checks pass and whether an approval is
  possible now.
- Ask for the smallest concrete human ruling: approve/revise the Shape, choose
  between named alternatives, or sign/defer/drop a SURVEY `Decide` row.
- Preserve the boundary: a chat acknowledgement, “looks good,” or silence is
  not a Shape approval unless the person explicitly approves the named Shape
  version. A pure evidence revision reports the inherited `shape-base` instead
  of asking for the same Shape decision again.

## Response shape

```text
## 🧭 Current Shape
<link · approval state · arc · C/P map · Section form audit when applicable>

## 🧾 Evidence owed
<link · typed/status count · distinct citation units · material item table>

## 🗣 What shaped it
<feedback/requirement/discussion links · routed rows → plan effect>

## 🧑 Decision for you
<what the person can decide now, and any blocker>
```

Use clickable local-file links when supported.  Keep this packet short enough
to inspect in one screen; the linked records remain the complete source.
