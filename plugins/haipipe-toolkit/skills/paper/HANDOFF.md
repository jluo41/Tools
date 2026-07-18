# Paper Skill Handoff — 2026-07-17

A skill-dev session reorganized the `paper` skill family's delivery side, wrote an evaluation method, and trimmed pervasive bloat. Everything below is **committed but NOT run end-to-end** — no paper was driven through the changed skills. This doc is the map for validating and continuing.

## Where things stand

- Branch: **`application-paper-align`** (off `main`), pushed to `origin`. Three `paper:` commits this session (`2ed0ef4` reorg → `71cfbdb` trim → `a6a6089` retire/merge/collapse); concurrent `application:` commits are interleaved on the same branch but touch only `application/`.
- **44 skills** (was 48: −5 retired/collapsed, +1 merged `polish`). All skill names unique and match their folders; frontmatter parses.
- Reference doc for judging the family: **`EVALUATION.md`** (top-down umbrella → phase → stage rubric, new this session). The delivery half now has its own umbrella, mirroring the lifecycle half.

## What changed this session (by area)

| Area | Change |
|---|---|
| **venue** | `_venue/` submodule → `venue/` (`.gitmodules` + all refs). |
| **docs** | added `EVALUATION.md` (the umbrella→phase→stage review method). |
| **retired-ref purge** | removed dead `components/`, `3-write-edit`, `4-build-submit`, `2-section-edit`, `5-minimap`, `minimap`, `edit-write/weaving`, `5-respond`, `2-rounds` tokens across live docs; moved `paper-folder-anatomy.md` from `3-*/‌_shared/` to `2-phase/REF/` (beside its companion `tex-file-anatomy.md`). |
| **3-deliver** | renamed `3-build-submit` → `3-deliver`, regrouped by verb-intent: **1-build** (scaffold/restructure/conform/folder) · **2-audit** (claim-audit/reviewer/optimizer) · **3-polish** (polish) · **4-ship** (compile/diffpdf/to-overleaf). Dropped `edit-*`/`build-*` prefixes; `paper-compile`→`haipipe-paper-compile`; `build-check`→**`conform`** (avoids collision with the CHECK phase worker). |
| **new umbrella** | `haipipe-paper-deliver` — artifact-side mirror of `haipipe-paper-lifecycle`; top router delegates delivery intents to it. |
| **bloat trim (−~1000 lines)** | moved inline payloads (LaTeX/beamer templates, Python gen-scripts, Codex prompts, proof taxonomy) to `ref/`/`scripts/`; deleted duplicated "Key Rules" + prohibition-wall "Anti-patterns"; deleted the display renderers' re-inlined shared contract (kept pointers). |
| **retire/merge/collapse** | retired `improve-loop` (legacy pre-DPRC harness); merged `submission-audit` into `optimizer` (kept only its venue preflight); collapsed the 3 v0.0.1 stubs (`consistency`/`format`/`typeset`) into one `haipipe-paper-polish` running the three passes in order. |

## Verified vs NOT verified

**Verified (static only):** all 44 skill names unique & match folders; zero live refs to any retired/renamed skill; zero stale tokens (`3-build-submit`, `_venue`, `components/`, `edit-*`, etc.); every inline `ref/`/`scripts/` pointer resolves; the 9 extracted payload files hold their content byte-for-byte; router verb table, deliver umbrella, feedback inbox map, wiki structure, and external structure docs all rewired.

**NOT verified (needs a real run):**
- **The `haipipe-paper-deliver` umbrella has never routed** — `build|audit|polish|ship` dispatch is untested against a live paper.
- **`haipipe-paper-polish` has never executed** — the merged 3-pass skill (consistency→format→typeset) is new; its comment-first + ordered-pass flow is unexercised.
- **`optimizer`'s new venue-preflight section** (absorbed from submission-audit) never run.
- **Extracted `ref/`/`scripts/` files** (poster template, PPTX script, Codex prompts, proof taxonomy) — the skills now *point* at them; the pointer-then-load flow was never driven.
- **`venue` submodule is uninitialized** — the rename is correct in `.gitmodules`, but no checkout was tested.

## How to continue

1. **Drive one paper through the delivery side** — scaffold → conform → (write) → audit → polish → ship — and confirm `haipipe-paper-deliver` routes each verb and the leaves still work post-rename. Cheapest smoke test of the whole reorg.
2. **Poster non-subtractive rewrite** — `paper-poster` is still 841 lines (down from 1133 but the audit floated ~450). Further cuts (decorative ASCII, the twin review-loop rubrics) need *rewriting*, not just extraction — deferred from this pass.
3. **Point `EVALUATION.md` at scales not yet swept** — the paper waffle/duplication sweep found ~2,000 trimmable lines; `application/` shares this lineage and almost certainly the same debt.

## Deferred / out of scope

- **poster residual** — see continue #2.
- **paper F2 bug** (flagged by the concurrent application session): `haipipe-paper-check` still asserts "DRAFT runs fully automatic", contradicting both DRAFT workers + the constitution — a paper-side wording bug (`application-check` is correct). Not touched this session.
- **3-polish granularity** — collapsing the trio into one `polish` skill dropped the per-pass verbs (`polish consistency` etc.); if per-pass invocation is wanted, `polish` takes a sub-arg — not yet wired.
