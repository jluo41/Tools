# Patient confirmation SMS · Design Items

One block per design target: the bet, its evidence, and its acceptance rules.
Runs name an item through `item:`; state is derived from those Runs, never typed here.

## ITEM01 · Send the tested winner, verbatim
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Field the salience template exactly as round 1 sent it
stance: follow
basis: evidence-informed
mode: compose
expected: salience stays the best arm on click and authentication when re-fielded against any concurrent arm
falsified: a concurrently fielded round-2 arm beats it on click outside overlapping intervals
evidence:
- handoff · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- carries the provider-name placeholder {NAME}
- no predicted-lift text
- byte-identical to the fielded salience template

## ITEM02 · Attribution removed
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Test whether the message works without the provider attribution
stance: challenge
basis: evidence-informed
mode: challenge
expected: click does not fall when the provider attribution is removed
falsified: click falls outside the attributed arm's interval
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 120 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no provider name and no {NAME} placeholder
- no predicted-lift text

## ITEM03 · Deadline stated
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: State a concrete review-by time to see whether a deadline changes click
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- states a review-by time in plain words
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM04 · Question opener
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Open with a question about the new prescription details instead of a statement
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- the first sentence is a question
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM05 · Action first
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Put the review action in the first three words and the sender second
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- the first three words name the review action
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM06 · Why it matters
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Add one clause on why the review helps, without any medical or outcome claim
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- one clause says why the review helps, with no medical claim
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM07 · Under 90 characters
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Test the shortest message that still names the sender, the action, and the opt-out
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 90 characters including the opt-out suffix
- carries the provider-name placeholder {NAME}
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM08 · Two steps
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Give the review as two numbered steps to see whether structure changes click
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- contains exactly two numbered steps
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM09 · Patient greeting
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Greet the patient by first name before the review ask
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- carries the patient first-name placeholder {FIRST_NAME}
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only

## ITEM10 · Help line close
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Close with one line on where to ask questions before the opt-out
stance: explore
basis: evidence-informed
mode: compose
expected: click stays inside the salience interval [65.56, 66.56] when fielded as a concurrent arm
falsified: click falls below 65.56 in the concurrent arm, outside overlapping intervals
evidence:
- evidence · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- carries the provider-name placeholder {NAME}
- one sentence before the opt-out says where to ask questions
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
- no predicted-lift text
- does not vary the message by age, gender, send day or region
- plain, non-coercive prescription-review framing only
