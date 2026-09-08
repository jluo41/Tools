# External Ideation Skill Map

This map records which ideas were adapted from the local reference checkouts
reviewed on 2026-09-07/08. External Skills are design references or bounded
workers; HAI Ideation retains the artifact, evidence, Run, Venue, Paper, and
human-decision authority described by the local family.

| Reference family / skill | Useful capability | HAI adaptation | What was not copied |
|---|---|---|---|
| econfin-workflow-toolkit `econfin-idea-finder` | funnel from broad candidate generation to per-candidate verification | diverse generation lenses, independent per-Idea tests, stable retained cards | fixed Windows output path, delete-below-score behavior, score ≥9 gate, finance-only assumptions |
| econfin-workflow-toolkit `novelty-check` | Core Claim extraction, multiple query formulations, recent-work sweep, closest-paper full read, adversarial rejection/defense | `haipipe-novelty-check` query ladder, four-part delta tuple, evidence-depth gate, steelmanned comparison | scalar 0–10 score, environment-specific verifier, contradictory score caps, direct writes outside HAI owners |
| ARIS `idea-creator` / `idea-discovery` | multi-step candidate generation, critique, and iterative refinement | numbered Generate/Test/Select orchestration and explicit return loops | ARIS checkpoint/output tree and independent selection authority |
| science-superpowers prior-work and feasibility lenses | distinguish grounding, confounds, effect plausibility, and feasibility | separate novelty, identification, feasibility, failure-value, and minimum-experiment axes | its independent human workflow and any unsupported domain assumptions |
| academic-research-skills reviewer/EIC pipeline | EIC journal-fit lens, checkpoint discipline, adversarial multi-role review | desk-rejection challenge, current-contract gate, machine recommendation followed by a human receipt | research mega-pipeline, duplicate paper state, multi-agent output folders |
| Nature-Paper-Skills | journal-first, claim-driven, figure-led storytelling and pre-submission discipline | `haipipe-nature-paper-review` significance, conceptual advance, evidence decisiveness, one-main-claim-per-figure, availability, and specialist reroute lenses | Nature-only workflow and remembered/static submission rules |
| auto-empirical-research-skills research-ideation and hypothesis-generation procedures | gap, mechanism, measurement, boundary, intervention, and hypothesis generation patterns | Generate lens table and minimum scientific object | whole upstream orchestrators, arbitrary fixed candidate counts, discipline-specific output trees |
| auto-research-skills catalog/site | catalog of possible research automations | provenance/context only | no executable procedure was present at the inspected checkout, so none is represented as implemented behavior |

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
