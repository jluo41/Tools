Quotas
======

What it is
----------

Azure limits how many vCPUs you can use per subscription per region. This
prevents accidental cost explosions but also blocks cluster creation if
you hit the cap.

Our situation
-------------

  Region: eastus
  Default vCPU quota: 4 cores
  Databricks clusters need: 8+ cores (driver + workers)

This means a fresh subscription CANNOT spin up a standard Databricks cluster
until you request a quota increase.

How to check
------------

    az vm list-usage --location eastus --output table | grep -i "total regional"

How to request an increase
--------------------------

1. Azure Portal -> search "Quotas"
2. Select "Compute" provider
3. Filter by region (eastus)
4. Find "Total Regional vCPUs" -> click "Request increase"
5. Request at least 16 cores (enough for a small cluster + headroom)
6. Approval usually takes minutes to hours for small increases.

Alternatively:

    az quota create \
      --resource-name "totalRegionalVCPUsPerSubscription" \
      --scope "/subscriptions/<sub-id>/providers/Microsoft.Compute/locations/eastus" \
      --limit-object value=16

Gotcha
------

Quota is per VM family too (e.g. Standard_DS_v2 has its own limit). If
"Total Regional" is fine but cluster creation still fails, check the
specific VM family quota.
