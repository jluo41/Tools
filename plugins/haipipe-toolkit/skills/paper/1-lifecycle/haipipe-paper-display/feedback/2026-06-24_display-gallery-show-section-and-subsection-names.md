---
status: open
created: 2026-06-24
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
---
"in the main display, the display should 1. first have the section name (so we
know which section we are in), and have a subsection name to explain it. The
display should be ordered correctly."

Standing requirement for the display gallery (`0-lifecycle/4-display/4-display.tex`):
every display must be reachable through TWO levels of heading so the reader always
knows where they are:

1. a `\section*{<paper section>}` banner (Introduction & Theory / Methods / Results
   / Discussion) -- tells the reader which manuscript section this display belongs
   to;
2. a `\subsection*{Figure N. <name>}` (or `Table N. <name>`) heading naming the
   individual display -- a short label that explains what it is.

Order must follow the NARRATIVE flow (the section banners run in reading order;
figures/tables numbered by order of appearance). This pairs with the existing
gallery requirements (venue display set + a Parking section at the end).

FIX (proposed): haipipe-paper-display should, when building/refreshing the gallery,
ALWAYS emit a `\section*` per manuscript section and a named `\subsection*` per
display before each unit's `\input`, ordered to the narrative. Treat a display that
sits under no section banner, or with no named subsection, as a defect. Add this to
the display stage done-gate next to "ordered to narrative / venue set / Parking
section."

Fix:
