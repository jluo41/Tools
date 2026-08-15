IAM (Identity and Access Management)
=====================================

What it is
----------

Azure IAM controls who can do what to which resources. It uses Role-Based
Access Control (RBAC) — you assign a role to a user at a scope.

The three parts of a role assignment
------------------------------------

    WHO   +   WHAT ROLE   +   WHERE (scope)
    user      Contributor     /subscriptions/xxx

Built-in roles (most common)
-----------------------------

  Owner ......... Full access + can assign roles to others
  Contributor ... Full access, CANNOT assign roles
  Reader ........ View-only, cannot change anything

Scope hierarchy
---------------

    Management Group  (rare for us)
      └── Subscription
            └── Resource Group
                  └── Individual Resource

A role assigned at subscription level cascades to all resource groups and
resources below it.

How to check
------------

    az role assignment list --output table
    az role assignment list --assignee <email> --output table

How to assign (if you have Owner or User Access Admin)
------------------------------------------------------

    az role assignment create \
      --assignee <email> \
      --role Contributor \
      --scope /subscriptions/<sub-id>

Note: JHU Azure AD may block CLI-based assignment due to Graph API
restrictions. Use the Azure Portal UI as fallback:
Portal -> Subscriptions -> Access control (IAM) -> + Add role assignment.
