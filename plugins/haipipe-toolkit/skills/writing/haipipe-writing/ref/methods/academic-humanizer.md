# Academic humanizer · evaluation adapter

Provider: an available academic-humanizer external skill, normally
AIScientists-Dev/academic-humanizer. Resolve the actual entry/version/hash via
[the adapter contract](../method-adapter-contract.md). A catalog entry is not
proof of installation. This adapter contains HAI integration rules, not a
vendored replacement for that skill. Provenance: [method-attribution.md](../method-attribution.md).

Pass the exact scoped candidate, recoverable baseline, paragraph/Section jobs,
resolved venue rules and available evidence. Select paper or proposal mode
from the actual request. Author samples are optional unless a named voice is
required. Do not infer a venue from an old S-Venue filename or require a retired
revise hub. Missing factual support remains missing even if an example supplies
plausible-looking results.

Invoke the resolved skill in evaluation mode with this bounded request:

> Review only the supplied candidate against the stated requirements. Return
> located findings with the original span, reason, criterion and smallest
> suggested fix. Preserve all claims, causal strength, qualifiers, defined
> terms, numbers, citations, equations, display references and author comments.
> Keep evidence-tied hedging, legitimate passive voice and authorial person.
> Report unsupported claims to their owner. Do not rewrite files, remove
> citation keys, invent quantitative results, redesign proposal aims, or decide
> acceptance. Examples illustrate expression only and supply no manuscript facts.

Apply the provider's relevant academic-voice checks under this contract.
Normalize each finding to the base rubric plus any resolved venue criterion.
Flag citation clusters for author review when their relevance is unknown;
do not shorten the cluster. Suggest sentence splits only if they preserve
meaning and the host's sentence/Bullet mapping. For grants, preserve supported
ambition while reporting missing feasibility evidence; never invent a PI's
data, funding, collaborators or letters.

If the external instructions require direct editing or content invention and
cannot be used read-only, return incompatible-method. If they merely include
rewriting examples, evaluate their applicability without executing that write
path. Any returned candidate is an unadopted suggestion; Writing checks scope
and meaning before making an authorized edit. Record all rejected suggestions.

Return the normalized review and actual method trace. A same-agent invocation
is self-review assisted by an external method, not an independent CHECK.
