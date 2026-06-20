Invocation modes — interactive vs headless (dual-mode contract)
===============================================================

Every DIKW filer skill — `haipipe-insight-data` / `-information` /
`-knowledge` / `-wisdom` — is callable two ways over ONE body. The mode is
chosen by **input completeness, NOT by who calls** — a human who supplies a
full spec also gets headless; a `card-creator-<layer>-agent` always supplies a
full spec, so it always runs headless.

(`haipipe-insight` umbrella = a router; `-explore` = read-only coverage scan.
 Neither files a card, so neither is dual-mode in this sense.)

```
              ┌────────────────────────────────────────────┐
  human ─────▶│  haipipe-insight-<layer>   (one body)       │
  (often      │  input gate:  spec complete?                │
   partial)   │     ✅ yes → SILENT  (file card, skip ASK)   │◀──── card-creator-<layer>-agent
              │     ❌ no + user → ASK only the missing      │      (always full spec → SILENT)
  agent ─────▶│     ❌ no + no user → status: blocked        │
  (full spec) │                       (name the missing src) │
              └────────────────────────────────────────────┘
                 every invocation ends with the structured return block
```


What "spec complete" means (per layer)
--------------------------------------

The BLOCKING input is always the SOURCE the card derives from — with no
source there is nothing to file. Everything else a silent run may auto-derive
(top candidate) and log a note; it never ASKs for it headless.

```
layer           BLOCKING (no source → blocked)                auto-derivable in --auto
──────────────────────────────────────────────────────────────────────────────────────
🟦 data         probe_ref present AND result.status == confirmed   slug · headline · numbers
🟩 information   --scope: ≥ 2 existing D ids                        slug · pattern · direction
🟨 knowledge     probe_ref present AND result.status == confirmed   slug · confidence · supporting I-ids (claim ← probe.claim)
🟧 wisdom        --scope: ≥ 1 existing K id                         slug · rec · rec_type · cost
```

`--project` resolves from cwd if absent (never an ASK). `NN` is always
auto-assigned (max existing + 1). A silent run that auto-derives a field logs
`note: auto-picked top candidate` into the return — never an ASK.


Rules
-----

1. **Silent (headless):** all BLOCKING inputs present → DO NOT ASK. Derive the
   rest from the sources, file the card, return.
2. **Interactive:** a BLOCKING input is missing AND a user is present → ASK
   ONLY for the missing source (not the auto-derivable fields).
3. **Missing source, no user (agent path):** do NOT hang on an ASK. Return
   `status: blocked` naming the missing source — the caller (a creator agent
   or an orchestrator) re-dispatches with it filled. NEVER fabricate a
   `source_id`, a `claim`, a `confidence`, or a number.
4. **A refusal stays a refusal.** `data` / `knowledge` still refuse a
   non-`confirmed` probe (and `knowledge` a probe with no `claim`);
   `information` still refuses < 2 D entries. In headless mode these return
   `status: blocked` (with the reason), NOT an ASK and NOT a silent pass.


Structured return (so an agent caller can consume it)
-----------------------------------------------------

Every invocation ends by emitting this block (in addition to any prose for a
human). It is the machine-readable form of each skill's "Specialist tail":

```
status:    ok | blocked | failed
card:      <insights/<LAYER>/<ID>_<slug>.md>     (on ok)
layer:     D | I | K | W
sources:   [<ids this card derives from>]
missing:   [<blocking input>, ...]               (on blocked)
note:      <one line — e.g. "auto-picked top candidate">
next:      <suggested next skill / card>
```

A `card-creator-<layer>-agent` reads `card` to know what it filed and
`sources` / `missing` to chain or re-dispatch; an interactive human reads the
prose + tail.
