#!/usr/bin/env python3
"""Rebuild a multi-lane timeline of a replication run from session + subagent transcripts."""
import json, glob, os, sys
from datetime import datetime

SESS = sys.argv[1]  # main session jsonl path
SUBDIR = SESS.replace('.jsonl', '') + '/subagents'

def parse(fp, lane, label):
    events = []
    for line in open(fp):
        try: d = json.loads(line)
        except: continue
        ts = d.get('timestamp')
        if not ts: continue
        t = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        if d.get('type') != 'assistant': continue
        for b in d.get('message', {}).get('content', []):
            if b.get('type') != 'tool_use': continue
            name, inp = b['name'], b.get('input', {})
            ev = None
            if name == 'Skill':
                ev = '🎯 Skill(%s)' % inp.get('skill')
            elif name == 'Agent':
                ev = '🤖 dispatch %s (bg=%s)' % (inp.get('subagent_type'), inp.get('run_in_background'))
            elif name == 'Write':
                p = str(inp.get('file_path', ''))
                short = '/'.join(p.split('/')[-2:])
                ev = '📝 Write %s' % short
            elif name == 'Edit':
                p = str(inp.get('file_path', ''))
                short = '/'.join(p.split('/')[-2:])
                ev = '✏️ Edit %s' % short
            elif name == 'AskUserQuestion':
                ev = '❓ ask user'
            if ev:
                events.append((t, lane, ev))
    return events

events = parse(SESS, 0, 'main')
lanes = {0: '🎬 d0 paper-session'}
metas = sorted(glob.glob(SUBDIR + '/*.meta.json'), key=os.path.getmtime)
for m in metas:
    meta = json.load(open(m))
    depth = meta.get('spawnDepth', 1)
    atype = meta.get('agentType', '?').replace('haipipe-', '').replace('-agent', '')
    jl = m.replace('.meta.json', '.jsonl')
    lane = len(lanes)
    lanes[lane] = '%s d%d %s' % (['🎬','🕵️','📚','✍️','🔍'][min(depth,4)], depth, atype)
    events += parse(jl, lane, atype)

events.sort(key=lambda e: e[0])
t0 = events[0][0]
print('LANES:')
for k in sorted(lanes): print('  L%d = %s' % (k, lanes[k]))
print()
prev_min = -1
for t, lane, ev in events:
    dt = (t - t0).total_seconds()
    mm, ss = int(dt // 60), int(dt % 60)
    indent = '    ' * lane
    print('%02d:%02d %s[L%d] %s' % (mm, ss, indent, lane, ev))
