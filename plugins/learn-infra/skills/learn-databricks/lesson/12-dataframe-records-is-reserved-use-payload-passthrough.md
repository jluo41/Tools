# Lesson 12: "dataframe_records" Is Reserved — Use Payload Passthrough

## The Problem

When sending a JSON payload to a Databricks Model Serving endpoint, the top-level key `"dataframe_records"` is **reserved** by Model Serving. It auto-extracts the array as DataFrame rows and discards all other top-level keys.

If your payload looks like:
```json
{
  "models": "MyModel",
  "source_tables": { ... },
  "dataframe_records": [{"col1": "val1"}]
}
```

Model Serving:
1. Extracts `dataframe_records` → DataFrame with columns `[col1]`
2. **Drops** `models` and `source_tables` entirely
3. Enforces signature schema against `[col1]` → schema mismatch → `BAD_REQUEST`

## Why It Happens

Databricks Model Serving has special handling for these top-level keys:
- `"dataframe_records"` → convert to DataFrame (row-oriented)
- `"dataframe_split"` → convert to DataFrame (split-oriented)
- `"instances"` → pass as list
- `"inputs"` → pass as dict

Any top-level key that isn't one of these is silently ignored. You cannot have `"models"` as a sibling of `"dataframe_records"`.

## The Fix: Payload Column Passthrough

Serialize the **entire** payload as a JSON string in a single column:

**Signature:**
```python
ModelSignature(
    inputs=Schema([ColSpec('string', 'payload')]),
    outputs=Schema([ColSpec('string', 'result')]),
)
```

**Client sends:**
```json
{"dataframe_records": [{"payload": "{\"models\":\"MyModel\",\"source_tables\":{...},\"dataframe_records\":[...]}"}]}
```

**predict() deserializes:**
```python
def _prepare_payload(self, model_input):
    if isinstance(model_input, pd.DataFrame) and 'payload' in model_input.columns:
        return json.loads(model_input.iloc[0]['payload'])
```

## When to Check

- Any PythonModel with nested/complex JSON input (not flat tabular)
- Any payload that has `dataframe_records` alongside other keys
- EHR payloads, multi-table joins, nested configs

## The General Rule

> If your input is nested or not a flat table, use a single string column and serialize.

```
Signature:  ColSpec("string", "payload")
Client:     {"dataframe_records": [{"payload": "<json>"}]}
predict():  json.loads(input["payload"])
```

## Source

REACH-ADHD endpoint deployment, 2026-06-26. v1 failed with BAD_REQUEST, v2 (passthrough) worked. Issue #11 in DATABRICKS_ISSUES.md.
