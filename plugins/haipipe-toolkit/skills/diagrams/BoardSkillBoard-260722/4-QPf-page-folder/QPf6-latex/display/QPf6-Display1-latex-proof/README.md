# QPf6-Display1-latex-proof

- claim: the `latex/` plugin really compiles this page, and page 1 of the PDF it produces is legible and carries the page's own three Content divisions; a projection that is asserted to work and never shown is the exact failure this unit exists to prevent
- kind: proof, PNG (the renderer is `pdftoppm`; the recipe is a two-line shell script and the artifact is the page's own compiled PDF)
- caption-job: let a reader see that the LaTeX export is real, at the size a reader would read it, without leaving the board page
- serves: QPf6-latex.md section 3
- fragility: bound entirely to `latex/QPf6-latex.pdf`. A rebuild of that projection changes what this unit shows, and `intake/manifest.yaml` carries its sha256 so the drift is computable rather than guessed
- renderer: `recipe/render.sh` = `pdftoppm -png -r 150 ../../latex/QPf6-latex.pdf assets/page` then copy the PDF to `preview.pdf`
- picked: 260815 CC, one candidate; re-rendered 260818 against the current PDF, because the 260816 assets were built from a PDF two revisions old
- accepted: ⬜ · the Log at `QPf6-latex.md:157` records JL accepting it on 260815 ("please just do them for me"), but this README did not exist then, so the tick had nowhere to live. It needs a fresh look at the re-rendered page.
- history: born 260815 as the latex plugin's own proof. It sat as three loose files with no README and no manifest until 260818, when `cli/check.py`'s two errors against it were traced: a folder is not a display, and a folder without a claim is not even a proposal.
