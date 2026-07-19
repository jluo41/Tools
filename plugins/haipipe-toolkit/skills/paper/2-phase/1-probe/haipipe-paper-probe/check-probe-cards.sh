#!/bin/sh
# check-probe-cards.sh -- deterministic PROBE-FILE verifier for the PROBE phase.
#
# THE FILENAME IS LOAD-BEARING AND DOES NOT CHANGE (65 refs across 33 files).
# Its INTERNALS were rewritten 2026-07-14 for the probe redesign
# (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, approved JL; rulings R1-R18). It no longer checks
# "cards": it checks PROBE FILES made of QUESTION SECTIONS.
#
# (paper family. The application family carries the same file, same rules, same shared
# LEAK_AWK pattern set, with `intervention_root` in place of `paper_root` -- and WITHOUT
# the RESOURCE-STAGE PASS below, which is paper-only. Keep the two in step.)
#
# Usage: sh check-probe-cards.sh <paper_root> [project_root] [--stage <key>]
#
# WHAT IT CHECKS -- three passes, plus a paper-only RESOURCE-STAGE pass.
#
# PASS 1: every <paper_root>/1-probes/PP*.md probe file, ENTRY BY ENTRY
#   (an entry = a `## QX<n>` heading + its ### q-executor / ### q-consumer / ### bank binding
#    (**route**/**bank**/**target**/**state**) / ### a-executor subsections)
#   1. state read           -> target: non-empty, no placeholder, resolves under
#                              project_root (or paper_root for answered-local:
#                              those cite the paper's OWN registries)
#   2. state answered       -> the target QA file exists but ### a-executor is still empty
#                              = the harvest never happened. FAIL (answered-not-read).
#   3. state planned        -> FAIL probe-not-run. A buffered section must not survive
#                              to VERIFY or the CHECK gate.
#   4. state commissioned   -> PASS only with owner: + eta: + blocks: + cross-project:,
#                              and eta in the FUTURE. A commissioned BUILD is legitimately
#                              in flight for weeks and must not red the gate; an OVERDUE
#                              one must. Without the date test, `commissioned` becomes the
#                              state every un-run section wears and the mechanism ships as a
#                              LAUNDERING TOKEN. (JL rulings C4 + C6, 2026-07-14)
#                              THE LOOP-CLOSER: the branch also OPENS a `*/QA/*` target --
#                              `answered` -> FAIL commissioned-target-answered (the answer
#                              LANDED; harvest it), `superseded-by:` -> FAIL commissioned-
#                              target-superseded, `working` -> PASS (honestly in flight; the
#                              TTL guards it). Without this a section whose answer landed
#                              sits GREEN until its eta expires.
#   5. state failed         -> surfaced as FAIL (the gate must not go green over it)
#   6. LAW 2 (surface 1)    -> the q-executor: block carries NO consumer vocabulary and
#                              NO stake disclosure. The commission is the ONLY thing that
#                              crosses to the executor; `## Why` never does.
#   7. harvest: OWED        -> FAIL on any lane line (values/sources/displays). The
#                              harvester was skipped; the phase cannot go green over it.
#   8. no markdown tables   -> a probe file holds SECTIONS, never a table (JL house rule)
#   9. a ref under _WorkSpace/ -> FAIL. _WorkSpace/ is gitignored and resolves under
#                              neither root. Name the TASK that produced/scanned the asset.
#  10. DEAD VOCABULARY      -> `verdicted`, `## Verdict`, `## Takeaways`, `answers:`,
#                              `_ASK`, `_ANS` in a probe file = a pre-v8 artifact. FAIL.
#  11. THE TARGET'S STATE LINE (R19/R20, 2026-07-14) -> a `state: read` section whose
#                              target: resolves to a QA file that is `state: working`
#                              (read-target-working: the paper claims it READ an UNFINISHED
#                              answer), that carries `superseded-by:` (read-target-
#                              superseded: the reading is built on a STALE answer), or that
#                              carries NO state line at all (read-target-no-state: `state:`
#                              is MANDATORY). EXISTENCE OF THE TARGET IS NO LONGER ENOUGH --
#                              the checker OPENS it.
#
# PASS 2: RETIRED 2026-07-19 -- no `_VALUES_` / `_CITATION_` sidecars anymore (JL: `1-probes/`
#   is the only consumer-side source of truth; `_LOG` is the only kept sidecar).
#
# PASS 3: THE BANK -- two rules on the same files, <project_root>/{tasks,discoveries}/**/QA/*.md.
#   (a) LAW 2 (surface 2): a QA file must carry NO consumer vocabulary. A QA file written in
#   the consumer's claim labels (i) contaminates the reusable bank -- the evidence comes back
#   consumer-SHAPED and is then effectively single-use -- and (ii) proves a consumer session
#   wrote it, which is LAW 1 broken. This is what would have caught
#   tasks/A03_welldoc_cycle_check/result.md, whose "C6"/"C7" arrived with no probe file
#   involved anywhere.
#   (b) THE CLAIM'S OWN VALIDITY (R19): NO `- state:` line at all = the field is MANDATORY and
#   its absence exempts the file from every check below (qa-no-state); `state: working` with no
#   `started:` = an UNEXPIRABLE claim (qa-working-no-started); `state: working` older than
#   QA_WORKING_TTL_HOURS = a ZOMBIE claim (qa-working-expired); `state: answered` with an EMPTY
#   `## Answer` = a LYING RECEIPT (qa-answered-empty).
#   PASS 3 also FAILs the RETIRED bank machinery: an `_ASK/` or `_ANS/` folder, or a PP id
#   in a QA filename. The bank is PROBE-UNAWARE (R2): none of those may exist.
#
# BOTH LAW-2 SURFACES SHARE ONE PATTERN SET -- the awk function library `LEAK_AWK` below.
#   They are the same rule on two surfaces; two hand-copied regex sets drift, and the
#   drift is silent. (2026-07-14: the first cut of this file carried two copies, and
#   BOTH of them missed the canonical bare-label leak `- C6: <question> -> NO`.)
#   THE STATE-LINE LOGIC IS FACTORED THE SAME WAY -- the `QA_STATE` shell-function block,
#   called by PASS 1 (a section's target) and PASS 3 (the bank's own files). Same reason.
#
# LEGACY: pre-v8 locations (1-probe-plans/PP*.md, 0-lifecycle/*/_PROBE/PP*.md) are still
#   GLOBBED, and reported as MIGRATE -- they are read-only history until a run touches them,
#   at which point ORGANIZE rewrites them into 1-probes/ in the new shape. A legacy file is
#   NOT silently passed: it is surfaced, so nobody mistakes "not checked" for "fine".
#
# --stage <key>  Assert only the entries that SERVE this stage (a `### q-consumer` id names it,
#   e.g. `Q-Seed-1` -> seed). Entries with no `### q-consumer` always assert. Without it, ONE
#   in-flight build reds the gate of EVERY downstream stage for as long as the build runs --
#   because every stage's CHECK invokes this same whole-paper glob. (JL ruling C8-i)
#
# Exit 0 = all PASS. Exit 1 = any FAIL. RUN this, never eyeball the checks.
# Called at the worker's VERIFY step and again by the stage CHECK gate.

set -u
paper_root=""
project_root=""
stage_filter=""
while [ $# -gt 0 ]; do
  case "$1" in
    --stage) shift; stage_filter=${1:?--stage needs a key}; ;;
    --stage=*) stage_filter=${1#--stage=} ;;
    *) if [ -z "$paper_root" ]; then paper_root=$1
       elif [ -z "$project_root" ]; then project_root=$1
       else echo "FAIL  unexpected arg: $1"; exit 1; fi ;;
  esac
  shift
done
[ -n "$paper_root" ] || { echo "usage: check-probe-cards.sh <paper_root> [project_root] [--stage <key>]"; exit 1; }

# Resolve project_root: FIRST ancestor of paper_root containing discoveries/.
# Never git rev-parse here -- repo-backed projects are their own git repos, so
# --show-toplevel returns paper_root itself, not the project.
if [ -z "$project_root" ]; then
  # GUARD THE cd. An unchecked `cd` into a missing root leaves $d EMPTY, and the walk below
  # then spins on `dirname "" -> . -> . -> .` -- a FIXED POINT that never reaches `/`. The
  # checker HANGS instead of failing fast (a typo'd or not-yet-created root in CI = a hung job).
  d=$(cd "$paper_root" 2>/dev/null && pwd) || d=""
  [ -n "$d" ] || { echo "FAIL  no such root: $paper_root"; exit 1; }
  while [ ! -d "$d/discoveries" ] && [ "$d" != / ] && [ "$d" != . ]; do d=$(dirname "$d"); done
  if [ ! -d "$d/discoveries" ]; then
    echo "FAIL  no project_root: no ancestor of $paper_root contains discoveries/"
    exit 1
  fi
  project_root=$d
fi

# ===========================================================================
# LEAK_AWK -- the ONE LAW-2 pattern set, shared by both surfaces.
#
# Prepended to the awk program of PASS 1 (commission blocks) and PASS 3 (bank
# QA files). LAW 2 is the SAME rule on two surfaces; keeping two hand-copied
# copies is how the first cut shipped with the canonical leak undetected.
#
# THE FALSE-POSITIVE GUARANTEE COMES FIRST. This domain legitimately writes bare
# H/C tokens -- forecast horizons (H1..H6), cohort arms ("arm C2"), and real task
# paths (tasks/.../C3-Visual-ForecastScaling/). A gate that FAILs correct work gets
# muted, and it takes the real detections down with it. So the lint fires on the
# three shapes in which an H/C id is actually USED AS A CONSUMER CLAIM ID:
#
#   VOCAB  an H/C id on a line that ALSO carries claim vocabulary
#          ("state whether claim C6 is supported")
#   LABEL  an H/C id used as a BULLET LABEL   ("- C6: does WellDoc ... -> NO")
#          <- the canonical leak (this is verbatim what A03's result.md carries),
#             and it carries NO claim vocabulary, so VOCAB alone provably misses it
#   PAIR   a slash-joined id pair            ("supports C6/C7", "refutes H1/H2")
#          <- and the OLD path-strip ATE these before any regex saw them
#
# PATH STRIPPING IS NARROW BY CONSTRUCTION. The first cut stripped every
# whitespace-delimited token containing a `/`, which deleted `C6/C7` and `H1/H2`
# outright. Here only genuinely path-shaped tokens are stripped: a URL, a known
# bank/consumer prefix, or a slashed token carrying a file extension.
# ===========================================================================
LEAK_AWK='
function strip_paths(s,   t) {
  t = s
  gsub(/https?:\/\/[^ \t]*/, " ", t)
  # known path prefixes (the bank + the consumer roots)
  gsub(/(tasks|discoveries|results|papers|applications|interventions|examples|configs|runs|workflow|_WorkSpace|0-lifecycle|1-probes|1-probe-plans|0-displays|0-artifacts|scripts|notebooks)\/[^ \t]*/, " ", t)
  # any slashed token that carries a file extension: foo/bar.md, a/b/c.json
  gsub(/[^ \t]*\/[^ \t]*\.[A-Za-z][A-Za-z]*[^ \t]*/, " ", t)
  return t
}
# an H/C id used as a BULLET LABEL. C-space is unconditional; H-space carves out the
# legitimate horizon breakdown (`- H1: 12.4 mg/dL`), whose value is numeric/unit-bearing.
function is_idlabel(s,   v, low) {
  if (s !~ /^[ \t]*[-*][ \t]*[HC][1-9][0-9]?([^:A-Za-z0-9][^:]*)?:/) return 0
  if (s ~ /^[ \t]*[-*][ \t]*H[1-9]/) {
    v = s; sub(/^[^:]*:[ \t]*/, "", v)
    if (v ~ /^[0-9]/) return 0
    low = tolower(s)
    if (low ~ /horizon|hour|mg\/dl|mae|rmse|minute/) return 0
  }
  return 1
}
# a slash-joined id pair: "C6/C7", "H1/H2". Exempt where the line names one of the
# legitimate H/C namespaces of this domain (horizons, arms, cohorts, columns...).
function is_idpair(s,   low) {
  if (s !~ /[HC][1-9][0-9]?\/[HC][1-9][0-9]?/) return 0
  low = tolower(s)
  if (low ~ /horizon|hour|arm|cohort|group|column|channel|class|cluster|bin/) return 0
  return 1
}
# an H/C id on a line that also carries claim vocabulary.
function is_vocab(s,   line, low) {
  line = strip_paths(s); low = tolower(line)
  if (low ~ /claim|hypothes|support|refut/ && line ~ /(^|[^A-Za-z])[HC][1-9][0-9]?([^A-Za-z0-9]|$)/) return 1
  return 0
}
function claim_leak(s) { return (is_vocab(s) || is_idlabel(s) || is_idpair(s)) ? 1 : 0 }
# consumer STAGE words. mode "comm" = a commission block (strictest: it must not name the
# consumer at all). mode "bank" = a QA file (a discovery legitimately says "the paper
# reports X" about a SOURCE paper, so bare "the paper" is not flagged there).
function stage_leak(s, mode,   low) {
  low = tolower(strip_paths(s))
  if (low ~ /claims-stage|the seed|the pitch|the narrative|our paper/) return 1
  if (mode == "comm" && low ~ /this paper|the paper we|seeds stage/) return 1
  if (mode == "bank" && low ~ /this paper needs/) return 1
  return 0
}
# stake disclosure: which answer the consumer WANTS. Never crosses, never lands.
function stake_leak(s,   low) {
  low = tolower(s)
  if (low ~ /rescue|we want|we hope|hoped-for|the answer we|would save|wants a positive|preferred outcome|consumer wants/) return 1
  return 0
}
'

# ===========================================================================
# QA_STATE -- the ONE state-line reader, shared by BOTH surfaces that read it:
#   PASS 1  a question section at `state: read`  -> is its target QA file FINISHED?
#   PASS 3  the bank's own QA files              -> is this claim VALID, ALIVE, HONEST?
#
# A QA FILE IS A TICKET THAT BECOMES A RECEIPT (R19/R20; Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ PART 3b,
# JL ruling 2026-07-14). It carries exactly ONE MUTABLE FIELD -- the state line:
#
#     # Q — <the question, restated by the executor in its own words>
#     - state:   working | answered | superseded-by: QA/<m>-<slug>.md
#     - started: 2026-07-14T09:12            <- MANDATORY when state: working
#     - by:      <run id | agent | human>    <- optional provenance
#     ## Answer   <- EMPTY while working. Filled at REPORT.
#
# ONE WRITER -- the EXECUTOR, and nobody else, EVER. "Write-once" was never the real rule;
# ONE WRITER was. The executor writes the START at the qa gate's (3) decision and the
# COMPLETION at REPORT. A CONSUMER-planted `working` file is the retired _ASK/ stub in a
# QA/ costume, and PASS 3 exists partly to make that visible.
#
# FACTORED ONCE, DELIBERATELY. The LAW-2 lint above learned this the hard way: two
# hand-copied regex sets drifted into IDENTICAL bugs, and both missed the canonical leak.
# The state-line logic is read by two passes and must never be typed twice.
#
# `superseded-by:` is APPENDED to the state line of an `answered` file -- it does NOT
# replace `answered`. The composed form on disk is:
#     - state:   answered · superseded-by: QA/2-cycle.md
# so `superseded` is tested against the WHOLE state value and wins over `answered`
# (staleness is the thing the reader must act on).
#
# A QA file with NO state line is MALFORMED, not "legacy". `state:` is MANDATORY, ALWAYS
# (the constitution, "The QA file" section). The first cut of this file mapped a stateless QA file to the kind
# `legacy` and EXEMPTED it from every claim check -- so an executor could defeat the whole
# lying-receipt tooth BY OMISSION: drop one line, ship an empty `## Answer`, and the gate
# goes green while a consumer publishes an `### a-executor` derived from nothing. The grandfather
# clause had ZERO beneficiaries (no QA file predates the field on disk). It is CLOSED:
# `qa-no-state` (bank side) / `read-target-no-state` + `commissioned-target-no-state`
# (consumer side). The file's OWNER -- the executor, never a consumer -- adds the line.
# ===========================================================================

# THE NAMED CONSTANT. Tune the working-file TTL HERE; never hard-code the literal anywhere else.
QA_WORKING_TTL_HOURS=24

qa_state()   { sed -n 's/^- state:[[:space:]]*//p'   "$1" | head -1; }
qa_started() { sed -n 's/^- started:[[:space:]]*//p' "$1" | head -1; }

# working | answered | superseded | no-state | unknown
qa_state_kind() {
  _qa_st=$(qa_state "$1")
  case "$_qa_st" in
    *superseded-by:*) printf 'superseded' ;;
    working*)         printf 'working' ;;
    answered*)        printf 'answered' ;;
    '')               printf 'no-state' ;;
    *)                printf 'unknown' ;;
  esac
}

# The `## Answer` body is EMPTY iff no non-blank line lives between `## Answer` and the
# next `##` heading. `state: answered` + an empty Answer = a LYING RECEIPT.
qa_answer_empty() {
  awk '
    /^##[[:space:]]/ { inans = ($0 ~ /^##[[:space:]]*Answer([[:space:]]|$)/) ? 1 : 0; next }
    inans { s = $0; gsub(/[[:space:]]/, "", s); if (s != "") body++ }
    END { exit (body + 0 > 0) ? 1 : 0 }
  ' "$1"
}

# The four BANK-side FAIL codes. Echoes a ";"-joined problem string, or nothing.
# `_qa_*` names throughout: sh has no locals, and PASS 1 calls these from INSIDE a
# read-loop whose own variables (f, state, target, ...) must not be clobbered.
qa_claim_problems() {
  _qa_f=$1; _qa_p=""; _qa_st=$(qa_state "$_qa_f")
  case "$_qa_st" in
    '')
      # `state:` is MANDATORY, always. Without it every check below is skipped, which is
      # how a LYING RECEIPT ships BY OMISSION -- drop one line and the tooth never bites.
      _qa_p="$_qa_p qa-no-state(no '- state:' line -- MANDATORY: working | answered | superseded-by:. The EXECUTOR that owns this file adds it);"
      ;;
  esac
  case "$_qa_st" in
    working*)
      # started: is MANDATORY on a working file. A claim that can never expire is not a
      # claim -- it is a zombie by construction, and every future reader defers to it forever.
      _qa_started=$(qa_started "$_qa_f")
      if [ -z "$_qa_started" ]; then
        _qa_p="$_qa_p qa-working-no-started(an UNEXPIRABLE claim);"
      else
        _qa_s=$(date -d "$_qa_started" +%s 2>/dev/null || echo 0)
        if [ "${_qa_s:-0}" -eq 0 ]; then
          # unparseable == unexpirable: same defect, same code.
          _qa_p="$_qa_p qa-working-no-started(unparseable started: '$_qa_started' -- want YYYY-MM-DDTHH:MM);"
        else
          _qa_age=$(( ( $(date +%s) - _qa_s ) / 3600 ))
          [ "$_qa_age" -ge "$QA_WORKING_TTL_HOURS" ] && \
            _qa_p="$_qa_p qa-working-expired(${_qa_age}h >= QA_WORKING_TTL_HOURS=${QA_WORKING_TTL_HOURS}: a ZOMBIE claim -- the next qa call may RESTART it);"
        fi
      fi
      ;;
  esac
  case "$_qa_st" in
    answered*)
      qa_answer_empty "$_qa_f" \
        && _qa_p="$_qa_p qa-answered-empty(state: answered with an EMPTY ## Answer -- a LYING RECEIPT);"
      ;;
  esac
  printf '%s' "$_qa_p"
}

fail=0
found=0

# ---------------------------------------------------------------------------
# PASS 1 -- probe files, section by section.
#
# awk splits each probe file into sections and emits ONE tab-separated record per
# section, plus one FILE record. Section parsing in pure sh is unreadable; awk does
# the walk, the shell does the two things awk cannot: resolve a path on disk and
# compare a date to today.
# ---------------------------------------------------------------------------
for probe in "$paper_root"/1-probes/PP*.md; do
  [ -e "$probe" ] || continue
  found=1
  name=${probe#"$paper_root"/}
  fprob=""

  # File-level: no markdown tables, no dead vocabulary.
  tables=$(grep -c '^|' "$probe")
  [ "$tables" -gt 0 ] && fprob="$fprob markdown-table(${tables}-lines: a probe holds SECTIONS);"

  # Dead vocabulary (R7 + R2): these belong to the retired card/gateway model.
  dead=$(grep -cEi '(^|[^a-z])verdicted([^a-z]|$)|^##[[:space:]]*Verdict|^##[[:space:]]*Takeaways|^[-[:space:]]*answers:|_ASK|_ANS[^A-Za-z]' "$probe")
  [ "$dead" -gt 0 ] && fprob="$fprob dead-vocab(${dead}-lines: verdicted/Verdict/Takeaways/answers:/_ASK/_ANS are DELETED);"

  # RETIRED old-format strings must not appear (constitution v9.5.0+). The stake now lives
  # in the stage-doc Q-consumer; the anatomy is `## QX<n>` entries with `###` subsections.
  stale=$(grep -cE '^[[:space:]]*-[[:space:]]*(serves|match|a-consumer):|^##[[:space:]]*Why([[:space:]]|$)' "$probe")
  [ "$stale" -gt 0 ] && fprob="$fprob stale-old-format(${stale}-lines: serves/match/a-consumer/## Why are RETIRED -- rewrite to the QX-entry format);"

  if [ -n "$fprob" ]; then
    echo "FAIL  $name  --$fprob"
    fail=1
  fi

  # Per-section records.
  awk -v FN="$name" -v SEP="$(printf '\037')" "$LEAK_AWK"'
    function flush(   leak) {
      if (qname == "") return
      leak = qx_claimid + qx_stage + qx_stake
      # US (\037) as the field separator, NOT tab: tab is IFS-WHITESPACE, so the shell
      # collapses consecutive tabs into one delimiter and every empty field (an absent
      # owner, an empty a-executor) silently SHIFTS the rest of the record. That shift is
      # invisible -- it produces confident wrong answers, not errors.
      printf "SEC%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s\n", \
        SEP, FN, SEP, qname, SEP, state, SEP, target, SEP, qconsumer, SEP, owner, SEP, eta, \
        SEP, blocks, SEP, xproj, SEP, (reading_nonempty ? "1" : "0"), SEP, owed+0, \
        SEP, leak+0, SEP, (has_qexec ? "1" : "0")
      qname=""; state=""; target=""; qconsumer=""; owner=""; eta=""; blocks=""; xproj=""
      reading_nonempty=0; owed=0; qx_claimid=0; qx_stage=0; qx_stake=0
      in_qexec=0; in_qcons=0; in_bank=0; in_aexec=0; has_qexec=0
    }
    # A new ENTRY: `## QX<n>` (the probe file is a list of q-executors).
    /^##[[:space:]]*QX/ { flush(); qname=$0; sub(/^##[[:space:]]*/, "", qname); next }
    qname == "" { next }

    # The four `###` subsections. Each switches context (and the `next` keeps the generic
    # `/^#/` closer below from immediately clobbering the flag we just set).
    /^###[[:space:]]*q-executor([[:space:]]|$)/            { in_qexec=1; in_qcons=0; in_bank=0; in_aexec=0; has_qexec=1; next }
    /^###[[:space:]]*q-consumer([[:space:]]|$)/            { in_qexec=0; in_qcons=1; in_bank=0; in_aexec=0; next }
    /^###[[:space:]]*bank[[:space:]]+binding([[:space:]]|$)/ { in_qexec=0; in_qcons=0; in_bank=1; in_aexec=0; next }
    /^###[[:space:]]*a-executor([[:space:]]|$)/            { in_qexec=0; in_qcons=0; in_bank=0; in_aexec=1; next }
    # any other heading closes every subsection.
    /^#/ { in_qexec=0; in_qcons=0; in_bank=0; in_aexec=0 }

    # `### bank binding` fields, written `**field**: value`.
    in_bank && /^[[:space:]]*\*\*state\*\*:/  { state=$0;  sub(/^.*\*\*state\*\*:[[:space:]]*/, "", state);  gsub(/[[:space:]].*$/, "", state) }
    in_bank && /^[[:space:]]*\*\*target\*\*:/ { target=$0; sub(/^.*\*\*target\*\*:[[:space:]]*/, "", target); sub(/[[:space:]]*$/, "", target) }
    in_bank && /\*\*owner\*\*:/ { owner=$0; sub(/^.*\*\*owner\*\*:[[:space:]]*/, "", owner); sub(/[[:space:]]*·.*$/, "", owner); sub(/[[:space:]]*$/, "", owner) }
    # No {n} intervals: mawk does not enable them by default, so spell the date out.
    in_bank && /\*\*eta\*\*:[[:space:]]*[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]/ {
      e=$0; sub(/^.*\*\*eta\*\*:[[:space:]]*/, "", e); sub(/[^0-9-].*$/, "", e); eta=e
    }
    in_bank && /\*\*blocks\*\*:/ { blocks="y" }
    in_bank && /\*\*cross-project\*\*:/ {
      x=$0; sub(/^.*\*\*cross-project\*\*:[[:space:]]*/, "", x); sub(/[[:space:]]*·.*$/, "", x)
      sub(/[[:space:]]*$/, "", x); xproj=x
    }
    in_bank && /harvest:[[:space:]]*OWED/ { owed++ }

    # `### q-consumer` bullets: the served stage-doc ids (+ each consumer'"'"'s copied
    # original question). The --stage gate greps these. They LEGITIMATELY carry claim ids
    # (the copied originals), so they are NEVER leak-scanned.
    in_qcons { qconsumer = qconsumer " " $0 }

    # LAW 2, surface 1: ONLY the `### q-executor` body crosses the wall -- scan it, and
    # nothing else. Shared pattern set (LEAK_AWK), identical to the bank lint in PASS 3.
    in_qexec {
      if (claim_leak($0))         qx_claimid++
      if (stage_leak($0, "comm")) qx_stage++
      if (stake_leak($0))         qx_stake++
    }

    # `### a-executor` body: non-empty iff the harvest happened (=> state read).
    in_aexec {
      r=$0; gsub(/[[:space:]]/, "", r)
      if (r != "" && r !~ /^#/) reading_nonempty=1
    }
    END { flush() }
  ' "$probe" > /tmp/.probe_sections.$$ 2>/dev/null

  while IFS="$(printf '\037')" read -r tag f qname state target qconsumer owner eta blocks xproj reading owed leak has_qexec; do
    [ "$tag" = "SEC" ] || continue
    owed=${owed:-0}; leak=${leak:-0}

    # --stage: an entry asserts at stage X's gate only if one of its `### q-consumer`
    # ids names stage X (e.g. `Q-Seed-1` -> seed). Trailing-s tolerant (claims -> Q-Claim).
    if [ -n "$stage_filter" ] && [ -n "$qconsumer" ]; then
      _stem=${stage_filter%s}
      if ! printf '%s' "$qconsumer" | grep -qiE "q-${_stem}"; then
        continue
      fi
    fi

    problems=""
    [ -z "$state" ] && problems="$problems no-state-field;"
    [ "$has_qexec" = "0" ] && [ "$state" != "answered-local" ] \
      && problems="$problems no-q-executor(the ### q-executor subsection is missing);"
    [ "$leak" -gt 0 ] && problems="$problems LAW2-q-executor-leak(${leak}: consumer vocab or stake disclosed);"
    [ "$owed" -gt 0 ] && problems="$problems harvest-owed(${owed}-lane);"

    case "$state" in
      read|answered-local)
        if [ -z "$target" ] || printf '%s' "$target" | grep -q '<'; then
          problems="$problems empty-target(state:$state);"
        else
          case "$target" in
            _WorkSpace/*)
              # _WorkSpace/ is gitignored and resolves under neither root, so this target can
              # never be checked, shared, or swept. Name the TASK that produced/scanned the
              # asset instead -- that lands the fact committed and sweepable. (JL C8-iii)
              problems="$problems workspace-target($target -> name the TASK that produced it);" ;;
            NEW\ *)
              problems="$problems unresolved-target(still NEW at state:$state);" ;;
            *)
              tgt=""
              if   [ -e "$project_root/$target" ]; then tgt="$project_root/$target"
              elif [ -e "$paper_root/$target" ];   then tgt="$paper_root/$target"
              fi
              if [ -z "$tgt" ]; then
                problems="$problems unresolved-target($target);"
              elif [ "$state" = "read" ]; then
                # R19/R20 -- OPEN THE TARGET AND READ ITS STATE LINE. Existence is no longer
                # enough: a QA file may exist and still be UNFINISHED (`working`) or STALE
                # (`superseded-by:`). Both are silent-false-claim bugs -- every file is
                # internally consistent, the paper's claim is FALSE, and before R19/R20
                # NOTHING fired. `answered-local` targets are the paper's OWN registries,
                # not QA files, so the `*/QA/*` guard leaves them alone.
                case "$target" in
                  */QA/*)
                    case "$(qa_state_kind "$tgt")" in
                      working)
                        problems="$problems read-target-working(target QA is state: working since $(qa_started "$tgt") -- an UNFINISHED answer: this section is commissioned, NOT read);" ;;
                      superseded)
                        problems="$problems read-target-superseded(target QA state line reads '$(qa_state "$tgt")' -- a STALE answer: re-point target: at the LIVE QA file and re-read);" ;;
                      no-state)
                        problems="$problems read-target-no-state(target QA carries NO '- state:' line -- the field is MANDATORY, and a stateless file may be an unfinished claim wearing no ticket. Its OWNER (the executor) must complete it);" ;;
                    esac ;;
                esac
              fi
              ;;
          esac
        fi
        [ "$state" = "read" ] && [ "$reading" = "0" ] \
          && problems="$problems read-with-empty-a-executor;"
        ;;
      answered)
        # The QA file landed but nobody interpreted it. The loop is not closed.
        problems="$problems answered-not-read(the QA file exists; copy it into the ### a-executor);"
        ;;
      commissioned)
        # THE BUILD-LANE FIELDS BELONG TO WHOEVER COMMISSIONED THE WORK -- NOT TO A SECTION
        # THAT MERELY JOINED A RUN SOMEONE ELSE STARTED. Resolve the target FIRST, then
        # decide who owes the deadline (see the in-flight carve-out below).

        # R19 OPENS AN IN-FLIGHT LOOP -- AND THIS CLOSES IT. Before R19, `commissioned` meant
        # "the task-folder exists, NO QA file yet", so the branch never had to open anything. Now the
        # MATCH->working path DELIBERATELY sets a section to `commissioned` with `target:`
        # pointing at a QA file that ALREADY EXISTS (the claim is written before the run
        # starts) -- and that path issues NO DISPATCH, so it has NO live return, EVER. Without
        # this test the section sits GREEN at `commissioned` from the moment the answer LANDS
        # until its eta expires (weeks), with no reading, no harvest, and a claim left
        # unsupported by evidence already on disk. The only other harvest tooth
        # (`answered-not-read`) fires only AFTER someone advanced the state -- which IS the
        # harvest step. That check is circular; this one is not.
        ctgt=""; ckind=""
        case "$target" in
          ''|*'<'*|NEW\ *|_WorkSpace/*) : ;;   # nothing resolvable to open
          */QA/*)
            if   [ -e "$project_root/$target" ]; then ctgt="$project_root/$target"
            elif [ -e "$paper_root/$target" ];   then ctgt="$paper_root/$target"
            fi
            [ -n "$ctgt" ] && ckind=$(qa_state_kind "$ctgt") ;;
        esac
        case "$ckind" in
          answered)
            problems="$problems commissioned-target-answered(the answer LANDED at $target -- HARVEST IT: copy it into the ### a-executor and flip the entry to state: read);" ;;
          superseded)
            problems="$problems commissioned-target-superseded(target QA state line reads '$(qa_state "$ctgt")' -- re-point target: at the LIVE QA file);" ;;
          no-state)
            problems="$problems commissioned-target-no-state($target carries NO '- state:' line -- MANDATORY; its OWNER (the executor) must complete it);" ;;
          # working -> PASS. This is the LEGITIMATE in-flight case: someone is answering the
          # question RIGHT NOW, and PASS 3's qa-working-expired is the TTL guard on it.
        esac

        # ACCOUNTABILITY LIVES IN EXACTLY ONE PLACE PER QUESTION.
        #   a `working` QA file exists  -> an EXECUTOR has CLAIMED this question, and its
        #     `started:` + QA_WORKING_TTL_HOURS IS the clock (PASS 3's qa-working-expired
        #     enforces it). This section did NOT start that run: it cannot honestly name an
        #     owner or an eta, and demanding one teaches people to INVENT data -- which is
        #     the very laundering the BUILD lane exists to prevent, inverted.
        #   no QA file yet             -> NOBODY has claimed the work. THIS section owes the
        #     deadline, and the BUILD-lane fields are mandatory.
        if [ "$ckind" = working ]; then
          : # IN-FLIGHT. The QA file's own claim is the deadline. Nothing owed here.
        else
        [ -z "$owner" ]  && problems="$problems commissioned-no-owner;"
        [ -z "$blocks" ] && problems="$problems commissioned-no-blocks;"
        [ -z "$xproj" ]  && problems="$problems commissioned-no-cross-project(path or 'none-found');"
        if [ -z "$eta" ]; then
          problems="$problems commissioned-no-eta(need YYYY-MM-DD);"
        else
          eta_s=$(date -d "$eta" +%s 2>/dev/null || echo 0)
          now_s=$(date +%s)
          if [ "$eta_s" -eq 0 ]; then
            problems="$problems commissioned-bad-eta($eta);"
          elif [ "$eta_s" -lt "$now_s" ]; then
            # SAY WHAT IS ACTUALLY ON DISK. "no QA file" was true by construction pre-R19 and
            # is now often a LIE: the in-flight path points `target:` at a file that has been
            # there for weeks. A misleading message at the gate people trust is how a real
            # FAIL gets muted.
            case "$ckind" in
              working)    cstate="state: working since $(qa_started "$ctgt")" ;;
              answered)   cstate="state: answered -- HARVEST IT" ;;
              superseded) cstate="SUPERSEDED -- re-point target:" ;;
              no-state)   cstate="present, but NO state line" ;;
              *)          cstate="absent" ;;
            esac
            problems="$problems commissioned-overdue(eta $eta, target $cstate);"
          fi
        fi
        fi
        ;;
      failed)
        problems="$problems state-failed(surface-it);"
        ;;
      planned)
        # A planned section at VERIFY or the CHECK gate means the probe was never run.
        problems="$problems state-planned(probe-not-run);"
        ;;
    esac

    if [ -n "$problems" ]; then
      echo "FAIL  $f :: $qname  --$problems"
      fail=1
    else
      echo "PASS  $f :: $qname  (state: ${state:-?})"
    fi
  done < /tmp/.probe_sections.$$
  rm -f /tmp/.probe_sections.$$
done

# Legacy locations: surfaced, never silently passed.
for legacy in "$paper_root"/1-probe-plans/PP*.md \
              "$paper_root"/0-lifecycle/*/_PROBE/PP*.md \
              "$paper_root"/0-lifecycle/*/*/_PROBE/PP*.md; do
  [ -e "$legacy" ] || continue
  echo "MIGRATE  ${legacy#"$paper_root"/}  -- pre-v8 location; ORGANIZE rewrites it into 1-probes/ on first touch"
done

# ---------------------------------------------------------------------------
# RESOURCE-STAGE PASS (paper-only; JL Q-not-PP ruling, 2026-07-14). Fires ONLY for
# `--stage resource`, and only on a paper that HAS a 1a-resource.md.
#
# The resource stage writes Q's and is FORBIDDEN to mint a PP id: the PROBE worker's
# ORGANIZE step opens one SECTION per GATE-1-approved Q, in a probe file under
# 1-probes/, and writes a `-> PP<NN>` backlink into 1a-resource.md. That backlink is
# the ONLY mechanical proof the question was ever ASKED -- so this is where it gets
# tested. Per Q<n> (its header line through the line before the next Q header)
# require exactly one of:
#
#   A:           the answer LANDED (answered | answered-local | scope-cut)
#   -> PP<NN>    ASKED; the probe file exists and its sections assert in PASS 1
#   DECLINED     the human said no at GATE 1 (logged in _LOG_1a-resource.md)
#
# A Q with NONE of the three is an UNASKED QUESTION: nothing was opened, nothing was
# dispatched -- and before this pass the gate went GREEN over it, because no section
# served the stage and PASS 1 had nothing to iterate. That is the VACUOUS GREEN. A
# backlink to a probe file that is not on disk is not proof either: it FAILs as a
# dangling backlink.
# ---------------------------------------------------------------------------
res_md="$paper_root/0-lifecycle/1a-resource/1a-resource.md"
res_log="$paper_root/0-lifecycle/1a-resource/_LOG_1a-resource.md"
res_open=0
if [ "$stage_filter" = "resource" ] && [ -f "$res_md" ]; then
  rname=${res_md#"$paper_root"/}
  rprob=""
  # One line per Q, in document order: "<qid> <answered:0|1> <PPNN|->".
  # `**` is stripped first, so `**Q1 (N1) -> PP12**` and a bare `Q1 ...` both parse.
  qtable=$(awk '
    { raw = $0; s = raw; gsub(/\*/, "", s); sub(/^[ \t]+/, "", s) }
    s ~ /^Q[0-9]+([^0-9]|$)/ {
      match(s, /^Q[0-9]+/); cur = substr(s, RSTART, RLENGTH)
      if (!(cur in seen)) { seen[cur] = 1; order[++n] = cur; ans[cur] = 0; pp[cur] = "-" }
    }
    cur != "" {
      if (s ~ /^A:/) ans[cur] = 1
      if (match(raw, /(->|→)[ \t]*PP[0-9]+/)) {
        tok = substr(raw, RSTART, RLENGTH); sub(/^.*PP/, "PP", tok); pp[cur] = tok
      }
    }
    END { for (i = 1; i <= n; i++) print order[i], ans[order[i]], pp[order[i]] }
  ' "$res_md")

  if [ -z "$qtable" ]; then
    echo "WARN  $rname  (no Q<n> questions -- resource DRAFT not written?)"
  fi

  oIFS=$IFS
  IFS='
'
  for row in $qtable; do
    IFS=$oIFS
    q=$(printf '%s' "$row" | awk '{print $1}')
    q_ans=$(printf '%s' "$row" | awk '{print $2}')
    q_pp=$(printf '%s' "$row" | awk '{print $3}')

    # DECLINED at GATE 1: the human said no out loud, in _LOG. Never opened,
    # never answered -- and it must not red the gate forever. Narrow exemption:
    # the Q id and the word DECLINED on the SAME _LOG line.
    if [ -f "$res_log" ] && grep -iE "\b${q}\b" "$res_log" | grep -qi 'declined'; then
      IFS='
'
      continue
    fi

    if [ "$q_ans" -eq 1 ]; then
      : # answered -- the A is the receipt
    elif [ "$q_pp" != "-" ]; then
      # asked. The backlink must resolve to a real probe file, or it is laundering.
      res_open=$((res_open + 1))
      c_hit=0
      for c in "$paper_root"/1-probes/"$q_pp"*.md \
               "$paper_root"/1-probe-plans/"$q_pp"*.md \
               "$paper_root"/0-lifecycle/*/_PROBE/"$q_pp"*.md; do
        [ -e "$c" ] && c_hit=1
      done
      [ "$c_hit" -eq 0 ] && rprob="$rprob dangling-backlink(${q} -> ${q_pp}, no probe file);"
    else
      # NEITHER an A nor a backlink: the stage never asked it.
      res_open=$((res_open + 1))
      rprob="$rprob unasked-question(${q});"
    fi
    IFS='
'
  done
  IFS=$oIFS

  if [ -n "$rprob" ]; then
    echo "FAIL  $rname  --$rprob"
    echo "      (every Q needs an A:, a -> PP<NN> backlink, or a DECLINED line in _LOG)"
    fail=1
  elif [ -n "$qtable" ]; then
    echo "PASS  $rname  (every Q answered, asked or declined)"
  fi
fi

if [ "$found" -eq 0 ]; then
  if [ -n "$stage_filter" ]; then
    if [ "$res_open" -gt 0 ]; then
      # THE VACUOUS GREEN, named. "No sections serve stage resource" is reassuring
      # and WRONG when the stage has open questions: it means nothing was opened.
      echo "FAIL  1-probes/  -- no entry serves stage 'resource' while ${res_open} question(s) are still open (vacuous green)"
      fail=1
    else
      echo "OK    no sections serve stage '$stage_filter' (other stages' probes were skipped, not failed)"
    fi
  else
    echo "WARN  no PP*.md probe files under $paper_root/1-probes/"
  fi
fi

# ---------------------------------------------------------------------------
# PASS 2 -- RETIRED 2026-07-19 (JL: no `_VALUES_` / `_CITATION_` sidecars; `1-probes/` is the
# ONLY consumer-side source of truth, and `_LOG` is the only kept sidecar). The old PASS 2
# checked those working docs for bibtex / tables; there are no such docs to check anymore.
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# PASS 3 -- THE BANK: LAW 2 (surface 2) + THE CLAIM'S OWN VALIDITY (R19).
#
# (a) LAW 2. QA files are the executor's own, written in GENERAL language, reusable by
#     every consumer. A QA file carrying a consumer's claim ids proves a consumer session
#     wrote in the bank (LAW 1 broken) and makes the evidence consumer-shaped (single-use).
#     SAME pattern set as the commission lint (LEAK_AWK) -- one rule, two surfaces.
# (b) THE CLAIM. A `working` file is a LIVE claim on a question, and every other reader
#     DEFERS to it -- so an invalid claim silently blocks the bank: no `started:` = it can
#     never expire; older than QA_WORKING_TTL_HOURS = the run that made it is dead. And an
#     `answered` file with an empty `## Answer` is a receipt for work nobody did.
#     SAME function block as the PASS-1 target test (QA_STATE) -- one rule, two surfaces.
# ---------------------------------------------------------------------------
for qa in "$project_root"/tasks/*/QA/*.md "$project_root"/tasks/*/*/QA/*.md \
          "$project_root"/discoveries/*/QA/*.md "$project_root"/discoveries/*/*/QA/*.md; do
  [ -e "$qa" ] || continue
  qname_f=${qa#"$project_root"/}
  qprob=""

  # A PP id in a bank filename is R2 broken: no PP id ever crosses to the bank.
  case "$(basename "$qa")" in
    *PP[0-9]*) qprob="$qprob pp-id-in-bank-filename(slug only);" ;;
  esac

  counts=$(awk "$LEAK_AWK"'
    { if (claim_leak($0) || stage_leak($0, "bank")) v++
      if (stake_leak($0)) k++ }
    END { print v+0, k+0 }
  ' "$qa")
  leak=$(printf '%s' "$counts" | awk '{print $1}')
  stake=$(printf '%s' "$counts" | awk '{print $2}')

  [ "${leak:-0}" -gt 0 ] && qprob="$qprob LAW2-consumer-vocab(${leak}-lines);"
  [ "${stake:-0}" -gt 0 ] && qprob="$qprob stake-disclosed(${stake}-lines);"

  # (b) the claim's own validity -- the SHARED QA_STATE block (same code PASS 1 runs).
  qprob="$qprob$(qa_claim_problems "$qa")"

  if [ -n "$qprob" ]; then
    echo "FAIL  $qname_f  --$qprob"
    case "$qprob" in
      *LAW2*|*stake-disclosed*|*pp-id-in-bank-filename*)
        echo "      (the bank is PROBE-UNAWARE: a QA file is general, reusable, and never speaks the consumer's vocabulary)" ;;
    esac
    case "$qprob" in
      *qa-working*|*qa-answered*|*qa-no-state*)
        echo "      (a QA file is a TICKET that becomes a RECEIPT: 'state:' is MANDATORY; 'working' needs a started: and expires after QA_WORKING_TTL_HOURS=${QA_WORKING_TTL_HOURS}h; 'answered' needs a real ## Answer. ONE WRITER: the EXECUTOR completes it -- never a consumer)" ;;
    esac
    fail=1
  else
    echo "PASS  $qname_f  (QA: probe-unaware · state: $(qa_state_kind "$qa"))"
  fi
done

# The RETIRED bank machinery. The bank is probe-unaware (R2): none of this may exist.
for dead_dir in "$project_root"/tasks/*/_ASK "$project_root"/tasks/*/*/_ASK \
                "$project_root"/discoveries/*/_ASK "$project_root"/discoveries/*/*/_ASK \
                "$project_root"/tasks/*/_ANS "$project_root"/tasks/*/*/_ANS \
                "$project_root"/discoveries/*/_ANS "$project_root"/discoveries/*/*/_ANS; do
  [ -e "$dead_dir" ] || continue
  echo "FAIL  ${dead_dir#"$project_root"/}  -- RETIRED mailbox (_ASK/_ANS are DEAD: the bank is probe-unaware, R2)"
  fail=1
done

echo "project_root: $project_root"
exit $fail
