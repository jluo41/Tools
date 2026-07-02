---
date: 2026-07-02
status: open
source: MISQ introduction editing session
recurrence: first instance
---

# Check existing bib before launching external search

## Rule

When a JL comment asks for a citation, FIRST check whether an existing `.bib` entry already fits the sentence. Only launch an external search agent if nothing in the bib works.

## Why

Launching a search agent for a paper that's already in the bib wastes 20-30 minutes and adds no value. The bib is the first place to look, not the last.

## How to apply

1. `grep` the `.bib` for keywords related to the claim
2. Check if any existing entry supports the sentence
3. If yes: propose the existing entry in a `> CC:` response
4. If no: then and only then launch a search (and put results in _CITATION_ with SEARCH markers, never directly into bib/tex)
