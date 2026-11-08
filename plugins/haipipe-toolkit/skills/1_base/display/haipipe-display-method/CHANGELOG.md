# haipipe-display-method · changelog

## 0.2.0 · 2026-11-06

- One figure per large step on simulated data (JL 261106): the section, its five steps, and where the study-specific simulation code lives.

## 0.1.2 · 2026-11-06

- After a second fresh-agent test: real script paths; `units.rule` prints the matching rule under the bars; a row's `later` is drawn past the clock's end, not inside the follow-up; one unit per comparison (rule 7); Run ids stay in method.md (rule 8); the review step names the revise-loop file; "example rows are made up" only for workflow; the result text wraps at 22.

## 0.1.1 · 2026-11-06

- After a fresh-agent test: the script writes `float.tex` and a full `method.md` (Message, Data, Sample, Method, Outcomes, Made by, Numbers), so `build_preview.py <dir>` works on the same folder; panel B grows with its labels; a row's `later` text; the spec section documents counts, `result`, shades and anchors.

## 0.1.0 · 2026-11-06

- New skill (JL 261106: "add a skill like /haipipe-display-method, to illustrate how these methods work"; "I want things like this, more like the real workflow").
- `scripts/method_display.py`: three kinds from a YAML spec: timeline (the main one, the study on one clock), workflow (steps with the file's columns), design (difference in differences, models, what each piece removes); writes figure.pdf, figure.png, method.md.
- `examples/`: one made-up clinic-closure study for each kind.
