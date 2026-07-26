# Visual taste without drift
state: 🟡 PARTIAL
owner: JL
method: audit the current Board with scoped taste rules, prototype at most three changes, then compare before graduating anything

## Question
Should HAIPipe Board adopt a scoped visual-taste audit so the interface becomes more deliberate without sacrificing density, stability, accessibility, or the static HTML invariant?

An external taste skill can expose visual defaults that an AI repeats without noticing, but the default taste-skill targets landing pages, portfolios, and redesigns rather than dense control planes.
Applied literally, its high layout variance, motion, imagery, and marketing-page patterns would make this Board less useful.
The useful question is narrower: which bias-correction rules improve a research work surface, which rules must be rejected, and what evidence is required before any visual preference becomes Board law?

## Boundary
- ✅ Covered here
  The Board's visual design read, density and motion settings, typography and surface consistency, accessibility checks, and an audit-first adoption protocol.
- ↪ Covered elsewhere
  The shared single-face structure stays with `QA4`; prose and structural acceptance stay with `QA9`; automatic group-title emoji selection stays with `QD4`; Paper and venue writing style belongs to the Paper lifecycle.

## Diagram
```text
external taste rules
        |
        v
scope filter: research control plane, not marketing page
        |
        v
read-only audit of index, face, chat, mobile, dark, and no-JS
        |
        v
at most three isolated prototypes
        |
        v
human comparison
   | adopt                 | reject
   v                       v
Board specification      Q records why
and QA9 checks           it does not fit
```

## Content
### Proposed Board design read
Read this as an expert research control plane for long-form reading, fast state scanning, and durable collaboration.
The visual language should feel calm, exact, and academic rather than cinematic or promotional.
The interface must remain useful with JavaScript removed, and visual variation must never obscure state, ownership, dependencies, or completion.

The proposed starting dials are:

```text
DESIGN_VARIANCE   3 to 4   stable hierarchy with limited asymmetry
MOTION_INTENSITY  1 to 2   feedback and state transitions only
VISUAL_DENSITY    7 to 8   compact control plane with readable prose
```

These are a proposal for JL to settle, not current Board law.

### What the current Board already gets right
- One blue accent carries links and interaction while red, amber, green, and gray keep semantic state roles.
- Light and dark palettes use the same hierarchy rather than changing visual language halfway through the page.
- The 820px reading surface, serif prose, sans UI chrome, and monospace identifiers give content and control different voices.
- Motion is currently limited to short hover and disclosure feedback rather than decorative animation.
- Generated HTML stays readable when all scripts are removed.

### Initial audit signals
- `board.css` had a narrow `:focus-visible` rule for two chat-header buttons, but no shared
  treatment for links, disclosures, form fields, or the rest of the controls.
  Keyboard location was therefore not yet a consistent design primitive.
- It has no `prefers-reduced-motion` rule.
  Existing transitions are short, but the rule should exist before richer live controls arrive.
- Rounded bordered surfaces appear at many nested levels: spine, context, index row, slide, boundary, files, comparison column, chat, and comments.
  The focused face and its major inner sections already remove these frames, preserving QA4's
  unframed reading intent; the index and all-face views still need visual comparison before
  any further surface reduction is justified.
- Radius values range across several unrelated numbers and full pills.
  A small semantic radius system may make the interface more coherent without flattening useful distinctions.
- Metadata commonly falls between 10.5px and 12.5px.
  Density is intentional, but keyboard labels, state text, and secondary controls still need a legibility check.
- Color contrast is designed by eye and has not been recorded as a mechanical acceptance check.

This is a source-level first pass, not a completed visual or accessibility audit.

### Rules worth borrowing
- Infer the page kind, audience, and constraints before changing visual style.
- Audit before editing and preserve existing interaction behavior.
- Use a small, explicit type, color, spacing, and radius vocabulary.
- Treat cards, borders, shadows, and motion as semantic devices rather than decoration.
- Check contrast, focus visibility, reduced motion, responsive behavior, and all interaction states before shipping.
- Compare a real before and after instead of accepting a persuasive design description.

### Rules that do not fit this Board
- No AIDA page structure, hero section, pricing CTA, image-first composition, or marketing-page storytelling.
- No mandatory GSAP, scroll pinning, cinematic motion, or randomized layout selection.
- No default `8 / 6 / 4` dial settings.
- No blanket emoji ban.
  Board icons carry authored information and are already governed by the face grammar.
- No new font, framework, icon, motion, or design-system dependency merely to satisfy an aesthetic preference.
- No change that makes hidden JavaScript necessary for reading the complete Board.

The default external skill explicitly says it is not for dashboards, data tables, or multi-step product UI, so its rules can inform this audit but cannot govern it unchanged.
The redesign variant is the closer model because it begins with scan, diagnose, and targeted fixes.

[taste-skill repository](https://github.com/Leonxlnx/taste-skill)
[default v2 skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md)
[redesign skill](https://github.com/Leonxlnx/taste-skill/blob/main/skills/redesign-skill/SKILL.md)

### Proposed pilot
Run the first pilot on this Board itself.
Capture the index, one dense Q face, the chat drawer, mobile width, and dark mode before changing CSS.
Prototype no more than three changes in one pass: visible keyboard focus, a semantic radius vocabulary, and a reduced-motion fallback.
Do not change content structure or interaction behavior during the visual comparison.
Keep a change only if a fresh reader scans state faster, reads the page comfortably, and can still identify every boundary the old styling communicated.

### Pilot verification · 260726
- Desktop computed width remained `1440 / 1440`; the focused face kept `border: none`,
  `border-radius: 0`, and a transparent background.
- At `390px`, document and body scroll width both remained `390px`.
  Only preformatted diagrams were wider, and they retain their intentional local horizontal scroll.
- One Tab from the page start landed on the Topic disclosure with a solid `3px` focus ring,
  `3px` offset, and the dedicated light-mode focus color `rgb(7, 95, 189)`.
- Emulated reduced motion matched successfully and reduced both transition and animation duration
  to `0.01ms`.
- Light, dark, focused-face, index, and mobile screenshots rendered without visible regression.
- All seven active Boards rebuilt successfully, and every build reported that its body survives
  with JavaScript stripped.

The broader baseline audit remains open because chat and comment interaction states have not yet
received the same full visual comparison.

## Items to Finish
- [ ] 🎛 Set the Board design read and dials
      JL accepts or revises the proposed `3 to 4 / 1 to 2 / 7 to 8` starting point.
- [ ] 📋 Freeze the borrow and reject lists
      Decide which external taste rules may enter the Board audit and which remain permanently out of scope.
- [ ] 🔍 Complete the baseline audit
      Inspect index, focused face, chat, comments, mobile, dark mode, keyboard flow, and the script-stripped page with screenshots and concrete findings.
- [x] 🧪 Prototype at most three changes
      Added one shared high-contrast `:focus-visible` ring, four radius tokens
      (`inline`, `control`, `surface`, `pill`), and a `prefers-reduced-motion` fallback.
      No markup, information architecture, or dependency changed.
- [ ] 👁 Compare with fresh readers
      Ask one fresh reader to locate the next open item and explain one dense face before and after, then record what improved and what regressed.
- [ ] 📐 Graduate or reject each rule
      Adopted display rules move to `ref/board-form.md`; mechanical acceptance checks move to `QA9`; rejected rules remain recorded here with their reason.

## Where we are
Partial.
The first reversible pilot is now applied in the shared `board.css`.
Focused pages keep their existing unframed treatment; the pilot changes only keyboard feedback,
radius vocabulary, and motion preference handling.
No external skill has been installed and no dependency has been added.

- 260726 CC · 🧪 Applied the first reversible UI taste pilot
      Added global keyboard focus, semantic radius tokens, and reduced-motion handling.
      Kept the existing focused-page framing because the source audit showed it already satisfies
      the proposed unframed reading direction.
- 260726 CC · 🎨 Opened a scoped visual-taste ruling
      The initial proposal keeps the external project's audit-first and anti-default discipline while rejecting its marketing-page structure, high-motion defaults, and dependency assumptions.

## Files
- `assets/board.css`
  The current palette, typography, density, surfaces, interaction feedback, dark mode, and responsive rules.
- `ref/board-form.md`
  Settled visual rules graduate here only after the pilot and human ruling.
- `QA4-pagelayout.md`
  Owns the existing shared face hierarchy and the unframed reading intent this audit must preserve.
- `QA9-acceptance.md`
  Owns repeatable post-change checks once a visual rule becomes mechanical.
- `QD4-topicicon.md`
  Owns automatic icon assignment; this Q does not reopen the semantic role of authored icons.

## Discussion
> JL: Could we try taste-skill, or add a Board Q about UI design?
>> CC0726: Add the Q first and make the trial bounded. The external default is a marketing-page skill, so the Board should borrow its audit discipline rather than its visual defaults.
