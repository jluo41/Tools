---
name: whoop-connect
description: "Connect a Whoop wearable device to the bot. Guides the user step-by-step through creating a Whoop developer app, OAuth login, and daily sync setup. Use when the user says connect my whoop, link whoop, set up whoop, or /whoop-connect."
---

Skill: whoop-connect
====================

Guides a user through connecting their Whoop account to the bot via a
friendly, step-by-step Discord conversation. No terminal or Python knowledge
required on the user's part.

Trigger phrases:
  /whoop-connect
  "connect my whoop"
  "set up whoop"
  "link whoop"

---

## Overview

This skill walks through 3 phases:

1. **App creation** — guide user to developer.whoop.com to create their free developer app
2. **Auth flow** — collect their credentials, start a local callback server, give them the login link
3. **Confirmation** — verify tokens saved, confirm daily sync is scheduled

The user only needs to:
- Fill out a short form on developer.whoop.com (2 min)
- Paste 2 values into Discord
- Click Allow in their browser once

---

## Phase 1 — Developer App Setup

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
> The most important field is **Redirect URI** — set it to EXACTLY:
> ```
> http://localhost:8080/callback
> ```
> Then click **Save** or **Create**."
>
> "Tell me when it's done."

**Step 1.3** — Say:
> "Perfect! Now you should see your **Client ID** and **Client Secret**.
> Please copy and paste both here — one at a time is fine.
>
> 🔒 These stay on your machine only and are never shared."

Wait for two messages from the user: the Client ID and Client Secret.
If they paste both in one message, extract both values.

---

## Phase 2 — Authentication

Once you have both values:

**Step 2.1** — Save credentials using exec:
```bash
cd /Users/jluo41/Desktop/OpenClawServer/jluo41-repo/Health-Sync/whoop
printf 'WHOOP_CLIENT_ID=%s\nWHOOP_CLIENT_SECRET=%s\n' '<CLIENT_ID>' '<CLIENT_SECRET>' > .env
chmod 600 .env
```

**Step 2.2** — Start the background auth listener:
```bash
cd /Users/jluo41/Desktop/OpenClawServer/jluo41-repo/Health-Sync/whoop
source /Users/jluo41/Desktop/OpenClawServer/env.sh
WHOOP_CLIENT_ID=<CLIENT_ID> WHOOP_CLIENT_SECRET=<CLIENT_SECRET> nohup python3 whoop_listen.py > /tmp/whoop_auth.log 2>&1 &
echo $!
sleep 1
cat /tmp/whoop_auth.log
```

The listener will print the auth URL. Extract it from the output.

**Step 2.3** — Send the user the link:
> "Almost there! Click this link, log in to Whoop, then click **Allow**:
>
> 🔗 [the auth URL from the output]
>
> Your browser will show a confirmation page. Come back here when you see it."

**Step 2.4** — After the user says they're done (or after ~30 seconds), check:
```bash
test -f /Users/jluo41/Desktop/OpenClawServer/jluo41-repo/Health-Sync/whoop/tokens.json && echo "CONNECTED" || echo "NOT_YET"
```

If NOT_YET, wait a moment and check again. If still not connected after 2 checks, show /tmp/whoop_auth.log and help troubleshoot.

---

## Phase 3 — Confirmation

Once tokens.json exists:

> "✅ You're connected! Your Whoop data will now sync automatically every morning at 7am.
>
> To pull today's data right now, just say: **sync whoop**
>
> You'll receive a summary like this every day:
> - 🟢 Recovery score
> - 😴 Sleep performance & duration
> - 💪 Daily strain"

---

## Handling "sync whoop"

If the user says "sync whoop" or "pull my whoop data":

Run:
```bash
cd /Users/jluo41/Desktop/OpenClawServer/jluo41-repo/Health-Sync/whoop
source /Users/jluo41/Desktop/OpenClawServer/env.sh
python3 whoop_sync.py
```

Read the output and present the summary in a friendly, readable format.
Use emoji. Highlight standout numbers (e.g. "Your HRV was 78ms — that's great!").

---

## Error Handling

- **"Missing credentials"** — they haven't run setup yet; go back to Phase 1
- **"Token refresh failed"** — tokens expired; ask them to run /whoop-connect again
- **Port 8080 in use** — tell them to close other apps and try again, or wait 30s
- **"Invalid client"** error — their Client ID or Secret is wrong; ask them to re-paste
