# PP02-landing-address
question: Do the probe orchestrator and collector agents accept an arbitrary landing directory today, or is `1-probes/` written into their prompts and code paths?
state: working
stake: A1.1 needs the orchestrators to land in a page's `probe/` and nowhere else; whether that is a parameter change or a rewrite decides the plan.

## Q-executor
In the toolkit at /Users/floydluo/Desktop/Tools-SPACE/plugins/haipipe-toolkit, examine the probe-related agent definitions and skills (files under agents/ and skills/ whose names or content concern probe dispatch). Report whether the literal path `1-probes/` appears in their instructions or code, citing each file and line, and state whether any of them accepts a caller-supplied landing directory for probe records.
Deliverable: QA digest citing files and lines. Accepted: hard-coded | parameterized | mixed.

## bank binding
route: task
bank: new
target: NEW ?
