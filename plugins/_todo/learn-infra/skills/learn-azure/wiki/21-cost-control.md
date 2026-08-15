Cost Control
============

Azure + Databricks costs can spike fast if clusters run idle. Key controls:

Cluster auto-terminate
----------------------

Always set auto-terminate on every cluster. 30 minutes is a good default.
A forgotten running cluster costs ~$5-15/hr depending on node type.

    Settings when creating cluster:
    -> Advanced options -> Auto termination -> 30 minutes

Spot instances
--------------

Use spot (preemptible) VMs for worker nodes to save 60-80%.
Driver node should stay on-demand (spot driver = lost work on eviction).

    Worker type: Spot
    Driver type: On-demand

Monitor DBU usage
-----------------

Databricks bills in DBUs (Databricks Units) on top of Azure VM costs.
Check usage in: workspace -> Settings -> Usage

Azure cost alerts
-----------------

Set a budget alert so you get emailed before costs exceed a threshold:

1. Azure Portal -> Cost Management -> Budgets -> + Add
2. Set amount (e.g. $200/month)
3. Set alert at 80% and 100%
4. Add notification email

Turn off idle endpoints
-----------------------

Model Serving endpoints bill per hour while active. After testing:

    # Check serving endpoints
    # workspace -> Serving -> find endpoint -> click Stop

Or configure scale-to-zero (has cold start penalty).
