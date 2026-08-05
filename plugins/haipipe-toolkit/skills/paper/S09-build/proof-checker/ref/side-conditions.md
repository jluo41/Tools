Extracted from haipipe-paper-proof-checker/SKILL.md; referenced from its Side-Condition Checklists section.

## Side-Condition Checklists for Common Theorems

When the proof invokes any of the following, require explicit verification of ALL listed conditions:

| Theorem | Required Conditions |
|---------|-------------------|
| **DCT** (Dominated Convergence) | Pointwise a.e. convergence + integrable dominating function |
| **MCT** (Monotone Convergence) | Monotone increasing + non-negative |
| **Fubini/Tonelli** | Product measurability + integrability (Fubini) or non-negative (Tonelli) |
| **Leibniz integral rule** | Continuity of integrand + dominating function for derivative |
| **Implicit Function Theorem** | Continuous differentiability + non-singular Jacobian |
| **Taylor with remainder** | Sufficient differentiability + remainder form (Lagrange/integral) |
| **Jensen's inequality** | Convexity of function + integrability |
| **Cauchy-Schwarz** | Correct inner product space + integrability of both factors |
| **Weyl/Davis-Kahan** | Symmetry/Hermiticity + perturbation bound conditions |
| **Analytic continuation** | Domain connectivity + identity theorem conditions |
| **WLOG reduction** | Invariance under claimed symmetry + reduction is reversible |
