---
status: fixed
created: 2026-06-22
context: ref/stage-strip.sh (gather_done predicate) — hit on three freshly-planned probes in examples/ProjC-LLMRecPhysicain/probes
fixed_in: "4.3.0"
---

Trigger: ran `plan` for three new probes (P.0622 / P.0622b / P.0622c). Each probe.yaml has a `claim:` and an `evidence_plan:` block, but `evidence_refs` and `calls` are EMPTY (nothing gathered yet — the probe is at the Gather frontier). The stage strip rendered:

```
Plan ✅ ─ Gather ✅ ─ Read ▶️ ─ Judge ⬜ ─ Deposit ⬜
   ← here Read: no evidence.md (Read not run)
```

That is wrong: it claims Gather is done and the frontier is Read, when in fact zero evidence is linked. The true state is Plan ✅, Gather ▶️.

Root cause: `gather_decl` (lines ~96-99) fires if ANY of `evidence_refs arms calls evidence_plan links design cells` keys is present. But `evidence_plan` is a PLAN artifact written at the Plan stage, so every planned probe has it. Combined with `broken=0` (a fresh probe has no path refs to break — only `source.ref` / `return_target`, which resolve), `gather_done=1` for any just-planned probe. The predicate conflates "a plan to gather exists" with "gathering happened."

Fix: drop `evidence_plan` from the gather_decl key list (it is the Plan predicate, not Gather). Gather should be "done" only when there is at least one ACTUAL linked/requested item — i.e. `evidence_refs` has a non-empty tasks/discoveries/insights entry OR `calls` is non-empty — AND every linked ref resolves. A bare `evidence_refs:` / `calls:` header with empty lists must NOT count. Consider grepping for a list item (`- ref:` / `- type:`) under those keys rather than just the key's presence.
