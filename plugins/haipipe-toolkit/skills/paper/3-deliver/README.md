# 3-deliver : build the folder, then finish & ship the manuscript

Everything downstream of the written argument. `1-lifecycle` decides what the paper says and `2-phase` writes it; this group turns that into a **physical folder** and then gets the draft **submission-ready**. It spans two moments — *build* (before prose) and *finish/submit* (after prose) — grouped by verb-intent, not by a flat `edit-*` prefix.

**Golden reference:** `examples/ProjA-PhyTraitLandScape/paper/Paper-MapPhyTrait-npjDM2025` (published, npj Digital Medicine 2025). The whole-folder contract lives in [`2-phase/REF/paper-folder-anatomy.md`](../2-phase/REF/paper-folder-anatomy.md).

## Shape of this group

```text
3-deliver/
├── README.md          ← you are here   (folder contract: ../2-phase/REF/paper-folder-anatomy.md)
│
├── 1-build/     ── structure the folder, zero prose
│   ├── haipipe-paper-scaffold        BUILD NEW: plan → conforming empty skeleton (tex + dirs + 1-compile.sh)
│   ├── haipipe-paper-restructure     MIGRATE: non-conforming paper → gold layout, prose byte-identical
│   ├── haipipe-paper-conform           VERIFY: conformance audit, report-only
│   └── haipipe-paper-folder          minimal container (README + STATUS + dirs); the get-or-create bootstrap
│
├── 2-audit/     ── read-only, produce findings (no mutation)
│   ├── haipipe-paper-claim-audit         every number/claim traces to raw results
│   ├── haipipe-paper-reviewer            formal reviewer-side evaluation
│   └── haipipe-paper-optimizer           claim/evidence/terminology drift review + late-stage venue preflight
│
├── 3-polish/    ── mutate the draft, whole-paper passes
│   └── haipipe-paper-polish              consistency → format → typeset, in order
│
└── 4-ship/      ── produce & move the artifact
    ├── haipipe-paper-compile             LaTeX → PDF, diagnose & fix errors
    ├── haipipe-paper-diffpdf             tracked-changes PDF (latexdiff style)
    └── haipipe-paper-to-overleaf         two-way Overleaf Git sync
```

## The build invariant (1-build only)

`1-build/` obeys one rule, the structural twin of section-edit's comment-only gate:

> **Build changes no prose.** `haipipe-paper-scaffold` creates files with no body sentences. `haipipe-paper-restructure` moves sentences but gates on prose parity (concatenated text identical before and after) and compile parity (both trees produce a PDF). `haipipe-paper-conform` writes nothing at all.

`2-audit/` also never mutates — it only reports. `3-polish/` is where the draft is changed; `4-ship/` produces and moves artifacts.

## Relationship to neighbors

| Need | Go to |
|------|-------|
| Decide story, claims, section architecture | `1-lifecycle` (then come back here) |
| No folder yet: build the skeleton | `1-build/haipipe-paper-scaffold` |
| Existing paper, wrong shape | `1-build/haipipe-paper-restructure` |
| Is this folder conforming? | `1-build/haipipe-paper-conform` |
| What should ONE `.tex` file look like inside | `2-phase/REF/tex-file-anatomy.md` |
| Write prose into the skeleton | `1-lifecycle/5-section-edit/haipipe-paper-section-edit` (DRAFT phase) |
| Improve existing prose | `1-lifecycle/5-section-edit` (REVISE phase) |
| Audit the finished draft | `2-audit/` |
| Polish the finished draft | `3-polish/` |
| Compile / diff / ship | `4-ship/` |

## Open reorg note

`haipipe-paper-folder` (minimal container) and `haipipe-paper-scaffold` (full tex skeleton) still overlap — the intended endpoint is one `scaffold` with a `--minimal` flag. The merge is deferred because `folder` is the get-or-create bootstrap the lifecycle calls, so it changes behavior, not just layout.
