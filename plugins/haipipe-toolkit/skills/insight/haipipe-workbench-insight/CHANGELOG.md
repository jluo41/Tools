## 0.1.1 · 2026-09-28 · No content hashes (JL 260928)

- `servers/workbench-insight`: a question registration writes no `definition_hash` or
  evidence `sha256`; the Run Spec reader and request text no longer check or show one.
- Handoff eligibility checks that the recorded files and anchored receipts exist; the
  handoff reads stale when the signed Page or a whole-file dependency is newer than the
  GI5 receipt (file time). Hash fields left in older records are ignored.

## 0.1.0 · 2026-09-22

- New skill: the served face of the Insight family, paired with
  `servers/workbench-insight`. Until now the two 🔎 routes were named only in
  the Board skill's route table; the page grain was described inside
  `haipipe-page-insight` and the board grain inside `haipipe-insight`. This
  skill states the read-only contract of both grains in one place and leaves
  the domain with its owners.
