# haipipe-plugin-display · Changelog

## 0.3.2 · 2026-08-31

- Point frozen-intake provenance at canonical `evidence/probe/`.

## 0.3.1 · 2026-08-31

Category-folder sweep: lane paths read `<page>/evidence/<lane>` or
`<page>/delivery/<lane>` (haipipe-page 0.47.0 §📁); flat names are the same
lane during migration (stubs).


## 0.3.0 — 2026-08-17

**Where a data-driven unit's numbers come from is now written down** (JL 260817
asked it directly). New §❄️: `intake/inputs/` freezes FROM a probe card's
`proof/`, verbatim, recording the CARD's own `sha256`. The unit never reaches
into the workspace a second time, because the card already crossed the wall and
a second unwitnessed pull can silently disagree with it.

- **Staleness becomes computable**: the manifest carries the card's hash, so a
  re-pull that moves the hash makes the intake stale and drops `accepted:` to ⬜.
- **A unit cannot exist before a card has ANSWERED**, since its intake freezes
  from a `proof/` that does not exist until then. That is why the display unit
  is created at EVIDENCE (`haipipe-page-workflow` §🃏) and why a plan carries a
  bare `🖼 owed` mark until the number lands.
- **The recipe types no cell** and fails loudly on a ragged read.
  `QC1-visitlbp-Display1-control-ladder`, the first unit built this whole way,
  caught Stata's `="771,449"`: the `=` outside the quote stops a CSV parser
  treating the quote as a quote, so the `N` row arrived as 11 cells, not 5.
- **A unit names the bullet it serves** in a `serves:` README row, the same
  backward link a probe card carries.
- Coherence pass (260819 law): §❄️'s creation rule is scoped to DATA kinds —
  a CONCEPT unit (diagram · tex · illustration) freezes a LISTING of the
  source files it reads and waits for no card.

## 0.1.0 · 2026-08-15
- Born in the thin-door round (JL 260815), the first FAMILY-WRITER variant: display's writer is a routing decision (five renderer kinds) plus a human gate (`accepted:`), which no roster row can hold.
- Owns the page-side delta only — unit address `<page>/display/<stem>-DisplayN-<slug>/`, kind→renderer routing, the five-step walk, and the `> Display:` evidence-card lane; the unit's internal shape stays the display family's contract, adopted verbatim per QPf5's ruling.

## 0.1.1 · 2026-08-16
- The citation's home is the SENTENCE (JL 260816, after the render showed a lane latched onto the wrong sentence): an id named in prose chips as the evidence card in place; the `> Display:` lane stays as the filing surface for machine-appended bindings and lines the id would clot.

## 0.1.2 · 2026-08-16
- The projections inherit the citation: the latex export embeds a cited unit as a float (winning asset + authored caption), the word export embeds the rasterized figure with inline (Figure n) and a 🖼 Display comment; mechanics recorded in the latex/word variant skills, this file only names the rule.

## 0.1.3 · 2026-08-16
- The display family consolidated behind its `haipipe-display` door (JL 260816): the kind→renderer table now routes table and figure through the door's `ref/table.md` and `ref/figure.md`; the retired `-table` and `-figure` skill names left the table.
