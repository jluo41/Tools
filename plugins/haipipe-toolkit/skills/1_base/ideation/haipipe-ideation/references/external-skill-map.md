# External Ideation Skill Map

Two treatments, the same rule as `writing/` and `discovery/`. An original we
**call** is vendored: an adapted copy in a numbered stage folder with its LICENSE,
a CHANGELOG stamping the upstream commit, and `metadata.haipipe.vendored_from` in
its frontmatter. A source we only **read** stays in `references/` and is digested
below. HAI Ideation retains the artifact, evidence, Run, Venue, Paper, and
human-decision authority in every case.

## Vendored originals · what we may call

| Stage folder | Original | Upstream | Commit | Licence | Second pass for |
|---|---|---|---|---|---|
| `../../1_generate/framing-research-questions/` | framing-research-questions | science-superpowers | `3150a27` | MIT | `haipipe-ideation-generate`, question sharpening |
| `../../1_generate/idea-creator/` | idea-creator | ARIS (wanshuiyin/Auto-claude-code-research-in-sleep) | `0472e53` | MIT | `haipipe-ideation-generate`, alternate lens |
| `../../2_test/novelty-check/` | novelty-check | ARIS | `0472e53` | MIT | `haipipe-novelty-check` |
| `../../2_test/kill-argument/` | kill-argument | ARIS | `0472e53` | MIT | `haipipe-idea-pressure-test` |
| `../../2_test/paper-reviewer/` | paper-reviewer | nature-paper-skills | `44cff42` | MIT | `haipipe-nature-paper-review` |

The ARIS copies were taken from the pinned tip `0472e53` (2026-09-07), not from
the submodule checkout, which sits at an older commit; their `../shared-references/`
links stay upstream paths, readable at `references/aris/skills/shared-references/`.

## Read-only sources · what was adapted into ours

Reviewed on 2026-09-07/08 from the local reference checkouts. Commits are the
checkouts at the time of this table; licences decide what may be copied.
The two Creative Commons sources are read and adapted, never vendored, so the
installed skills stay under one licence family.

| Reference family / skill | Commit | Licence | Useful capability | HAI adaptation | What was not copied |
|---|---|---|---|---|---|
| econfin-workflow-toolkit `econfin-idea-finder` | `e1406b8` | CC BY-SA 4.0 | funnel from broad candidate generation to per-candidate verification | diverse generation lenses, independent per-Idea tests, stable retained cards | fixed Windows output path, delete-below-score behavior, score ≥9 gate, finance-only assumptions |
| econfin-workflow-toolkit `novelty-check` | `e1406b8` | CC BY-SA 4.0 | Core Claim extraction, multiple query formulations, recent-work sweep, closest-paper full read, adversarial rejection/defense | `haipipe-novelty-check` query ladder, four-part delta tuple, evidence-depth gate, steelmanned comparison | scalar 0–10 score, environment-specific verifier, contradictory score caps, direct writes outside HAI owners |
| ARIS `idea-creator` / `idea-discovery` | `0472e53` | MIT | multi-step candidate generation, critique, and iterative refinement | numbered Generate/Test/Select orchestration and explicit return loops; `idea-creator` itself is now vendored above, `idea-discovery` (the orchestrator) stays read | ARIS checkpoint/output tree and independent selection authority |
| science-superpowers prior-work and feasibility lenses | `3150a27` | MIT | distinguish grounding, confounds, effect plausibility, and feasibility | separate novelty, identification, feasibility, failure-value, and minimum-experiment axes | its independent human workflow and any unsupported domain assumptions |
| academic-research-skills reviewer/EIC pipeline | `c22c17e` | CC BY-NC-SA 4.0 | EIC journal-fit lens, checkpoint discipline, adversarial multi-role review | desk-rejection challenge, current-contract gate, machine recommendation followed by a human receipt | research mega-pipeline, duplicate paper state, multi-agent output folders |
| Nature-Paper-Skills | `44cff42` | MIT | journal-first, claim-driven, figure-led storytelling and pre-submission discipline | `haipipe-nature-paper-review` significance, conceptual advance, evidence decisiveness, one-main-claim-per-figure, availability, and specialist reroute lenses | Nature-only workflow and remembered/static submission rules |
| auto-empirical-research-skills research-ideation and hypothesis-generation procedures | `e1406b8` | CC BY-SA 4.0 | gap, mechanism, measurement, boundary, intervention, and hypothesis generation patterns | Generate lens table and minimum scientific object | whole upstream orchestrators, arbitrary fixed candidate counts, discipline-specific output trees |
| auto-research-skills catalog/site | `4eb34b3` | see references/sources.yaml | catalog of possible research automations | provenance/context only | no executable procedure was present at the inspected checkout, so none is represented as implemented behavior |

## Authority boundary

- External query or generation recipes may propose work; Discovery admits and
  verifies external Subjects.
- External feasibility advice may propose a minimum experiment; Task/Run owns
  any computation and receipt.
- Journal packs and Nature guidance may suggest a target or editorial lens;
  only a current `haipipe-paper-venue` contract establishes a desk rule.
- External scoring or ranking never selects an Idea. The I3 human receipt is
  the sole selection authority.
- External output folders, agent traces, and citation stores are not copied
  into the Ideation unit.
