# <Venue>: the call, as read on <YYYY-MM-DD>

venue: <full name of the journal, funder or office>
desk: <the desk token the paper uses, lowercase: misq · jama-im>
link: <the call's own page>
read: <YYYY-MM-DD, the day these rules were read>
bank: <the shared Venue Page this follows, venue/bank/1-QBv-desks/QBv<n>-<slug>/, or none>

## Dates

| what | date | from |
|---|---|---|
| <submission deadline, or rolling> | <date> | <link or quoted line> |

## Limits

| what | limit | counts |
|---|---|---|
| words | <main text limit> | <what is counted: abstract, references, tables?> |
| references | <limit or none> | |
| abstract | <words, structure> | |

## Displays

How the venue wants its figures and tables (JL 261101: "the display ... should also follow the venue"). The paper's
display plan (haipipe-paper-plan `s06-paper-displays`) is checked against these rows by `display_plan.py check`; a
row left out is not checked, and the check names it.

| rule | value | source |
|---|---|---|
| main limit | <n (figures and tables together), or "n figures, m tables"> | <link or quoted line> |
| supplement limit | <n, or no limit> | |
| main labels | <Figure n, Table n> | |
| supplement labels | <eFigure n, eTable n · Supplementary Figure n …> | |
| width | <the widest a figure prints: 7 in (two columns)> | |
| resolution | <300 dpi> | |
| format | <PNG, PDF, TIFF, EPS> | |
| font | <8 pt or larger> | |
| table style | <no vertical rules; units in the column heads> | |
| caption | <at most n words> | |

## Format

- article type: <the type the paper is sent as>
- structure: <required sections, in order>
- files: <manuscript, supplement, cover letter, data statement>

## Review rules

- <blind, double-blind or open; suggested reviewers; data and code policy; preprint policy>

## Kit

`kit/` holds the author template as shipped (LaTeX class, Word template), unchanged; the version's build reads it.

## Changed since last read

- <what Check the rules found different from the last read, or "first read">
