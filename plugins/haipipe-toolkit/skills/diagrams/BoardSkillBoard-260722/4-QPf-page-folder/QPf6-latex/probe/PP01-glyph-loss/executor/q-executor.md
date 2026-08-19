# q-executor
🧱 STAKE FORBIDDEN · this is the ONLY file that is dispatched.

Compare the characters in one markdown file's fenced code blocks against the
text of the pdf compiled from it.

The pair is
  source: /Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf6-latex/QPf6-latex.md
  pdf:    /Users/jluo41/Desktop/Physician-SPACE/Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/4-QPf-page-folder/QPf6-latex/latex/QPf6-latex.pdf
If that pdf is not on disk, rebuild it first by running the same export the
board runs, and say which command produced it.

Report:
① every distinct character outside the plain ascii range 0x20 to 0x7E that
   appears inside a fenced code block in the source, with its unicode code
   point, its name, and how many times it appears
② for each of those, whether it appears in the text extracted from the pdf
③ the total number of distinct characters lost, and the total number of
   occurrences lost
④ the font the compiled document actually used, read from the pdf itself

State how the pdf text was extracted, by tool and version, since a character
present in the pdf but unextractable is a different finding from one that was
dropped at compile time; keep those two apart.
If the pair cannot be built, say so rather than reporting a different page.
Aggregate output only; no row-level record, beneficiary id or physician id.
Deliverable: the per-character table and the two totals. Accepted: an exact
count with the character list | the export could not be produced.
