"""
Reference template — Intent-bearing docstring for a C_task run script.

Convention: half-fixed (option b).
  - Mandatory: top-of-file module docstring with an `Intent` section.
  - Mandatory: at least one bullet under Intent.
  - Free-form: any other sections you like (Confounds / Inputs /
    Outputs / Notes / References / etc.).

The Task Reviewer agent (Tools/plugins/haipipe-toolkit/skills/C_task/agents/haipipe-task-reviewer-agent.md)
reads this docstring as the authoritative "what this script is supposed to do"
and compares it against the actual code. If Intent is missing, review fails
hard — the writer must state intent before any review can run.

Below: one good example, one bad example.
"""


# ========================================================================
# GOOD example
# ========================================================================
GOOD_EXAMPLE = '''
"""
LHM-A: substitution-with-noise pretraining for next-2h CGM forecast.

Intent
------
- Pretrain target: only the horizon bins [288:312] (B92-style); positions
  [1:288] are prompt and MUST NOT receive substitution noise.
- SS noise scope: ONLY horizon positions. Loss is also computed ONLY on
  horizon — prompt positions contribute zero gradient.
- Backbone: TE-CLM with embedding frozen; only the LHM head trains.
- Eval horizon: bins [288:312] (next 2h, post-event dynamic).

Confounds declared
------------------
- +20% params vs baseline (param-matched re-test pending) — caveat ⚠️.
- Same AIData v3 across arms; same training schedule. Only architecture varies.

Inputs / Outputs
----------------
- Input AIData:  PretrainCGM_Stride4H @v0002_WellReadi_tewindow (Samsung)
- Output:        results/<RUN>/{metrics.json, runtime.yaml, checkpoints/}

References
----------
- B92 paper: <link or repo path>
- Prior failure mode: SS noise applied to full input [1:L]; see
  project_lhm_ss_scope_bug memory.
"""

import torch
# ... rest of script
'''


# ========================================================================
# BAD example — agent will FAIL this with category `no-intent-declared`
# ========================================================================
BAD_EXAMPLE_1 = '''
"""LHM-A training script."""

import torch
# ... rest of script
'''


# ========================================================================
# BAD example — has docstring but no `Intent` section header
# ========================================================================
BAD_EXAMPLE_2 = '''
"""
LHM-A: substitution-with-noise pretraining.

This script does pretraining on CGM data with SS noise and outputs
checkpoints to results/.

Run with: bash runs/<NAME>.sh
"""

import torch
# ... rest of script
'''


# ========================================================================
# Quick reference for new scripts — copy this stub to the top of your .py
# ========================================================================
STUB = '''
"""
<one-line description of what this script does>

Intent
------
- <intent bullet 1 — be specific about what behavior you're claiming>
- <intent bullet 2>
- ...

<optional sections below — free-form>
Confounds declared
------------------
- ...

Inputs / Outputs
----------------
- ...
"""
'''
