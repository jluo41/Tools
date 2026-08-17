# Application Skill Handoff — 2026-07-17

A skill-dev session aligned the `application` skill family to `paper` and the shared `probe` layer (`probe/haipipe-probe/SKILL.md`). Everything below is **committed but NOT run end-to-end**. The next step is to drive a REAL intervention through the lifecycle and see whether the model actually holds — this doc is the map for that.

## Where things stand

- Branch: **`application-paper-align`** (off `main`, **not pushed**). 5 application commits (`5ad7ed6` → `c4235dd`); concurrent `paper:` commits are interleaved on the same branch but touch only `paper/`.
- 23 skills; all frontmatter parses; `checks.sh` (`bash -n`) + `check-probe-cards.sh` (`sh -n`) lint clean.
- Reference doc for judging the family: **`EVALUATION.md`** (top-down umbrella → phase → stage rubric). It was run once this session and caught 4 real bugs (now fixed) — run it again after any change.

## What changed this session (by area)

| Area | Change |
|---|---|
| **umbrella** | dropped the `discover`/`task` proxy verbs — the bank has its own door (`/haipipe-task qa`, `/haipipe-discovery qa`), never proxied. Family-wide insight-KB retirement. |
| **1-lifecycle** | **Q-consumer migration**: every stage doc's tail section `Probes` (PP roster) → `Q-consumer` (`## Q` question blocks); the stage RAISES questions, APPROVE organizes them into `1-probes/`. Template fixes D1–D4 (esp. the silent claims PP02 defect). |
| **2-phase** | CHECK worker F1: fragile `../../1-probe/...` checker path → layout-agnostic glob + not-found FAIL. |
| **3-deliver** | renamed from `3-build-deploy` to match `paper/3-deliver`; kept FLAT (compose → audit → ship), no LaTeX sub-phasing (option B). New `3-deliver/README.md`. |
| **venue / audience** | `_venue/` → `venue/`; `_audience/` deleted — tone folds into the venue pack's tone-by-audience. |
| **4-iterate** | removed the insight write-back section. |

## Verified vs NOT verified

**Verified (static only):** routing resolves, no dead routes, no proxy verbs; EVIDENCE is the only bank door; both human gates present; F1 glob in place; zero stale `Probes`/`_venue`/`_audience`/`3-build-*`/insight-route tokens; every SKILL's section list matches its template; Q-consumer migration left no downstream breakage in probe-worker / enter / dashboard.

**NOT verified (needs a real run):**
- No intervention has actually been driven seed → deploy. The whole model is untested against a live folder.
- The Q-consumer contract's key claim — that a `## Q` question gets **organized into `1-probes/PPNN` at APPROVE** with a pointer + state — has never fired.
- `claims` option A (in-doc PP plans moved OUT to `1-probes/`) — never exercised; the probe worker may or may not find what it needs.
- `seed`'s Q-consumer semantics (feasibility *questions*, with takeaways woven into Opportunity/Mechanism) — a judgment call this session; may not match real flow.
- The **audience content gap**: skills now point at "the venue pack's tone-by-audience", but the venue packs don't carry that content yet (the deleted `_audience/` profiles were the only home). First real artifact that needs tone rules will hit this.

## How to continue: run a REAL intervention (the validation path)

Start CHEAP, then go DEEP.

**Pass 1 — an `sms` intervention (light settlement; skips narrative/display/section-edit).** Exercises the core loop with the fewest moving parts:

```
/haipipe-application enter examples/<project>/applications/interventions/NN_<slug>   # get-or-create scaffolds the folder
/haipipe-application seed
/haipipe-application ladder            # 1a-descriptions → 1b-themes → 1c-claims → 1d-advice
/haipipe-application venue "<topic>"   # pin sms (light)
/haipipe-application pitch
/haipipe-application draft             # compose 0-artifacts/<slug>-v1.md
/haipipe-application review · claim-audit · deploy
```

**Pass 2 — a `dashboard` or `report` intervention (full settlement; ALL stages fire).** Exercises the venue-gated stages (narrative/display/section-edit), the deeper claims settlement, and the Evidence Campaign.

## Open risks to watch DURING the real run

1. **APPROVE → 1-probes/.** After each DRAFT, confirm the `## Q` blocks in the stage doc's Q-consumer section actually become sections in `1-probes/PPNN_<topic>/` (state `planned`, a real `q-executor:`). If they don't, the Q-consumer migration is name-only and the door is broken.
2. **EVIDENCE reads what it needs (claims-A).** With the full PP plan now in `1-probes/` and only lean `## Q` in the stage doc, check `haipipe-application-evidence` still has mode/route/Refutes-if to work with.
3. **CHECK's F1 glob resolves.** Confirm the check worker finds `check-probe-cards.sh` via the glob and FAILs loudly if absent (not a silent skip).
4. **Audience tone hole.** When `draft`/`revise` reach for tone-by-audience, see whether the venue pack actually supplies it or the rule dead-ends. If it dead-ends, the audience tone rules need to be authored into the venue packs (the deferred content move).
5. **seed feasibility flow.** Watch whether seed's Q-consumer (questions) + takeaway-into-content actually produces a usable go/no-go, or leaves the feasibility answer homeless.

## Deferred / out of scope

- **audience content**: fold the old patient/clinician/regulator/executive tone rules INTO the venue packs' style-profiles (only the directory was deleted; the content move is TODO).
- **paper F2**: `paper-check` still asserts "DRAFT runs fully automatic", contradicting both DRAFT workers + `probe/haipipe-probe/SKILL.md` — a paper-side wording bug (application-check is correct).
- **push**: the branch is local only.
