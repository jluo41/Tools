# j02_missingness · Missing-input robustness

goal: Does masking inputs during training preserve prediction quality when deployment observations are missing?
close: The named deliverables are reviewed against their acceptance conditions.

bands: t0N Framing · t1N Assessment · t2N Decision
emoji: 💡

## Topic

Does masking inputs during training preserve prediction quality when deployment observations are missing?

The candidate is a hypothesis for this example. Training with a declared masking mechanism may reduce performance degradation under the same deployment missingness mechanism.

**Method:** Declare missingness mechanisms; compare unmasked and masked training; evaluate on fixed incomplete test data.

**Minimum experiment:** A small controlled comparison across random and structured missingness, reporting degradation rather than claiming universal robustness.

[Canonical Card](cards/i02_idea.yaml) · [Evidence pointers](bundle/evidence-bundle.yaml) · [Working projection](projection/paper-ideation-sync.yaml)

A null or reversed comparison would narrow or reject the claim. Novelty, feasibility and target fit require the assessment Tasks below.

## Tasks

1. t01_missingness_boundary · Missingness boundary
2. t11_stress_test_design · Stress-test design

