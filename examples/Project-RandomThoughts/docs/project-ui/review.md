# Project UI preview review

Scope: proposed Project UI, not the current Project renderer or a production migration.

## Round 1 — independent review

The preview follows the requested navigation and is clearly marked **Proposed UI**. The screenshot keeps the shared white cards, blue selection and collapsed sections.

Three defects to fix:

1. **Decisions/Checklist silently change scope.** Their “Open…” links use `v.blocks[0]`, so Work opens b10 only while appearing to represent the whole Work Theme. Label these links with the source Block, or show one source link per Block.
2. **“Project UI” breadcrumb opens b10’s default view.** Add `section=report&group=ui-project` so it returns directly to the new Project UI.
3. **Plan’s documented interaction exceeds the preview.** The guide promises steps “linked to the work responsible,” but the steps are plain text. Add source Block links to the example steps or describe the current preview as an unbound proposed sequence.

Scores: Glance **8** · Place **8** · Lean **9** · Words **8** · One job **8** · Same look **9** · Salience **8** · Plain **9** · Complete **7**. Mean **8.2**. Phone **n/a**; Works **n/a**—no direct browser walk performed.

The design is suitable for discussion after these link/scope corrections; this review does not certify production behavior.

## Round 2 — fresh independent review

The three corrections are present and resolve the earlier defects:

- Project UI breadcrumb returns directly to `group=ui-project`.
- Decisions and Checklist name each source Block; Project explicitly names b10.
- Plan’s guide accurately identifies the sequence as proposed and its step bindings as unassigned.

No further blocking defects found within this preview’s scope. Project remains above Themes; the preview has Theme buttons, no Work/Report switch, and collapsed sections.

Scores: Glance **8** · Place **9** · Lean **9** · Words **9** · One job **8** · Same look **9** · Phone **9** · Salience **8** · Works **8** · Modern **8** · Plain **9** · Complete **8**. Mean **8.5**.

Phone and Works scores use the supplied 390-pixel measurement, screenshots, tab checks and console result—not an independent browser walk. Suitable for design discussion; this does not certify production migration or persisted planning behavior.

## Builder checks

- Nine targeted Project UI and existing UI tests passed.
- Project UI appears on b10 and its proposed preview loads in place.
- All eight Project/Theme buttons select their matching panel.
- Work → Plan opens the proposed sequence; the matrix Plan explanation opens and closes.
- Preview measured at 390px: document width 390px, no horizontal overflow.
- Preview console: no recorded errors.
- Corrected source Block labels and direct Project UI breadcrumb verified in browser.
- The current live Project page remains separately accessible; no walkthrough recording is claimed.
