Invite Users to Azure + Databricks
===================================

Step-by-step runbook for adding a new team member.

Prerequisites
-------------

- You have Owner or User Access Administrator on the Azure subscription
- You have admin access to the Databricks workspace

Step 1: Azure Subscription Access
----------------------------------

1. Go to portal.azure.com
2. Navigate to: Subscriptions -> "Azure subscription 1"
3. Click: Access control (IAM) -> + Add -> Add role assignment
4. Select role: Contributor
5. Click: Members -> + Select members
6. Search for the user's email (e.g. xzhi2@jh.edu)
7. Select them -> Review + assign

Repeat for each user.

Note: CLI alternative may fail at JHU due to Graph API restrictions:

    az role assignment create --assignee <email> --role Contributor \
      --scope /subscriptions/530d4204-b4df-48a6-9581-196248aa95f0

If it errors with "Insufficient privileges", use the Portal UI.

Step 2: Databricks Workspace Access
------------------------------------

1. Open the Databricks workspace URL
2. Go to: Settings (gear icon) -> Identity and access -> Users
3. Click: Add User
4. Enter the user's email
5. Check entitlements:
   [x] Workspace access
   [x] Databricks SQL access
   [x] Allow cluster creation   <-- if they need to create clusters
6. Click: Add

Step 3: Verify
--------------

Ask the new user to:
1. Go to portal.azure.com and confirm they see "Azure subscription 1"
2. Open the Databricks workspace URL and confirm they can log in
3. Try creating a small test cluster (if cluster creation was granted)

Troubleshooting
---------------

"User not found" in Azure Portal
  -> They may need to be invited as a guest first if they're from a
     different Azure AD tenant. Use: Azure AD -> Users -> New guest user.

"Insufficient privileges" from CLI
  -> Normal for non-admin JHU accounts. Use Portal UI instead.

Cluster creation fails with quota error
  -> Check vCPU quota (see 05-quota.md). Request increase if needed.
