# Run catalogue reference

The shared [Run catalogue](../../../run/haipipe-run/ref/run-catalog.md) owns
reusable type/profile registration and the authoritative domain index. Load it
when resolving a Run Spec key, comparing kinds, or defining an extension.
This path remains a compatibility entry point; do not keep a second semantic
catalogue here.

`table-workflow` owns the catalogue's table projection, the Run Spec × Workspace
matrix, and planned-versus-actual presentation. Use
[workflow-table-schema.md](workflow-table-schema.md) for the worked Design
specification and Cells. The current Design types are Commission, Generate,
and Verify. Delivery presents exact Verify-passed Results and adds no Run;
a failure route names the next Spec and does not authorize automatic retries.

For every presented row resolve its owner, target, actor, action, close rule,
native Result/receipt and allowed routes. Mark unresolved contracts explicitly.
Catalogue types, planned cardinality, allocated native instances and projected
cards have different grains. A human queue points to the existing decision Run
or the Run containing its human gate; it does not create a new identity.
