Resource Group
==============

What it is
----------

A resource group is a logical container that holds related Azure resources
(VMs, storage accounts, Databricks workspaces). It exists for organization
and access control — you can grant someone access to one resource group
without touching others.

Key facts
---------

- Every Azure resource must belong to exactly one resource group.
- Deleting a resource group deletes everything inside it.
- Resource groups have a region, but can contain resources in other regions.
- IAM roles can be scoped to a resource group (narrower than subscription).

How to check
------------

    az group list --output table
    az resource list --resource-group <name> --output table
