---
status: fixed
created: 2026-06-22
context: ref/probe-yaml-schema.md (canonical ref `P.<MMDD>`) + SKILL.md resolver. Raised while opening discovery-sourced probes P.0622/b/c in examples/ProjC-LLMRecPhysicain
fixed_in: "4.1.0"
---

Reporter (JL): 如果这个是 discovery 的话,你也可以说 P.Dxxxx;如果是 task,可以是 P.Txxxx;或者现在这种 P.xxx。这个当作 feedback 给我加进去。

Idea: let the probe ref encode the TYPE of evidence-source the probe was opened from (the `source.type` already in probe.yaml):

```
P.Dxxxx   probe opened from a discovery   (source.type: discovery)
P.Txxxx   probe opened from a task        (source.type: task)
P.xxxx    current plain form              (paper_claim_gap / human_idea / etc.)
```

So the source kind is legible from the ref alone, the same way the discovery layer encodes type with 搜/析/创. Under this convention the three ProjC probes (all source.type: discovery) would read P.D0622 / P.D0622b / P.D0622c instead of P.0622/b/c.

JL decision (2026-06-22): unify on just two letters, P.D and P.T. Every probe carries a letter; the plain three-form (P.D / P.T / plain) is dropped. The open design questions were settled this way:
- Letter mandatory (only D and T). source.type discovery -> D, task -> T; any other source.type derives the letter from the primary evidence_plan kind, so the result is always D or T.
- Folder renames too: probes/<LETTER><MMDD>_<slug>/ (not ref-only). New probes get the letter at creation; the three ProjC probes were renamed in place.
- Only D and T (no per-source alphabet soup).
- Resolver accepts lettered refs AND legacy letterless refs.

Fix (applied 4.1.0): ref/probe-yaml-schema.md Location + canonical-ref grammar rewritten to P.<LETTER><MMDD>[suffix] with the D/T derivation + lazy legacy migration; id field-table example updated; SKILL.md resolver updated to accept lettered + legacy refs; version bumped to 4.1.0. Applied to examples/ProjC-LLMRecPhysicain: P.0622/b/c -> P.D0622/b/c, folders + _index.md + discovery.consumed_by + project.log.jsonl all renamed and revalidated. Existing letterless probes (ProjB P.0605 etc.) migrate lazily on next touch, not in a mass rename.
