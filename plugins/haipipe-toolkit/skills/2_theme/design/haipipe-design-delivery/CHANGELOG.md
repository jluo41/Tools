# haipipe-design-delivery · version history

- 261013 · (JL 261012, from the 10-08 demo: an executive summary as a one-page PDF, and a drive-home example) (version unchanged): new `scripts/summary.py` writes the Block's `delivery/summary.html` and `summary.pdf` (goal, the answered questions' Openings, one row per Job, who approved, one design traced, next); `tests/test_summary.py`.

- 261012 · (JL 261012, from the 10-08 Loop demo to leadership; b12 related/) (version unchanged): `release.py` carries `job_name`, `against` and `why` into designs.json;
  designs.md heads each design by its Job's folder name and adds its prediction and why. One review, one sign.

- 261007 · review fixes (version unchanged): Screens: the Job's delivery/screens/<dNN>.<ext>, the Block's delivery/screens/<jNN>-<dNN>.<ext>; a ranked Job releases only after its ranking is projected; placeholder words are refused; everything is checked before anything is written; a person signs the freeze with the release and later the close; trigger "design delivery", not bare "delivery".

0.4.0 current · 261007 · created (JL 261007; b12 s12, s21)
- Owns `run-freeze-predictions-j<NN>` and `run-release-j<NN>`, both soft and signed by a person, and the
  designs.json schema (`ref/designs-schema.md`): b12 s12 decided "one owner for the one file another system reads".
- `scripts/release.py` (+ test): a Job's kept, passed designs with frozen predictions into its `delivery/` and the
  Block's, never twice; `--freeze <YYMMDD>` freezes draft predictions first.
