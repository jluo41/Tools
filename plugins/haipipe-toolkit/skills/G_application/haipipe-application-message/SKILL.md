---
name: haipipe-application-message
description: "Message specialist of the haipipe-application family. Outer-loop session that drafts patient or clinician messages from the project's K/W knowledge base. Reads K_knowledge + W_wisdom from E_insight, can trigger /haipipe-insight ask when a load-bearing claim is missing, then writes the final message to examples/<project>/applications/messages/. NEVER writes back to insights/. Trigger: message, patient message, clinician message, sms, send to user, /haipipe-application message."
argument-hint: [--audience patient|clinician] [--project <path>] [--slug <slug>] "<intent>"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-application-message
===================================

Outer-loop session that produces an audience-tailored message from
the project's accumulated K/W. The classic use case:

```
"Write a message to patients with high CGM variability explaining
 why we recommend logging pre-meal."
   ↓
Phase 0  audience=patient, intent="explain pre-meal logging"
Phase 1  load K03 (variability → swings), K07 (logging → adherence),
                W02 ("recommend pre-meal logging for hi-var subset")
Phase 2  gap check: covered.
Phase 5  draft message (≤ 200 words, warm tone, plain language)
Phase 6  self-review against audience-requirements
Phase 7  write applications/messages/2026-05-25_patient_premeal-logging.md
Phase 8  return path + cited [K03, K07, W02]
```


Input
------

```
examples/<project>/insights/INDEX.md         (always)
examples/<project>/insights/K_knowledge/*    (filtered by tag/topic)
examples/<project>/insights/W_wisdom/*       (filtered by deriving K)
```


Output
-------

```
examples/<project>/applications/messages/<YYYY-MM-DD>_<audience>_<slug>.md
```


Audiences supported
--------------------

```
patient      end-user with diabetes / CGM
clinician    endocrinologist / nurse / care team
```

Other audiences route to other specialists (see umbrella SKILL).


Hard rules
-----------

- Tone + length governed by `ref/audience-requirements.md` (audience=patient
  ≤ 200 words; audience=clinician ≤ 400 words).
- Every claim cites a K or W in frontmatter (`cited_K`, `cited_W`).
- Patient messages: NO K-id in body (only in frontmatter).
- Clinician messages: inline K-id mandatory.
- NEVER edit insights/. If a gap surfaces, call `/haipipe-insight ask`.


Workflow
---------

```
Phase 0 — Parse args
  args: "<intent>" [--audience patient|clinician] [--slug <slug>] [--project <path>]
  If --audience missing → ASK (patient or clinician?).
  If --slug missing → derive from intent (kebab-case, ≤ 6 words).

Phase 1 — Load knowledge
  Per ../haipipe-application/ref/application-input-contract.md "Loading sequence":
    1. Read insights/INDEX.md
    2. Tag-filter K/W to topics matching intent
    3. Read shortlisted K*.md + W*.md (≤ 5 K + ≤ 3 W)

Phase 2 — Gap check
  Apply gap detection from input-contract.md.
  → if no gap: jump to Phase 5
  → if gap: Phase 3

Phase 3 — Trigger insight-session (optional)
  ASK user: "Knowledge gap: <gap statement>. Run insight-session to close
             it (may trigger experiments), OR proceed with draft + flag
             open question?"
  → option A: Skill("haipipe-application-ask", args="<gap question>")
              → on return, Phase 4
  → option B: proceed with status=draft + Open Questions section
              → Phase 5

Phase 4 — Re-load
  Re-read insights/ — pick up new K/W. If gap resolved, Phase 5;
  else loop Phase 3 (with budget) or mark draft.

Phase 5 — Draft
  Compose the message body following audience constraints (see schema below).

Phase 6 — Self-review
  Run the checklist from audience-requirements.md "Self-review checklist".

Phase 7 — Write
  Atomic write to applications/messages/<DATE>_<audience>_<slug>.md.
  Update applications/INDEX.md (auto-rebuild if exists).

Phase 8 — Return
  Specialist tail with path + cited entries.
```


Message artifact schema
------------------------

```
---
kind:         message
audience:     patient | clinician
intent:       "<one-line restatement>"
created:      YYYY-MM-DD
cited_K:      [K01, K03]
cited_W:      [W02]
triggered:    [insight_session_id, exp_id]   # if Phase 3 fired
status:       draft | reviewed | shipped | superseded
---

# <Short title — for clinician messages; OMIT for patient messages>

<Body — see length budget below>

## Open questions   (only if status=draft and gap unresolved)

- <question 1>
- <question 2>
```

Length budget:
```
audience=patient     ≤ 200 words; single section (no headings beyond title);
                     warm, plain language; second-person ("you can...").
audience=clinician   ≤ 400 words; OK to use 2-3 short sections; clinical
                     precision; inline K-id citations mandatory.
```


Definition of done
-------------------

```
[ ] applications/messages/<DATE>_<audience>_<slug>.md written
[ ] Frontmatter complete (cited_K + cited_W populated)
[ ] Body within word budget for audience
[ ] Self-review checklist passed (ref/audience-requirements.md)
[ ] No edits made to insights/
[ ] If gap unresolved: status=draft + "## Open questions" section present
```


Risk profile
-------------

WRITES new file under `applications/messages/`. May TRIGGER
`/haipipe-application ask` in Phase 3, which can chain
`/haipipe-experiment` → GPU jobs. Budget via MAX_EXPERIMENTS (default 3,
inherited from insight-session).

NEVER writes to insights/, tasks/, or experiments/ directly.


Specialist tail
----------------

```
status:    ok | blocked | failed | gap_unresolved
summary:   "Patient message drafted: '<intent>' — cites K03, K07, W02"
artifacts: [applications/messages/<DATE>_<audience>_<slug>.md,
            applications/INDEX.md (if exists),
            insights/sessions/<...> (if Phase 3 fired)]
next:      Open artifact for review; status=draft → resolve Open questions
```
