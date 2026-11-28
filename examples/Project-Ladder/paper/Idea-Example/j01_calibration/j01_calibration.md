# j01_calibration · Calibration under shift

goal: Does recalibration reduce prediction error after a population shift without retraining the predictor?
close: The named deliverables are reviewed against their acceptance conditions.

bands: t0N Framing · t1N Assessment · t2N Decision
emoji: 💡

## Topic

Does recalibration reduce prediction error after a population shift without retraining the predictor?

The candidate is a hypothesis for this example. Recalibration may reduce calibration error on a shifted test population while preserving discrimination.

**Method:** Freeze a predictor; fit calibration on a separate sample; compare locked calibration and discrimination metrics on an untouched shifted test set.

**Minimum experiment:** A held-out comparison with and without recalibration across two prespecified shifts.

[Canonical Card](cards/i01_idea.yaml) · [Evidence pointers](bundle/evidence-bundle.yaml) · [Working projection](projection/paper-ideation-sync.yaml)

A null or reversed comparison would narrow or reject the claim. Novelty, feasibility and target fit require the assessment Tasks below.

## Tasks

1. t01_falsifiable_claim · Falsifiable claim
2. t11_closest_work · Closest-work comparison
3. t12_minimum_experiment · Minimum experiment

