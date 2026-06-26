# Lesson 02: Guest Users Need Invitation Before Role Assignment

## The Problem

When adding a user from a different Azure AD tenant (e.g. `xzhi2@jh.edu` to the `cdhaijhucloudoutlook.onmicrosoft.com` tenant), `az ad user list --filter "mail eq 'xzhi2@jh.edu'"` returns an empty array — the user doesn't exist in YOUR tenant yet.

You can't assign a role to a user who doesn't exist in the tenant.

## The Symptom

```bash
az ad user list --filter "mail eq 'xzhi2@jh.edu'"
# returns []
```

The user exists at JHU but is invisible to your tenant until invited.

## The Solution

**Step 1: Invite as guest user first**

```bash
az rest --method POST \
  --url "https://graph.microsoft.com/v1.0/invitations" \
  --body '{
    "invitedUserEmailAddress": "xzhi2@jh.edu",
    "inviteRedirectUrl": "https://portal.azure.com",
    "sendInvitationMessage": true
  }'
```

The response includes the user's new object ID in your tenant:
```json
{
  "invitedUser": {
    "id": "8d3f5bc1-...",
    "userPrincipalName": "xzhi2_jh.edu#EXT#@cdhaijhucloudoutlook.onmicrosoft.com"
  },
  "status": "PendingAcceptance"
}
```

**Step 2: Assign role using the object ID**

```bash
az role assignment create \
  --assignee-object-id 8d3f5bc1-... \
  --assignee-principal-type User \
  --role Contributor \
  --scope /subscriptions/530d4204-b4df-48a6-9581-196248aa95f0
```

**Step 3: User accepts the invitation** (they get an email) and can then access the subscription.

## Why It Works This Way

Azure AD is a directory service. Each tenant has its own user directory. A user at `jh.edu` is in JHU's tenant, not yours. The invitation creates a "guest user" entry (#EXT#) in YOUR tenant that references the original identity. Only after this entry exists can you assign roles.

## When to Apply

- Adding any user whose email domain differs from your tenant's domain
- The `#EXT#` suffix in the UPN is the telltale sign of a guest user
- Applies to both CLI and Portal workflows (Portal just hides the two-step dance)
