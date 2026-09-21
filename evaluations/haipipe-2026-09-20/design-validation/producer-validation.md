# Fresh-context Design Unit producer validation

Selected skill: `/Users/jluo41/Desktop/Tools-SPACE/plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md` (`haipipe-design-unit`, 0.4.0). Read mandatory `references/unit-contract.md`, the compose row in `references/modes.md`, both exact frozen configs, both approval records, and the repository fresh-context validation requirement. Both Tickets have producer identity `design-validation-producer`; both are explicitly authorized brief-only compose units with no source inputs.

## SMS — completed self-check

Result: `/tmp/design-skill-validation-20260920/sms/Design-01-library-pickup-sms/results/rd02_generate_item01/result.yaml`

Content: `Review your pickup time for your reserved book. Reply STOP to opt-out`

Verdict: pass. Coverage: 4/4 artifact × criterion pairs. Measured 69 Unicode code points against 160; exact required phrase and opt-out suffix present. Reading the complete text found no invented dates, fees, deadlines, or availability claims. No effectiveness claims or independent-review claims.

Commands run from `/Users/jluo41/Desktop/Tools-SPACE`:

```sh
python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/check_unit.py --ticket /tmp/design-skill-validation-20260920/sms/Design-01-library-pickup-sms/runs/rd02_generate_item01.yaml
PYTHONDONTWRITEBYTECODE=1 python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/check_unit.py --ticket /tmp/design-skill-validation-20260920/sms/Design-01-library-pickup-sms/runs/rd02_generate_item01.yaml --result /tmp/design-skill-validation-20260920/sms/Design-01-library-pickup-sms/results/rd02_generate_item01/result.yaml
```

Both exited 0: `PASS: Ticket inputs`; `PASS: Result integrity and check coverage`.

## Screen — first render observation

Working Result directory: `/tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01`

Content: `content/screen.html`. One self-contained HTML file, native `select`, one `button`, and explicit bindings for sample book and location values. A Python HTMLParser audit asserted no scripts, inline event handlers, or external `src`/`href`; one select and one button; bindings `{BOOK_TITLE}`, `{PICKUP_LOCATION}`, `{PICKUP_LOCATION_PRIMARY}`, `{PICKUP_LOCATION_ALTERNATE}`.

Commands:

```sh
python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/check_unit.py --ticket /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/runs/rd02_generate_item01.yaml
PYTHONDONTWRITEBYTECODE=1 python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/render_screen.py --result-dir /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01 --html /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/content/screen.html --png /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/screen-v1.png --manifest /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/manifest.json --json /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/measurements-v1.json --item ITEM01 --candidate rd02_generate_item01 --version 1
sips -g pixelWidth -g pixelHeight /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/screen-v1.png
```

Ticket checker exited 0. The first renderer attempt aborted with Chrome SIGABRT in the sandbox and wrote no picture. The same renderer command was allowed by automatic approval review outside the sandbox and exited 0.

Observed v1: screenshot 780 × 1688 at scale 2; requested viewport label 390 × 844, but measured width 500 and height 757. Viewed the actual PNG with `view_image`: card, selector and button are clipped at the right edge. The renderer reported `fits_one_screen: true` despite this mismatch. r02 therefore fails on this render. Other reported values: last block bottom 623; one button, zero links, one control, zero scripts; select and button each 52 pixels high; weakest text contrast 8.38:1; control border 7.58:1; button label contrast 11.04:1.

The parent repaired actual viewport handling using an explicit Playwright browser context. Per parent instruction, v1 evidence was preserved unchanged while the Result remained open for v2. No ticket, config, approval, runtime, repository source, Board, or service has been edited by this producer.


## Screen — corrected v2 and completed self-check

Result: `/tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/result.yaml`

Verdict: pass. Coverage: 4/4 artifact × criterion pairs. `render/manifest.json` pins both pictures and the unchanged source HTML. The v1 image remains unchanged (SHA-256 `5af5a9f115c167a242006f9049628821776fc7f05569eeba36f7a37035194d30`); final visual checks explicitly use v2.

Commands after parent renderer repair:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/render_screen.py --result-dir /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01 --html /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/content/screen.html --png /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/screen-v2.png --manifest /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/manifest.json --json /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/measurements-v2.json --item ITEM01 --candidate rd02_generate_item01 --version 2
sips -g pixelWidth -g pixelHeight /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/render/screen-v2.png
PYTHONDONTWRITEBYTECODE=1 python3 plugins/haipipe-toolkit/skills/design/haipipe-design-unit/scripts/check_unit.py --ticket /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/runs/rd02_generate_item01.yaml --result /tmp/design-skill-validation-20260920/screen/Design-01-library-pickup-ui-card/results/rd02_generate_item01/result.yaml
```

The renderer ran with permitted sandbox escalation; all commands exited 0. Checker: `PASS: Result integrity and check coverage`.

Viewed `render/screen-v2.png` using `view_image`. The full heading, card, native selector, button, and sample-data note are visible without clipping or overlap. Actual viewport is 390 × 844; page dimensions are 390 × 844; device pixel ratio is 2; PNG is 780 × 1688. Last content block ends at 623 pixels. Select and button each measure 52 pixels high. There is one button, zero links, one control, zero scripts. Weakest text contrast is 8.38:1, weakest control border 7.58:1, and button label 11.04:1. All commissioned criteria pass using the corrected render.

No remaining content or check-coverage gaps. These are producer self-checks only; runtime closure and independent verification remain caller responsibilities. The single HTML artifact is a static commissioned preview, with no deployment or behavioral effectiveness claim. Iteration use: one content draft and two successful renders producing v1/v2 evidence (three renderer invocations including the initial sandbox abort); no source-content revision was required.
