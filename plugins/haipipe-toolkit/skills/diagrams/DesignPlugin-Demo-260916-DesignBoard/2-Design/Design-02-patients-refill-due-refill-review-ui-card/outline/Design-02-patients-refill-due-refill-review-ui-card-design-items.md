# Refill review app card for patients with a refill due within 7 days · Design Items

One block per design target: the bet, its evidence, and its acceptance rules.
Runs name an item through `item:`; state is derived from those Runs, never typed here.

## ITEM01 · Refill approaching card
type: ui-card
audience: patients with a refill due within 7 days
job: refill review
goal: Make the refill date and the one next action visible at a glance
stance: generate
basis: brief-only
mode: compose
acceptance:
- shows the refill date placeholder {REFILL_DATE}
- exactly one action: 'Review options'
- fits a 320px card with one heading
