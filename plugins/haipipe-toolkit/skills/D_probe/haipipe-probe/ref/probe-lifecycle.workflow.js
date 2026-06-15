export const meta = {
  name: 'haipipe-probe-lifecycle',
  description: 'Five-stage probe lifecycle with loop: Design → Materialize → Harvest → Judge → Insight. Two-mode Design (A: human, B: auto agents). DIKW cascade in Insight. Loop from Judge back to Design via Explore.',
  phases: [
    { title: 'Design', detail: 'Mode A: human writes probe.yaml; Mode B: idea-creator + idea-reviewer agents' },
    { title: 'Materialize', detail: 'bridge scaffolds arms as C_task tasks, code review, sanity arm, deploy' },
    { title: 'Harvest', detail: 'link runs + aggregate stats + write claim + structural review' },
    { title: 'Judge', detail: 'structural → integrity (Codex) → claim verdict (Codex); gates Insight' },
    { title: 'Insight', detail: 'DIKW cascade: D (per-arm) → I (cross-arm) → K (claim) → W (optional)' },
  ],
}

const parsed = typeof args === 'string' ? JSON.parse(args) : (args || {})
const project = parsed.project
if (!project) { log('probe-lifecycle: no project in args'); return { status: 'blocked', reason: 'missing project' } }
const probeRef = parsed.probe || null
const autoMode = !!parsed.auto
const interactiveOverride = !!parsed.interactive
const maxRounds = parsed.rounds || 4
const maxRetries = parsed.maxRetries || 2
log(`probe-lifecycle: project=${project}, probe=${probeRef || 'new'}, auto=${autoMode}, maxRounds=${maxRounds}`)

const SKILL_RESULT = {
  type: 'object', required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'blocked', 'failed', 'skipped'] },
    probe_id: { type: 'string' },
    probe_folder: { type: 'string' },
    summary: { type: 'string' },
    artifacts: { type: 'array', items: { type: 'string' } },
    next: { type: 'string' },
  }
}

const REVIEWER_RESULT = {
  type: 'object', required: ['verdict'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail', 'revise'] },
    issues: { type: 'array', items: { type: 'string' } },
    feedback: { type: 'string' },
  }
}

const IDEA_RESULT = {
  type: 'object', required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    probe_id: { type: 'string' },
    probe_folder: { type: 'string' },
    hypothesis: { type: 'string' },
    arms: { type: 'array', items: { type: 'string' } },
    summary: { type: 'string' },
  }
}

const AGGREGATE_RESULT = {
  type: 'object', required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'blocked', 'failed'] },
    result_status: { type: 'string', enum: ['confirmed', 'refuted', 'inconclusive', 'exploratory', 'pending'] },
    delta: { type: 'number' },
    p_value: { type: 'number' },
    N: { type: 'number' },
    summary: { type: 'string' },
  }
}

const REVIEW_RESULT = {
  type: 'object', required: ['verdict'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail'] },
    errors: { type: 'number' },
    warnings: { type: 'number' },
    issues: { type: 'array', items: { type: 'string' } },
  }
}

const INTEGRITY_RESULT = {
  type: 'object', required: ['verdict'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'warn', 'fail'] },
    categories: { type: 'object' },
  }
}

const CLAIM_VERDICT = {
  type: 'object', required: ['verdict', 'confidence'],
  properties: {
    verdict: { type: 'string', enum: ['yes', 'partial', 'no'] },
    confidence: { type: 'string', enum: ['high', 'medium', 'low'] },
    next_probes_needed: { type: 'array', items: { type: 'string' } },
  }
}

const CARD_RESULT = {
  type: 'object', required: ['status'],
  properties: {
    status: { type: 'string', enum: ['ok', 'skipped', 'failed'] },
    card_path: { type: 'string' },
    card_id: { type: 'string' },
  }
}

let currentProbeId = probeRef
let currentProbeFolder = probeRef ? `probes/${probeRef.replace('P.', '')}_unknown` : null
let round = 0
let finalVerdict = null
let loopLog = []

// ═══════════════════════════════════════════════════════════════════
// MAIN LOOP — stages 1-4 repeat until converged or budget exhausted
// ═══════════════════════════════════════════════════════════════════
while (round < maxRounds) {
  round++
  log(`\n═══ Round ${round}/${maxRounds} ═══`)

  // ─── Stage 1: DESIGN ─────────────────────────────────────────
  phase('Design')
  let designResult = null

  const useAutoDesign = (round > 1 || autoMode) && !interactiveOverride

  if (useAutoDesign) {
    log(`Design: Mode B (auto) — round ${round}`)
    let ideaFeedback = ''
    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      const retryNote = attempt > 0 ? `\n\nATTEMPT ${attempt + 1}. Reviewer feedback:\n${ideaFeedback}\nAddress these issues.` : ''

      const ideaResult = await agent(
        `Design Mode B: auto-generate a probe for project ${project}.\n\n` +
        `You are the probe-idea-creator. Generate a probe.yaml from coverage gaps.\n` +
        `1. Read probes/coverage.md and probes/propose.md for gap analysis\n` +
        `2. Read existing probes/*/probe.yaml to avoid duplicates\n` +
        `3. Read insights/K_knowledge/ and insights/W_wisdom/ for what we already know\n` +
        `4. Read D_probe/ref/probe-yaml-schema.md for field rules\n` +
        `5. Pick the highest-priority gap from the propose list\n` +
        `6. Write a falsifiable hypothesis + concrete arms + aggregation spec\n` +
        `7. Create the probe folder and probe.yaml via Skill("haipipe-probe-design", "new ...")\n\n` +
        `Return probe_id, probe_folder, hypothesis, arms.` + retryNote,
        { label: `design:idea-create:${attempt}`, phase: 'Design',
          agentType: 'probe-idea-creator-agent', schema: IDEA_RESULT }
      )

      if (!ideaResult || ideaResult.status !== 'ok') {
        log(`Design:idea-creator: ${ideaResult ? ideaResult.status : 'null'} — stopping`)
        designResult = ideaResult
        break
      }

      const ideaReview = await agent(
        `Design Mode B: review the auto-generated probe idea.\n\n` +
        `Probe: ${ideaResult.probe_id || 'unknown'}\n` +
        `Hypothesis: ${ideaResult.hypothesis || 'unknown'}\n` +
        `Arms: ${(ideaResult.arms || []).join(', ')}\n\n` +
        `Check:\n` +
        `1. Is the hypothesis falsifiable? (not tautological)\n` +
        `2. Is this NOT already answered by an existing confirmed/refuted probe?\n` +
        `3. Are arms well-defined? (baseline exists, treatment is one variable change)\n` +
        `4. Is N≥3 planned for statistical claims?\n` +
        `5. Is it worth the compute cost vs expected information value?\n\n` +
        `Return verdict: pass, revise (with feedback), or fail (duplicate/unfalsifiable).`,
        { label: `design:idea-review:${attempt}`, phase: 'Design',
          agentType: 'probe-idea-reviewer-agent', schema: REVIEWER_RESULT }
      )

      log(`Design: attempt=${attempt}, creator=${ideaResult.status}, reviewer=${ideaReview ? ideaReview.verdict : 'null'}`)

      if (!ideaReview || ideaReview.verdict === 'pass') {
        designResult = ideaResult
        break
      }
      if (ideaReview.verdict === 'fail') {
        log('Design: idea-reviewer rejected — probe unfalsifiable or duplicate')
        designResult = { status: 'failed', summary: 'idea rejected: ' + (ideaReview.feedback || 'unfalsifiable/duplicate') }
        break
      }
      if (ideaReview.verdict === 'warn' && attempt > 0) {
        designResult = ideaResult
        break
      }
      ideaFeedback = (ideaReview.feedback || (ideaReview.issues || []).join('; ')) + '\nFix the issues above.'
    }
  } else {
    log(`Design: Mode A (interactive) — round ${round}`)
    const probeNote = currentProbeId ? `Existing probe: ${currentProbeId}. Update if needed.` : 'New probe. Design from research question.'
    designResult = await agent(
      `Stage: DESIGN (Mode A: interactive). Project: ${project}. ${probeNote}\n\n` +
      `Create or validate probe.yaml:\n` +
      `1. Read D_probe/ref/probe-yaml-schema.md for field rules\n` +
      `2. Read existing probes/ for context (coverage, existing claims)\n` +
      `3. Interactively define: hypothesis, claim_target, arms, aggregation spec\n` +
      `4. Write probe.yaml in the probe folder\n` +
      `5. Validate: id matches folder date, arms ≥1, aggregation.metric non-empty`,
      { label: 'design:interactive', phase: 'Design', schema: SKILL_RESULT }
    )
  }

  if (!designResult || designResult.status === 'failed') {
    log(`Design: ${designResult ? designResult.status : 'null'} — stopping loop`)
    loopLog.push({ round, stage: 'Design', status: 'failed' })
    break
  }

  currentProbeId = designResult.probe_id || currentProbeId
  currentProbeFolder = designResult.probe_folder || currentProbeFolder
  log(`Design: probe=${currentProbeId}, folder=${currentProbeFolder}`)

  // ─── Stage 2: MATERIALIZE ────────────────────────────────────
  phase('Materialize')

  const bridgeResult = await agent(
    `Stage: MATERIALIZE. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `Scaffold arms as C_task tasks and deploy:\n` +
    `1. Read probe.yaml arms and run_specs\n` +
    `2. For each arm × seed: Skill("haipipe-task", "task-folder <task_type> ...")\n` +
    `3. Wire configs/<run>.yaml from run_spec params\n` +
    `4. Code review each scaffolded task (Run Script Reviewer agent)\n` +
    `5. Sanity arm first (smallest arm, verify exit_code + metrics.json)\n` +
    `6. Deploy remaining arms\n` +
    `7. Link completed run-paths into probe.yaml arms[].runs[]\n\n` +
    `Bridge is the ONLY path where D_probe creates C_task artifacts.`,
    { label: 'materialize:bridge', phase: 'Materialize', schema: SKILL_RESULT }
  )

  let bridgeReview = null
  if (bridgeResult && bridgeResult.status === 'ok') {
    bridgeReview = await agent(
      `Stage: MATERIALIZE review. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
      `Code review the scaffolded tasks:\n` +
      `1. Read each arm's task folder: configs/, runs/, *.py\n` +
      `2. Check intent-vs-implementation match (probe hypothesis vs task code)\n` +
      `3. Verify configs have _meta.git_sha and match across arms\n\n` +
      `Return verdict: pass, warn, revise, fail.`,
      { label: 'materialize:review', phase: 'Materialize',
        agentType: 'haipipe-task-reviewer-agent', schema: REVIEWER_RESULT }
    )
    log(`Materialize: bridge=${bridgeResult.status}, review=${bridgeReview ? bridgeReview.verdict : 'null'}`)
  } else {
    log(`Materialize: bridge=${bridgeResult ? bridgeResult.status : 'null'} — stopping`)
    loopLog.push({ round, stage: 'Materialize', status: 'failed' })
    break
  }

  // ═══ C_task handoff: D_probe is asleep while C_task runs ═══
  // In auto mode, the bridge deploys and waits for completion.
  // In manual mode, the user runs tasks externally.

  // ─── Stage 3: HARVEST ────────────────────────────────────────
  phase('Harvest')

  const harvestResult = await agent(
    `Stage: HARVEST. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `Link runs, aggregate stats, and write claim:\n` +
    `1. Verify all arms have linked runs in probe.yaml\n` +
    `2. For each arm, for each run: read results/<RUN>/metrics.json\n` +
    `3. Extract aggregation.metric value (scalar or {point, ci_lower, ci_upper})\n` +
    `4. Compute statistic per aggregation spec (mean_std_paired_t, sign_test, etc.)\n` +
    `5. Determine result.status: confirmed|exploratory|inconclusive|refuted\n` +
    `6. Write result: block in probe.yaml\n` +
    `7. Walk ref/probe-caveats-checklist.txt → fill caveats[]\n` +
    `8. Compose claim sentence from claim_target + result + caveats\n` +
    `9. Write claim: field in probe.yaml`,
    { label: 'harvest:aggregate-claim', phase: 'Harvest', schema: AGGREGATE_RESULT }
  )

  let harvestReview = null
  if (harvestResult && harvestResult.status === 'ok') {
    harvestReview = await agent(
      `Stage: HARVEST review. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
      `Structural check on the result:\n` +
      `- arms paired, equal N\n` +
      `- N≥3 for statistical claims (else mark exploratory)\n` +
      `- git_sha consistent across arms\n` +
      `- AIData version consistent\n` +
      `- caveats cover detectable confounds\n` +
      `- if confirmed: p<0.05 AND |Δ|>noise_floor\n\n` +
      `Return verdict: pass, warn, fail.`,
      { label: 'harvest:structural', phase: 'Harvest',
        agentType: 'probe-structural-reviewer-agent', schema: REVIEW_RESULT }
    )
    log(`Harvest: result_status=${harvestResult.result_status}, Δ=${harvestResult.delta}, p=${harvestResult.p_value}, review=${harvestReview ? harvestReview.verdict : 'null'}`)
  } else {
    log(`Harvest: ${harvestResult ? harvestResult.status : 'null'} — stopping`)
    loopLog.push({ round, stage: 'Harvest', status: 'failed' })
    break
  }

  // ─── Stage 4: JUDGE ──────────────────────────────────────────
  phase('Judge')

  // Gate 1: integrity (Codex)
  const integrityResult = await agent(
    `Stage: JUDGE — integrity audit. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `Codex-backed fraud-pattern audit (5 categories):\n` +
    `A. Ground-truth provenance\n` +
    `B. Metric-definition consistency\n` +
    `C. Phantom results\n` +
    `D. Scope-language mismatch\n` +
    `E. Individual/split leakage\n\n` +
    `Collect file PATHS only; Codex reads and judges.\n` +
    `Write INTEGRITY_AUDIT.md in the probe folder.`,
    { label: 'judge:integrity', phase: 'Judge',
      agentType: 'probe-integrity-auditor-agent', schema: INTEGRITY_RESULT }
  )
  log(`Judge:integrity: ${integrityResult ? integrityResult.verdict : 'null'}`)

  if (integrityResult && integrityResult.verdict === 'fail') {
    log('Judge: integrity=fail — claim verdict refused, stopping')
    finalVerdict = 'no'
    loopLog.push({ round, stage: 'Judge', integrity: 'fail', verdict: 'blocked' })
    break
  }

  // Gate 2: claim verdict (Codex)
  const capNote = (integrityResult && integrityResult.verdict === 'warn')
    ? '\n\nINTEGRITY=WARN: cap confidence ≤ medium.'
    : ''
  const claimVerdict = await agent(
    `Stage: JUDGE — claim verdict. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `Codex-backed semantic verdict: does the evidence support the intended claim?\n` +
    `Read probe.yaml (claim_target + result + claim) and INTEGRITY_AUDIT.md.\n` +
    `Return: yes|partial|no + confidence + what is/isn't supported + next_probes_needed.\n` +
    `Write CLAIMS_FROM_RESULTS.md in the probe folder.` + capNote,
    { label: 'judge:claim-verdict', phase: 'Judge',
      agentType: 'claim-verifier-agent', schema: CLAIM_VERDICT }
  )
  log(`Judge:claim: verdict=${claimVerdict ? claimVerdict.verdict : 'null'}, confidence=${claimVerdict ? claimVerdict.confidence : 'null'}`)

  finalVerdict = claimVerdict ? claimVerdict.verdict : 'no'
  loopLog.push({
    round,
    harvest_status: harvestResult ? harvestResult.result_status : null,
    harvest_review: harvestReview ? harvestReview.verdict : null,
    integrity: integrityResult ? integrityResult.verdict : null,
    claim_verdict: finalVerdict,
  })

  // ── Verdict check: converge or loop ──
  if (finalVerdict === 'yes') {
    log(`Judge: verdict=yes — converged at round ${round}, proceeding to Insight`)
    break
  }

  // verdict = partial/no → Explore → loop back to Design
  log(`Judge: verdict=${finalVerdict} — exploring for next probe`)

  const exploreResult = await agent(
    `Loop-back: Explore. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `The claim verdict was "${finalVerdict}". Propose next probes:\n` +
    `1. Build coverage map across all probes in the project\n` +
    `2. Identify gaps: unconfirmed single-seed runs, missing baselines, untested axes\n` +
    `3. Factor in claim-verifier's next_probes_needed suggestions\n` +
    `4. Rank proposals by: information value > cost > risk\n` +
    `5. Output top 3-5 proposals with rationale\n\n` +
    `Write probes/coverage.md and probes/propose.md.`,
    { label: `explore:round${round}`, phase: 'Judge',
      agentType: 'probe-explorer-agent', schema: SKILL_RESULT }
  )
  log(`Explore: ${exploreResult ? exploreResult.status : 'null'}`)

  if (round >= maxRounds) {
    log(`Budget exhausted: ${round}/${maxRounds} rounds without converging`)
    break
  }

  // Next round will pick up in Design (Mode B if auto, Mode A if interactive)
  log(`Looping back to Design for round ${round + 1}...`)
}

// ═══════════════════════════════════════════════════════════════════
// Stage 5: INSIGHT — DIKW cascade (only on convergence)
// ═══════════════════════════════════════════════════════════════════
let insightCards = { d: [], i: null, k: null, w: null }

if (finalVerdict !== 'yes') {
  log(`Insight: skipped — verdict=${finalVerdict} (not converged)`)
} else {
  phase('Insight')

  // Step 1: 🟦 D_data — per-arm observations
  log('Insight Step 1: filing D_data cards per arm')
  const probeArmsNote = `Read probe.yaml for ${currentProbeId} to get the arm list and their linked runs.`
  const dCards = await agent(
    `Stage: INSIGHT — D_data. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `File one D_data observation card per arm:\n` +
    `${probeArmsNote}\n` +
    `For each arm:\n` +
    `1. Read the arm's linked run results (metrics.json via C_task I cards if available, else directly)\n` +
    `2. Record per-arm observations: mean, std, N, key metric values\n` +
    `3. File via Skill("haipipe-insight-data") with source_id pointing to this probe + arm\n` +
    `4. Pure observations — NO interpretation, NO claims\n\n` +
    `Return the list of D card paths created.`,
    { label: 'insight:d-data', phase: 'Insight',
      agentType: 'card-creator-data-agent', schema: SKILL_RESULT }
  )

  if (dCards && dCards.status === 'ok') {
    const dReview = await agent(
      `Review D_data cards just filed for probe ${currentProbeId}.\n` +
      `Check: every number traces to metrics.json, no interpretation leaked, format correct.\n` +
      `Cards: ${(dCards.artifacts || []).join(', ')}`,
      { label: 'insight:d-review', phase: 'Insight',
        agentType: 'card-reviewer-data-agent', schema: REVIEWER_RESULT }
    )
    log(`Insight:D: ${dCards.status}, review=${dReview ? dReview.verdict : 'null'}`)
    insightCards.d = dCards.artifacts || []
  }

  // Step 2: 🟩 I_information — cross-arm patterns
  if (insightCards.d.length >= 2) {
    log('Insight Step 2: filing I_information card (cross-arm patterns)')
    const iCard = await agent(
      `Stage: INSIGHT — I_information. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
      `File one I_information card synthesizing cross-arm patterns:\n` +
      `1. Read the D_data cards just filed: ${insightCards.d.join(', ')}\n` +
      `2. Identify patterns: which arm wins/loses, consistency across seeds, margin trends\n` +
      `3. File via Skill("haipipe-insight-information")\n` +
      `4. Cross-observation patterns — NOT claims, NOT recommendations`,
      { label: 'insight:i-info', phase: 'Insight',
        agentType: 'card-creator-information-agent', schema: CARD_RESULT }
    )

    if (iCard && iCard.status === 'ok') {
      const iReview = await agent(
        `Review I_information card for probe ${currentProbeId}.\n` +
        `Check: pattern is actually visible in the cited D cards, direction matches, counter-evidence not omitted.\n` +
        `Card: ${iCard.card_path || 'unknown'}`,
        { label: 'insight:i-review', phase: 'Insight',
          agentType: 'card-reviewer-information-agent', schema: REVIEWER_RESULT }
      )
      log(`Insight:I: ${iCard.status}, review=${iReview ? iReview.verdict : 'null'}`)
      insightCards.i = iCard.card_id || iCard.card_path
    }
  } else {
    log('Insight:I: skipped — need ≥2 D cards for cross-arm patterns')
  }

  // Step 3: 🟨 K_knowledge — validated belief
  log('Insight Step 3: filing K_knowledge card (validated claim)')
  const kCard = await agent(
    `Stage: INSIGHT — K_knowledge. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
    `File one K_knowledge card from the confirmed claim:\n` +
    `1. Read probe.yaml claim: field + result: block + caveats:\n` +
    `2. Read I_information card if available: ${insightCards.i || 'none'}\n` +
    `3. Read CLAIMS_FROM_RESULTS.md for the Codex verdict context\n` +
    `4. File the probe's claim as a validated belief\n` +
    `5. Scope must ⊆ evidence; no overclaim`,
    { label: 'insight:k-knowledge', phase: 'Insight',
      agentType: 'card-creator-knowledge-agent', schema: CARD_RESULT }
  )

  if (kCard && kCard.status === 'ok') {
    const kReview = await agent(
      `Review K_knowledge card for probe ${currentProbeId}.\n` +
      `Check: claim scope ⊆ cited evidence, ALL counter-evidence listed, confidence justified,\n` +
      `source chain traces to a CONFIRMED probe.\n` +
      `Card: ${kCard.card_path || 'unknown'}`,
      { label: 'insight:k-review', phase: 'Insight',
        agentType: 'card-reviewer-knowledge-agent', schema: REVIEWER_RESULT }
    )
    log(`Insight:K: ${kCard.status}, review=${kReview ? kReview.verdict : 'null'}`)
    insightCards.k = kCard.card_id || kCard.card_path
  }

  // Step 4: 🟧 W_wisdom — actionable recommendation (optional)
  if (insightCards.k) {
    log('Insight Step 4: filing W_wisdom card (optional)')
    const wCard = await agent(
      `Stage: INSIGHT — W_wisdom. Project: ${project}. Probe: ${currentProbeId}.\n\n` +
      `File one W_wisdom card — the actionable next step from this probe:\n` +
      `1. Read K card: ${insightCards.k}\n` +
      `2. Derive a concrete, actionable recommendation\n` +
      `3. Must pass the "could I write the exact command?" test\n` +
      `4. SKIP if the probe implies no concrete next step (return status: skipped)\n` +
      `5. File via card-creator-wisdom-agent`,
      { label: 'insight:w-wisdom', phase: 'Insight',
        agentType: 'card-creator-wisdom-agent', schema: CARD_RESULT }
    )

    if (wCard && wCard.status === 'ok') {
      const wReview = await agent(
        `Review W_wisdom card for probe ${currentProbeId}.\n` +
        `Check: recommendation follows from cited K, is actionable (could write the exact command).\n` +
        `Card: ${wCard.card_path || 'unknown'}`,
        { label: 'insight:w-review', phase: 'Insight',
          agentType: 'card-reviewer-wisdom-agent', schema: REVIEWER_RESULT }
      )
      log(`Insight:W: ${wCard.status}, review=${wReview ? wReview.verdict : 'null'}`)
      insightCards.w = wCard.card_id || wCard.card_path
    } else {
      log(`Insight:W: ${wCard ? wCard.status : 'null'} (skipped or failed — acceptable)`)
    }
  }

  // Final: cross-ref integrity audit
  const indexAudit = await agent(
    `Stage: INSIGHT — index integrity. Project: ${project}.\n\n` +
    `Audit the cross-reference graph in insights/:\n` +
    `- sources↔ref_by symmetry\n` +
    `- id↔layer match\n` +
    `- no dangling ids\n` +
    `- INDEX.md consistent with files on disk`,
    { label: 'insight:index-audit', phase: 'Insight',
      agentType: 'index-integrity-auditor-agent', schema: REVIEWER_RESULT }
  )
  log(`Insight:index-audit: ${indexAudit ? indexAudit.verdict : 'null'}`)
}

// ─── Output ────────────────────────────────────────────────────
const converged = finalVerdict === 'yes'
return {
  probe_id: currentProbeId,
  probe_folder: currentProbeFolder,
  project: project,
  converged: converged,
  rounds: round,
  max_rounds: maxRounds,
  final_verdict: finalVerdict,
  loop_log: loopLog,
  insight_cards: converged ? insightCards : null,
  status: converged ? 'converged' : (round >= maxRounds ? 'budget_exhausted' : 'blocked'),
}
