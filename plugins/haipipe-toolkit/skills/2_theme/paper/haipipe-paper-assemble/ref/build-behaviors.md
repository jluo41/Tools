The three behaviors every build must have, and the expect-fail procedure that proves each one (haipipe-paper-assemble).

## 🔢 Three behaviors every build must have (260908)

Found paper-locally by Paper-Example-Misq, now in the engine with a tooth each in
`tests/test_build_delivery.py`:

```text
A  print a display ONCE          md2tex already embeds a cited display as a real float inside the
                                 fragment; the master never re-\inputs the unit's float.tex after it.
                                 Without this every figure and table printed twice (Figure 1 = Figure 2).
                                 switch: DEDUPE_EMBEDDED_FLOATS
B  a not-ready page keeps        its H1 declares number and title ("# t04_<title> · §4 Title"):
   its number                    the master emits a real numbered \section{Title} plus one italic
                                 "[This section is not yet compiled into this build.]" line; the
                                 REASONS live in build-manifest.json and the register, never in the
                                 reader's PDF/DOCX (JL: "the delivered pdf or word must be clean").
                                 An unnumbered
                                 "[NOT READY]" heading slid every later section down one number.
                                 parser: page_heading()
C  the display register          delivery/display-register.md counts what the MASTER prints, walking
                                 master.tex in \input order, and compares with the number each unit's
                                 README `## Placement` declares. Five teeth: declared ≠ printed · printed
                                 with no declared number · one label printed twice · one number claimed
                                 by 2+ units, scanned over ALL units on disk so a collision on a
                                 not-ready page is visible before that page compiles · ONE WORK under
                                 two bib keys, both cited, which apalike prints as 2018a + 2018b with
                                 two entries in the reference list (staged-but-uncited = a warning).
                                 also in build-manifest.json under "displays"
```

## 🧪 The expect-fail procedure (the Gate-1 lesson)

A check that measures what a page CONTAINS is blind to what the document
PRINTS: the first register counted fragments and reported the same findings on
the broken build as on the good one. Every tooth in this skill is therefore
proven by making it fail first: `test_behavior_A_expect_fail_register_catches_the_double_print`
switches `DEDUPE_EMBEDDED_FLOATS` off and asserts the register reports the
double print; only then does the positive test count. When you add a behavior,
add the tooth that fails without it, and record both runs. Run the suite with
`bash Tools/plugins/haipipe-toolkit/skills/2_theme/paper/haipipe-paper-assemble/tests/run.sh`
(it runs from the tests directory on purpose: the repository's `code/` package
shadows the stdlib `code` module and breaks pytest startup from the repo root).

Since 0.7.0 the engine also guarantees: a display prints once in the whole
DOCUMENT, so a page that `\ref`s a float another page embeds never re-inputs it,
whichever page comes first; a bib key that two pages define differently is a
document warning (first page's entry kept); a missing `latexmk` or Word engine is
reported as `rc 127` in the manifest, never a traceback; the master carries the
status word only, never counts or build times.
