# Lesson 01: Graph API Blocked at JHU — Use Portal for User Management

## The Problem

Running `az role assignment create --assignee <email>` fails with "Insufficient privileges to complete the operation" on the JHU Azure AD tenant, even when the logged-in account is a subscription Owner.

```
ERROR: Insufficient privileges to complete the operation.
GraphError: Authorization_RequestDenied
```

The CLI tries to resolve the email by querying the Microsoft Graph API (service principal lookup first, then user lookup), and JHU's tenant blocks non-admin Graph API reads.

## The Symptom

The `az role assignment create` command fails before it even attempts the role assignment. The error comes from the user-lookup step, not the permission-assignment step.

## The Solution

### Option A: Use the Azure Portal UI (reliable)

1. portal.azure.com → Subscriptions → Access control (IAM) → + Add role assignment
2. The Portal uses a different auth path for user lookup — it works.

### Option B: Use `az rest` with the Graph API directly (works for invitations)

```bash
az rest --method POST \
  --url "https://graph.microsoft.com/v1.0/invitations" \
  --body '{"invitedUserEmailAddress":"user@jh.edu","inviteRedirectUrl":"https://portal.azure.com","sendInvitationMessage":true}'
```

This works because the invitation API uses a different permission scope than the user-lookup API. But you still need the Portal for the role assignment step.

### Option C: Supply the object ID directly (if you know it)

```bash
az role assignment create \
  --assignee-object-id <guid> \
  --assignee-principal-type User \
  --role Contributor \
  --scope /subscriptions/<sub-id>
```

Get the object ID from `az ad user list --filter "mail eq 'user@jh.edu'"` (this query works even when the role-assignment lookup doesn't).

## Why It Fails

The CLI's `az role assignment create` calls two Graph API endpoints sequentially:
1. `GET /servicePrincipals?$filter=...` — looks for a service principal matching the email
2. `GET /users?$filter=...` — falls back to user lookup

Step 1 requires `Application.Read.All` or `Directory.Read.All`, which JHU's Azure AD doesn't grant to regular users. The CLI fails at step 1 and never reaches step 2.

## When to Apply

- Any JHU Azure subscription where you're not a Global Admin
- Any university/enterprise tenant that restricts Graph API reads
- First sign: the error says "Insufficient privileges" but you're Owner on the subscription
