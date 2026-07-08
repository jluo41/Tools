#!/bin/bash
# detect-paper-class.sh
#
# Inspect a LaTeX master tex file, identify the document class, and emit
# recommended latexdiff configuration as shell variable assignments on stdout.
# Diagnostic information is printed to stderr.
#
# Usage:
#   eval "$(./detect-paper-class.sh path/to/master.tex)"
#   # exposes: LATEXDIFF_EXCLUDE_TEXTCMD, LATEXDIFF_APPEND_TEXTCMD,
#             LATEXDIFF_APPEND_CONTEXT2CMD, PROTECTED_BLOCKS,
#             DETECTED_CLASS, COMPILER_HINT
#
# Recognized classes (extend by adding cases below):
#   informs0/3/4    — INFORMS journals (MS, MNSC, ISR, etc.)
#   acmart          — ACM venues (CHI, KDD, SIGGRAPH, etc.)
#   IEEEtran        — IEEE journals & conferences
#   llncs           — Springer LNCS (lecture notes)
#   neurips_<year>  — NeurIPS conference style
#   icml<year>      — ICML conference style
#   article         — Standard LaTeX article (fallback)
#   <other>         — Generic fallback (uses article defaults)

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 <master.tex>" >&2
    exit 1
fi

MASTER="$1"

if [ ! -f "$MASTER" ]; then
    echo "Error: $MASTER does not exist" >&2
    exit 1
fi

# Extract documentclass — handles \documentclass[opt1,opt2]{class}
CLASS_LINE=$(grep -E '^\\documentclass' "$MASTER" | head -1)
CLASS_NAME=$(echo "$CLASS_LINE" | sed -nE 's/.*\\documentclass(\[[^]]*\])?\{([^}]*)\}.*/\2/p')
CLASS_OPTS=$(echo "$CLASS_LINE" | sed -nE 's/.*\\documentclass\[([^]]*)\]\{[^}]*\}.*/\1/p')

if [ -z "$CLASS_NAME" ]; then
    echo "Warning: could not detect \\documentclass in $MASTER; using generic article fallback" >&2
    CLASS_NAME="article"
fi

# Compiler hint: scan for tikz/microtype/fontspec to guess pdflatex vs xelatex
COMPILER_HINT="pdflatex"
if grep -q '\\usepackage{fontspec}\|\\usepackage{unicode-math}' "$MASTER" 2>/dev/null; then
    COMPILER_HINT="xelatex"
fi
if grep -q '\\usepackage{luacode}\|\\directlua' "$MASTER" 2>/dev/null; then
    COMPILER_HINT="lualatex"
fi

# Class-specific presets
# Each case sets:
#   EXCLUDE   — commands whose contents are NOT word-level diffed (treated opaque)
#   APPEND    — commands whose contents ARE word-level diffed (in addition to defaults)
#   CTX2      — commands treated as context (renamed/replaced as a whole, not diffed inside)
#   PROTECT   — block names whose contents the silencer must NEVER touch
case "$CLASS_NAME" in
    informs0|informs3|informs4)
        # INFORMS journals: TITLE/RUNTITLE/RUNAUTHOR are short top-of-page commands;
        # word-level diff inside them overruns the title block (empty-page-1 bug).
        # ABSTRACT/KEYWORDS are body-like, safe to diff at word level.
        EXCLUDE="section,subsection,subsubsection,TITLE,RUNTITLE,RUNAUTHOR"
        APPEND="ABSTRACT,KEYWORDS"
        CTX2="abstract,caption"
        PROTECT="ABSTRACT,TITLE"
        ;;
    acmart)
        # ACM venues. Standard \title{} / \abstract{} / \author{}.
        # affiliation blocks are noisy — exclude.
        EXCLUDE="section,subsection,subsubsection,affiliation,thanks"
        APPEND="title,subtitle,abstract,keywords"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
    IEEEtran)
        # IEEE journals/conferences. \markboth{}{} for running heads.
        EXCLUDE="section,subsection,subsubsection,markboth,thanks,IEEEauthorrefmark"
        APPEND="title,IEEEkeywords,IEEEpubid"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
    llncs|sn-jnl)
        # Springer Lecture Notes / SN journals.
        EXCLUDE="section,subsection,subsubsection,institute,thanks"
        APPEND="title,subtitle,author,abstract,keywords"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
    neurips_*|icml*|tmlr|colm)
        # ML conferences (NeurIPS / ICML / TMLR / COLM all use \title / \author / \abstract).
        EXCLUDE="section,subsection,subsubsection,thanks,affiliation"
        APPEND="title,abstract"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
    elsarticle|cas-sc|cas-dc)
        # Elsevier journal classes.
        EXCLUDE="section,subsection,subsubsection,thanks,address"
        APPEND="title,author,abstract"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
    article|amsart|book|report|memoir|*)
        # Generic LaTeX standard classes — also the fallback for anything unknown.
        EXCLUDE="section,subsection,subsubsection,thanks,maketitle"
        APPEND="title,subtitle,author,abstract"
        CTX2="abstract,caption"
        PROTECT="abstract,title"
        ;;
esac

# Diagnostics to stderr (visible to user)
{
    echo "─── detect-paper-class ────────────────────────────────────────────"
    echo "  master tex:    $MASTER"
    echo "  class:         $CLASS_NAME"
    [ -n "$CLASS_OPTS" ] && echo "  class options: $CLASS_OPTS"
    echo "  compiler hint: $COMPILER_HINT"
    echo "  --exclude-textcmd      $EXCLUDE"
    echo "  --append-textcmd       $APPEND"
    echo "  --append-context2cmd   $CTX2"
    echo "  protect-block:         $PROTECT"
    echo "──────────────────────────────────────────────────────────────────"
} >&2

# Emit shell-eval-friendly assignments to stdout
printf 'DETECTED_CLASS=%q\n' "$CLASS_NAME"
printf 'DETECTED_CLASS_OPTS=%q\n' "$CLASS_OPTS"
printf 'COMPILER_HINT=%q\n' "$COMPILER_HINT"
printf 'LATEXDIFF_EXCLUDE_TEXTCMD=%q\n' "$EXCLUDE"
printf 'LATEXDIFF_APPEND_TEXTCMD=%q\n' "$APPEND"
printf 'LATEXDIFF_APPEND_CONTEXT2CMD=%q\n' "$CTX2"
printf 'PROTECTED_BLOCKS=%q\n' "$PROTECT"
