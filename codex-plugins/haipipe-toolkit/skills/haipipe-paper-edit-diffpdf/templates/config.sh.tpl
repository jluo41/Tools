# config.sh — per-diff overrides for make-diff.sh
#
# Drop this file into 1-diff/<sub>/ to override the auto-detected class
# defaults. Sourced by make-diff.sh after detect-paper-class.sh runs, so any
# variables set here override the auto-detected ones.
#
# Empty file = use defaults. Uncomment / edit only the lines you need.

# ── latexdiff markup style ────────────────────────────────────────────────
# Choices: UNDERLINE (default — blue+wave for adds, red+strike for dels),
#          CFONT (color only, no underline — denser),
#          BOLD, CHANGEBAR, TRADITIONAL.
# LATEXDIFF_TYPE="UNDERLINE"

# ── Which commands to word-level diff into vs leave opaque ────────────────
# Auto-detected. Override only when the auto choice misbehaves
# (e.g., diff inside \TITLE{} overruns the title block — see known-bugs.md).
# LATEXDIFF_EXCLUDE_TEXTCMD="section,subsection,subsubsection,TITLE,RUNTITLE"
# LATEXDIFF_APPEND_TEXTCMD="ABSTRACT,KEYWORDS"
# LATEXDIFF_APPEND_CONTEXT2CMD="abstract,caption"

# ── Protected blocks for the silencer ─────────────────────────────────────
# Override the silencer's default block list. Whatever you put here, the
# silencer will NEVER touch text inside \<NAME>{...} for those names.
# (Easier to set this in silenced-changes.txt via `protect-block: NAME` lines.)
# PROTECTED_BLOCKS="ABSTRACT,TITLE"

# ── Compiler ──────────────────────────────────────────────────────────────
# Auto-detected from preamble (pdflatex / lualatex / xelatex).
# COMPILER_HINT="pdflatex"
