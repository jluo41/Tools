# Humanizer (blader) · evaluation adapter

Provider: the vendored `humanizer` skill at `../../../2_evaluate/humanizer/`
(blader/humanizer 3.0.0, MIT). Resolve entry, version and hash via
[the adapter contract](../method-adapter-contract.md). This adapter carries the
HAI integration rules only; the skill's twenty-five patterns are its own.

Select it for general-register prose: a Page's Opening, notes, documentation,
a README, an email. For a paper, thesis, rebuttal or grant proposal select
`academic-humanizer` instead; its checks keep scholarly conventions that this
skill would flag as tells. Never select both on one candidate.

Pass the exact scoped candidate, a recoverable baseline, the host's requirements
and the reader named in the request. Invoke the skill in evaluation mode with
this bounded request:

> Review only the supplied candidate for AI tells. Return located findings, each
> with the original span, the pattern (by the skill's own group and number), why
> it reads as machine-written here, and the smallest fix. Preserve every claim,
> number, name, citation, defined term, hedge tied to evidence, and the author's
> person and register. Do not rewrite the file, reorder the argument, add facts,
> or decide acceptance. Apply the skill's "when not to act" section before
> flagging: a pattern used once, on purpose, is not a tell.

Normalize each finding to the base rubric in [evaluation.md](../evaluation.md);
a finding that names no span is dropped. Findings are input to the owning Run's
review, never an automatic edit. Record the resolved entry, version and hash in
the method trace as the contract requires.
