Azure + Databricks Wiki
=======================

Quick-reference wiki for the Azure and Databricks concepts our team uses daily.
Each file covers one concept — read them in any order.


Index
-----

Core Azure
  01-subscription.md .... What a subscription is, how billing works
  02-resource-group.md .. Logical container for related resources
  03-iam.md ............. Identity and Access Management (roles, assignments)
  04-azure-ad.md ........ Azure Active Directory / Entra ID (users, tenants)
  05-quota.md ........... vCPU quotas, how to request increases

Databricks on Azure
  10-workspace.md ....... What a workspace is, how it maps to Azure
  11-cluster.md ......... Clusters vs serverless, config, auto-terminate
  12-unity-catalog.md ... Catalog / schema / volume — the data governance layer
  13-volumes.md ......... Where files live (managed vs external volumes)
  14-notebook.md ........ Notebooks, %pip, dbutils, and cluster libraries
  15-model-serving.md ... MLflow model registration + serving endpoints
  16-user-management.md . Adding users, entitlements, cluster creation rights

Operations
  20-invite-users.md .... Step-by-step: invite someone to Azure + Databricks
  21-cost-control.md .... Spot instances, auto-terminate, DBU monitoring
