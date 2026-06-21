# Toy Walkthrough

This is a fake example that shows the full flow.

## Starting Point

Assume a project has a completed probe:

```text
examples/ProjToy/
  probes/
    P001_model_ood/
      probe.yaml
      CLAIMS_FROM_RESULTS.md
      review.md
  insights/
    INDEX.md
    D_data/
    I_information/
    K_knowledge/
    W_wisdom/
```

The probe says:

```text
Claim: The new model improves validation accuracy but does not improve OOD accuracy.
Verdict: confirmed with caveat.
Caveat: only tested on one OOD split.
```

## Step 1: Review The Probe

Run:

```bash
/haipipe-insight review examples/ProjToy/probes/P001_model_ood
```

The review step asks:

```text
What here is worth keeping as a permanent card?
Is it already represented in insights/?
Should it be D, I, K, or W?
Should it file a new card, update an old card, or skip?
```

It writes:

```text
examples/ProjToy/probes/P001_model_ood/INSIGHT_REVIEW.yaml
```

## Step 2: Read The Review Checklist

The checklist may propose:

```text
C1: file K card
    "Validation gain does not transfer to OOD"

C2: file W card
    "Do not use validation gain as OOD evidence"

C3: skip raw run note
    "already covered by task logs"
```

At this point, no permanent cards have been written yet.

## Step 3: Apply The Checklist

Run:

```bash
/haipipe-insight apply examples/ProjToy/probes/P001_model_ood/INSIGHT_REVIEW.yaml
```

Apply writes accepted items into:

```text
examples/ProjToy/insights/K_knowledge/
examples/ProjToy/insights/W_wisdom/
```

It also rebuilds:

```text
examples/ProjToy/insights/INDEX.md
examples/ProjToy/insights/views/
```

## Step 4: Future Work Cites Cards

A later narrative can cite:

```text
K03: Validation gain does not transfer to OOD.
W02: Do not use validation gain as OOD evidence.
```

The narrative does not need to reread the whole probe folder. It can cite the
stable insight cards.
