# Current handoff eligibility

Load when recording GI5/GI6, handing Wisdom to Design, or diagnosing a signed
Page that the Board reports as historical/unverified. A signature token remains
historical evidence. Current eligibility additionally requires the exact signed
payload, current dependencies, passed owner receipts, and a settled Question cell.
The Board and Design viewers read this evidence; they grant no approval.

## Owner sequence

1. Wisdom CHECK-closes the intended Page and pins its exact version and bytes.
   Collect all required source and verdict versions/hashes, including MT00's
   partition register for a partition-major verdict. Resolve current
   applicability at the source owners; a historical Result alone cannot prove it.
2. A person states the signature for that exact payload. Wisdom records GI5 in
   `outline/<wisdom-stem>-log.md`, with the actor, Runtime id, Page pin, signature,
   and dependency pins. Record the person's authorization; never synthesize it.
3. Question settles each SERVES cell against that same Page and signature and
   writes GI6 in its own `outline/<register-stem>-log.md`.
4. Index these existing records in the Wisdom Folder's `workflow/handoff.yaml`
   and the aggregate Runtime's `resource_controls`. The index creates no Run and
   has no independent approval authority. Any missing or changed required pin,
   open/held/stale Page, missing GI6, or reopened Queue cell blocks current use.

Finish the signed Page bytes before hashing them; later log appends belong in
Outline. A change to the signed Page or its dependency pins requires new owner
records and a new person signature. Keep historical records and consumer pins.
A POOL deferral exports no handoff and needs no index or signature. A licensed
`UNDETERMINED` partial-final W non-answer likewise creates no current handoff
record: it has no GI5 pass, signature, or Design input. A separate answered,
person-signed W may still qualify when it stays within its authorized scope and
all of its dependencies are current.

The receipt examples below describe an exported, signed handoff. Do not create
this index for an `UNDETERMINED` partial-final page. Its Question-owned GI6
receipt instead pins the answering Page and quotes the partial-final licensing
sentence; it has no `signature_receipt` because no GI5 handoff occurred.

## Index and receipts

All paths in this index **and its referenced receipt payloads** resolve relative
to the Wisdom Folder, including GI6 Page/signature references. Absolute paths
are allowed. Use exact versions, never `latest`.

```yaml
schema: haipipe.insight-handoff/v1
page:
  path: FW01-counsel.md
  version: v001
  sha256: <exact-Page-bytes-sha256>
dependencies:
  - {path: <current-source-or-version-record>, version: <exact-version>, sha256: <sha256>}
  - {path: <current-verdict-record>, version: <exact-version>, sha256: <sha256>}
gi5: {path: outline/FW01-counsel-log.md#signed-v001, sha256: <record-body-sha256>}
gi6:
  - {path: <Question-Outline-log>#settled-qw1-v001, sha256: <record-body-sha256>}
```

A whole-file reference hashes its bytes. A Markdown `#record-id` reference
selects the body under a unique exact heading `### record-id` (levels 2–6 are
supported), ending before the next heading of equal or shallower depth. Strip
leading/trailing whitespace and hash the body's UTF-8 bytes, including its YAML
fence. Thus appending another record does not invalidate an older receipt.
Use a unique anchor; duplicate anchors are invalid.

GI5's anchored body contains one YAML record:

```yaml
key: GI5
status: passed
authority: haipipe-insight-wisdom
actor: <person-who-authorized>
workflow_runtime_id: <actual-runtime-id>
page: <exact-page-mapping-from-index>
signature: <initials-and-YYMMDD-exactly-as-on-Page>
dependencies: <exact-dependency-list-from-index>
```

GI6 contains:

```yaml
key: GI6
status: passed
authority: haipipe-insight-question
actor: <settlement-actor>
workflow_runtime_id: <actual-runtime-id>
page: <exact-page-mapping-from-index>
target: {question: QW1, partition: F}
signature_receipt: <exact-gi5-reference-from-index>
```

Index one GI6 receipt per served QW at this Page's partition. The current Queue
cell must still settle to this Page (`✅`, or licensed `🟡 … final`). Receipt
fields are auditable owner assertions, not cryptographic proof of a human's
identity or an independent scientific review. Required dependency completeness
remains the owner CHECK's responsibility; the viewer checks recorded pins.

Existing signed Pages lacking these records remain visible as historical /
unverified. On the next authorized handoff use, owners verify applicability and
materialize the records from real evidence. Do not fabricate historical GI5 or
GI6 receipts to make the viewer green.
