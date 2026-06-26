# Lesson 01: Azure VM Stockout — Use Confidential Compute (DC-series)

## The Problem

When creating a Databricks cluster in Azure **eastus** region, 9+ standard VM types returned `CLOUD_PROVIDER_RESOURCE_STOCKOUT`:

| VM Type | Result |
|---------|--------|
| DS3_v2 | STOCKOUT |
| D4ds_v6 | STOCKOUT |
| E2ds_v6 | STOCKOUT |
| F4s_v2 | STOCKOUT |
| D4ps_v6 | STOCKOUT |
| D4a_v4 | STOCKOUT |
| E4ads_v7 | STOCKOUT |
| D4ads_v5 | STOCKOUT |
| D4s_v4 | STOCKOUT |

This happens because Azure regions have limited capacity and standard VM pools are heavily oversubscribed.

## The Solution

**Standard_DC4as_v5** (confidential compute, AMD SEV-SNP) was available because it draws from a **separate capacity pool** that most users don't request.

- 4 cores, 16 GB RAM — enough for single-node ML workloads
- Confidential compute is a security feature (memory encryption), but for our purposes it's just a VM that's available when others aren't
- Create from the Databricks UI rather than CLI when stockout errors occur — the UI shows which VMs are actually available

## Why It Works

Azure allocates different VM families to different physical hardware pools. Confidential compute (DC-series) uses AMD EPYC processors with SEV-SNP, which are on dedicated hardware that doesn't compete with the general-purpose pool. When a region is sold out of D-series / E-series / F-series, DC-series often still has capacity.

## When to Apply

- Any Azure Databricks deployment where standard VM types fail with STOCKOUT
- Priority: try DC4as_v5 first (cheapest confidential), then DC8as_v5 if more cores needed
- This is region-specific — check your region's availability. `eastus` had this problem heavily in Jun 2026

## Caveats

- DC-series is slightly more expensive per core than standard D-series
- The confidential compute overhead is negligible for data science workloads
- DC4as_v5 has only 4 cores — installing too many packages can crash the driver (see Lesson 09)
