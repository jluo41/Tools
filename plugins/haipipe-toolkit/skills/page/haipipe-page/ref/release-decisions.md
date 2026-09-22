# Page release decisions

This is the Page-family authority for interpreting existing acceptance and
release decisions. It complements the Run identities in `page-run-families.md`.
A Workflow is a list of Runs. Context collection, adoption, and whole-Page
Check are controller operations unless independently commissioned under a
complete Run contract. A feedback Step, retry, gate, or legacy Run names
does not allocate a Run.

## Profile and decision precedence

| Context | Required evidence | Action |
|---|---|---|
| Interactive Page writing | The exact Structure/Writing Run versions have durable human acceptance; every required dependency and Evidence Result is current | Reuse those decisions. An explicit Page release request authorizes adoption/delivery; an empty historical `approved:` field does not require the same approval again. |
| Interactive writing with an unfinished or unaccepted scope | The outstanding Run/scope, version, evidence, and decision owner are named | Continue that Run or present its missing decision. A general release request does not accept an unfinished candidate. |
| Non-interactive or unmigrated Shape profile | Approved G>=1 Shape and that profile's declared human gates | Follow its Shape gate. Machine `checked:` cannot substitute for human acceptance. |
| Refusal, pause, or acceptance of a different version | Original words and exact target/version | Preserve the decision. Do not transfer approval to changed content or interpret silence as approval. |

Resolve the profile from the owning Page workflow and its actual Run records,
not from a UI label. Record the release instruction verbatim, its time, exact
accepted versions, and evidence references. If the profile is ambiguous,
resolve that ambiguity before adoption; never guess a permissive profile.
Interactive acceptance must identify the final Structure artifact; an
unsettled v0 candidate is not released merely because a user requests a build.

Writing Steps save candidates, review/diagnosis, affected Bullets, and feedback
in their current Run. They do not adopt Page Content or rebuild delivery.
Release adopts the accepted candidate once; each commissioned RD records its
own delivery artifact and receipt. A whole-Page Check judges that immutable
version independently and does not rewrite the version it judges.

## Review packet

Before a human decision, show every required gate with its owner, exact
artifact/version, supporting evidence, recorded decision, and next action.
Include an owner ruling when required. Count only required gates, using
`settled / required`; a machine check and a human decision are distinct facts.
Reuse existing applicable decisions instead of asking for the same approval.
