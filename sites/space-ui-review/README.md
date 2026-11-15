# SPACE UI review

Open `index.html` directly in a browser. It is a self-contained local report;
no server, dependencies, network assets, publication or account is needed.
External source links open only when clicked. No production UI is changed.

This review covers shared Focus navigation, preview dialogs, the waiting tray,
section helpers, selected Design views and their governing UI instructions.
The report distinguishes confirmed source inconsistencies, conditional risks
and optional design improvements. Illustrations are synthetic comparisons,
not captured application screenshots. Every recommendation includes evidence,
impact, a bounded proposal, rationale, validation steps and limitations.

## Maintain

From the repository root:

```sh
python3 sites/space-ui-review/build.py
python3 sites/space-ui-review/check.py
```

`findings.py` owns reviewed claims and references. `template.html` owns the page,
styles and filtering. `build.py` embeds source excerpts and illustrative samples.
`source-receipt.json` records the source file hashes at generation time. If a
source changes, revisit the claim and line ranges before rebuilding the receipt.
Do not treat regeneration alone as revalidation of a finding.

Static checks use Python's standard library and `node --check`. They verify
source excerpts/hashes, anchor targets, absence of remote assets, script syntax,
the section-placeholder behavior with isolated pure helpers, and color ratios.
They do not test browser rendering, filtering interaction, keyboard traversal,
touch targets or screen-reader announcements. Browser access was unavailable
in this session. Those checks remain listed individually in the report.

The independent source review was performed by a Codex reviewer; it is not
represented as a Claude Code review. Other repository audit/session websites
are separate and remain untouched.
