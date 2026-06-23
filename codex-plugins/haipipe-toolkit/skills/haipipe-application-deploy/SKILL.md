---
name: haipipe-application-deploy
description: "Deployment specialist for the intervention lifecycle. STUB. Packages reviewed artifacts for delivery through the specified channel (SMS vendor API, dashboard endpoint, email system). Parallel to paper's compile+submit. Trigger: deploy, ship, go live, send, /haipipe-application deploy."
argument-hint: "[variant-id] [--channel sms|dashboard|email] [intervention-path]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-22"
  summary: "Deployment specialist (STUB) — package + ship to channel."
  changelog:
    - "1.0.0 (2026-06-22): initial stub."
---

Skill: haipipe-application-deploy   (STUB)
============================================

**Status: STUB.** Will package reviewed artifacts for delivery
through the specified channel.

When implemented:

```
Step 1: Verify all deployment prerequisites from 5-delivery-plan.md.
Step 2: Package artifact for channel (SMS API payload, dashboard
        config, email template).
Step 3: Deploy to staging / test environment.
Step 4: Verify delivery (test send, preview render).
Step 5: On approval: deploy to production.
Step 6: Update variant status: reviewed → deployed.
Step 7: Log deployment in STATUS.md.
```

Deployment channels (future):

```
SMS:        vendor API integration (Twilio, etc.)
Dashboard:  endpoint update via /haipipe-end
Email:      template system integration
In-app:     UI component deployment
```


Risk profile
=============

HIGH — deploys to external channels. Must be gated by review +
explicit user approval. Never auto-deploy.
