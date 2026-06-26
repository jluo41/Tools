Databricks Workspace
====================

What it is
----------

A Databricks workspace is a cloud environment for running notebooks,
clusters, jobs, and ML workflows. On Azure, each workspace is an Azure
resource inside a resource group.

Key facts
---------

- One workspace = one URL (e.g. adb-1234567890.azuredatabricks.net).
- A workspace has its own user list, permissions, and settings — separate
  from Azure IAM (you need BOTH Azure access AND workspace access).
- Workspaces contain: notebooks, repos, clusters, jobs, models, volumes.

How it maps to Azure
--------------------

    Azure Subscription
      └── Resource Group
            └── Azure Databricks Service (the workspace resource)
                  ├── Managed Resource Group (auto-created, holds VMs/networking)
                  └── Storage Account (DBFS root)

The "managed resource group" is created automatically — don't touch it.

How to access
-------------

1. Have an Azure role (Reader minimum) on the subscription or resource group.
2. Be added as a user in the Databricks workspace.
3. Navigate to the workspace URL or use the Azure Portal shortcut.
