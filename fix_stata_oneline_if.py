"""fix_stata_oneline_if.py — convert the single-line braced guard
`if !_rc { drop `x' }` (invalid: Stata needs `}` on its own line -> r(198))
to the braceless single-command form `if !_rc drop `x'`. Targeted + verified.
Usage: python fix_stata_oneline_if.py <file.do> [<file.do> ...]
"""
import re, sys

# if <cond> { <single drop command, no nested braces> }
PAT = re.compile(r'(if\s+![_a-zA-Z()]*rc\s+)\{\s*(drop\s+[^{}]+?)\s*\}')

for f in sys.argv[1:]:
    with open(f, "r", encoding="utf-8") as fh:
        t = fh.read()
    n = len(PAT.findall(t))
    t2 = PAT.sub(r"\1\2", t)
    # verify: no single-line braced `if !_rc { ... }` remains
    assert not re.search(r'if\s+![_a-zA-Z()]*rc\s+\{[^{}]*\}', t2), f"{f}: pattern remains"
    with open(f, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(t2)
    print(f"{f.split('/')[-1].split(chr(92))[-1]}: fixed {n}")
