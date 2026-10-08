# haipipe-design-goal · version history

- 261007 · review fixes (version unchanged): run-setup-goal only confirms the pin; run-setup-inputs is goal.md's one writer and waits for inputs/method.md; design-goal.md carries `rules: r<k>` and `signed:`; a goal is signed with aim, who, venue and n filled (only leave-out may stay `?`); a step may name its own from; the fence check is run-open-designs' first pass; a fix that needs a new input is a new inputs version and a new Job; sha256 stored as 12 hex; triggers sharpened (add a design goal, inputs manifest); no Brief line as a current source.

0.4.0 current · 261007 · Onto the design ladder (JL 261007, b12 s11 · s12 · s21) (version unchanged; the Design family version is frozen)
- Owns what a design reads on the ladder: the Block's goal list (`board.md ## Goals`, one yaml entry per goal,
  signed by a person), the shared rules (`design-goal.md`), frozen inputs versions (`inputs/iN/` + manifest.yaml)
  and a Job's `inputs/` fence (goal.md, relative links chosen by the method's `sees:`, manifest.yaml with sha256).
- Runs: run-add-goal-<goal>, run-setup-rules, run-add-inputs-i<N>, run-setup-goal-j<NN>, run-setup-inputs-j<NN>.
- New `ref/inputs.md`, `scripts/make_inputs.py` (freeze · job), `tests/test_goal_make_inputs.py`.
- The older board's design-goal.md contract (Aim · Venue · Rules · Resources · Leave out) moved word for word to
  `ref/legacy/design-goal-older.md`; the old page keeps reading it. The Brief's goal list merges in here.

0.4.0 · 261002 · Elements under Resources (JL 261002) (version unchanged; the Design family version is frozen)
- `Elements:` names the starting text's parts in reading order (greeting, sender, news,
  ask, link, opt-out), each quoted as it stands; the Design Space reads every design slot
  by slot against them.

0.4.0 current · 261001 · First version (JL 261001)
- `Starting text:` under Resources: the starting message word for word, which each
  card's Design elements are read against.
- Owns the board's `design-goal.md`: five blocks (Aim · Venue · Rules · Resources ·
  Leave out), `key: value <- source` lines, `?` for a gap, `Task · <folder>` overrides.
- One run type per Design Goal view, run by haipipe-designer-agent; the person signs
  the aim and the rules. Starts at the Design family version 0.4.0.
