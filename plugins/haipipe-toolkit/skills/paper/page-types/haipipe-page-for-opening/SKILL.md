---
name: haipipe-page-for-opening
description: >-
  The VARIANT contract for the OPENING page, exactly one per paper. It establishes the paper's identity before Narrative orders the argument: research question, stakes, source-page inventory, headline establishment and limit, selected venue and audience, editor-facing promise, and a compact handoff to Narrative. Use when creating or repairing the front door of a paper, combining legacy Seed, Venue, and Pitch decisions, retargeting a paper, or deciding what Narrative may assume. Trigger: paper opening, opening page, paper identity, venue position, editor pitch, research question, narrative handoff, page-type opening, /haipipe-page-for-opening.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-17"
  summary: "One Opening owns paper identity plus venue position and hands a bounded promise to Narrative; it reads existing Pages through PageX and owns no Probe folder."
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "identity → stakes → source pages → establishment → venue position → editor promise → Narrative handoff"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-page-for-opening · establish the paper before ordering it

**LOAD `haipipe-page` FIRST.** It owns the shared Page frame and lifecycle. Load `haipipe-page-for-stage` when this Opening is also a lifecycle S page. Load `haipipe-plugin-pagex` only when linking or inspecting existing Pages.

This variant covers exactly one Opening per paper.

```text
kind      subject                                  closes when
────────────────────────────────────────────────────────────────────────
Opening   the paper's identity, position, promise  a person accepts the
                                                    Narrative handoff
```

Declare `page-type: opening`. The key is required and beats the filename under the base Page resolver.

## 🧭 Boundary

Opening answers **what paper is this, for whom, and what may Narrative assume?** It does not decide the order of the full argument and does not write manuscript sections.

```text
Opening     identity · RQ · stakes · sources · headline establishment
            selected venue · audience · editor promise · hard limit
Narrative   claim roles · order · reader journey · section map
Section     prose and local display/citation placement
```

The opening of the lifecycle is not the manuscript Introduction. It is the control page from which an Introduction can later be written.

## 🆓🎯 Two layers in one page

Keep the venue-free core visibly separate from the venue-aligned position.

```text
SURVIVES RETARGET    identity · RQ · stakes · source inventory · what is established
REWRITES ON RETARGET selected venue · audience · editor question · pitch · framing
```

Retargeting rereads the first layer and rewrites the second. Never rewrite the research identity merely to imitate a new venue.

## 📐 Fixed Content outline

Use these seven divisions in this order. Titles may add a paper-specific phrase after the fixed role.

```text
### 1 · Identity · <working title and one-sentence paper identity>
### 2 · Stakes · <problem, reader, and why now>
### 3 · Source Pages · <existing Pages the paper can actually read>
### 4 · Establishment · <headline finding, support, and hard limit>
### 5 · Venue Position · <selected desk, audience, and fit>
### 6 · Editor Promise · <why this desk should care and what is new>
### 7 · Narrative Handoff · <bounded packet Narrative may assume>
```

Division 3 is an inventory of Page references, not copied evidence. Division 4 distinguishes established, provisional, and absent. Division 7 is concise and typed:

```text
identity        <one sentence>
primary claim   <one testable sentence>
support         <PageX references>
hard limit      <one boundary the paper will not cross>
venue           <selected target and audience>
promise         <the reader/editor payoff>
open tensions   <questions Narrative must order around, not silently answer>
```

## 🔎 PageX and Probe are parallel

Opening preferentially reads work that already exists as a Page on another Board through PageX. It may inspect that Page's own probes, displays, and citations through the Page boundary, but it does not recreate them locally.

Probe remains a separate evidence route for Task and Discovery folders. This contract does not merge the two routes and does not add a `probe/` folder to Opening.

```text
existing Board Page ── PageX ──▶ Opening
Task / Discovery folder ─ Probe ─▶ its owning evidence Page
```

If an essential establishment exists in neither route, record the gap and hand it to the owning workflow. Do not invent an answer inside Opening.

## 🔁 Legacy compatibility

The target runtime file is one Opening page such as `S-Open-0-opening.md`. Until paper runtimes migrate, an agent may assemble this page from the legacy Seed, Venue, and Pitch pages plus the Claims control page.

That is a read-and-fold compatibility operation. Do not delete the legacy pages, change stage registration, or duplicate their prose without an explicit migration request.

## 📥📤 Runtime shape

```text
<OpeningPage>.md
├── outline/    derived or authored outline material under the Page contract
├── pagex/      references and snapshots for existing source Pages
└── bibex/      optional bibliography bindings used by this page
```

Opening owns no `probe/`, `proof/`, manuscript `.tex`, or display unit. Displays remain Page plugins on the Page that owns the evidence.

**Input:** paper intent, legacy opening controls when present, venue pack, and PageX source Pages.

**Output:** one accepted Narrative handoff. Narrative reads the handoff; it does not absorb the entire Opening page as its own content.

## ✅ Closing checks

- Exactly one paper identity and one primary research question are visible.
- Every claimed establishment is marked established, provisional, or absent and names its source Page.
- Venue-free and venue-aligned divisions can be separated during retargeting.
- The editor promise does not exceed the hard limit.
- Narrative can begin from Division 7 without rereading legacy Seed, Venue, or Pitch pages.
- No manuscript prose, raw evidence copy, local Probe folder, or display placement has leaked into Opening.

## 📂 Skill files

```text
haipipe-page-for-opening/
├── SKILL.md
├── CHANGELOG.md
└── agents/openai.yaml
```

This variant owns no scripts.
