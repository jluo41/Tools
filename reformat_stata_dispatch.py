"""reformat_stata_dispatch.py — expand one-liner if/else-if branches in a Stata
dispatcher to the house multi-line-brace style. Cosmetic only:

  else if "x" { do "w.do" `year' }            ->  else if "x" {
                                                       do "w.do" `year'
                                                   }
  else if "x" == "y"   local out_file "${z}"  ->  else if "x" == "y" {
                                                       local out_file "${z}"
                                                   }

Leaves multi-line blocks, `if ... {` openers, `}` lines, comments, and any other
line untouched. Verifies brace balance and statement counts are preserved.
Usage: python reformat_stata_dispatch.py <file.do> [<file.do> ...]
"""
import re
import sys

# one-liner WITH braces: <ws>(else )?if <cond> { <body> }   (body has no trailing quote after })
RX_BRACED = re.compile(r'^(\s*)((?:else )?if) (.+?)\s*\{\s*(.+?)\s*\}\s*$')
# braceless single command: <ws>(else )?if <cond == "x">  <local ...>
RX_BRACELESS = re.compile(r'^(\s*)((?:else )?if) (.+?== ".+?")\s+(local\s.+?)\s*$')


def transform_line(line):
    m = RX_BRACED.match(line)
    if m and '{' not in m.group(4) and '}' not in m.group(4):
        ind, kw, cond, body = m.groups()
        return [f"{ind}{kw} {cond} {{", f"{ind}    {body}", f"{ind}}}"]
    m = RX_BRACELESS.match(line)
    if m:
        ind, kw, cond, body = m.groups()
        return [f"{ind}{kw} {cond} {{", f"{ind}    {body}", f"{ind}}}"]
    return [line]


def reformat(path):
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    lines = src.splitlines()
    out, n_changed = [], 0
    for ln in lines:
        new = transform_line(ln)
        if new != [ln]:
            n_changed += 1
        out.extend(new)

    # --- verifications (must hold or we abort without writing) ---
    new_src = "\n".join(out) + ("\n" if src.endswith("\n") else "")
    assert new_src.count("{") == new_src.count("}"), f"{path}: brace imbalance"
    # braceless->braced conversions legitimately ADD balanced brace pairs, so we
    # check balance (above) + statement-count preservation (below), not raw counts.
    for tok in ('do "', "local out_file"):
        assert src.count(tok) == new_src.count(tok), f"{path}: '{tok}' count changed"
    assert not any(RX_BRACED.match(l) for l in out), f"{path}: one-liner remains"

    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(new_src)
    print(f"OK  {path}  ({n_changed} branches expanded)")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        reformat(p)
