---
name: whoop-connect
description: "Guide the user through a Whoop connection and token verification. This skill does not configure or promise a daily sync. Use when the user says connect my whoop, link whoop, set up whoop, or /whoop-connect."
metadata:
  version: "0.2.1"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: whoop-connect
====================

Guides a user through a bounded Whoop connection task. App creation, local
credential setup, OAuth consent, and token verification are Steps inside that
task. A daily sync is a separate capability and is not configured here.

Trigger phrases:
  /whoop-connect
  "connect my whoop"
  "set up whoop"
  "link whoop"

---

## Overview

This skill guides one Whoop-connection Run, when the local Health-Sync checkout
and its supported credential method are available. Its internal Steps are:

1. **App creation** — guide user to developer.whoop.com to create their free developer app
2. **Auth flow** — the user stores credentials locally, starts the documented callback server, and approves access
3. **Confirmation** — verify tokens were saved; report scheduling only if a separate scheduler is configured and verified

The Run target is authorization of this user's Whoop account for the verified
local checkout. Close it only after a fresh OAuth callback succeeds and the
token file is created or updated. Record a non-secret receipt with the outcome,
check time, verified path, and evidence; never include token contents. If the
invoking workflow provides no Run identity or receipt store, do not invent one
or claim a durable Run close. A daily scheduler has its own target and receipt.

The user creates the app and approves access in their browser. They must enter
credentials through a local prompt or secret store. Never ask them to paste a
Client ID or Client Secret into this chat, Discord, a command line, or a log.
If the checkout has no documented local credential method, stop and explain
that setup is not ready; do not improvise a way to transmit the secret.

---

## Preflight — before asking the user to create an app

Resolve the Health-Sync checkout from an existing configured path or ask for
its location. Confirm `whoop_listen.py`, `whoop_sync.py`, setup instructions,
the Python environment, and the documented local credential loader exist.
This skill does not ship that application. If it is missing, explain the
missing prerequisite before asking the user to configure a developer app.

Read the listener configuration to determine its exact redirect URI and the
status evidence it produces for one OAuth attempt. Confirm the browser and
callback host can reach that endpoint. Do not assume localhost:8080: a remote
listener or another port may require a different configured URI. Record the
verified URI and non-secret startup/status commands. If a safe credential
loader or callback status interface is absent, setup is not ready.

Set `WHOOP_PROJECT_DIR` to the directory containing the verified scripts and
`WHOOP_PYTHON` to its verified interpreter. Restore these non-secret values in
any new shell. Keep credentials in the documented local store/environment,
never command arguments, shell history, chat, or pasted logs.

## Step 1 — Developer App Setup

Greet the user warmly. Explain in plain language:

> "To connect your Whoop, you need a free developer app on Whoop's website.
> This is like giving me a key to read your data — you stay in full control
> and can revoke it any time."

Then guide them step by step:

**Step 1.1** — Send this message:
> "Let's start. Please open this link:
> 👉 https://developer.whoop.com
>
> Sign in with your Whoop account, then click **Create App**."
>
> "Tell me when you see the app creation form."

**Step 1.2** — Once they confirm, say:
> "Great! Fill in any name you like (e.g. 'My Health Bot').
>
> Set **Redirect URI** to the exact callback URI we verified in your local
> listener configuration: **[insert the verified URI]**.
> Then click **Save** or **Create**."
>
> "Tell me when it's done."

**Step 1.3** — Say:
> "Perfect! Now you should see your **Client ID** and **Client Secret**.
> Keep both on your machine and enter them only through the local credential
> prompt or secret store documented by your Health-Sync checkout. Do not send
> either value in this chat. Tell me when local setup confirms they were stored.
>
> 🔒 I will not handle or repeat either value."

Do not request, extract, repeat, or save credentials supplied in chat. If the
user accidentally shares a secret, do not quote it back; advise them to rotate
it in the Whoop developer console and configure the replacement locally.

---

## Step 2 — Authentication

Use the checkout and credential method verified in preflight. Once the user
confirms local storage, start only its documented listener command. Verify the
process is live and obtain its non-secret consent URL from the documented
status interface. Do not dump the auth log or expose credential values.

**Step 2.1** — Send the user the link:
> "Almost there! Click this link, log in to Whoop, then click **Allow**:
>
> 🔗 [the auth URL from the output]
>
> Your browser will show a confirmation page. Come back here when you see it."

**Step 2.2** — After the user says they're done, verify that this OAuth
callback reported success and that `tokens.json` was created or updated inside
the verified checkout. Inspect only callback status and file metadata; do not
print token contents or dump auth logs into chat. If the callback status or
fresh file update is missing, report the connection as unverified and ask the
user to finish browser consent. A pre-existing token file alone is not proof
that this connection Run succeeded.

---

## Step 3 — Confirmation

Once the current callback succeeds and the token file is freshly stored,
report only what those checks prove:

> "✅ This Whoop authorization callback succeeded and the local token file was
> updated. I have not confirmed a token refresh, data sync, or daily schedule.
>
> To pull today's data, ask for **sync whoop** when the local sync command is
> available.
>
> A daily schedule has not been configured by this connection flow."

Only say that daily sync is scheduled after creating or locating the scheduler,
checking its active job, and observing a successful sync receipt. Token presence
alone proves neither authorization for this Run, token refresh, data sync, nor
scheduling.

---

## Handling "sync whoop"

If the user says "sync whoop" or "pull my whoop data":

Resolve the verified checkout and confirm that `whoop_sync.py` exists before
running the checkout's documented command. Confirm that its documented
credential loader reads local credentials without printing them; if that
cannot be established, ask the user to run the documented sync locally rather
than guessing how to load secrets. Treat one requested sync as its own bounded
Run only when it has an execution identity and result/receipt.

Run:
```bash
cd "$WHOOP_PROJECT_DIR"
"$WHOOP_PYTHON" whoop_sync.py
```

Read only the non-secret sync result and present the summary in a friendly,
readable format. Never paste a full auth or sync log into chat.
Summarize the recorded values and timestamps without labeling a health value
as good or bad without appropriate context.

---

## Error Handling

- **"Missing credentials"** — return to Step 1 and use the local credential setup; never request values in chat
- **"Token refresh failed"** — tokens expired; ask them to renew access through the local setup
- **Configured callback port in use** — identify the local conflict; use the
  checkout's supported port configuration and update the registered URI to
  match. Do not close unrelated applications automatically.
- **"Invalid client"** error — ask them to correct credentials through the local setup; never ask them to re-paste a secret
