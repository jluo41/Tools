# Separate class, region, uncertainty, and rationale
state: ✅ SETTLED
owner: JL
method: Bind each completed annotation to four separately validated fields.

## Opening
How must final class, seven-region diagnostic position, uncertainty, and rationale be recorded so that none stands in for another?
Each item needs one semantic outcome, one map position, one statement of doubt, and one reason.
A boundary location can coexist with a firm class, while NONE records trait absence rather than doubt.
This page fixes the four-field contract and leaves only numeric scales and review cutoffs to configuration.

**Where this page sits**: QA0 defines the approved revised conception, and this page makes its label and region rules explicit for each item record.

**Why it matters**: Collapsing these fields would contaminate NONE with doubtful cases, hide which boundary an item tests, and make uncertainty impossible to audit.

**What this page decides**: The approved six-part roster covers record shape, final class, diagnostic region, uncertainty, rationale, and cross-field validation.

**What stays configurable**: The uncertainty scale, number of bands, routing cutoff, and any region sampling quota are numeric project settings rather than blocking human decisions.

## Diagram
**Four-field annotation**: each completed item carries one value in each independent semantic field.

```text
📄 ITEM RECORD
├── 🏷 class_label         H | L | N
├── 🗺 diagnostic_region   H | L | N | HL | LN | HN | HLN
├── 🌡 uncertainty         value on configured scale
└── 🧾 rationale           concise inspectable reason

🚫 FORBIDDEN ALIASES
├── ⚪ N / NONE            trait evidence absent
├── 🟡 HL · LN · HN       pairwise diagnostic boundaries
├── 🔴 HLN                 triple diagnostic junction
└── 🌡 uncertainty         doubt about the annotation
```

## Content

### 1 · The annotation record
**One item, four fields**: the record keeps semantic outcome, diagnostic position, doubt, and reason apart.

```text
📄 one completed annotation
├── 🏷 class_label
├── 🗺 diagnostic_region
├── 🌡 uncertainty
└── 🧾 rationale
```

#### 1.1 · Four required fields
(Defines the smallest complete semantic record without allowing one field to carry another field's meaning.)
A completed annotation stores `class_label`, `diagnostic_region`, `uncertainty`, and `rationale` as four named fields.
Each field is required because each answers a different question about the item.
The field names remain distinct in human-facing tables, machine-readable records, exports, and evaluation inputs.

#### 1.2 · Completion and unresolved work
(Keeps temporary workflow state outside the final class vocabulary.)
An item is complete only when all four fields contain valid values under the active project configuration.
A workflow may mark an item unresolved before completion, but unresolved is a workflow state rather than a fourth class.
An unresolved item must never be stored as N merely to satisfy the class field.

### 2 · The final class
**One semantic outcome**: H, L, and N are the only final class values.

```text
🏷 class_label
├── 🟢 H     HIGH under the trait-specific rule
├── 🔵 L     LOW under the trait-specific rule
└── ⚪ N     NONE because trait evidence is absent
```

#### 2.1 · Closed H, L, and N vocabulary
(Fixes the final outcome enum and gives NONE one semantic meaning.)
Every completed item has exactly one final class: H, L, or N.
H names HIGH, L names LOW, and N is the stored token for NONE.
HIGH and LOW follow trait-specific evidence rules rather than positive and negative sentiment alone.
NONE means the review lacks sufficient evidence of the target trait.

#### 2.2 · Final class does not encode doubt
(Separates the adjudicated outcome from confidence in that outcome.)
A final class records the best semantic judgment after applying the current guideline.
The annotation may still carry high uncertainty, but that uncertainty does not create another class or change H, L, or N.
If no final class can yet be defended, the item remains unresolved outside the class enum until review closes it.

### 3 · The seven diagnostic regions
**Three centers, three boundaries, one junction**: the region records where an item tests the current concept.

```text
🗺 diagnostic_region
├── 🟢 centers       H · L · N
├── 🟡 boundaries    HL · LN · HN
└── 🔴 junction      HLN
```

#### 3.1 · Seven valid region values
(Defines the complete region roster without treating it as a second class label.)
The three center regions H, L, and N contain items that clearly anchor the corresponding class under the current concept.
The pairwise regions HL, LN, and HN contain items that probe the named two-class boundary before final adjudication.
The HLN junction contains items for which all three classes are diagnostically relevant before final adjudication.
The region remains diagnostic metadata for sampling, error analysis, and guideline maintenance.

#### 3.2 · Region and class compatibility
(States which final outcomes can close each diagnostic position while preserving both fields.)

| `diagnostic_region` | Compatible `class_label` |
|---|---|
| H | H |
| L | L |
| N | N |
| HL | H or L |
| LN | L or N |
| HN | H or N |
| HLN | H, L, or N |

An HN boundary item therefore closes as H or N while retaining HN as its diagnostic region.
Compatibility does not merge the fields because class records the final outcome and region records the tested location.
If adjudication produces a class outside the region's compatible set, the region must be corrected rather than forcing an incoherent record.

#### 3.3 · Region assignments can change
(Keeps early diagnostic judgments from becoming permanent semantic facts.)
A region assignment may change when later dialogue clarifies the concept or exposes a different boundary.
The new region is versioned with the annotation rather than silently overwriting the earlier interpretation.
Changing region does not by itself authorize a final class change.

### 4 · The uncertainty field
**Doubt has its own channel**: uncertainty reports how unsure the annotator or executor is about the current annotation.

```text
🌡 uncertainty
├── 📏 scale          declared in project configuration
├── 🔢 value          valid point on that scale
└── 🚨 review cutoff  configurable numeric threshold
```

#### 4.1 · Meaning of uncertainty
(Defines uncertainty as doubt about a judgment rather than absence of the trait.)
The uncertainty field reports the degree of doubt attached to the current class and region judgment.
It does not report trait prevalence, evidence absence, or region membership.
A clear N center can have low uncertainty, while an HN boundary judged N can have high uncertainty.

#### 4.2 · Configurable numeric settings
(Leaves empirical calibration choices open without reopening the semantic contract.)
Project configuration declares the uncertainty scale, its direction, its allowed values, and any threshold that routes an item to review.
The number of bands or numeric precision may change between validated configurations.
Every exported value must identify the configuration or schema version that gives the number meaning.
These numeric settings can be tuned from pilot evidence without asking the human to redefine H, L, N, or the seven regions.

### 5 · The rationale field
**The reason remains inspectable**: rationale explains the judgment without becoming an uncertainty score.

```text
🧾 rationale
├── 🔎 evidence       decisive text or implication
├── ⚖️ alternative    strongest rejected class
└── 🧭 reason          center, boundary, or junction logic
```

#### 5.1 · Concise structured reason
(Makes a decision auditable without requiring hidden chain-of-thought.)
The rationale states the decisive evidence, the strongest rejected alternative, and the rule that separates the chosen class from that alternative.
A center case may use a shorter rationale when one piece of evidence clearly anchors the class.
A boundary or junction case names the competing classes and why the final class won.
The field contains an inspectable reason rather than hidden chain-of-thought.

#### 5.2 · Rationale is not uncertainty
(Prevents prose length or strength from being treated as a confidence measure.)
Rationale explains why the annotation was made, while uncertainty reports how doubtful the annotator or executor remains.
A long rationale does not imply high uncertainty, and a short rationale does not imply confidence.
Changing rationale wording must not silently alter class, region, or uncertainty.

### 6 · Cross-field validation
**Coherent without collapse**: validation checks each field and their compatibility while preserving all four values.

```text
✅ VALID RECORD       class · region · uncertainty · rationale
❌ INVALID CLASS      uncertainty bucket
❌ INVALID REGION     second final class
❌ INVALID RATIONALE  confidence surrogate
```

#### 6.1 · Valid combinations
(Shows that final class, diagnostic position, and doubt can vary independently within the compatibility law.)

| Example | `class_label` | `diagnostic_region` | `uncertainty` | Rationale focus |
|---|---:|---:|---|---|
| Clear HIGH anchor | H | H | low on active scale | Direct HIGH evidence |
| HN case judged absent | N | HN | high on active scale | Apparent evidence rejected |
| LN case judged LOW | L | LN | high on active scale | Weak but sufficient LOW evidence |
| Triple case judged HIGH | H | HLN | high on active scale | All alternatives considered |

The uncertainty terms in this table show relative positions on the active configured scale rather than fixed thresholds.
The HN and HLN rows demonstrate that a boundary or junction does not prevent one final class from being recorded.

#### 6.2 · Rejection rules
(Defines the checks that stop semantic collapse from entering data or evaluation.)
A record is invalid when `class_label` falls outside H, L, and N or `diagnostic_region` falls outside the seven-region roster.
A record is invalid when its class is incompatible with its region, its uncertainty is missing or invalid under the active configuration, or its rationale is blank.
A record is also invalid when N is described as uncertainty, when region is used as a split class, or when rationale is used as the uncertainty value.
Compatibility validation checks coherence but never derives final class from region.

## Aims

### A1 · 📄 The annotation record
- A1.1 · Every completed annotation preserves four independently named semantic fields.
  **Done when:** The rendered page requires `class_label`, `diagnostic_region`, `uncertainty`, and `rationale` without aliases.

### A2 · 🏷 The final class
- A2.1 · H, L, and N form the complete final class vocabulary, with N reserved for trait absence.
  **Done when:** No class value represents uncertainty, ambiguity, or unresolved workflow state.

### A3 · 🗺 The seven diagnostic regions
- A3.1 · Three centers, three pairwise boundaries, and one junction remain diagnostic positions rather than final outcomes.
  **Done when:** All seven values and their compatible final classes are explicit and testable.

### A4 · 🌡 The uncertainty field
- A4.1 · Uncertainty has one independent field whose numeric scale and routing cutoff are configuration settings.
  **Done when:** A reader can change numeric settings without changing the meaning of class or region.

### A5 · 🧾 The rationale field
- A5.1 · Rationale gives an inspectable reason without standing in for uncertainty.
  **Done when:** The field names decisive evidence and alternatives while uncertainty remains separate.

### A6 · ✅ Cross-field validation
- A6.1 · Validation rejects collapsed or incoherent records while allowing compatible class-region combinations.
  **Done when:** The page states field-level, compatibility, NONE, and completeness checks.

## States

### A1 · 📄 The annotation record
- ✅ A1.1 · Met; Section 1 defines four required fields and keeps unresolved workflow state outside the final class.

### A2 · 🏷 The final class
- ✅ A2.1 · Met; Section 2 fixes H, L, and N and reserves N for absence of trait evidence.

### A3 · 🗺 The seven diagnostic regions
- ✅ A3.1 · Met; Section 3 defines H, L, N, HL, LN, HN, and HLN with an explicit compatibility table.

### A4 · 🌡 The uncertainty field
- ✅ A4.1 · Met; Section 4 gives doubt its own field and delegates only numeric scale and cutoff choices to configuration.

### A5 · 🧾 The rationale field
- ✅ A5.1 · Met; Section 5 keeps the inspectable reason separate from the uncertainty value.

### A6 · ✅ Cross-field validation
- ✅ A6.1 · Met; Section 6 lists valid combinations and rejects NONE misuse, missing fields, and incompatible values.

## Files

### 🔗 Related Board Pages · what this Page READS BY SCOPE
- `constrained by · ALL` · [QA0 §6](QA-semantic-contract/QA0-the-revised-conception.md)
  QA0 Section 6 establishes that class, region, and uncertainty answer different questions.
- `constrained by · ALL` · [QA0 §7](QA-semantic-contract/QA0-the-revised-conception.md)
  QA0 Section 7 establishes the three centers, three pairwise boundaries, and triple junction.

## Law
- 260806 JL · 🧩 Class, region, uncertainty, and rationale never substitute for one another
      Every completed item records one H/L/N final class, one seven-region diagnostic position, one uncertainty value, and one rationale.
      Region identifies the center, boundary, or junction that the item probes, while class records the final semantic outcome.
      NONE means trait evidence is absent and never means that the annotator is unsure.
      Numeric uncertainty scales and routing cutoffs belong to project configuration and cannot redefine these semantic fields.

## Glossary
- 🏷 **Final class**: the adjudicated H, L, or N semantic outcome for one completed item.
- 🗺 **Diagnostic region**: one of seven positions used to describe which class center, pairwise boundary, or triple junction an item probes.
- 🌡 **Uncertainty**: the separately recorded degree of doubt about the current annotation.
- ⚪ **NONE**: the N final class used when the review lacks sufficient evidence of the target trait.

## Log
260806 · DRAFT reopened QA2 and replaced its previous-edition purpose about model-panel labeling and disagreement routing with the approved semantic field contract.
