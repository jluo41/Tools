# Lesson 08: Check pandas Version Compatibility in Your Runtime

## The Problem

Different Databricks Runtimes ship different pandas versions, and the API differences between pandas 1.5.3 and 2.x cause silent data corruption or hard crashes:

| Runtime | pandas version |
|---------|---------------|
| 15.4 LTS | 1.5.3 |
| 16.4 LTS | 2.2.x |
| 17.3 LTS ML | 2.x |

The haipipe codebase was written for pandas 2.x. Running on Runtime 15.4 caused three distinct failures.

## The Breaking Changes

### 1. `value_counts().reset_index()` column naming

```python
# pandas 2.x — new column is named 'count'
df['col'].value_counts().reset_index()
#   col  count
# 0  A    5
# 1  B    3

# pandas 1.5.3 — new column keeps the original column name
df['col'].value_counts().reset_index()
#   index  col
# 0  A      5
# 1  B      3
```

**Fix**: detect column name dynamically instead of hardcoding `'count'`:
```python
df_results = df_results.reset_index()
rec_col = 'count' if 'count' in df_results.columns else \
    [c for c in df_results.columns if c != id_col][0]
```

### 2. `pivot()` with duplicate entries

```python
# pandas 2.x — silently handles duplicates in some cases
df.pivot(index='PID', columns='Name', values='Count')

# pandas 1.5.3 — raises ValueError on any duplicate index/column pair
# ValueError: Index contains duplicate entries, cannot reshape
```

**Fix**: use `pivot_table(aggfunc='sum')` which explicitly handles duplicates:
```python
df.pivot_table(index='PID', columns='Name', values='Count', aggfunc='sum')
```

### 3. `sum()` of mixed str/int columns

```python
# pandas 2.x — auto-coerces types
df[numeric_cols].fillna(0).sum(axis=1)  # works

# pandas 1.5.3 — raises TypeError if any column is object dtype
# TypeError: '>' not supported between instances of 'str' and 'int'
```

**Fix**: explicit type coercion:
```python
rec_count = pd.to_numeric(df[cols].fillna(0).sum(axis=1), errors='coerce').fillna(0)
```

### 4. `.str` accessor on non-string columns

```python
# pandas 2.x — more lenient with .str accessor on object columns
df['col'].str.contains(',')

# pandas 1.5.3 — strict: raises AttributeError if column has non-string values
# AttributeError: Can only use .str accessor with string values!
```

**Fix**: cast to string first, or use pure Python:
```python
df['col'] = df['col'].astype(str).fillna('')
n_overlap = sum(',' in str(v) for v in df['col'])
```

## The Best Solution

**Use Runtime 16.4+ LTS** (or 17.3 LTS ML). Don't fight pandas 1.5.3 — upgrade the Runtime.

If you must support both versions, the defensive patterns above work across both.

## Files That Were Fixed in haipipe

| File | Change |
|------|--------|
| `haipipe/record_base/builder/human.py` | pivot_table, dynamic col name, pd.to_numeric |
| `haifn/fn_case/fn_trigger/REACHADHDLabeledVisit.py` | astype(str), pure Python `in` check |

## When to Apply

- Before running any haipipe pipeline on Databricks, check the Runtime's pandas version: `python -c "import pandas; print(pandas.__version__)"`
- If pandas < 2.0, switch to Runtime 16.4+ or apply the defensive patterns
