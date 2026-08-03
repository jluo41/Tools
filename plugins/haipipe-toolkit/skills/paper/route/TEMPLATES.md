Stage-Template Design — hub
===========================

The single place to design the paper's stage templates. The lifecycle's control center for template SHAPE — not a wiki, not per-section fill rules. Keep it lean.

Charter — the design language every stage template obeys
--------------------------------------------------------
C1  Rules live INLINE in `ref/<stage>-template.md` as `<!-- RULE: … -->` comments — the author FOLLOWS then DELETES them (a RULE comment never ships in the filled doc). The template is the SINGLE source of both skeleton (`<placeholders>`) and rules; the SKILL never restates fill rules. DRAFT REFERS to the template and CREATES a fresh filled doc from it.
C2  UNIFORM Q-consumer across ALL stages (rename any local "Questions" / "Questions Raised"). One block per question — `## Q-<Prefix>-<n> · <title>` + `Description` / `Reason` / `Answer` — the SAME fields everywhere, because the PROBE stage COLLECTS every stage's Q-consumer questions and resolves them through one uniform pipeline; a shared shape is the interface. Stage-specific DISCIPLINE (e.g. resource's existence/fitness/KILLS answer + its `N<n>` keying, display's gated-on) lives in the section's `<!-- RULE -->` guidance, NOT in different fields. Every stage may ask — pitch and narrative included. Every question must be ANSWERABLE + SPECIFIC — a concrete check a task/discovery can answer with a definite result, decomposed into small differently-angled questions, never broad/ambiguous (the PROBE stage has to be able to answer it).
C3  Question ids are `Q-<Prefix>-<n>` (prefix table below) — leading `Q-`, then the stage name, then the stage's own index. The leading `Q-` puts every question in ONE namespace (grep `[Q-` finds every question citation — what the probe-collects-all model wants) AND disambiguates a question from a same-named content id (`Q-Resource-1` the question vs `Resource 1` the asset; `Q-Claim-1` vs `C1` the claim). Each stage owns its own index; a cited id is unambiguous across stages.
C4  A question is CITED INLINE in the content sentence(s) it hangs on — `[Q-<Prefix>-<n>]` (the forward link). `Reason` names every anchor it is cited from (the back link). One question may be cited from several sentences/sections — that is the multi-section link.
C5  DPRC loop = the answer's THREE STATIONS (defined in `../../probe/haipipe-probe/SKILL.md` → "The answer's three stations"). DRAFT raises `## Q-<Prefix>-<n>` + cites `[Q-<Prefix>-<n>]` inline. PROBE lands the answer in ① the probe entry's `### a-executor` AND ② the Q-consumer's a-consumer — its `Answer:` field, anchored `[source: PPnn]` (self-contained Q&A). REVISE weaves it into ③ the citing sentences AND discharges the bracket. Born from content (DRAFT drops the bracket), dies into content (REVISE discharges it).
C6  CORE QUESTION (a SKILL check, not a template field). Each stage's SKILL states the ONE question that stage answers — seed "why might this paper exist?" · resource "does what we need EXIST, and can it CARRY the claim?" · claims "what do we claim, and is it supported?" · venue "which venue, and what does it REQUIRE of the final paper?". A template review verifies the skill declares it.

Stage prefix table (C3) — CONFIRMED · Scheme A (JL 2026-07-18)
-------------------------------------------------------------
Principle: the id is `Q-` + the stage's canonical spine name (capitalized) + index — the stage name is vocabulary you already use (maps 1:1 to the owning Board S page), and the leading `Q-` marks it a question. (Alt considered: stage-first `Seed-Q1` — rejected: collides visually with same-named content ids like `Resource 1` / `C1`, and questions don't share one greppable prefix. Also 3–4 char codes Rsrc/Clm/Narr/… — rejected for legend cost + ambiguity.)
  seed          Q-Seed-<n>
  resource      Q-Resource-<n>
  claims        Q-Claim-<n>       (singular reads better in an id)
  venue         Q-Venue-<n>
  pitch         Q-Pitch-<n>
  narrative     Q-Narrative-<n>
  display       Q-Display-<n>
  section-edit  Q-Sec<unit><Slug>-<n>   (PER-UNIT: the unit IS the stage —
                                   Q-Sec0Abstract-<n>, Q-Sec6Results-<n>,
                                   Q-SecAPrompts-<n>. RULED JL 2026-07-27)
  review        Q-Review-<n>

Adoption matrix (live)
----------------------
C1 rule-comments · C2 Q-consumer named · C3 prefix id · C4 inline cite · C5 DPRC loop
  seed          C1 ✅  C2 ✅  C3 ✅  C4 ✅  C5 ✅   DONE — reference instance
  resource      C1 ✅  C2 ✅  C3 ✅  C4 ✅  C5 ✅   DONE — description-first (Resource N + topics + Serves&carries); uniform Q-consumer; KILLS in RULE
  claims        C1 ✅  C2 ✅  C3 ✅  C4 ✅  C5 ✅   DONE — Q-Claim-<n> uniform, M:N (Evidence: lists Qs; a Q settles many C); answerable rule; Evidence Campaign cut
  venue         C1 ✅  C2 ✅  C3 ✅  C4 ✅  C5 ✅   DONE — resource-shaped (Venue Decision · Relevant Files · Requirements); Q-Venue-<n>; pipe table cut; core question added
  pitch         C1 ✅  C2 ✅  C3 ✅  C4 ✅  C5 ✅   DONE — converted to sibling style; Q-Pitch-<n> added; H→RQ pipe table cut; core question
  narrative     C1 ⬜  C2 ⬜  C3 ⬜  C4 ⬜  C5 ⬜   add Q-consumer
  display       C1 ⬜  C2 ✅  C3 ⬜  C4 ⬜  C5 ⬜
  section-edit  C1 ⬜  C2 ⬜  C3 ⬜  C4 ⬜  C5 ⬜   rename Questions Raised → Q-consumer
  review        C1 ⬜  C2 ⬜  C3 ⬜  C4 ⬜  C5 ⬜   no template on disk yet — create?

Per-stage notes
---------------
seed          Landscape section is SEED-ONLY (JL 2026-07-18). Reference instance for C1–C5.
resource      Description-first: `Resource Description` (## Resource N + ### topics + ### Serves & carries), NOT a Demand/needs list (JL 2026-07-18). Feasibility gate lives in Serves & carries + the Q-consumer.
claims        M:N claims↔questions — a claim = several small TYPED questions (fit/eval/robustness/placebo…); a question may settle several claims. Answerable+specific questions only.
section-edit  per-unit, and the token carries the unit: `Q-Sec<unit><Slug>-<n>`, both halves read off
              the S page filename `S-<Family>-<unit>-<slug>.md`. RULED JL 2026-07-27; the old shared
              `Q-Section-<n>` collided across the nine units and broke the probe layer's own
              consumer-ids-never-collide invariant.

Rollout (spine order)
---------------------
Apply the charter one stage at a time, seed → review. Done: seed, resource, claims, venue, pitch. Next up: narrative.

Open
----
- review: no `review-template.md` exists yet — create one under the charter?
