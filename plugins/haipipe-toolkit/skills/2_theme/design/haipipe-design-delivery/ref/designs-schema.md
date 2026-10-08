designs.json: the released designs
==================================

The one file another system reads (b12 s12, JL 261007). A Job writes its own `delivery/designs.json`; the Block's
`delivery/designs.json` gathers every Job's, one entry per released design, never twice. Written only by
`run-release-j<NN>` (`scripts/release.py`); never by hand.

```json
{
  "designs": [
    {
      "job": "j03",
      "design": "d04",
      "name": "<short name>",
      "words": "<the design, word for word>",
      "predicted": "<effect against the control, with its interval>",
      "released": "<YYMMDD>",
      "pins": {"goal": "G01", "method": "M04 m2", "inputs": "i2"},
      "screen": "screens/d04.png"
    }
  ]
}
```

| field | from | note |
|---|---|---|
| `job` | the Job folder's id | `jNN` |
| `design` | the design Task's id | `dNN`; with `job`, the key: never twice |
| `name` | the design face's `name:` | optional |
| `words` | the design face's `## Design`, verbatim (projected from the closed draft; never the scaffold's placeholder) | for a UI, the screen's visible text |
| `predicted` | `prediction.yaml` `predicted:` | frozen before the release |
| `released` | the day a person signed | `YYMMDD` |
| `pins` | the Job face's `goal:` · `method:` · `inputs:` | what made this design |
| `screen` | relative to the file's own `delivery/`: `screens/<dNN>.<ext>` in a Job's, `screens/<jNN>-<dNN>.<ext>` in the Block's | a UI design only |

A system that sends has its own shape; an adapter reads this file, never the Tasks. `designs.md` holds the same
designs for a reader: one `## <job> · <design>` heading each, then the words.
