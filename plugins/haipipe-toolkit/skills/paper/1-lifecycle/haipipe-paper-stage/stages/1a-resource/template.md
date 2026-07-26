<!-- TEMPLATE (follow, don't ship). Fill 0-lifecycle/1-work/1a-resource.md from this skeleton: replace every <…>, and each `<!-- RULE: … -->` comment is guidance to FOLLOW then DELETE — a RULE comment never appears in the finished doc. Delete this top line too. -->
1a-resource: <paper title> (what the paper's resources ARE, and whether they carry the claim)
============================================================================================

Date: YYYY-MM-DD
Status: DRAFT
Venue-FREE. Exactly two sections: Resource Description and Q-consumer. No sidecars.


Resource Description
--------------------
<!-- RULE: describe the resources this paper HAS — one `## Resource <n> · <name>` subsection per resource (a dataset, a model/pipeline, or producing-code; scope is DATA + MODELS + CODE alike). Inside each, `### <topic>` sub-subsections for its aspects (coverage/size, provenance, validation, …). Close each with a `### Serves & carries` topic: which `H<n>` it serves and whether it CAN carry them — a resource that exists but cannot carry a claim says so HERE, naming what it KILLS. Cite the Q-consumer question that tests a fitness/gap claim inline, e.g. [Q-Resource-1]. A hypothesis with NO fit resource is a SCOPE CUT — say it at the gate, log it in `_LOG`. Keyed on `H<n>`, never `C<n>` (claim ids do not exist yet at resource time). -->

## Resource 1 · <resource name>

### <topic — e.g. coverage & size>
<description — one sentence per line>

### <topic — e.g. provenance / validation>
<description>

### Serves & carries
<which `H<n>` this serves, and whether it CARRIES them (or what it KILLS). [Q-Resource-<n>]>

## Resource 2 · <resource name>
### <topic>
<description>
### Serves & carries
<which `H<n>`; carries or kills. [Q-Resource-<n>]>


Q-consumer
----------
<!-- RULE: what we still need to KNOW about the resources — one `## Q-Resource-<n>` block per question, uniform Description / Reason / Answer (the PROBE stage collects every stage's Q-consumer through one pipeline, so the shape is shared across all stages).
     · Cite the question inline in the `### Serves & carries` (or topic) line it tests, e.g. [Q-Resource-1] (forward link); `Reason` names the resource + `H<n>` it bears on (back link).
     · Description = the existence-or-fitness question. Reason = which resource + `H<n>` it bears on + why a bad answer matters. Answer = empty in DRAFT; PROBE fills it from the answering QA file.
     · RESOURCE DISCIPLINE for the Answer: it states existence AND fitness AND what it KILLS. A woolly Answer ("probably fine") is a DEFECT, not an answer. A BUILD question's Answer records: COMMISSIONED · owner · eta · blocks `H<n>` · cross-project · what it yields and what it does NOT fix.
     · The `-> PP<NN>` probe binding is written by the PROBE WORKER, not this stage; it surfaces as the Answer's `[source: PP<NN>]`. -->

## Q-Resource-<n> · <question title>
Description: <does the resource exist / can it CARRY the hypothesis it serves? — one sentence per line>
Reason: <which resource + `H<n>` it bears on, and what a bad answer KILLS>
Answer: <empty in DRAFT — PROBE fills it: existence AND fitness AND what it KILLS, with [source: PP<NN>]>
