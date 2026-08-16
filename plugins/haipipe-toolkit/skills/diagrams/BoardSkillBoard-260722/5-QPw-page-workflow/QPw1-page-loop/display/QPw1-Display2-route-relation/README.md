# QPw1-Display2-route-relation

- claim: the four-row legal-route table is two rules, and those two rules imply the page's two central laws — CLOSE is reachable from CHECK alone, and CHECK is unreachable from CHECK, so no version is judged twice without a producer between
- kind: tex, TeX-native (a display equation; the writer is a person, the recipe IS the figure)
- caption-job: turn §9.1's sentence "only CHECK may CLOSE" into a statement a reader can check against the shipped table, and surface the second law that the prose never states
- fragility: none data-bound; every set is transcribed from `src/page_lifecycle.py`, named in `intake/manifest.yaml`. If `LEGAL_ROUTES` changes, this unit is wrong and must be rebuilt, not patched
- renderer: CC as the TeX hand; rebuild = `pdflatex preview.tex`, then `recipe/asset.tex` for `assets/figure.pdf`
- picked: 260816 CC · one candidate, clean on the first compile; only the paper height was trimmed
- accepted: ⬜ · awaiting JL's read of `preview.pdf`, the row no machine may tick
- history: born 260816 beside Display1, from the observation that `R(CHECK)` omits CHECK — a law the page argues nowhere in prose
