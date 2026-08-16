# QD4-Display1-stop-gate

- claim: calibration stops only when quality, stability, coverage and risk all hold at once — the rule is a conjunction, so a strong overall score cannot buy a failed class, an unmeasured region, or an unowned high-severity risk
- kind: equation, TeX-native (✒️ tex; `amsmath align*`, the recipe IS the float body)
- caption-job: state in one object what QD4 §1–§3 spend three sections saying in prose, so a reader can see that the gates are ANDed rather than traded off, and so a later page cannot quietly turn the rule into a weighted score
- fragility: none data-bound; every threshold appears as a symbol (`q_min`, `K`, `ε`, `n_min`) because QD4 §2.1 fixes them as project configuration chosen before the sequence is read — a number typed in here would invent a threshold the page refuses to fix
- renderer: CC as the TeX hand; rebuild = `xelatex preview.tex` from this folder
- picked: 260816 CC · second candidate; the first gave every conjunct its own alignment column and the top line ran off the page, so it was rebuilt with one alignment point
- accepted: ⬜ · awaiting JL's read of preview.pdf, the row no machine may tick
- history: first equation unit on this board, built beside QA0-Display1 so one algorithm and one equation could be judged together before more are authored
