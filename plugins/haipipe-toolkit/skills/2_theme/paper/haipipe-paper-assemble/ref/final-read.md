The final read: the blind-review loop a build passes before an author or coauthor reads it (haipipe-paper-assemble).

## 🔁 The final read · before an author reads a build (JL 261104)

JL 261104, of the assembled paper view: "please work until you update this ready, I will just read this." A build goes
to an author or a coauthor only after this loop comes back clean (one Page's own Word export for a coauthor is the other lane, SKILL.md § Two Word lanes):

```text
1 READ    one fresh blind reviewer: the main paper and the cover letter; another fresh one: the supplement
          they read the rendered PDFs and view every table and figure page as an image
2 VERIFY  check each finding against the source; a reviewer can be wrong
3 FIX     in the source or the generator, never in the build; rebuild
4 REPEAT  from 1, with fresh reviewers, until a round finds no must-fix item
5 HAND    the author gets one link: the assembled paper view (the Board's Writing view)
```

An author's own words, a decision they made, or a scientific choice is never changed silently: list it for them with
the link, even when a reviewer calls a sentence weak. The reviewers use `haipipe-draft-review`, see no earlier round's findings, and must check at least:

| Check | The defect it catches |
|---|---|
| A display's data unit against its caption | a figure plots physicians, its caption says visits |
| The topic of each display citation after a renumbering | "eTable 5" now names another table; a sweep must match `eTable~5` with a tie as well as "eTable 5" with a space |
| Every stated count | "5 specifications" where the table shows 6 |
| Math and layout in the Word version | a lost square root, layout codes printed as text, hyphens for minus signs |
| A number the text cites from a table | the cited row was never printed in that table |

A clean final read does not replace the person's reading pass (`ref/submission-readiness.md` § Human reading pass); it
is what makes that pass worth a person's time. Checklist: D10.
