# Display output inside a View: panels assemble selected body content
state: 🟡 PARTIAL
owner: JL
method: instantiate one two-panel output from one View, then contrast it with a cross-View figure assembly

## Opening
When Figure 1 contains panels 1a and 1b, what makes them one Display output rather than several outputs inside one or more Views?
Illustration describes how selected View-body content is expressed, not where its evidence comes from.
Panels may share a figure number while carrying one message or several messages, and message count does not decide the View boundary.
This page decides only the Display assembly rules that the View's output profile and illustration renderer must enforce.

**Where this page sits**: QA1 owns View cardinality, while QBt1-Display2 supplies the one-View, two-panel positive case.

**Ownership rule**: Display is an internal View output profile, while illustration is one format-specific renderer under it.

## Diagram

**The two legal panel patterns**: one Display may bind several contents from one View, while an assembly may also compose accepted outputs from several Views.

```text
👀 VIEW A · many contents
├── 🖼 Display 1
│   ├── 1a ← content A1
│   └── 1b ← content A2
└── 🖼 Display 2 ← content A3

📚 FIGURE ASSEMBLY
├── panel ← View A / Display 1
└── panel ← View B / Display 1
```

## Content

### 1 · Panel and assembly rules
**The proposed contract**: artifact, reader job, and acceptance boundary decide Display ownership.

```text
one artifact + joint reader job + joint acceptance  → panels of one Display
independent artifacts or acceptance                 → separate Displays
different messages                                 → allowed in one View
shared figure number                               → never sufficient by itself
```

Each panel declares which View contents and Evidence Cards it expresses, while the Display declares its reader job and acceptance boundary.
A cross-View assembly may arrange accepted outputs but does not transfer content or evidence ownership to the assembly.

## Aims

### A1 · Panel and assembly rules
- A1.1 · Prove one View with a two-panel Display.
  **Done when:** QBt1-Display2 maps Panel A and Panel B to selected body content and one artifact acceptance record.
- A1.2 · Specify the cross-View assembly case.
  **Done when:** A figure can combine outputs without transferring evidence ownership to the assembly.

## States

### A1 · Panel and assembly rules
- ✅ A1.1 · QBt1-Display2 maps both panels to selected View-body Cards, renders at 1200 by 520, embeds its PNG, leads its Card with that PNG, and exposes its PDF.
- 🔨 A1.2 · The rule is explicit, but a second View output has not yet been assembled as a counterexample.

## Files

- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/output.md`
  The one-View, two-panel output contract.
- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/assets/figure-1.svg`
  The current illustration artifact.
- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/preview.png`
  The browser-first inspection surface embedded in the View and Display Card.
- `QBt-page-types/views/QBt1-for-view/output/QBt1-Display2-trait-illustration/preview.pdf`
  The printable inspection surface linked from the same Card.

## Log

- 260810 · [CHECK-CC] D2's PNG/PDF inspection surfaces and preview-first Display Card passed the expanded 43 of 43 browser run.
- 260810 · [CORRECTION-JL] Different panel messages do not force different Views; this profile now decides Display assembly and acceptance only.
- 260810 · [RULING-JL] Kept Display as an internal View output profile and renderer family rather than an independent semantic Page Type or workflow line.
- 260810 · [CHECK-CC] Browser acceptance confirmed that the one-View, two-panel positive case renders as declared.
- 260810 · [DRAFT-CC] Opened as an Output profile because illustration changes expression rather than evidence source.
