"""Pull a timeline out of a Claude Code transcript: the person's own messages, peer messages, and each assistant
reply's first line, all with timestamps. Usage: extract.py <jsonl> <out.md> <name>"""
import json, sys, re
src, out, name = sys.argv[1:4]
rows = []
def text_of(c):
    if isinstance(c, str):
        return c
    return "\n".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
for line in open(src, encoding="utf-8", errors="replace"):
    try:
        e = json.loads(line)
    except Exception:
        continue
    t, ts = e.get("type"), (e.get("timestamp") or "")[:16].replace("T", " ")
    m = e.get("message") or {}
    if t == "user" and not e.get("isMeta") and not e.get("toolUseResult"):
        txt = text_of(m.get("content", "")).strip()
        if not txt or txt.startswith(("<local-command", "<command-", "Caveat:")) or "tool_use_id" in txt:
            continue
        if txt.startswith("This session is being continued"):
            continue
        cm = re.search(r'<cross-session-message from="[^"]*" from-name="([^"]*)"[^>]*>\s*(.*?)\s*</cross-session-message>', txt, re.S)
        if cm:
            rows.append((ts, "PEER " + cm.group(1), cm.group(2)[:700]))
            continue
        txt = re.sub(r"<system-reminder>.*?</system-reminder>", "", txt, flags=re.S).strip()
        if txt.startswith("<"):
            continue
        rows.append((ts, "JL", txt[:1200]))
    elif t == "assistant":
        txt = text_of(m.get("content", [])).strip()
        if len(txt) > 80:
            first = txt.splitlines()[0][:300]
            rows.append((ts, "AI", first))
with open(out, "w", encoding="utf-8") as f:
    f.write(f"# {name}\n\n")
    last = None
    for ts, who, txt in rows:
        if who == "AI" and last == "AI":
            continue
        f.write(f"- {ts} · {who} · " + txt.replace("\n", " ⏎ ") + "\n")
        last = who
print(name, len(rows))
