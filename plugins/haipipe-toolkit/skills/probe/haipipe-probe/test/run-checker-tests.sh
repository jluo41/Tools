#!/bin/sh
# run-checker-tests.sh -- regression harness for the probe-file checkers.
#
# WHY THIS EXISTS. `check-probe-cards.sh` is the gate every stage's PROBE phase must pass,
# and it is ~1000 lines of shell with no tests. Worse, the paper and application families
# each carry their OWN copy: measured 2026-07-19, 445 of ~1000 lines had diverged, and the
# application copy was missing PASS 4 (placeholder ownership), the `concern` terminal state,
# and stage_stem() ENTIRELY -- none of it declared anywhere. Nothing detected that, because
# nothing compared them and nothing tested either one.
#
# The fixture under fixture/ exercises each mechanism once, so a refactor can be verified
# instead of hoped at. Run it BEFORE and AFTER any checker change and diff the output.
#
#   sh run-checker-tests.sh                 # run + show
#   sh run-checker-tests.sh --save BASE     # write output to BASE/
#   diff -r BASE_before BASE_after          # the actual regression check
#
# NOTE ON COVERAGE, stated honestly: the fixture covers the PAPER family only, because there
# is NO application/intervention data anywhere on disk to build a real case from (verified
# 2026-07-19: the one applications/ folder in examples/ holds a .gitkeep and nothing else).
# Porting anything to the application checker therefore ships UNVERIFIED until an application
# fixture exists. That is a known gap, not an oversight.
set -u
here=$(cd "$(dirname "$0")" && pwd)
skills=$(cd "$here/../../.." && pwd)
paper_chk="$skills/paper/workers/haipipe-paper-probe/check-probe-cards.sh"
fx="$here/fixture/proj/papers/Paper-Fx"
out=""
[ "${1:-}" = "--save" ] && { out=${2:?--save needs a dir}; mkdir -p "$out"; }

run() {
  label=$1; shift
  if [ -n "$out" ]; then sh "$@" > "$out/$label.txt" 2>&1; echo "  wrote $out/$label.txt"
  else echo "───── $label"; sh "$@" 2>&1; fi
}
run all       "$paper_chk" "$fx"
run stage-seed "$paper_chk" "$fx" --stage seed
run final      "$paper_chk" "$fx" --final
