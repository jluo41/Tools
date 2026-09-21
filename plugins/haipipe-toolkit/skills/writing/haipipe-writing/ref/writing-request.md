# Writing request and return · version 1

Use this contract for a Section, paragraph/group, or standalone file. It is a
view of the host's existing authority, stored in its Ticket/Step when needed;
do not create a second plan or runtime ledger.

## Request

```yaml
worker: haipipe-writing
writing:
  mode: revise                    # draft | revise | evaluate
  scope: paragraph                # section | paragraph | paragraph-group | file
  target: C1.P2                   # actual host address or file/selection
  run: null                       # existing host id; null for standalone work
  version: null                   # use host values when present
  step: null
  baseline: null                  # exact saved text or recoverable path/version/hash
  candidate: null                 # evaluate: text/path being reviewed; defaults to baseline
  plan: null                      # host slice; required for plan-based realization
  evidence: []                    # exact Results/static sources for factual claims
  neighbors: []                   # relevant seams, not permission to edit neighbors
  requirements: []                # resolved venue/host/user requirements with sources
  feedback: []                    # original words, target and source; interpretation separate
  protected: []                   # outside scope and accepted text
  methods: []                     # selected ids/roles only; see method-adapter-contract.md
  evaluation:
    rubric: haipipe-writing/base-v1
    max_revision_passes: 1        # nonnegative integer; host/user may override
```

Values above illustrate the envelope, not a ready-to-run Ticket. Fill it from
the actual request. A file edit needs its text, scope and applicable constraints;
it does not require a Page, Outline, Evidence workspace, or a new Run. For
Page work, resolve identities and inputs from its existing Ticket and records.
The rubric's content hash and selected method versions/hashes are frozen in
the effective packet. Resolve a declared requirement conflict before judging
that criterion; do not invent a policy to make the packet complete.

Resolve request-relative file paths from the request file's directory (or the
host's explicitly recorded base directory for an inline request). In evaluate
mode, a separate candidate is compared with the baseline; when omitted, review
the baseline itself. Neither source is changed.

A Section request includes its paragraphs' jobs and order; evaluate coverage,
argument and seams across that scope. A paragraph request keeps its fixed
target and checks the neighboring seam. A wording-only Step reads its dependent
Bullet without modifying plan metadata. Missing required material is a named
block; optional unsupplied style is not a block. SHAPE candidates may carry
explicit unsupported slots; final realization may not present those as facts.

## Invocation

The owning agent reads this request, loads haipipe-writing, and resolves only
the selected methods using [method-adapter-contract.md](method-adapter-contract.md).
It applies the skill instructions and invokes the declared tool when the
method has one. The YAML is configuration interpreted by that agent, not a
shell command, scheduler, model launcher, or additional Run.

Default methods are empty: use the native Writing worker and base self-review.
An explicitly supplied Writing DNA packet selects the writing-dna style
adapter; an explicit legacy anti_slop packet selects anti-slop once. Normalize
these to the same method trace. If legacy and new selections disagree, report
the conflict rather than running both. Reuse the effective packet for ordinary
feedback; material changes to frozen inputs follow the host's reopening rules.

## Return

Return these fields in the host's existing record, without creating mandatory
per-call files:

| Field | Content |
|---|---|
| identity | Same request target and Run/Version/Step, if present |
| candidate | Complete scoped text, exact source/version/hash; unchanged supplied candidate for evaluate mode |
| changes | Actual Before/After and local reasons for material edits only |
| evaluation | Rubric/version/hash, evaluator mode, located findings, initial/final verdicts; see evaluation.md |
| methods | Selected method, resolved entry/version/hash, execution/skip/block state and output reference |
| unresolved | Missing input, requirement conflict or out-of-scope fix, with the owning authority |
| disposition | ready-for-review, needs-work, or blocked; never implicit human acceptance |

In evaluate mode, report findings without revising or writing source. In revise
mode, corrections remain within authorization. Preserve every scientific claim,
qualifier, defined term, number, citation, display reference and author comment
unless the user explicitly commissioned the corresponding content change.
Keep evidence-tied hedging, legitimate passive voice and authorial person.
Return unsupported claims to their owner; no invented measurements, narrower
claims, removed citation keys, redesigned grant aims, preliminary results or
partner letters to improve style.

Page owns saving/promoting the candidate and managing acceptance. Its presenter
computes visual changes from clean Before/After fields. Writing never inserts
diff markup into candidate prose, mutates accepted Content, edits generated
TeX/Word, or creates a Run per method call. A Section cycle can write multiple
paragraphs within one existing Step. Standalone apply follows the user's file
authorization; original-preserving requests return a candidate and keep the
source unchanged. Signed review records are append-only under the host policy.

If a style suggestion requires splitting a sentence, first preserve meaning
and the host's sentence/Bullet mapping. A required plan change returns to the
plan owner. Word count is a prompt to inspect, not an instruction to split.
