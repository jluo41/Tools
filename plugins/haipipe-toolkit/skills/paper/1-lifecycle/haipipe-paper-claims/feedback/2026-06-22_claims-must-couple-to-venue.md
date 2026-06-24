---
status: fixed
created: 2026-06-22
context: haipipe-paper-claims / claims stage; felt on Paper-Personality-Opioid-MedJournal deciding the core claim for JAMA Internal Medicine
fixed_in: "haipipe-paper-claims v1.2.0"
---
我们这 llm 出来的东西 肯定不能是方法，因为我们已经有其他的论文在做这件事了。这里肯定以 clinical 为主，所以在这里我感觉 claims 应该要和 venue 挂钩。把这个加入到 feedback 吧

Distilled ask:
- The claim ledger must be COUPLED TO THE TARGET VENUE. The same evidence base yields different headline claims for different venues; the ledger should designate a PRIMARY (load-bearing) claim aligned to what the venue rewards and demote the rest to SUPPORTING.
- A claim's role (primary / supporting / out-of-scope) is venue-dependent. The same result can be the contribution at one venue and merely an enabler at another. Concretely: an LLM-derived measurement is the contribution at an informatics/IS venue, but NOT a contribution at a clinical venue (JAMA Internal Medicine) when other papers already own that method — there it is just the enabling method, and the CLINICAL finding is the contribution.
- The current claims stage lists claims with status (supported / weak / GAP) but does NOT tie them to the venue or mark a venue-primary claim, so all claims read as co-equal.

Why this matters:
- Which claim leads is the single most consequential framing decision, and it is venue-specific. Without venue coupling, the ledger, pitch thesis, narrative, and display emphasis can foreground the wrong contribution (e.g. a method that is novel elsewhere but old-news to this venue's readers).

Proposed solution:
1. claims stage reads STATUS `venue` (+ pitch Audience/Venue Fit) and adds a venue-coupling step: designate PRIMARY claim(s) for the venue, mark the rest SUPPORTING, and name the leading frame (clinical / method / policy).
2. Record each claim's role as venue-dependent; explicitly flag when a claim that is "novel/contribution" for one venue is "already done elsewhere / enabler only" for this one.
3. The designated primary claim then DRIVES the pitch thesis, the narrative arc, and which display gets hero status. A venue change re-runs this designation.
4. STATUS could carry a one-line "venue + primary claim" so a session loader sees the spine immediately.

Where it touches:
- haipipe-paper-claims: add a "couple to venue → designate primary/supporting" step and a primary marker in the ledger matrix.
- ties to STATUS `venue`, pitch Audience/Venue Fit, narrative, and display hero selection.

Structural home (checked 2026-06-22): the skill tree ALREADY splits venue cleanly, so do NOT relocate venue:
- `skills/0_venue/<venue>-playbook` = venue KNOWLEDGE (what the venue rewards, article-type, format, contribution-vs-enabler criteria), cross-family, reusable. This is where "what claim leads for venue X" belongs. (existing: nature-portfolio, pnas, misq, isr, ms-is, grant, patent...)
- `skills/paper/_venue/haipipe-paper-{conference,journal,is}` = paper WORKFLOW routers per venue, which should CONSULT the 0_venue playbook.
- STRUCTURE.md already labels `0_*` as "venue playbooks".

Resolution: (1) each 0_venue playbook states the venue's contribution criteria / primary-claim rule; (2) haipipe-paper-claims consults it to designate the venue-primary claim; (3) the journal/conference/is router routes to the right playbook.

Gaps found (the real work):
- NO clinical-medicine / JAMA(-Internal-Medicine) playbook in 0_venue. Existing nature-portfolio + pnas are BASIC science, misq/isr are IS; clinical medicine is unrepresented, yet it is the target venue of Paper-Personality-Opioid-MedJournal.
- `haipipe-paper-journal` DEFAULTS to Nature-portfolio (basic science); a clinical journal would mis-route to basic-science framing. Needs a clinical-medicine branch.
- claims stage does not yet consult any venue playbook.

Sharpened (2026-06-22, user): "当我们选择 claim 的时候，一定要先选好 venue" — venue
selection must come FIRST, before selecting/ordering claims. Venue is a PREREQUISITE
to the claims stage, not a parallel concern: lock the venue (at seed/pitch, recorded
in STATUS `venue`) and confirm it before the claims stage runs, because the venue
decides which claim is primary and what counts as a contribution vs an enabler.
Implication: the lifecycle should GATE the claims stage on a confirmed venue (+ its
0_venue playbook consulted); do not let claim selection proceed venue-blind. Concretely:
add a "venue confirmed?" precondition to haipipe-paper-claims (and surface it in the
seed/pitch gates), so reaching claims without a venue is flagged.

Fix:
