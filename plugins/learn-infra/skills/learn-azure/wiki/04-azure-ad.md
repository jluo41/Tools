Azure Active Directory (Entra ID)
=================================

What it is
----------

Azure AD (now called Microsoft Entra ID) is the identity provider behind
Azure. It manages users, groups, and authentication. When you log in with
jluo41@jh.edu, Azure AD is what validates you.

Key concepts
------------

  Tenant ........ An organization's directory (JHU has one tenant).
                  Our tenant ID: b550674d-036c-41e9-979d-e10c7e9974cb

  User .......... An identity in the tenant (e.g. jluo41@jh.edu).
                  External guests get a #EXT# suffix internally.

  Group ......... A collection of users. Roles can be assigned to groups
                  instead of individual users (cleaner at scale).

  Service
  Principal ..... A non-human identity for apps/automation.

Why it matters for us
---------------------

- JHU controls the tenant — we can't create new users, only invite guests.
- The "Insufficient privileges to complete the operation" error from the CLI
  means your account doesn't have Graph API read access on the JHU tenant.
  This is normal for non-admin accounts.
- Workaround: use the Azure Portal UI for user lookups and role assignments.

How to check
------------

    az ad signed-in-user show     # your own profile
    az account show               # tenant ID in the output
