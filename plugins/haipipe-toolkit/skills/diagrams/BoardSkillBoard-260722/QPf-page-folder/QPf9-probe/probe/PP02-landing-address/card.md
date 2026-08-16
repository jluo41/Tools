# PP02-landing-address
question: Do the probe orchestrator and collector agents accept an arbitrary landing directory today, or is `1-probes/` written into their prompts and code paths?
state: bound
binding: → tasks/A01_toolkit_probe_audit/01_probe_landing_path_scan/QA/1-probe-landing-path-hardcoding.md
stake: A1.1 needs the orchestrators to land in a page's `probe/` and nowhere else; whether that is a parameter change or a rewrite decides the plan.

## Q-executor
In the toolkit at /Users/floydluo/Desktop/Tools-SPACE/plugins/haipipe-toolkit, examine the probe-related agent definitions and skills (files under agents/ and skills/ whose names or content concern probe dispatch). Report whether the literal path `1-probes/` appears in their instructions or code, citing each file and line, and state whether any of them accepts a caller-supplied landing directory for probe records.
Deliverable: QA digest citing files and lines. Accepted: hard-coded | parameterized | mixed.

## bank binding
route: task · bank: new → answered · target: the binding line above

## A-executor
Hard-coded. `1-probes/` is a fixed path segment in about 300 live occurrences across the shared probe skill, its agent definitions, and the application family; only the consumer ROOT above it is caller-supplied, and no agent accepts a landing directory (the collector explicitly refuses to choose folders). Notably, the paper family has already retired `1-probes/` for papers in favor of `0-lifecycle/<stage>/probes/`, so the shared skill text and the paper checker disagree with each other today.
