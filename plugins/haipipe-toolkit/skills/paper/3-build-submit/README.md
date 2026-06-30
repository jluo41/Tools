# 4-build-submit : the paper build stage

Materialize the plan into a **physical paper folder** that follows the gold-standard layout, and keep that folder structurally sound for the rest of the lifecycle. Build work changes **structure only, never prose**.

**Golden reference:** `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025` (published, npj Digital Medicine 2025). Every rule in this stage is grounded in that folder. The full contract lives in [`_shared/paper-folder-anatomy.md`](_shared/paper-folder-anatomy.md).

## Position in the lifecycle

```
1-lifecycle  (decide what the paper says)
    │   contract: NARRATIVE_REPORT.md / PAPER_PLAN.md / PAPER_ARCHITECTURE.md
    ▼
4-build-submit    (HERE: build the folder the prose will live in)
    │   output: compileable skeleton, zero prose
    ▼
3-write / 3-write-edit  (realize + refine the tex)  →  4/5-revise → 5-review → 5-respond → 6-present
```

This is the hop that the retired `haipipe-paper-create` once performed inline at its Phase 2 ("scaffold tex root"). 4-build-submit extracts it as a first-class, reusable stage with a verifiable contract, so any workflow (write, restructure, venue port) can call it and any folder can be audited against it. Prose drafting now lives in `3-write-edit/haipipe-paper-edit-write`.

## Shape of this stage

```
4-build-submit/
├── README.md                       ← you are here
├── _shared/
│   └── paper-folder-anatomy.md     the whole-folder contract (what a conforming paper folder IS)
│
├── haipipe-paper-build-scaffold/                 BUILD NEW: plan → conforming empty skeleton
│   ├── SKILL.md
│   └── templates/                  driver / wrapper / leaf / SI driver / compile script / README
│
├── haipipe-paper-build-restructure/              MIGRATE: non-conforming paper → gold layout, prose untouched
│   └── SKILL.md
│
└── haipipe-paper-build-check/          VERIFY: conformance audit, report-only
    ├── SKILL.md
    └── scripts/check_structure.sh  mechanical checks (gaps, orphans, roles, broken paths)
```

## The three skills

| Skill | You have | It produces |
|-------|----------|-------------|
| `haipipe-paper-build-scaffold` | a plan (or just title + section list), no folder yet | a new conforming folder: driver tex, wrappers, leaf stubs with paragraph banners, `0-displays/`, SI driver, `1-compile.sh` |
| `haipipe-paper-build-restructure` | an existing paper that does not conform (monolithic `main.tex`, flat `sections/`, ad-hoc names) | the same paper re-housed in the layout; prose byte-identical, compile verified |
| `haipipe-paper-build-check` | any paper folder | a ✓/✗ conformance report; routes each finding to the skill that fixes it |

## The build invariant

Everything in this stage obeys one rule, the structural twin of 3-write-edit's comment-only gate:

> **Build changes no prose.** `haipipe-paper-build-scaffold` creates files that contain no body sentences. `haipipe-paper-build-restructure` moves sentences but gates on prose parity (concatenated text identical before and after) and compile parity (both trees produce a PDF). `haipipe-paper-build-check` writes nothing at all.

## Relationship to neighbors

| Need | Go to |
|------|-------|
| Decide story, claims, section architecture | `1-lifecycle` (then come back here) |
| No folder yet: build the skeleton | **here** (`haipipe-paper-build-scaffold`) |
| Existing paper, wrong shape | **here** (`haipipe-paper-build-restructure`) |
| Is this folder conforming? | **here** (`haipipe-paper-build-check`) |
| What should ONE `.tex` file look like inside | `3-write-edit/_shared/tex-file-anatomy.md` |
| Write prose into the skeleton | `3-write-edit/haipipe-paper-edit-write` |
| Improve existing prose | `3-write-edit` |
| Compile or fix LaTeX errors | the folder's own `1-compile.sh` (shipped by `haipipe-paper-build-scaffold`); `components/compile/` for latexmk-based pipelines |
