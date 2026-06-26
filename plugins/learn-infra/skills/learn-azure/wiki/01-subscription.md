Subscription
============

What it is
----------

A subscription is Azure's top-level billing and resource boundary. Everything
you create (VMs, storage, Databricks workspaces) lives inside a subscription.
One Azure account can own multiple subscriptions.

Our setup: "Azure subscription 1" (ID: 530d4204-b4df-48a6-9581-196248aa95f0),
tied to the JHU tenant.

Key facts
---------

- Billing rolls up per subscription — one invoice per subscription per month.
- Quotas (vCPU limits) are per subscription per region.
- IAM role assignments can be scoped to the subscription (broad) or to a
  single resource group (narrow).

How to check
------------

    az account show           # current subscription
    az account list --output table   # all subscriptions you can access

Common tasks
------------

Switch default subscription:

    az account set --subscription <name-or-id>
