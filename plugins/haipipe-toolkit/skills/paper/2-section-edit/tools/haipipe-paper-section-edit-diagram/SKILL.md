---
name: haipipe-paper-section-edit-diagram
description: ASCII diagrams of a LaTeX paper at three zoom levels — sections (whole paper), paragraphs (one section), sentences (one paragraph). Use when reviewing structure, spotting empty/thin sections, auditing paragraph roles, or checking sentence-level rhetorical flow. Trigger words — paper structure, section overview, section map, paragraph map, paragraph roles, sentence breakdown, rhetorical flow, /haipipe-paper-section-edit-diagram.
argument-hint: "[scope] [section] [paragraph]"
metadata:
  version: "1.1.0"
  last_updated: "2026-05-31"
  summary: "ASCII diagrams of a LaTeX paper at three zoom levels — sections (whole paper), paragraphs (one section), sentences (one paragraph)."
  changelog:
    - "1.1.0 (2026-06-05): renamed from paper-structure-diagram to haipipe-paper-section-edit-diagram (haipipe-paper-* name unification)."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

# /haipipe-paper-section-edit-diagram — Section / Paragraph / Sentence Maps

**Purpose**: visualize the *structural skeleton* of a LaTeX paper at three zoom levels. Pure structure, no content rewrite. Companion to `/diagram-ascii` but specialized for papers — emoji-rich, monospace-aligned, `.txt` output.

**🎨 Emoji-first.** Every paragraph gets a role glyph; every section gets a status glyph; every sentence gets a role tag. Density is the point.

## When to Use
- Auditing whether the paper's section balance matches the venue's page budget
- Spotting empty / stub / TODO sections at a glance
- Mapping paragraph roles (hook → gap → approach → contributions → roadmap) inside a section
- Checking sentence-level rhetorical flow (topic → setup → claim → evidence → bridge) inside a paragraph
- Pairing with `/paper-revise` or `/haipipe-paper-edit-optimizer` to pick *which* paragraph or sentence to revise next

## When to Defer
- Want figures inside the paper rendered → use `/haipipe-paper-display-figure`
- Want a logical-argument diagram (claim flow across sections) → use `/diagram-ascii` ref/08-paper-section
- Want word-by-word style review → use `/haipipe-paper-section-edit-write-scientific` or `/paper-revise`

---

## Commands

```
/haipipe-paper-section-edit-diagram                              section view of paper at cwd
/haipipe-paper-section-edit-diagram sections [path]              section view (whole paper)
/haipipe-paper-section-edit-diagram paragraphs <sec> [path]      paragraph view of one section
/haipipe-paper-section-edit-diagram sentences <sec> <par> [path] sentence view of one paragraph
/haipipe-paper-section-edit-diagram all [path]                   all three for whole paper
```

`<sec>` accepts:
- index — `1`, `01`, or `§1`
- filename stem — `01_introduction`
- partial title — `intro`

`<par>` accepts: `1`, `¶1`, or `3` (ordinal among prose paragraphs in section).

`path` defaults to cwd. The skill auto-detects the paper folder by finding a root `.tex` (one of: `0-*.tex`, `main.tex`, or sole top-level `.tex`) and a sections directory (`0-sections/` or `sections/`).

---

## Inputs

Compatible with both `haipipe-paper-build-scaffold` layout and the user's `0-` prefix convention:

```
<paper-root>/
├── 0-{slug}.tex      OR   main.tex             ← root, has \input{...} per section
├── 0-sections/       OR   sections/
│   ├── 00_abstract.tex   01_introduction.tex   ...
└── .target.yaml      (optional, see below)
```

### Optional inline annotations

Inside section `.tex` files:

```latex
% role: hook              → paragraph role
% role: gap
% role: approach
% role: contributions
% role: roadmap
% role: background | tradeoff | evidence | transition

% sentence-role: topic    → sentence role (one comment per sentence above it)
% sentence-role: setup
% sentence-role: claim
% sentence-role: evidence
% sentence-role: bridge
```

If absent, the skill **infers** roles from cue words (see Heuristics below).

### Optional `.target.yaml`

```yaml
target_pages: 8
sections:
  abstract: 250
  introduction: 800
  related_work: 600
  method: 1200
  results: 1000
  discussion: 600
  conclusion: 200
```

If absent, defaults are applied based on filename stem (e.g. `01_introduction` → 800w).

---

## Outputs

Saved under `<paper-root>/notes/structure/` (created if missing):

```
notes/structure/
├── structure-sections.txt                            whole-paper section view
├── structure-{NN}-{slug}-paragraphs.txt              paragraph view per section
└── structure-{NN}-{slug}-{P}-sentences.txt           sentence view per paragraph
```

Always also printed inline in the conversation. **`.txt` only** — markdown breaks monospace.

---

## View 1 — Section View (whole paper)

```text
📄 Paper-FairGlucose-icml2026                     target: 8 pages, ~7000w
══════════════════════════════════════════════════════════════════════════════
§0  📝 Abstract           ▓▓▓▓▓░░░    150w / 250w   ✅
§1  🎯 Introduction       ▓▓▓▓▓▓▓░    720w / 800w   ⚠ light
§2  📚 Related Work       ▓▓▓░░░░░    280w / 600w   ❌ stub
§3  📦 Dataset Design     ▓▓▓▓▓▓▓▓    900w          ✅
§4  ⚙️ Benchmark Protocol ▓▓▓▓▓▓▓▓    850w          ✅
§5  📊 Baseline Results   ▓▓▓▓▓▓░░    600w / 1000w  ⚠ thin
§6  💬 Discussion         ░░░░░░░░    empty         ❌ TODO
§7  🏁 Conclusion         ▓▓▓░░░░░    120w / 200w   ⚠ short
══════════════════════════════════════════════════════════════════════════════
Σ 3,720w  (~4.2 pages of 8 target)   📊 figures: 5   📋 tables: 3
```

Status rules:
- `✅` ratio ≥ 0.85 of target
- `⚠` 0.40 – 0.85 (`light` if intro/discussion type, `thin` for results/methods, `short` for conclusion)
- `❌` < 0.40 (`stub` if has any text, `TODO` if empty / only comments)

Bar chart (`▓▓▓▓░░░░`) is 8 cells = ratio × 8, capped at 8.

Section glyphs (by filename heuristic):
```
📝 abstract     🎯 introduction    📚 related_work    📦 dataset/data
⚙️ method/protocol/algorithm    📊 results/experiments    💬 discussion
🏁 conclusion    🧪 ablation    📐 theory/proof    🔍 analysis
```

---

## View 2 — Paragraph View (one section)

```text
🎯 §1 Introduction — 5 paragraphs, 720w
══════════════════════════════════════════════════════════════════════════════
¶1  [120w]  🎯 hook            "Glucose monitoring devices have transformed..."
¶2  [180w]  ❓ gap             "Despite this progress, prior benchmarks fail..."
¶3  [200w]  💡 approach        "We propose FairGlucose, a benchmark that..."
¶4  [110w]  ✓  contributions   "Our contributions are as follows..."
¶5  [110w]  🗺️ roadmap         "The remainder of this paper is organized..."
══════════════════════════════════════════════════════════════════════════════
flow:  hook → gap → approach → contributions → roadmap   ✅ canonical intro shape
```

**Role glyphs:**
```
🎯 hook         💡 approach/insight    ✓  contributions
❓ gap/problem  📊 evidence            🗺️ roadmap
📚 background   ⚖️ tradeoff            🔄 transition
🧩 setup        🔬 experiment          •  unlabeled
```

**Flow line** at the bottom names the role sequence and flags common shapes:
- `hook → gap → approach → contributions → roadmap` ✅ canonical intro
- `background → background → background → ...` ⚠ all background, no claim
- gap-less or roadmap-less intros get `⚠ missing: gap` / `⚠ missing: roadmap`

---

## View 3 — Sentence View (one paragraph)

```text
🎯 §1 ¶3 — approach (5 sentences, 200w)
══════════════════════════════════════════════════════════════════════════════
S1  [topic]     "We propose FairGlucose, a benchmark that explicitly stratifies..."
S2  [setup]     "Unlike prior work, FairGlucose evaluates models across five..."
S3  [claim]     "This enables, for the first time, a quantitative measure of..."
S4  [evidence]  "Across 5 demographic axes, our protocol reveals systematic..."
S5  [bridge]    "The remainder of this paper details the protocol and..."
══════════════════════════════════════════════════════════════════════════════
shape:  topic → setup → claim → evidence → bridge   ✅ canonical paragraph
```

**Sentence roles:**
```
[topic]    paragraph's main proposition
[setup]    context, definitions, constraints
[claim]    the assertion the paragraph is making
[evidence] data, citation, derivation supporting the claim
[bridge]   transition into next paragraph
[caveat]   qualification or scope-limiting clause
[example]  concrete instantiation
```

Common shape diagnostics:
- `topic → claim → evidence → bridge` ✅ standard
- `topic → setup → setup → setup → claim` ⚠ buried claim
- `claim → claim → claim → claim` ⚠ unsupported claims
- no `[evidence]` flagged for results/methods sections only

---

## Implementation

### Detection

```python
from pathlib import Path
import re

def find_paper_root(start: Path) -> Path:
    p = start.resolve()
    for cand in [p, *p.parents]:
        roots = list(cand.glob("0-*.tex")) + list(cand.glob("main.tex"))
        secs  = [d for d in [cand/"0-sections", cand/"sections"] if d.is_dir()]
        if roots and secs:
            return cand
    raise SystemExit("No paper root found (need 0-*.tex or main.tex + sections/)")

def section_files(root: Path) -> list[Path]:
    secs_dir = root/"0-sections" if (root/"0-sections").is_dir() else root/"sections"
    return sorted(secs_dir.glob("[0-9]*_*.tex"))
```

### LaTeX stripping & word count

```python
def strip_latex(s: str) -> str:
    s = re.sub(r'(?m)^\s*%.*$', '', s)                       # comment lines
    s = re.sub(r'(?<!\\)%.*$', '', s, flags=re.M)            # trailing comments
    s = re.sub(r'\$\$.*?\$\$', '', s, flags=re.S)            # display math $$
    s = re.sub(r'\$[^$]*\$', '', s)                          # inline math
    s = re.sub(r'\\\[.*?\\\]', '', s, flags=re.S)            # \[ ... \]
    s = re.sub(r'\\\(.*?\\\)', '', s, flags=re.S)            # \( ... \)
    s = re.sub(r'\\begin\{(equation|align|gather)\*?\}.*?'
               r'\\end\{\1\*?\}', '', s, flags=re.S)
    s = re.sub(r'\\begin\{(figure|table)\*?\}.*?'
               r'\\end\{\1\*?\}', ' [FLOAT] ', s, flags=re.S)
    s = re.sub(r'\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?', ' ', s)
    s = re.sub(r'[{}]', ' ', s)
    return s

def word_count(s: str) -> int:
    return len(strip_latex(s).split())
```

### Paragraph parsing (within a section file)

```python
def paragraphs(text: str) -> list[dict]:
    raw_paras = re.split(r'\n\s*\n', text)
    out = []
    for raw in raw_paras:
        if not strip_latex(raw).strip():
            continue
        m = re.search(r'%\s*role:\s*(\w[\w-]*)', raw)
        role = m.group(1).lower() if m else None
        out.append({
            "raw": raw.strip(),
            "text": strip_latex(raw).strip(),
            "words": word_count(raw),
            "role": role,
        })
    return out
```

### Sentence splitting

```python
ABBREV = ['e.g.', 'i.e.', 'et al.', 'cf.', 'Fig.', 'Eq.', 'Sec.',
          'Ref.', 'vs.', 'approx.', 'Tab.', 'Ch.', 'Thm.', 'Def.']

def sentences(para_raw: str) -> list[dict]:
    s = strip_latex(para_raw)
    for a in ABBREV:
        s = s.replace(a, a.replace('.', '<DOT>'))
    parts = re.split(r'(?<=[.!?])\s+(?=["“(\[]?[A-Z])', s.strip())
    out = []
    for i, sent in enumerate(parts):
        if not sent.strip():
            continue
        sent = sent.replace('<DOT>', '.').strip()
        # role from preceding `% sentence-role:` comment in raw text
        marker = re.search(
            rf'%\s*sentence-role:\s*(\w+)\s*\n[^%\n]*?{re.escape(sent[:30])}',
            para_raw)
        role = marker.group(1).lower() if marker else None
        out.append({"text": sent, "role": role, "words": len(sent.split())})
    return out
```

### Heuristics (when annotations absent)

```python
PARA_HEURISTICS = [
    (r'^\s*(We propose|We introduce|We present|In this (paper|work),?\s*we)',
        'approach'),
    (r'^\s*(Despite|However|Although|Unfortunately|Existing|Prior work)',
        'gap'),
    (r'^\s*(Our contributions|We make the following|This paper makes)',
        'contributions'),
    (r'^\s*(The remainder|We organize|This paper is organized)',
        'roadmap'),
    (r'^\s*(Recent (work|advances)|Prior (work|approaches)|A long line of)',
        'background'),
]

SENT_HEURISTICS = [
    (r'^\s*(We propose|We introduce|We present)', 'topic'),
    (r'^\s*(This (enables|allows|provides|yields))', 'claim'),
    (r'^\s*(Across|On|We evaluate|Empirically|Table|Figure)', 'evidence'),
    (r'^\s*(Unlike|In contrast|Compared|Whereas)', 'setup'),
    (r'^\s*(The remainder|Next|We now turn|Section)', 'bridge'),
]
```

Run heuristics top-to-bottom; first match wins; default to `unlabeled` / `[—]`.

### Targets

```python
DEFAULT_TARGETS = {
    'abstract': 250, 'introduction': 800, 'related_work': 600,
    'background': 600, 'method': 1200, 'methods': 1200, 'approach': 1200,
    'protocol': 900, 'dataset': 900, 'data': 900,
    'experiments': 1000, 'results': 1000, 'evaluation': 1000,
    'analysis': 800, 'ablation': 600,
    'discussion': 600, 'conclusion': 200, 'limitations': 300,
}

def target_for(stem: str, override: dict) -> int:
    key = re.sub(r'^\d+_', '', stem).lower()
    if key in override: return override[key]
    for k, v in DEFAULT_TARGETS.items():
        if k in key: return v
    return 600  # generic fallback
```

### Rendering helpers

```python
def bar(words: int, target: int, width: int = 8) -> str:
    fill = max(0, min(width, round(width * words / max(target, 1))))
    return '▓' * fill + '░' * (width - fill)

def status(words: int, target: int, kind: str) -> str:
    if words == 0: return '❌ TODO'
    r = words / max(target, 1)
    if r >= 0.85: return '✅'
    if r >= 0.40:
        return ('⚠ thin'  if kind in ('results','method','dataset')
           else '⚠ short' if kind == 'conclusion'
           else '⚠ light')
    return '❌ stub'
```

---

## Run sequence

For any command, the skill should:

1. **Detect** paper root + section files + load `.target.yaml` if present.
2. **Read** the requested scope (one file, one paragraph, or all sections).
3. **Parse** with the helpers above. Apply heuristics for missing role tags.
4. **Render** ASCII per the View templates above. Use box-drawing chars (`═`, `─`, `│`) and pad columns so `%` and `w` align.
5. **Save** to `notes/structure/<filename>.txt`.
6. **Print** the same content inline, in a fenced ` ```text ` block.
7. **Append** a one-line "next action" hint when something is flagged:
   - `→ §6 Discussion is empty. Run /paper-revise §6 to draft.`
   - `→ §1 ¶3 has no [claim]. Run /haipipe-paper-section-edit-diagram sentences 1 3 to inspect.`

---

## Cross-references

- `haipipe-paper-build-scaffold` (`05_prewrite/`) — initial folder layout this skill reads.
- `haipipe-paper-section-edit-weaving` (`07_revise/`) — interactive section/paragraph revision; pair with this to pick *what* to revise next.
- `haipipe-paper-edit-optimizer` (`07_revise/`) — structural revision pass; this skill is its visual companion.
- Strategic architecture blueprint — now folded into `haipipe-paper-minimap` (see its `ref/architecture-blueprint.md`); use this skill for paper-shaped structure views.
- `diagram-ascii` (`Tools/plugins/diagram-skill/`) — general ASCII diagrams; this skill is the paper-specialized application.

---

## Rules

- **`.txt` only**, never `.md` — markdown breaks monospace.
- **Never modify section files.** This skill is read-only; it only writes under `notes/structure/`.
- **Annotations are optional.** Missing `% role:` and `% sentence-role:` comments → fall back to heuristics, never error.
- **Width 78** for the `═` separator; inner content fits within 76 cols.
- **Cap** bar chart at 8 cells even when ratio > 1 (over-target sections show `▓▓▓▓▓▓▓▓ 1100w / 800w  ⚠ over`).
