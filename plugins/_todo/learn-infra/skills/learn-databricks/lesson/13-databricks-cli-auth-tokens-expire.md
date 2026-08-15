# Lesson 13: Databricks CLI Auth Tokens Expire

## The Problem

Databricks CLI OAuth tokens expire after ~1 hour. When expired, all CLI and SDK operations fail:

```
Error: A new access token could not be retrieved because the
refresh token is invalid. To reauthenticate, run:
  $ databricks auth login --profile cdhai-new
```

This also affects Python scripts using `databricks.sdk.WorkspaceClient()` and `mlflow` with `tracking_uri="databricks"`, since they rely on the same token cache.

## The Fix

Re-authenticate interactively (requires browser):
```bash
databricks auth login --profile cdhai-new
```

This opens a browser OAuth flow. Cannot be done non-interactively (no `--token` flag for OAuth profiles).

## Tips

- Run `databricks auth token --profile cdhai-new` to check token validity before long operations
- Token TTL is ~1 hour; plan accordingly for multi-step deployments
- The MLflow SDK and Databricks SDK both read from `~/.databrickscfg` — re-auth once fixes both
- If running a script that takes >1 hour (e.g., large artifact upload + endpoint creation), the token may expire mid-run

## When to Check

- At the start of any Databricks session
- Before long-running deployment scripts
- When any `databricks` CLI command or SDK call returns auth errors

## Source

REACH-ADHD deployment, 2026-06-26. Token expired between sessions (Jun 20 → Jun 26).
