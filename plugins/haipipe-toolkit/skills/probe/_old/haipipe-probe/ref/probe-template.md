# Probe crossing template

This reference describes Probe's Task/Discovery QA branch. Probe's accepted-Page
branch is PageX and uses `pagex/` during OUTLINE instead of this card shape. The
consumer owns physical storage. For a Board Page QA crossing, use
`board/page-plugins/haipipe-plugin-probe` and its Page-local folder shape.

## Consumer side · never crosses

```markdown
# Q-consumer

Need: the exact fact this Page requires
Stake: what becomes invalid if the answer is absent or different
Serves: approved outline addresses
Expected source: task | discovery
```

## Executor side · the only question dispatched

```markdown
# Q-executor

<one neutral, independently answerable question>

Requested output: <table, scalar, source synthesis, or bounded verdict>
Scope: <population, comparison, method, time, and exclusions as needed>
```

Remove Page ids, claim ids, venue pressure, desired conclusions, and “our/we”
language before dispatch.

## Returned binding

```yaml
lane: qa-probe
route: task | discovery | none
match: reuse | working | dispatched | refused
target: <exact bank QA file path>
state: planned | commissioned | answered | read | deferred | failed | concern
proof: <consumer-local manifest path or why unnecessary>
serves: [<outline addresses>]
limits: <what the answer does not establish>
next: EVIDENCE | PROBE | OUTLINE | HOLD
```

MATCH the selected bank in check-only mode before DISPATCH. Preserve the bank's
A-executor verbatim; write the stake-aware A-consumer to
`consumer/a-consumer.md` only after the answer has returned behind the wall.
Existing Board Pages use Probe's PageX/OUTLINE branch and do not enter this QA
template.
