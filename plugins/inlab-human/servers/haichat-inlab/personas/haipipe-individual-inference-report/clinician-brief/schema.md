Output EXACTLY one <report> block, no prose outside it:

<report>
  <basics>
    <individual_id>…</individual_id>
  </basics>
  <current>
    <last_bg_mg_dl>…</last_bg_mg_dl>
  </current>
  <forecast_summary>
    <direction>rising | falling | flat</direction>
    <pred_min>…</pred_min>
    <pred_max>…</pred_max>
    <delta_mg_dl>…</delta_mg_dl>
  </forecast_summary>
  <interpretation>
    <why>one sentence: what the model appears to be responding to</why>
    <actions>a review action for the clinician</actions>
    <safety_flag>none | hypo_risk | hyper_risk | hypo_and_hyper_risk</safety_flag>
    <confidence>high | moderate | low</confidence>
  </interpretation>
  <nl>The 3-5 sentence clinician-facing interpretation.</nl>
</report>
