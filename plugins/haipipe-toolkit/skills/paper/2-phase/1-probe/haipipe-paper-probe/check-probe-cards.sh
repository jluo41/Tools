#!/bin/sh
# check-probe-cards.sh -- deterministic PP-card verifier for the PROBE phase.
# Usage: sh check-probe-cards.sh <paper_root> [project_root]
#
# Checks every <paper_root>/0-lifecycle/*/_PROBE/PP*.md card, plus the
# section-level cards one directory deeper (0-lifecycle/*/*/_PROBE/PP*.md):
#   1. status read|verdicted|answered-local -> refs: non-empty, no placeholder,
#      every path resolves under project_root (or paper_root: answered-local
#      cards cite the paper's OWN registries; JL 2026-07-10 paper-local sweep)
#   2. no markdown tables in any card (inline-evidence smell; JL standing rule: no tables in probes)
#   3. card <= 80 lines (a fat card = findings pasted inline instead of landed project-side)
#   4. status: failed is surfaced as FAIL (the gate must not go green over it)
#   5. status planned|dispatched -> FAIL probe-not-run (a buffered/in-flight card
#      must not survive to VERIFY or the CHECK gate; JL 2026-07-07)
#   6. "harvest: OWED" on any lane line (pick_list/value_refs/unit_refs) -> FAIL
#      harvest-owed (the harvester was skipped; Part-0 harvester ruling)
# Plus a working-doc pass: _CITATION_/_VALUES_/_DISPLAY_ carry no bibtex entries;
# _CITATION_ carries no markdown tables (durable mirror of harvest acceptance).
#
# Exit 0 = all PASS. Exit 1 = any FAIL. RUN this, never eyeball the checks.
# Called at the worker's STEP 4 (VERIFY) and again by the stage CHECK gate.

set -u
paper_root=${1:?usage: check-probe-cards.sh <paper_root> [project_root]}
project_root=${2:-}

# Resolve project_root: FIRST ancestor of paper_root containing discoveries/.
# Never git rev-parse here -- repo-backed papers are their own git repos, so
# --show-toplevel returns paper_root itself, not the project.
if [ -z "$project_root" ]; then
  d=$(cd "$paper_root" && pwd)
  while [ ! -d "$d/discoveries" ] && [ "$d" != / ]; do d=$(dirname "$d"); done
  if [ ! -d "$d/discoveries" ]; then
    echo "FAIL  no project_root: no ancestor of $paper_root contains discoveries/"
    exit 1
  fi
  project_root=$d
fi

# expand_ref: emit one path per line from a ref token.
#   prefix/{a,b,c}  -> prefix/a prefix/b prefix/c   (agents write this shorthand)
#   a,b             -> a b                           (top-level comma list)
#   a               -> a
expand_ref() {
  t=$1
  case "$t" in
    *'{'*'}'*)
      pre=${t%%\{*}; rest=${t#*\{}; inner=${rest%%\}*}; post=${rest#*\}}
      oIFS=$IFS; IFS=,
      for item in $inner; do printf '%s\n' "${pre}${item}${post}"; done
      IFS=$oIFS ;;
    *)
      oIFS=$IFS; IFS=,
      for item in $t; do printf '%s\n' "$item"; done
      IFS=$oIFS ;;
  esac
}

fail=0
found=0
for card in "$paper_root"/0-lifecycle/*/_PROBE/PP*.md "$paper_root"/0-lifecycle/*/*/_PROBE/PP*.md; do
  [ -e "$card" ] || continue
  found=1
  name=${card#"$paper_root"/}
  problems=""

  status=$(grep -o 'status: [a-z-]*' "$card" | head -1 | awk '{print $2}')
  [ -z "$status" ] && problems="$problems no-status-field;"

  tables=$(grep -c '^|' "$card")
  [ "$tables" -gt 0 ] && problems="$problems markdown-table(${tables}-lines);"

  lines=$(wc -l < "$card")
  [ "$lines" -gt 80 ] && problems="$problems too-long(${lines}-lines>80);"

  case "$status" in
    read|verdicted|answered-local)
      refs=$(grep -m1 '^- refs:' "$card" | sed 's/^- refs:[[:space:]]*//')
      if [ -z "$refs" ] || printf '%s' "$refs" | grep -q '<'; then
        problems="$problems empty-refs(status:$status);"
      else
        for ref in $(printf '%s\n' "$refs" | tr '·' ' '); do
          for eref in $(expand_ref "$ref"); do
            [ -n "$eref" ] || continue
            [ -e "$project_root/$eref" ] || [ -e "$paper_root/$eref" ] || problems="$problems unresolved-ref($eref);"
          done
        done
      fi
      ;;
    failed)
      problems="$problems status-failed(surface-it);"
      ;;
    planned|dispatched)
      # A planned/dispatched card at VERIFY or the CHECK gate means the probe
      # was never run (DRAFT-buffered skeleton or in-flight dispatch never
      # TRANSLATEd). The gate must NOT go green over it (JL 2026-07-07, T1).
      problems="$problems status-$status(probe-not-run);"
      ;;
  esac

  # Lane obligations (harvester model, JL 2026-07-07 Part-0 ruling): TRANSLATE
  # records what each lane owes as "harvest: OWED" on the pick_list /
  # value_refs / unit_refs line; acceptance flips it to "harvest: accepted".
  # An OWED lane surviving to VERIFY / the gate = the harvest was skipped.
  owed=$(grep -c 'harvest: OWED' "$card")
  [ "$owed" -gt 0 ] && problems="$problems harvest-owed(${owed}-lane);"

  if [ -n "$problems" ]; then
    echo "FAIL  $name  --$problems"
    fail=1
  else
    echo "PASS  $name  (status: ${status:-?})"
  fi
done

[ "$found" -eq 0 ] && echo "WARN  no _PROBE/PP*.md cards under $paper_root/0-lifecycle/"

# Working-doc pass (B10): the no-bibtex / no-tables rules must hold durably,
# not only during a harvest run. Mirrors the harvest-acceptance greps.
for doc in "$paper_root"/0-lifecycle/*/_CITATION_*.md "$paper_root"/0-lifecycle/*/_VALUES_*.md "$paper_root"/0-lifecycle/*/_DISPLAY_*.md \
           "$paper_root"/0-lifecycle/*/*/_CITATION_*.md "$paper_root"/0-lifecycle/*/*/_VALUES_*.md "$paper_root"/0-lifecycle/*/*/_DISPLAY_*.md; do
  [ -e "$doc" ] || continue
  dname=${doc#"$paper_root"/}
  dprob=""
  bib=$(grep -cE '^[[:space:]]*@[A-Za-z]+\{[^,}]+,' "$doc")
  [ "$bib" -gt 0 ] && dprob="$dprob bibtex-entry(${bib});"
  case "$doc" in *_CITATION_*)
    dtab=$(grep -c '^|' "$doc")
    [ "$dtab" -gt 0 ] && dprob="$dprob markdown-table(${dtab}-lines);"
  ;; esac
  if [ -n "$dprob" ]; then
    echo "FAIL  $dname  --$dprob"
    fail=1
  fi
done

echo "project_root: $project_root"
exit $fail
