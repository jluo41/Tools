STATUS -- 01_sms_young_male
===========================

Intervention state file. The Intervention Console re-derives current state from
disk each session; this file is the machine-read state header + Gate Ledger.
Venue rows (venue / stages_skipped / claims_settlement) are written by the venue
stage at pin time -- absent here because the venue is not yet pinned.

State
-----

| Field | Value |
|---|---|
| intervention | 01_sms_young_male |
| audience | young male patients |
| current_layer | 0-seed |
| maturity | prospect |
| active_round | none |
| created | 260718 |

Venue is **unpinned** (venue-FREE spine only: seed -> the 1a-1d evidence ladder).
The venue stage runs after the ladder gate and writes the venue / stages_skipped /
claims_settlement rows here.

## Gate Ledger

Records who approved each stage as done. A stage is `✅` only when its `.md` has
real content on disk AND its row here is `| <stage> | yes | <who> | <date> |`.
Empty until the first stage gate passes.

| stage | confirmed | by | date |
|---|---|---|---|
