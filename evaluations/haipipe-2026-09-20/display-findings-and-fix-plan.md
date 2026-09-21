# Display skill evaluation and completed fixes

**Date:** 2026-09-20  
**Scope:** The ten current Display entry skills, shared display-unit contracts, Page Evidence / Delivery documentation, the Page checker, Board export, and the shared LaTeX and Word converters. Retired material under display/_todo and third-party vendored internals were not treated as current skill behavior.

## Outcome

The audit found real contract and export gaps between Page prose, selected typed DISPLAY Results, and the generated LaTeX/Word files. Those paths are now wired to the current Result ledger and selected payload units. I also corrected remaining stale workflow labels, sample feature counts, and old project references.

No confirmed documentation or static integration mismatch remains in the reviewed scope. Page LaTeX and Word Delivery were not executed after these changes, so runtime behavior there remains unverified.

## Findings and fixes

| Finding | Status | Fix |
|---|---|---|
| D01 · Page, Display, and Paper used conflicting unit paths | Fixed | Current Results resolve to results/<run>/result.yaml and payload/<unit>/. The Outline display reference and Word/LaTeX Delivery instructions now match that structure. Historical folders remain read-only migration paths. |
| D02 · TeX-native source and PDF fallback had conflicting compile bases | Fixed | The shared contract now states the TeX renderer's two wrapper compiles and its relative-input exception. |
| D03 · Concept renderers could reject verified numeric values | Fixed | Numeric labels are allowed only from a declared, verified values source; renderers do not calculate or invent values. |
| D04 · Table N and figure examples could silently mislead or fail | Fixed | Missing or conflicting N is a HOLD; the table reads verified N fields. Figure examples define their constants, resolve inputs from the unit, and use the contract asset names. |
| D05 · Candidate work could overwrite the active winner before caller selection | Fixed | Direct caller-directed renders and comparison candidates have separate paths. Candidate previews are distinct from the active preview; caller promotion and human acceptance remain separate decisions. |
| D06 · Figure-to-SVG bridge path and command signature were unclear | Fixed | The documented arguments and output location match the bundled scripts. |
| D07 · Internal steps were labeled as Workflows without stating Run scope | Fixed | Table, figure, and illustration now call their numbered sequences procedures and state that one unit is one Run. Figure-to-SVG already states its whole-source-to-master Run boundary. |
| D08 · Figure quick reference implied this skill handled architecture diagrams | Fixed | The quick-reference row routes architecture diagrams to haipipe-display-diagram. |
| D09 · HTML/PPT examples had stale counts, output assumptions, and notes wording | Fixed | Scaffold output is caller-relative, render dimensions are configurable, notes are disclosed as present in shared HTML, count copy is aligned, old counts in sample slides were corrected, and an unavailable project path was removed. |
| D10 · HTML-to-SVG pointed to a reference deck that is not shipped | Fixed | The skill points to its bundled drawing library and examples. |
| D11 · Figure-to-SVG could overstate reconstruction fidelity | Fixed | The skill identifies the result as an approximation and explains when to preserve source raster/vector artwork. |
| D12 · Converters could appear to create accepted Page evidence | Fixed | Converter output remains standalone; the Page/View/Paper caller owns placement, promotion, and acceptance. |
| D13 · Review receipts could conflate inspection, selection, and acceptance | Fixed | The table receipt distinguishes rendered/inspected, caller selection, and authorized human acceptance. Candidate review instructions identify the preview belonging to the candidate. |

### Additional Page Delivery defects found during implementation

- Page prose documented D_ display tokens, but the Board export path did not resolve those tokens from selected Result labels into the unit's manuscript label. The exporter now rewrites a temporary source copy and inserts the selected float in both delivery paths.
- The Word converter previously missed backslash display tokens and some LaTeX reference commands. It now recognizes figure, table, and algorithm tokens plus ref, autoref, Cref, and cref forms. Literal code spans are protected from reference substitution.
- Word export now stages only the selected Result units, so an older same-label folder cannot take precedence.
- A selected payload.unit could resolve into a different Result's payload. Resolution is now confined to the selected manifest's own payload tree.
- The checker could silently omit an invalid current Result pointer, including a blank binding, and could mistake a stale folder with the same basename for the unit embedded in the projection. It now reports invalid and missing bindings, checks the actual resolved asset path, and warns when prose uses a D_ token absent from selected Result labels.
- Board Delivery now blocks a cited D_ token absent from selected Result labels, as well as invalid or unready current Results, instead of exporting a pending marker or using stale evidence. Direct shared-writer use still preserves pending markers for drafts.
- Direct use of the shared writers keeps unresolved display tokens readable as pending text; Board Delivery enforces current Result selection and cited D_ label bindings.

Main code paths: page/haipipe-page/src/evidence_selection.py, page/haipipe-page/src/page_evidence.py, board/haipipe-board/live/export.py, page/page-plugins/_shared-export/md2tex.py, and page/page-plugins/_shared-export/md2docx.py. The matching guidance is in page-workflows/haipipe-page-check/SKILL.md and page-plugins/haipipe-plugin-delivery/ref/{latex,word}.md.

## Review and limits

Static review covered the updated procedures, contracts, selected-Result resolution, token handling, projection embedding checks, and HTML/PPT examples. A separate earlier fresh-context table walkthrough rendered a synthetic table with N=120 and N=118 and inspected its preview; that does not validate the new Page Delivery integration.

No tests, scripts, or conversions were run for this repair. In particular, Page LaTeX/Word export, TeX compilation, image bridge availability, and browser/PowerPoint rendering still need runtime validation if requested.
