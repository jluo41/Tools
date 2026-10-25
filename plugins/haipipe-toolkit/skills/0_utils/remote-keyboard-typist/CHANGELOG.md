# remote-keyboard-typist changelog

## 0.1.0 (2026-10-25)

- First version, from the lessons of a three-day Codex session that typed six
  PowerShell files into a no-paste remote editor through the Chrome Remote
  Desktop on-screen keyboard.
- Five steps: CLEAN, PREPARE (person, one checklist message), CONFIRM (six
  checks and an 8-key probe), TYPE (one line per call, checked), REPORT.
- `scripts/key_plan.py`: Markdown cleaning (`--from-markdown`, refused on code
  files), `--compare` against the repository copy, lost-indent warning, base-key
  plan with `Shift` and `Backslash` tokens plus the probe keys, stop on keyless
  characters.
- Revised after a fresh-subagent test: file-first search, clean-up counted from
  the screen, Delete from the extended keys, resume steps, non-VS Code editors.

## 0.2.0 (2026-10-25)

- Main typing path is now `scripts/crd_type.js`: a page script that presses the
  CRD on-screen keyboard buttons at 70 ms per key. Tested on a 35-line file:
  1,162 keys in 84 s, about 2 minutes in all, against 8 minutes for click
  batches. 25 ms scrambled lines.
- `crd_batches.py --js` prints the key list for it; `--iso` handles the layout
  with an extra key before `z`.
- Probe now `Aa$\({"; z/` (bottom row and Space included). Shift and Control
  latch for one key; a double click locks Shift, one more click unlocks.
- Replaces the 0.1.0 one-line-per-call typing; the probe, C3 and the
  fix steps now say which path they mean. `--js --probe` prints the probe keys;
  `PROBE_KEYS` gained z, / and Space; allowed-tools lists the browser tools.
- Fixes: a wrong line is replaced whole with keys only; one click into the
  editor to give it focus is allowed (JL).
