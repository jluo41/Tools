# The s10 map face: its yaml blocks

`scripts/related_map.py` draws `studio/s10-related-work-map/` from five yaml blocks in the face. Only `map:` is
needed; each other block adds one small frame once there is something to say. Worked example:
Paper-LLMRecPhy's `studio/s10-related-work-map/` (27 papers, five types, 2026-10-13).

```text
map       ① main     every closest paper in four quadrants, ours as the key point
nearest   ② small    the nearest papers side by side with ours, one row per property
gaps      ③ small    each kind of closest work: what it leaves open → what we add
lessons   ④ small    what several papers do → what we change in our methods
papers    ⑤ on       one frame per type, each paper a step: how it helps us, its method
```

## map (frame ①)

```yaml
map:
  title: "① Where our two papers sit among the closest work"
  sub: "★ closest in its group · pp: percentage points"         # define every short word here
  key: "{builds} closest papers build a recommender, {audits} audit chatbot answers. Ours ask which stage decides who is seen."
  left: "🛠️ builds a recommender"                               # the across axis: what a paper does
  right: "🔍 audits one"
  top: "live answers to real queries"                            # the up axis: what it runs on
  bottom: "offline logs or synthetic cards"
  quadrants: {TL: "...", TR: "...", BL: "...", BR: "..."}        # optional quadrant titles
  clusters:                                                      # optional: bottom-left cards in named boxes
    BL:
    - title: "LLM rankers"
      keys: ["Zeng et al. 2026", "Zheng et al. 2025"]
  ours:                                                          # the key point: our paper(s), top right
  - title: "📄 Paper A (proposed) · who enters?"
    lines: ["listed vs unlisted, 1 model", "❓ quality evidence not run"]
  placements:                                                    # every Closest row, by its item name
    "Gillani & Baig 2026": {at: BR, label: "+31.4 pp choice"}
    "Derr 2026": {at: "off", label: "perspective"}             # quoted: YAML reads a bare off as false
```

1. **Axes**: pick the two that make our gap visible, not a generic field map.
2. **Counts**: the key may use `{closest}` `{placed}` `{TL}` `{TR}` `{BL}` `{BR}` `{left}` `{right}`, counted on
   every build; LLMRec's older `{builds}` (= left) and `{audits}` (= right) still work.
3. **Red**: a Closest row with no placement is drawn red, "not placed yet".
4. **Labels**: a number or a few words read from the paper's Result or full read, never invented.

## nearest (frame ②)

```yaml
nearest:
  title: "② The two nearest audits, beside our two papers"
  sub: "what each runs on, how, at what scale, its headline, and what it cannot say"
  key: "<one sentence: how the nearest differ from ours>"
  columns: ["", "Gillani & Baig 2026", "Ibrahim & Zaki 2026", "📄 Paper A", "📄 Paper B"]
  rows:
  - ["design", "randomized conjoint", "audit, search on vs off", "...", "..."]
  - ["scale", {big: "40,068", tag: "answers · 7 models"}, ...]   # a value cell: its number large, label small
  - ["cannot say", "...", "...", "...", "❓ unfairness, until quality is measured"]   # ❓ = open
  note: "<every abbreviation defined>"
```

## gaps (frame ③)

```yaml
gaps:
  title: "③ What each kind of closest work leaves open, and what we add"
  key: "<one sentence: where every kind stops>"
  rows:
  - {kind: "🔍 chatbot name audits", open: "hand-checked names, ≤20 cities", add: "📄 A: 1,983 queries, a real roster"}
  open: ["❓ a choice the person makes"]
```

## lessons (frame ④)

```yaml
lessons:
  title: "④ What the related work teaches our methods"
  key: "<one sentence>"
  rows:
  - {they: "Several audits hand-check every name", we: "match every name to the NPI roster, then hand-check a sample"}
```

## papers (frames ⑤ on)

```yaml
papers:
  groups:                                     # one frame per type, in the order of the s11-s19 topics
  - act: Act 3 · Chatbots naming doctors
    keys: [Oca et al. 2023, Parikh et al. 2024]
  records:
  - key: Oca et al. 2023
    topic: s11                                # the type topic that reads it in full, or none
    depth: full text                          # or: deep read, not full text
    method: <one sentence>
    evaluation: <one sentence>
    contribution: <one sentence>
    helps_us: <one sentence: what it changes for our paper>
    relation: gap-we-fill                     # borrow-method · borrow-evaluation · baseline · gap-we-fill · threat
    source: <its Discovery Result or reads/ folder>
```

`relation: threat` is drawn red: a result our paper must answer before it claims anything.
