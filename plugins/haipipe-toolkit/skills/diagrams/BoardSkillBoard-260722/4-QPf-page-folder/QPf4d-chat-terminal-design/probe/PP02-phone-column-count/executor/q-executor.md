# Q · the column count a phone viewport gives an xterm.js terminal, and the width the claude command line needs

Two measurements, reported together.

1 · On a phone-width viewport, with an xterm.js terminal at the font family and
    size it is configured with, report the exact column and row count the fit
    addon computes, and the per-cell pixel width it derives from those metrics.
    Report the device, its CSS pixel width, its device pixel ratio, and the font
    family and size used.

2 · Run the `claude` command line program in a terminal and narrow the window
    step by step. Report the smallest column count at which its box-drawn frames
    still render without wrapping into themselves, and what it does below that
    width. Report the program version.

Deliverable: a QA digest carrying both numbers with the device, font and version
each was measured with.
Accepted: an exact column count for each half.
