---
name: haipipe-page-evidence
description: >-
  The EVIDENCE phase contract for a Board Page: land every support item the
  approved outline promised into the plugin that owns it — citations in
  bibex/, Task or Discovery answers and values in probe/, frozen display
  material in display/. Never writes Content. Trigger: page evidence, EVIDENCE
  phase, bind an answer, probe value, display intake, /haipipe-page-evidence.
metadata:
  version: "0.12.0"
  last_updated: "2026-08-20"
---

# /haipipe-page-evidence · land support before prose uses it

EVIDENCE changes what a Page can safely know. It does not decide the argument
and does not write a sentence of `## Content`.

Load contracts in this order:

```text
haipipe-page
  → matching Page Type
  → haipipe-page-evidence
  → page-local plugin for each promised support item
  → haipipe-probe QA branch only when an answer crosses from Task or Discovery
```

## ⚡ Phase card

```text
READS    target Page · approved outline version · raised local cards
WRITES   <page>/bibex/ · <page>/probe/ · <page>/display/
NEVER    target prose · purpose · Aims · bank-owned QA files by hand
EXITS    OUTLINE when all promised support is pointable; otherwise EVIDENCE/HOLD
HUMAN    verifies citation · reads probe answer · accepts display at CHECK
```

PageX belongs to the Probe family but not to the EVIDENCE phase. It already
supplied accepted Page context while OUTLINE was designed. EVIDENCE is for
support that still must be made or bound.

## 🧾 Three support lanes

```text
outline mark   local owner                         bindable when
──────────────────────────────────────────────────────────────────────────
📚 citation    <page>/bibex/                       key resolves; source is
                                                   transcribed, not invented
🧮 value       <page>/probe/PP<NN>-<slug>/         exact QA target + A-executor +
                                                   proof/value address resolve
🖼 display     <page>/display/<unit>/               frozen intake + recipe/assets +
                                                   preview.pdf are present
```

The plugins own their schemas. This phase coordinates their landing and returns
a receipt; it does not create a second evidence Page, `E0/E<n>` divisions,
`1-probes/`, or Paper S03/S04 stages.

## 📚 Citation lane

Load `../../page-plugins/haipipe-plugin-bibex`.

- A machine may subset or transcribe a real bibliographic record; it never
  composes one from memory.
- Preserve the source and key so later prose can cite it deterministically.
- `verified` is a human gate. EVIDENCE may report it missing but may not tick it.
- If the outline's requested claim and the source disagree, preserve the source
  and return to OUTLINE. Do not bend the citation to the claim.

## 🧮 Value lane

Load `haipipe-probe` and `../../page-plugins/haipipe-plugin-probe` only for an
obligation whose source is a Task or Discovery folder.

PROBE already created the local card and ran ORGANIZE, MATCH, and DISPATCH.
EVIDENCE owns the return half:

```text
④ POINT       bind card.md target: to the exact bank QA file
⑤ INTERPRET   preserve A-executor verbatim and write consumer/a-consumer.md
BIND          pull allowed aggregate proof and allocate PP<NN>.v<n> values
```

One answer may yield many values. A sentence-level value is pointable only as
`PP<NN>.v<n>`, whose row names the exact proof file and field. Never pull
row-level data, identifiers, or PHI into a Page.

`answered` is machine completion; `read` is the human gate. EVIDENCE may write
the Page-specific interpretation in `consumer/a-consumer.md`, but it does not
write target Page prose and cannot mark `read`. A changed target, proof, or
A-consumer invalidates an earlier read gate.

## 🖼 Display lane

Load `../../page-plugins/haipipe-plugin-display` and the renderer named by the
unit. EVIDENCE owns the material and drawing, not the prose that discusses it:

```text
① INTAKE   freeze the accepted source material into intake/
② RENDER   named renderer writes its recipe/candidates
③ PICK     record the selected candidate when the plugin calls for one
④ BUILD    create assets, float source, and preview.pdf
⑤ ACCEPT   human gate at CHECK; never ticked here
```

For a data display, intake freezes from probe proof or another declared,
non-sensitive source. For a conceptual display, intake lists the exact source
Pages/files and versions. A folder without intake is not evidence; frozen intake
without a preview is a HOLD.

## 🔗 Evidence bundle

For each approved outline point, expose a derived bundle rather than writing a
new artifact:

```text
C3.P1.B4
  ├─ citations      bibex keys + verification state
  ├─ values         PP ids + target path + proof manifest + read state
  ├─ displays       unit id + frozen intake + preview + acceptance state
  └─ prose          still absent until DRAFT/REVISE
```

The outline address is stable. Local cards point back with `serves:`. EVIDENCE
does not edit the frozen outline to pre-author card ids; the OUTLINE fold may
append derived ids after cards exist.

## 🔀 Exit and routing

The exit test is support, not prose:

```text
every promised citation resolves,
every promised Task/Discovery question has an exact local card and bank target,
every used value has a PP<NN>.v<n> proof address,
and every declared display is built and previewable.
```

Route the result:

```text
all support pointable                      → OUTLINE
answer changes claim, order, or allocation → OUTLINE with the conflict named
authorized question still unresolved      → EVIDENCE again
no allowed route can answer it             → HOLD with reason
```

EVIDENCE always returns to OUTLINE because the plan must absorb the answer and
recheck coverage, address, value, and shape before drafting. It never routes
directly to DRAFT, REVISE, or CLOSE.

## 📖 Read economy

Read fully only the target Page, approved outline, and cards that changed. Trust
unchanged card summaries except for one spot check. Scope checker output to the
target Page and keep build logs out of the reasoning context.

## 🧾 RUN receipt

When called by RUN, follow `../haipipe-page-workflow/ref/page-run-contract.md`
and add:

```text
reason:       unsupported outline obligations addressed
cards:        one row per citation, probe card, and display unit changed
targets:      exact bank QA paths and bibex keys
values:       PP<NN>.v<n> bindings created or revalidated
renderers:    display unit → renderer → preview path
human_gates:  verified/read/accepted states, never synthesized
limits:       support still absent or weaker than the outline promised
route:        OUTLINE | EVIDENCE | HOLD
reopens:      true when the returned support changes purpose, Aim, or shape
```

The Page source hash may remain unchanged because EVIDENCE normally writes only
plugin surfaces. The receipt must still name every artifact it landed.
