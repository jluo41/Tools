# Issue Taxonomy (20 categories, 4 groups)

Extracted from haipipe-paper-proof-checker/SKILL.md; referenced from its Issue Taxonomy section.

### Group A: Logic & Proof Structure

| Category | Description | Example |
|----------|-------------|---------|
| **UNJUSTIFIED_ASSERTION** | Claim stated without proof or reference | "The Hessian splits into Gram blocks" |
| **UNPROVEN_SUBCLAIM** | "Clearly" / "it follows" hides a nontrivial lemma | "By symmetry, the cross-terms vanish" without checking |
| **QUANTIFIER_ERROR** | Wrong order ∀/∃, missing "for sufficiently small κ" | "For all π, there exists ε" vs "there exists ε for all π" |
| **IMPLICATION_REVERSAL** | Uses (A⇒B) as (B⇒A), or claims equivalence with only one direction | |
| **CASE_INCOMPLETE** | Misses boundary/degenerate cases | Singular covariance, zero weight, non-unique argmin |
| **CIRCULAR_DEPENDENCY** | Lemma uses theorem that depends on it | |
| **LOGICAL_GAP** | A step is not justified by what precedes it | B=Θ(1) → β_K=0 without analyzing W |

### Group B: Analysis & Measure Theory

| Category | Description | Example |
|----------|-------------|---------|
| **ILLEGAL_INTERCHANGE** | Swaps limit/expectation/derivative/integral without DCT/MCT/Fubini | Differentiating under E without domination |
| **NONUNIFORM_CONVERGENCE** | Pointwise convergence used as uniform | sup and limit swapped |
| **MISSING_DOMINATION** | DCT cited but no dominating function given | |
| **INTEGRABILITY_GAP** | Uses E|X|^p without proving/assuming finite moments | |
| **REGULARITY_GAP** | Differentiability/Lipschitz/convexity used but not established | |
| **STOCHASTIC_MODE_CONFUSION** | Mixes a.s./in prob./in L²/in expectation | |

### Group C: Model & Parameter Tracking

| Category | Description | Example |
|----------|-------------|---------|
| **MISSING_DERIVATION** | A quantity is used but never derived from the model | Risk functional with undefined B, W |
| **HIDDEN_ASSUMPTION** | Proof silently uses a condition not in the theorem | Gaussianity assumed but not stated |
| **INSUFFICIENT_ASSUMPTION** | Hypotheses too weak for proof (counterexample exists) | Moment conditions admitting 2-point distributions |
| **DIMENSION_TRACKING** | Parameter dependence (d, n, K, ...) not explicit | d enters only through κ |
| **NORMALIZATION_MISMATCH** | Coordinate/scaling conventions inconsistent | Rescaled vs raw coordinates |
| **CONSTANT_DEPENDENCE_HIDDEN** | "C" depends on d,n,K but treated as universal | |

### Group D: Scope & Claims

| Category | Description | Example |
|----------|-------------|---------|
| **SCOPE_OVERCLAIM** | Conclusion stated more broadly than proof supports | "β_K=0" with only generic overlap |
| **REFERENCE_MISMATCH** | Cited theorem's hypotheses not verified at point of use | |
