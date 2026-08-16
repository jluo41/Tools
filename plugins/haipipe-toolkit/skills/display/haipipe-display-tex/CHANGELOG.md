# haipipe-display-tex · Changelog

## 0.1.0 · 2026-08-16
- Born when JL asked whether tikz should join `-diagram` or get its own skill, and ruled its own (260816). Named after the MECHANISM, `tex`, not after one package: the same 260816 ruling makes a TikZ figure, an `algorithm2e` block, and a display equation ONE kind, because they share a writer (a person), a recipe (a hand-authored `.tex`), and a binding (`float.tex` `\input`s it).
- Kept OUT of `haipipe-display-diagram` deliberately: that skill compiles a JSON FigureSpec through 1095 lines of SVG machinery, and this kind has no script at all. FigureSpec also cannot express what TeX-native is FOR — QPf5's two units used named tikz styles, a dashed fallback arc, and TeX macros, none of which the spec has vocabulary for.
- The craft comes from those two units, authored by hand the day before: the two-compile law (`assets/figure.pdf` must exist for consumers who cannot carry your preamble), `preview.tex`'s package list as the dependency declaration, and the clipped-preview rule (Display2 needed paperwidth 200 → 235mm).
