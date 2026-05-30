haipipe-toolkit — Architecture (the whole world)
==================================================

This is the TOP-LEVEL vision: how the whole system fits together, from
raw data to real-world deliverables. Read this FIRST. The 4-layer
mechanics (C / D / E / G) live in MENTAL_MODEL.md; this doc is the
world they sit inside.

Two naming notes carried from MENTAL_MODEL.md:
  - "D_probe" is the concept; `D_probe` / `probes/` /
    `/haipipe-probe` remain compatibility names. New folder name
    for this layer is `probes/`.
  - "KB" (Knowledge Base) = probes/ + tasks/ + insights/ together —
    the project's single source of truth about facts.


TL;DR — one line, one heartbeat
================================

    Source → Task → Probe → Insight ═══ Narrative → Application → (回流)
      🌱      ✋      🔧       🧠     ⇅      📖           🥢            ↺

Seven layers in one line. But only ONE link is a double arrow — the
heart — and everything else is its intake or its output:

        🧠 KB  ⇄[🔥 ignite]⇄  📖 Narrative

    facts tell you the story  /  story tells you which probe to run

KB without Narrative = a pile of dead cards nobody sells.
Narrative without KB  = an empty story with no evidence under it.
The two together — and only together — are one complete "research".


The heart: KB ⇄ Narrative (the only double arrow)
==================================================

Everything is a pipeline (one-way) EXCEPT this. This is the engine.

```
        ┌──────────────────────────────────────────────┐
        │   ⇅  double arrow = the loop = ignite lives here │
        ▼                                                │
   🧠 KB (facts)  ⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄⇄  📖 Narrative (story)
   probes/ tasks/                              story / claims /
   insights (D/I/K/W)                          ignite-log
        │                                                │
        └→ KB→N (induction): "I got K03, it ignited a    │
                              story angle I didn't plan"  │  facts drive story
        └← N→KB (deduction): "my story is missing K05,   ←┘
                              go crack one probe to fill"     story drives facts
```

- **KB → Narrative** (induction / up): a probe returns an unexpected
  claim that *ignites* a story you hadn't planned. Data tells you the story.
- **Narrative → KB** (deduction / down): the story hits a spot where the
  evidence isn't hard enough, so you *crack a whip* — fire a probe to fill it.
  Story tells you which probe to run.

Either direction ALONE breaks:
  - KB→N only (run everything, then invent a story) = work for work's
    sake; a heap of results nobody can sell.
  - N→KB only (fix the story first, then go find data) = dangerous;
    degenerates into "hunting for evidence to fit a conclusion".

Double arrow = walking on two legs, alternating. **ignite** is the
metronome on this arrow: every round-trip asks once "am I ignited?" —
ignited → take another step; not ignited → change direction.


All the layers (the full table)
================================

```
#   Layer          Role / metaphor      N/V        Unit                  Produces                  Arrows to neighbours                     Folder
─── ────────────── ──────────────────── ────────── ───────────────────── ───────────────────────── ──────────────────────────────────────── ──────────────────────────
0   Source         🌱 raw evidence       noun (feed) one dataset / one     raw / record / case /     down ↓ feeds KB;                          1_data (source/record/
                                                     individual            aidata                    UP ↑ receives intervention回流           case/aidata)
1   Task (C)       ✋ hands/feet          verb (do)   one run.sh + results/ D + I material (obs.)     probe whips → spawns it;                  tasks/
                                                                                                     it → feeds insight
2   Probe (D)      🔧 engine             noun+verb   one probe.yaml(1 whip) K + W material (claims)   references many tasks;                    probes/ (was probes/)
                                                                                                     claim → feeds insight
3   Insight (E)    🧠 memory             noun(settle) one D/I/K/W card      permanent KB cards +      reads task+probe only; writes cards only  insights/ (D/I/K/W)
                                                                           cross-refs
─   = KB           facts as a whole      noun        probes+tasks+insights single source of truth    ⇄ NARRATIVE (double arrow, the engine)    (layers 1+2+3)
4   Narrative      📖 story / the line   noun (alive) one story line        angle + claims list +     ⇄ KB (double arrow); → feeds application  narratives/ (new)
                                                                           ignite-log
─   ③ Ignite       🔥 gate              judgment    once per round-trip   "am I ignited?" decision  lives ON the KB⇄Narrative arrow           narratives/*/ignite-log.md
5   Application    🥢 whip-hand / cash-out verb     one session=1 product deliverable               reads KB+Narrative; ask-kind writes KB     applications/
5a  ├ ask          writes-KB whip主力    verb        one research session  report.md + writes insight ONLY kind that writes back to KB         applications/ask/
5b  ├ paper/report communication (read)  verb        one manuscript/report venue snapshot           reads KB+Narrative; read-only on world    applications/paper/ report/
5c  └ message/ui   intervention (on人)   verb        one message / one UI  deployed to real people   product reaction ↑ 回流 Source ★flywheel  applications/message/ ui/
6   (G) Session    🎛️ dispatcher         mechanism   SESSION_STATE+plan+gate orchestrates all above   all applications share one skeleton       G_application/
```


Two ways to read that line (resolve the ordering question)
===========================================================

There are TWO valid "orders", on two different axes. Don't conflate them.

```
Ruler A — control flow / intent (top-down, "who drives whom")
   Narrative → Probe → Task → Insight
   start from the question, it whips out tasks, results get filed.
   → best for TEACHING / narrating.

Ruler B — dependency / build (bottom-up, "who can't live without whom")
   Source → Task → Probe → Insight → Narrative → Application
   no run → no metric to aggregate; no claim → nothing to file.
   → best for the FILESYSTEM / codebase letters (C→D→E).
```

Decision: **letters stay C→D→E (build order); diagrams/teaching use
Narrative-first (control order).** We do NOT swap C/D — Source-is-the-
foundation, and renaming would touch dozens of skill names + commands.
Insight (E) is last on BOTH rulers (it is pure downstream), so E never moves.


Application = the cash-out layer
=================================

    application = one action that cashes an insight out into a
                  real-world deliverable.

paper cashes out into **academic credit**; message into a **patient
intervention**; report into a **decision**. Different shapes, same move:
read KB → produce a deliverable.

Two axes classify every application:

```
                 COMMUNICATION (output is "words")   INTERVENTION (output "acts on a person")
              ──────────────────────────────────   ──────────────────────────────────────────
 reads KB      paper · report · slides               message · UI · treatment
 writes KB     ask (the ONLY kind that writes KB)     ——
```

- **paper is NOT special by template — it is just the (communication,
  read-only) cell.** It happens to be the most-built one.
- The genuinely different cell is **intervention** (message/ui): its
  output acts on a real person, and the person's reaction is measurable.


The flywheel (why this is not a pipeline)
==========================================

Communication apps (paper) end at the deliverable. Intervention apps
(message/ui), once deployed, GENERATE NEW DATA that flows back to Source:

```
  Source → KB → Narrative → Application(message) → deployed to patient
     ▲                                                      │
     └──────────── patient reaction = new Source data ◀─────┘
                   ("does this message work?" is itself new evidence)
```

So "let's see if the message works" is NOT the end of an application —
it is the START of the next turn of Source data. message design →
deploy → collect reaction → new insight → better message. **paper has no
return path (it only communicates); message has one (it intervenes).**
That return path is what makes the whole thing a flywheel, not a line.


Multiplicity (one project, many of everything)
===============================================

```
examples/Proj-X/
│
├── 🌱 source/          raw evidence (= 1_data). individual OR population.
│
├── 🧠 KB — one shared copy, neutral, the single source of truth
│   ├── probes/         01_film_vs_baseline/probe.yaml ...
│   ├── tasks/          A01/... (atomic, reusable by ANY probe/narrative)
│   └── insights/       D_data/ I_information/ K_knowledge/ W_wisdom/
│
├── 📖 narratives/     many story lines; each picks a SUBSET of the KB
│   ├── INDEX.md
│   ├── 01_fairness_angle/
│   │   ├── story.md          the angle + why it sells
│   │   ├── claims.md         this story needs [K01, K03, K05]  (by reference!)
│   │   ├── decision-tree.md  section paths A/B/C/D
│   │   └── ignite-log.md     ③ the ignite judgments
│   └── 02_robustness_angle/   same project, different angle, reuses same K cards
│
└── 🥢 applications/   the cash-out layer; each run = one deliverable
    ├── ask/            advances a narrative (writes narratives/ + insights/)  ★whip主力
    ├── paper/
    │   ├── 01_icml26_fairness/   meta: narrative=01_fairness, venue=ICML2026
    │   └── 02_jmlr_fairness/     meta: narrative=01_fairness, venue=JMLR  ← same narrative, 2nd paper
    ├── report/
    ├── message/        intervention → reaction 回流 source/  ★flywheel
    └── ui/
```

Three iron rules:

1. **KB is ONE shared copy, flat.** Two narratives both use K03 → do NOT
   copy K03; each `claims.md` just references `[K03]`. Evidence is a
   project asset, not any paper's private property. (Same principle as
   "tasks never nest inside probes": hierarchy is expressed by
   REFERENCE, never by directory nesting.)

2. **narrative : paper = 1 : N.** One story line can spawn an ICML paper,
   a JMLR paper, a workshop paper. Each paper points home via a single
   `narrative: <id>` line in its meta. Narrative is the living story;
   paper is its frozen render for one venue.

3. **ignite-log lives with the narrative, NOT the paper.** "Am I ignited?"
   is a story-level judgment. A paper is born AFTER ignition ("the two
   lines cross at a node, THEN you start writing"). So `papers/` holds
   only frozen manuscripts; the living judgment all lives in `narratives/`.


Noun vs verb (the knot that's easy to trip on)
===============================================

```
narrative   = NOUN = the "story" itself (angle, why, claims needed, ignite)
application = VERB = the "act of cracking the whip" (open session, fire
                     probes, collect, ship a product)
```

They are not competitors — they are noun vs verb. Narrative is the story
being advanced; application is the action that advances or renders it.
"Writing a narrative" is an `ask` application (verb); the narrative
itself (noun) lives outside, shared, in `narratives/`.


Where to go from here
======================

```
4-layer mechanics (C/D/E/G):     MENTAL_MODEL.md
D_probe ↔ C_task boundary:       skills/D_probe/MENTAL_MODEL.md
E_insight card schema:           skills/E_insight/ref/insight-md-schema.md
G_application session skeleton:  skills/G_application/haipipe-application/SKILL.md
data / source layer:             skills/1_data/haipipe-data/SKILL.md
```
