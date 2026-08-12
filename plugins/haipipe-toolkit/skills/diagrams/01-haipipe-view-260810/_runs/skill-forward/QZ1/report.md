# View creation · QZ1

date: 2026-08-10
skill: haipipe-view (not registered in the marketplace listing; run directly via its SKILL.md and `scripts/view.py`)

## Assignment

Create a realistic View for Board Page `QZ1-for-view` from two answered Probes and one bibliography source, write a readable View body with evidence Cards, render one table Display with PNG and PDF inspection surfaces, bind it to the existing consumer Page `QS-consumers/S-Main-4-results.md`, validate, package, and stop before human acceptance.

## Created identities

- View: `QZ1-for-view` (view-id `QZ1-for-view`, page id `QZ1`)
- Display: `QZ1-Display1` (folder `QZ1-Display1-agreeableness-summary-table`, kind table)
- Consumer: `C1` → `QS-consumers/S-Main-4-results.md`, placement "Results / construct interpretation", status `planned`
- Value/evidence Cards in `view.md`: `V1` (construct description), `V2` (observable signal), `V3` (bound source-Probe count)

## Files

```text
views/QZ1-for-view/
├── view.md
├── manifest.json
├── input/
│   ├── probes/1-canonical-definition.md      (state: answered, copied from QBt1-for-view's bank)
│   ├── probes/2-observable-signal.md          (state: answered, copied from QBt1-for-view's bank)
│   └── sources/references.bib                 (john1999bigfive)
└── output/QZ1-Display1-agreeableness-summary-table/
    ├── artifact.svg
    ├── preview.png
    ├── preview.pdf
    └── output.md

packages/QZ1-for-view/
├── view.md
├── manifest.json
└── outputs/QZ1-Display1-agreeableness-summary-table/
    ├── artifact.svg
    ├── preview.png
    ├── preview.pdf
    └── output.md
```

Both Probes and the bibliography file are copied verbatim (byte-identical) from `QBt-page-types/views/QBt1-for-view/input/`; no value in `view.md` or the Display was invented beyond what they and the reference state.

PNG/PDF previews were produced with the skill's local SVG fallback (`rsvg-convert -f png|pdf`), run directly inside the Display folder, since the artifact is authored as SVG.

## Validation commands

```bash
python3 scripts/view.py check   _runs/skill-forward/QZ1/views/QZ1-for-view
# valid ... 2 probes · 1 displays · 1 consumers · acceptance waiting

python3 scripts/view.py status  _runs/skill-forward/QZ1/views/QZ1-for-view
# View QZ1-for-view · Displays QZ1-Display1:rendered/waiting · Consumers C1:planned · Acceptance waiting

python3 scripts/view.py build   _runs/skill-forward/QZ1/views/QZ1-for-view --target _runs/skill-forward/QZ1/packages/QZ1-for-view
# built ... 6 files · private inputs excluded

python3 scripts/view.py build   _runs/skill-forward/QZ1/views/QZ1-for-view --target _runs/skill-forward/QZ1/packages/QZ1-for-view --check
# current ... 6 files
```

## Gate state

- View `QZ1-for-view`: `acceptance: waiting` — not yet accepted by a person.
- Display `QZ1-Display1`: `status: rendered`, `acceptance: waiting`.
- Consumer `C1`: `status: planned`, blocked on both View and Display acceptance (per `S-Main-4-results.md`'s own Stage Contract).
- Package is current and contains no `input/` or `source/` (private material excluded).

Stopped here, before human acceptance, as the skill's step 7 requires.
