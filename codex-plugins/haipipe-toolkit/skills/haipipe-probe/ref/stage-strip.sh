#!/bin/sh
# stage-strip.sh <probe-dir> — render the haipipe-probe lifecycle stage strip.
#
# DERIVE-FROM-DISK (probe Golden Rule). A step is ✅ only when its expected
# artifact resolves on disk, NOT because probe.yaml says so. When a linked ref no
# longer resolves, the strip appends ⚠ drift. This is the deliberate divergence
# from paper/ref/stage-strip.sh, which trusts STATUS.md `current_layer`. Probes
# never trust stored stage: disk wins, and disagreement is surfaced, not hidden.
#
# Lifecycle:  Plan → Gather → Read → Judge → Deposit
# Frontier = first step whose disk predicate fails (▶️). Before it = ✅, after = ⬜.
#
# Done predicates (disk):
#   Plan    probe.yaml has a `claim:` block          (probe.yaml IS the plan artifact)
#   Gather  evidence declared AND every linked ref resolves on disk
#   Read    evidence.md exists   (lean atom: a `result:` block in probe.yaml)
#   Judge   verdict.md exists    (lean atom: a `verdict:` block in probe.yaml)
#   Deposit deposit.md exists    (lean atom: a `deposit:` block in probe.yaml)
#                                (▶️ until probe.yaml status is deposited/closed)
#   LEAN ATOM = a leaf probe declaring `parent:` (a comparison decomposition leaf):
#   it logs Read/Judge/Deposit compactly in probe.yaml instead of separate .md files.
#
# Path-like refs checked: tokens under examples/ tasks/ discoveries/ insights/
# probes/ paper/ applications/ . _WorkSpace/ refs are NOT checked — they are
# server-side PHI, legitimately absent on a laptop, so they never count as drift.
# Refs resolve by exact path OR prefix-glob, so a prose abbreviation of a real
# path (discoveries/L01 for discoveries/L01_foo) still counts as resolved.
#
# Output (1-2 lines):
#   Plan ✅ ─ Gather ▶️ ─ Read ⬜ ─ Judge ⬜ ─ Deposit ⬜   ⚠ drift
#      ← here Gather: 5/6 linked refs unresolved: R01_Regression_TraitOpioid
#
# Usage: sh stage-strip.sh [probe-dir]   (defaults to cwd; walks upward for probe.yaml)

probe="${1:-.}"

# --- resolve the probe dir: given dir, else walk upward for probe.yaml ---------
find_probe() {
  d=$(cd "$1" 2>/dev/null && pwd) || return 1
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    [ -f "$d/probe.yaml" ] && { printf '%s\n' "$d"; return 0; }
    d=$(dirname "$d")
  done
  return 1
}
pdir=$(find_probe "$probe") || { echo "stage-strip: no probe.yaml at or above $probe" >&2; exit 1; }
yaml="$pdir/probe.yaml"

# --- resolve project root (nearest ancestor with probes/) and repo root --------
find_up() {  # find_up <start> <test-relpath>
  d="$1"
  while [ -n "$d" ] && [ "$d" != "/" ]; do
    [ -e "$d/$2" ] && { printf '%s\n' "$d"; return 0; }
    d=$(dirname "$d")
  done
  return 1
}
projroot=$(find_up "$pdir" "probes") || projroot=$(dirname "$(dirname "$pdir")")
reporoot=$(find_up "$pdir" "pyproject.toml" || find_up "$pdir" ".git" || printf '%s' "$projroot")
status=$(grep -m1 '^status:' "$yaml" | sed 's/^status:[[:space:]]*//; s/#.*//' | tr -d '[:space:]')

# --- helpers ------------------------------------------------------------------
has_key()  { grep -qE "^${1}:" "$yaml"; }            # top-level yaml key present
has_file() { [ -f "$pdir/$1" ]; }                    # human artifact present
resolve_ref() {                                      # exact OR prefix-glob, any base
  r="$1"
  [ -e "$projroot/$r" ] && return 0
  [ -e "$reporoot/$r" ] && return 0
  [ -e "$r" ]           && return 0
  for b in "$projroot/" "$reporoot/" "./"; do
    for m in "$b$r"*; do [ -e "$m" ] && return 0; done
  done
  return 1
}
refkey() {                                           # compact label for a broken ref
  case "$1" in
    */tasks/*)       printf '%s' "${1#*/tasks/}"       | cut -d/ -f1 ;;
    tasks/*)         printf '%s' "${1#tasks/}"         | cut -d/ -f1 ;;
    */discoveries/*) printf 'discoveries/%s' "$(printf '%s' "${1#*/discoveries/}" | cut -d/ -f1)" ;;
    discoveries/*)   printf 'discoveries/%s' "$(printf '%s' "${1#discoveries/}"   | cut -d/ -f1)" ;;
    *)               printf '%s' "$1" | cut -d/ -f1-2 ;;
  esac
}

# --- linked path-like refs, excluding server-side _WorkSpace PHI --------------
refs=$(grep -oE '(examples|tasks|discoveries|insights|probes|paper|applications)/[A-Za-z0-9._/-]+' "$yaml" 2>/dev/null \
        | sed 's:/*$::' | sort -u)
broken=0; reftotal=0; broken_keys=""
for r in $refs; do
  reftotal=$((reftotal + 1))
  resolve_ref "$r" && continue
  broken=$((broken + 1))
  k=$(refkey "$r")
  case " $broken_keys " in *" $k "*) : ;; *) broken_keys="$broken_keys $k" ;; esac
done

# --- per-step done predicates -------------------------------------------------
plan_done=0;   has_key claim && plan_done=1
gather_decl=0
for k in evidence_refs arms calls evidence_plan links design cells; do
  has_key "$k" && { gather_decl=1; break; }
done
gather_done=0; [ "$gather_decl" -eq 1 ] && [ "$broken" -eq 0 ] && gather_done=1
# LEAN-ATOM MODE: a leaf atom of a comparison decomposition (declares `parent:`)
# records its Read/Judge/Deposit COMPACTLY in probe.yaml (result/verdict/deposit
# blocks) instead of separate .md files. For such atoms the strip reads the yaml
# block; for normal probes it still requires the human .md artifact. yaml IS disk,
# so this stays within the derive-from-disk rule.
is_lean=0; has_key parent && is_lean=1
read_done=0;    { has_file evidence.md || { [ "$is_lean" -eq 1 ] && has_key result;  }; } && read_done=1
judge_done=0;   { has_file verdict.md  || { [ "$is_lean" -eq 1 ] && has_key verdict; }; } && judge_done=1
deposit_done=0; { has_file deposit.md  || { [ "$is_lean" -eq 1 ] && has_key deposit; }; } && deposit_done=1

# --- frontier: first not-done (0-based over Plan..Deposit) ---------------------
i=0; frontier=5
for done in "$plan_done" "$gather_done" "$read_done" "$judge_done" "$deposit_done"; do
  [ "$done" -eq 0 ] && { frontier=$i; break; }
  i=$((i + 1))
done
# all artifacts present but probe not declared closed -> Deposit is still active
if [ "$frontier" -eq 5 ]; then
  case "$status" in deposited|returned|closed) : ;; *) frontier=4 ;; esac
fi

drift=0; [ "$broken" -gt 0 ] && drift=1

# --- render line 1: the strip -------------------------------------------------
labels="Plan Gather Read Judge Deposit"
out=""; i=0
for L in $labels; do
  if   [ "$i" -lt "$frontier" ]; then m="✅"
  elif [ "$i" -eq "$frontier" ]; then m="▶️"
  else                                m="⬜"
  fi
  seg="$L $m"
  [ -z "$out" ] && out="$seg" || out="$out ─ $seg"
  i=$((i + 1))
done
[ "$drift" -eq 1 ] && out="$out   ⚠ drift"
printf '%s\n' "$out"

# --- line 2: why the frontier is here (only when it carries information) ------
fname=$(printf '%s' "$labels" | cut -d' ' -f$((frontier + 1)))
nkeys=$(printf '%s' "$broken_keys" | wc -w | tr -d ' ')
shown=$(printf '%s' "$broken_keys" | sed 's/^ *//' | cut -d' ' -f1-3 | sed 's/ /, /g')
extra=""; [ "$nkeys" -gt 3 ] && extra=" (+$((nkeys - 3)) more)"
why=""
case "$frontier" in
  0) why="probe.yaml has no claim:" ;;
  1) if [ "$gather_decl" -eq 0 ]; then why="no evidence declared yet"
     elif [ "$broken" -gt 0 ];    then why="${broken}/${reftotal} linked refs unresolved: ${shown}${extra}"
     fi ;;
  2) why="no evidence.md (Read not run)" ;;
  3) why="no verdict.md (Judge not run)" ;;
  4) if [ "$deposit_done" -eq 1 ]; then why="deposit.md present but probe not closed (status: ${status:-active})"
     else why="Judge done; Deposit not run (no deposit.md)"; fi ;;
esac
[ -n "$why" ] && printf '   ← here %s: %s\n' "$fname" "$why"
