# Page reader and Draft prompt implementation

Date: 2026-09-20. Source repository: Tools-SPACE. No live site was rebuilt or restarted; the Board folder/site URL is still required.

## Reader and Draft Space

- The Board Page reader retains Copy prompt for headings, sentences, and selected passages. Inline editing, comment controls, and chat entry icons are removed. Old prose-write endpoints return 405, including requests from stale tabs.
- Draft Space offers **Structure prompt**, **Section prompt**, and **Paragraph prompt** in Table and Reading views. The prompt contains the Page source, selected Outline, Evidence ledger, exact scope, and matching Run/Version/Step where one exists.
- Copying creates no Run and changes no source. Multiple open matching Runs remain ambiguous. Missing Structure closure blocks dependent writing. Legacy paragraph addresses require reconciliation with the frozen target; invalid/duplicate addresses are blockers.
- Clipboard denial exposes a selectable, read-only prompt field. Keyboard copy preserves paragraph folding. Existing explicit Scratch behavior is retained.

## Audit follow-through

| Finding | Result |
|---|---|
| F01 Workflow units | Controller operations are separate from Run Specs in the live Workflow map and canonical table. Current workflow/folder.yaml identity is preserved separately from historical phase receipts. Existing corrected ontology and glossary work was preserved. |
| F02 Studio prompt | Active injected prompt and its reference now distinguish candidate feedback, published-source maintenance, and a new goal. |
| F03 Release rules | One shared profile/decision table; exact interactive acceptances and an explicit release request are reused. Legacy Shape gates remain scoped to their profile. |
| F04 Roster | Removed active Adopt/feedback-composer/Run Scripts claims; current evidence comes from selected Results, with legacy lanes identified. |
| F05 Render provenance | Documented separate current Design Result and division-delivery profiles, manifests, ownership, readiness, and acceptance. Preserved existing hash-checked Design reader. |
| F06 Page structure | Reader face is Opening + Content; planning remains in workspaces. |
| F07 Space/Check mapping | Current Run ownership and all four workspace checks replace the old phase-only matrix. |
| F08 Evidence/export | Evidence Cards, inline labels, and exports select the ledger-bound Result. Missing/current conflicting bindings block export. Word stages only selected displays; CITE export uses verified `payload.bibliography`. Export provenance records selection mode and manifest hashes. |
| F09 Ready | `status: ready` maps to Ready; damaged/unknown records remain Held. |
| F10 Human gates | Neutral review guidance includes every required owner gate, exact version, evidence, status, next action, and settled/required counts. Existing owner-ruling logic was preserved and exercised. |
| F11 Run history label | Already corrected to Runs in existing work; preserved. |
| F12 Plugin ordering | Folder guidance follows the current plugin/workspace arrangement. |
| F13 Completion packet | Uses the current Run or named blocker rather than requiring a Content phase label. |
| F14 Check owner | Uses the current Folder owner checker rather than retired Application authority. |
| F15 Sentence rail | Read-only address and copy behavior verified in the rebuilt fixture. |

## Validation

- **53 Board tests passed:** sentence addressing/edit-history compatibility, all six retired write endpoints, plugin surfaces, exact evidence selection, both export entry points, Word display staging, and owner-gate ledger.
- **25 Page tests passed:** scoped prompts, ambiguity/address blockers, Ready status, Scratch behavior, and Evidence label rendering.
- **13 affected skill packages passed `quick_validate.py`.** Changed Python modules parse successfully. The focused diff whitespace check passed.
- Fresh-context skill walkthrough: same-target feedback resumes the saved Run; completed Steps are preserved; exact accepted versions plus explicit release do not require a duplicate approval. Rechecked contradictions were resolved, including the final roster, Render source path, Workflow map, and duplicate bibliography-key checks.
- **Chrome Draft fixture:** actual clipboard readback, Structure/Section/Paragraph copy, keyboard activation without folding, Reading view, denied-clipboard manual fallback; zero copy write requests, no source changes, no JavaScript errors. Mobile-width layout inspected.
- **Board rebuild + Chrome reader fixture:** generated static Page builds; prompt copy works; no edit/chat/comment rail buttons; double-click opens no editor; zero write requests from these interactions and no JavaScript errors. The static fixture has no activity service; its unrelated page-load activity ping is excluded from interaction assertions.

Tests ran separately for Page and Board to avoid their shared Python module namespace collision. Browser fixtures used temporary folders and a temporary local HTTP server. No user content or live service was changed by these checks.

## Deployment and limits

- Source changes are ready. Rebuild the user's actual Board and restart its serving process once its location is known; refresh the browser to receive the new assets.
- Current CITE Results need a `payload.bibliography` binding to their frozen BibTeX source. An older Result lacking it gets a named blocker; the exporter will not silently use an unrelated legacy Bib.
- Export selection and invocation paths were tested; a complete production LaTeX/PDF or Word/PDF build was not run against a user Page.
- Existing unrelated modifications and dirty submodules were preserved. Three existing Python invalid-escape deprecation warnings in the shared Word writer remain.
