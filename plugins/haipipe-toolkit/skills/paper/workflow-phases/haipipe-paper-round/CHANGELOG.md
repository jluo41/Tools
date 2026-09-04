## 0.4.1 · 260831
- Runtime home is the desk's -Round group (JL 260831); combined B<x>-<desk> and lone C1-RD-round grandfathered.

## 0.4.0 — 2026-08-31

- **Renamed and moved** (JL 260831: "replace page-types to be workflow-phases"):
  `paper/page-types/haipipe-page-for-round/` is now `paper/workflow-phases/haipipe-paper-round/`.
  The skill is one paper JOURNEY PHASE and still owns its `page-type:` key;
  a new `## 🧭 Journey phase` block places the phase and its gates, and the
  description carries the P-number. Contract body unchanged.

## 0.3.0 — 2026-08-24

- **Rounds live in their desk's B group** (JL 260824, journey 0.5.0 P5-P6
  mapping): `B<x>-<desk>/RD<NN>-<event>/` beside that desk's section pages;
  the lone C1-RD-round group is grandfathered; a foreign-desk round mints its
  desk's B group even when the group holds only RD pages.

## 0.2.0 — 2026-08-23

- **A Round parents to a NAMED Narrative — or to the Seed when the telling has
  no page on this board**: the new `foreign-desk` round-kind covers a review
  arriving from a desk this paper never told (the ICIS case), with the desk
  named in intake.
- **The routing table gains the Seed** as the destination for a concern that
  demands evidence the paper does not yet hold (new analysis class, ablation,
  downstream outcome).
- **Letters live inside the Round page's folder**, never at repo root; the
  runtime group is `paperboard/C1-RD-round/RD<NN>-<desk>-<event>/`.
- Frontmatter gains version, summary, and `group-token: RD`.

## 0.1.0 — baseline

- The pre-260823 contract, written before this file carried versioned
  metadata; that history lives in git. (This CHANGELOG was created in the
  260823 family review, which found the 0.2.0 bump had no log.)
