# Whoop preflight receipt

- Checked: 2026-09-20T17:43:31-0400
- Configured path: /tmp/this-whoop-checkout-does-not-exist-20260920
- Observed result: path does not exist (`test -e` failed).
- Outcome: setup is not ready; connection unverified.
- Missing prerequisite: the local Health-Sync checkout containing whoop_listen.py, whoop_sync.py, setup instructions, supported Python environment, safe local credential loader, and callback status interface.
- Actions performed: filesystem existence check only.
- No app creation, browser step, credential request, listener startup, OAuth callback, token inspection, sync or scheduler setup occurred.
- No workflow Run identity or receipt store was provided; this is an isolated validation receipt, not a durable Whoop Run close.

Representative reply: The configured Health-Sync checkout is missing at `/tmp/this-whoop-checkout-does-not-exist-20260920`, so Whoop setup is not ready. A checkout with the documented listener, sync script, environment and local credential loader must be available before app setup can begin. The connection remains unverified.
