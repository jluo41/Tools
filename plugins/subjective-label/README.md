subjective-label
================

A multi-agent panel for subjective text annotation.

**One researcher + an AI panel = the output of a 3-5 person annotator team, validated against public-dataset human consensus.**

---

## What this solves

Subjective labeling — the kind where "high/medium/low humanity" or "performative vs sincere" is the target — normally needs a panel of human annotators plus a moderator plus weeks of calibration. That cost collapses research projects.

This plugin replaces the annotator team with a cooperating set of AI agents. The researcher keeps the PI role (define the topic, adjudicate boundary cases, sign off). The agents do the labeling, the calibration, and the disagreement analysis.

Convergence is proved against public datasets (GoEmotions, MFTC, POPQuorn, DICES) with known human-κ ceilings. When agent-panel κ matches the dataset's human κ, we can deploy the guideline to the researcher's private corpus at scale.

---

## Skills (5 entry points)

| Command              | What it does                                                                |
|----------------------|-----------------------------------------------------------------------------|
| `/subjective-label`  | Router — lists sub-commands                                                 |
| `/sl-init`           | Create project, define topic + boundaries via Moderator + Prober dialogue   |
| `/sl-iterate`        | One iteration: Prober picks batch → Panel labels → Analyzer → researcher    |
| `/sl-validate`       | Benchmark against a public dataset, compute κ, issue verdict                |
| `/sl-scale`          | Batch-label full corpus using converged gallery (single / panel / cascade) |
| `/sl-status`         | Show state, κ trajectory, gallery stats, next step                          |

---

## Agents (9 workers)

Researcher talks only to the **Moderator**. Everything else is orchestrated:

| Agent                       | Role                                                              |
|-----------------------------|-------------------------------------------------------------------|
| `moderator`                 | State machine + researcher-facing window. Escalates only when needed. |
| `sampler`                   | Stage-aware item selection (init_map / iterate_batch / validate_heldout / scale_preflight / diagnostic). |
| `embedder`                  | Sentence embeddings + FAISS. Serves Tier 0 of cascade; used by Sampler, Gallery Keeper, Validator. |
| `classifier`                | Small trained model (logreg / SetFit) on gallery. Serves Tier 1; drives hard-example mining. |
| `prober`                    | LLM-judgment layer on Sampler's candidate pool. Picks final 20-30. |
| `labeler-panel`             | Spawns 3-5 personas from `personas/` to label in parallel.        |
| `disagreement-analyzer`     | Classifies disagreement as A/B/C/D; surfaces only what matters.   |
| `gallery-keeper`            | Sole writer of `gallery.json` + `guideline.md`; versions every change. |
| `validator`                 | Runs public dataset benchmark; compares to human κ ceiling.       |

---

## Personas (the panel's "roster")

Loaded at runtime by `labeler-panel`. Mix-and-match per topic:

- `close-reader` — slow, evidence-based
- `plain-reader` — ordinary-reader intuition (baseline)
- `skeptic` — adversarial, finds counter-readings
- `fast-patterns` — shallow, high-throughput (cascade fast-path)
- `domain-expert` — parameterized by topic (medical / legal / consumer / ...)

Add your own persona by dropping a new file in `personas/`.

---

## Plugin layout

```
subjective-label/
├── .claude-plugin/plugin.json
├── skills/              # 5 user-facing skills (+ router)
├── agents/              # 9 subagents (top-level per Claude Code spec)
├── personas/            # 5 persona templates for the panel
├── lib/                 # Python utilities invoked by agents
│   ├── embed.py         # sentence embeddings + FAISS (used by embedder)
│   ├── classify.py      # logreg / SetFit small classifier (used by classifier)
│   └── requirements.txt
├── ref/
│   ├── ref-architecture.md   ← read this first
│   ├── ref-stages.md         ← big / medium / small loops
│   ├── ref-cascade.md        ← 3-tier cascade (Tier 0 / 1 / 2)
│   ├── ref-embeddings.md     ← model choices + config
│   ├── ref-datasets.md       ← public validation datasets
│   ├── ref-assets.md         ← file schemas
│   └── ref-schema.md         ← label schema design principles
├── workflow.excalidraw / .png
└── README.md
```

---

## The three loops

This plugin operates at three nested scales — see `ref/ref-stages.md` for detail.

**BIG loop (project lifecycle)**
```
/sl-init  →  /sl-iterate × N  →  /sl-validate  →  /sl-scale
                  ▲                    │
                  └── STALLED / refine ┘
```

**MEDIUM loop (one iteration)**
```
Sampler → Prober → Panel → Analyzer → Moderator (talk to researcher)
     → Gallery Keeper → Classifier.train (ready for next iter)
```

**SMALL loop (cascade inside /sl-scale)**
```
Tier 0: Embedder k-NN         ~$0.00001/item    ~60-80% of items
Tier 1: Trained classifier    ~$0.0001/item     ~10-30% of remaining
Tier 2: LLM panel             ~$0.05-0.20/item  ~5-15% hardest
```

Per iteration, the researcher sees at most 5-10 items to decide on. A convergent project runs 3-6 iterations — roughly 20-60 researcher decisions, versus hand-labeling thousands.

---

## Design references

- Plank (2022) "Disagreement is not noise" — disagreement as signal
- Hashemi et al. (2025) "LLM-Rubric" — rubric calibration for LLM judges
- Kiritchenko & Mohammad (2017) — pairwise comparison for subjective intensity
- Ratner et al. (Snorkel) — weak supervision + labeling functions
- Wang et al. (2023) — self-consistency for LLM reasoning

See `ref/ref-architecture.md` for the full protocol.

---

## Setup

```bash
# One-time: install Python deps for embedder + classifier
pip install -r lib/requirements.txt
```

Default config (in project's `config.yaml`) uses free local models (`sentence-transformers/all-MiniLM-L6-v2` + `logreg`). Upgrade to OpenAI embeddings or SetFit classifier by changing the `embedding:` / `classifier:` sections.

---

## Status

Version 0.3.0 — adds Sampler + Embedder + Classifier for stage-aware sampling, active-learning hard mining, and 3-tier scale cascade.

Previous: v0.2.0 — multi-agent panel architecture. v0.1.x — two-phase (superseded).
