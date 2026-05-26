# Silenced changes for the <baseline-tag> → working diff
# Format: OLD<TAB>NEW   (tab-separated; lines starting with # are ignored)
#
# Each line specifies a (old, new) pair where the change should be silently
# accepted in DIFF.tex — i.e., only the new value is shown, no struck-through
# old value.
#
# protect-block: <COMMAND>   directives define LaTeX command blocks whose
# contents are NEVER silenced. Any change inside \<COMMAND>{...} stays visible
# in the tracked-changes PDF, even if the (old, new) pair would match elsewhere.
# Defaults are auto-populated from class detection (e.g. ABSTRACT/TITLE for
# INFORMS, abstract/title for standard LaTeX). Add more as needed.
#
# Used by silence-minor-changes.pl (called from make-diff.sh).

# ── Auto-populated by detect-paper-class.sh ──
protect-block: <CLASS_PROTECT_DEFAULTS>


# ── Numerical / cosmetic changes to silence ──
# (Add (old, new) pairs below, one per line, tab-separated.
#  Example: a v0503 audit corrected 6.7→6.5 throughout the body. To stop
#  showing those in the diff, add this line:)
#
# 6.7	6.5
# 3.5	3.4
# 7.7	7.8
