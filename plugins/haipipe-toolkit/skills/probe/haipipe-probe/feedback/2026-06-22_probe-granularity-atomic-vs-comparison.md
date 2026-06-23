---
status: fixed
created: 2026-06-22
context: P.0605 discretion-gradient (felt too complex during Judge)
fixed_in: "4.3.0"
---

JL: "我感觉这一个 probe 有点过于复杂,其实可以有一些小的 probe,比如专门研究 lbp 的 probe 之类的." (this one probe is too complex; we could have smaller probes, e.g. a probe dedicated to LBP.)

## The diagnosis

P.0605 felt heavy because it bundled TWO different jobs into one probe:
1. the per-cohort DERIVATION (each cohort's Agreeableness->opioid effect, across 8 outcomes, OLS + IV + C2-C4 facets), AND
2. the cross-cohort COMPARISON (the discretion gradient: strong where discretion high, attenuates where low).

That bundling is why the Judge verdict came out "partial/medium with a multi-outcome nuance" — the complexity is real, but most of it is per-cohort detail that does not belong in a comparison verdict.

## The principle (atomic vs comparison probes)

- ATOMIC probe = one claim about ONE effect/comparison that a single body of evidence settles. e.g. "Agreeableness is associated with higher opioid intensity in LBP" (one cohort; the effect + its shape). Verdict is simple.
- COMPARISON / META probe = a claim ABOUT a relationship ACROSS atomic probes' verdicts. e.g. "the effect concentrates where discretion is high and attenuates where low" (a gradient over cohorts). It should LINK to the atomic verdicts, NOT re-derive all their numbers.
- Heuristic: if a verdict needs an "across N cohorts x M outcomes x K methods" structure, it is a comparison probe sitting on TOP of atomic ones; split the atoms out and let the comparison link them.

A gradient/cross-cohort claim is INHERENTLY multi-arm, so P.0605 must stay multi-arm — but it should be LEAN: link the per-cohort atomic verdicts, judge only the comparison.

## This hierarchy already partly exists in ProjB

- P.0622 trait-behavior-matrix   = landscape meta-probe (cells filled by the probes below)
- P.0605 discretion-gradient     = cross-cohort COMPARISON probe (this one)
- P.0622-AO-LBP                  = the ATOMIC within-LBP probe (the "probe just for LBP" JL is asking for ALREADY EXISTS)

So the missing pieces are atomic per-cohort probes for osteo / headache / cancer, mirroring P.0622-AO-LBP, with P.0605 linking their verdicts instead of carrying their CSV-level detail.

## Fix (skill-owner decision)

1. Skill guidance: Plan (fn/plan.md) should ask "is this an ATOMIC claim or a COMPARISON across claims?" A comparison probe's arms should be REFERENCES to atomic-probe verdicts, not raw tables it re-judges.
2. ProjB refactor (optional, concrete): promote the osteo work to its own atomic probe "Agreeableness->opioid in osteoarthritis" (mirror P.0622-AO-LBP), and slim P.0605's osteo arm to a link to it. Same later for headache/cancer.
3. Trade-off to note: more folders, but each verdict is simple and atomic probes are reusable (the LBP atom feeds BOTH the MISQ gradient and the MedJournal within-LBP paper). Precedent: the "one probe -> N discoveries" decomposition already accepted in this project.

## Acted (JL: "现在就拆") + two more principles

JL chose to split NOW and added two principles:
1. Probe KIND purity: a probe is pure-task OR pure-discovery, never mixed. Introduced a `kind:` field (task | discovery | comparison).
2. There should be a probe that DECOMPOSES the complex clinical-condition axis. P.0605 is that decomposition probe (kind: comparison): it orders conditions by discretion and LINKS per-condition atomic probes.

Project refactor done this session:
- NEW atoms (kind: task), one clinical condition each, leaf of P.0605:
    probes/0622_agreeableness-opioid-osteo      (P.0622-AO-OST, verdict yes)
    probes/0622_agreeableness-opioid-headache   (P.0622-AO-HA,  verdict no on mme_ttl)
    probes/0622_agreeableness-opioid-cancer     (P.0622-AO-CA,  verdict no on mme_ttl)
  (LBP atom already existed: probes/0622_agreeableness-opioid-lbp = P.0622-AO-LBP)
- P.0605 slimmed to kind: comparison; arms are now `atom:` links to the four atoms (raw tables removed).

Skill fix still OPEN: fn/plan.md should ask "atomic or comparison? task or discovery?" and set `kind:`; comparison arms must be atom links (not raw tables); a pure-task probe must not carry discovery refs and vice versa; stage-strip / dashboard could surface `kind`.
