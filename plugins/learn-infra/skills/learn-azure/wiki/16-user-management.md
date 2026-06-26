User Management (Databricks)
============================

What it is
----------

Databricks has its own user directory, separate from Azure IAM. A person
needs BOTH Azure-level access AND Databricks workspace-level access.

Two-layer access model
----------------------

    Layer 1: Azure IAM
      - Grants access to the Azure resource (the workspace)
      - Role: Contributor (manage resources) or Reader (view only)
      - Assigned at: subscription or resource group scope

    Layer 2: Databricks workspace
      - Grants access to workspace features (notebooks, clusters, models)
      - Entitlements: Workspace access, Databricks SQL, Allow cluster creation
      - Managed in: workspace Settings -> Identity and access -> Users

Without Layer 1, the user can't reach the workspace URL.
Without Layer 2, the user can see the workspace but can't do anything in it.

Entitlements
------------

  Workspace access ......... Basic access to notebooks, repos, files
  Databricks SQL access .... Can use SQL warehouses and dashboards
  Allow cluster creation ... Can spin up new clusters (costs money!)

Adding a user — step by step
-----------------------------

1. Azure Portal -> Subscriptions -> Access control (IAM)
   -> Add role assignment -> Contributor -> add user email

2. Databricks workspace -> Settings (gear) -> Identity and access -> Users
   -> Add User -> enter email -> check all needed entitlements

3. User receives email invitation. They log in with their institutional
   credentials (e.g. JHU SSO via @jh.edu).
