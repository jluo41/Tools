# OhioT1DM logs a CLASS, not a product

service: describe-medication
HTTP 200

5,026 rows. MedicationID is EMPTY -- zero distinct values in the whole cohort. Ingredient stays null because no product directory can resolve a therapeutic class, and MedSource says class_only rather than blaming the bank. IsInsulin is still true, so the row routes to describe-insulin.
