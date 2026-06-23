Output exactly one `<report>...</report>` block. Inside, follow this
structure verbatim. Do not add fields. Do not add prose outside.

```xml
<report>
  <basics>
    <individual_id>...</individual_id>
    <dataset>...</dataset>
    <gender>Male | Female | Unknown</gender>
    <year_of_birth>1978</year_of_birth>
    <age_years>47</age_years>
    <disease_type>Type 1 diabetes | Type 2 diabetes | Unknown</disease_type>
  </basics>

  <current>
    <last_obs_dt>YYYY-MM-DD HH:MM:SS</last_obs_dt>
    <last_bg_mg_dl>123.4</last_bg_mg_dl>
    <recent_window_n>288</recent_window_n>
    <recent_min>78.0</recent_min>
    <recent_max>234.0</recent_max>
    <recent_mean>132.5</recent_mean>
  </current>

  <forecast_summary>
    <horizon_minutes>120</horizon_minutes>
    <n_windows>45</n_windows>           <!-- diagnostic only; pred stats below
                                              describe ONLY the most-recent
                                              window, anchored at last_obs_dt -->
    <pred_min>78.0</pred_min>
    <pred_max>148.0</pred_max>
    <pred_mean>118.2</pred_mean>
  </forecast_summary>

  <interpretation>
    <verdict>rising | stable | falling | mixed</verdict>
    <why>One-sentence cause: meal carbs, fasting trend, recent exercise, etc.</why>
    <actions>
      <action>concrete action 1</action>
      <action>concrete action 2</action>
    </actions>
    <confidence>high | medium | low</confidence>
    <safety_flag>none | hypo_risk | hyper_risk | hypo_and_hyper_risk</safety_flag>
  </interpretation>

  <nl>
    Free-text patient message. 3–6 short sentences, one paragraph, max
    400 characters. Plain English. Warm. Concrete actions. NO insulin
    doses. NO contradicting a clinician. Flag safety risk plainly if any.
  </nl>
</report>
```

CONSTRAINTS:
- `verdict`, `confidence`, `safety_flag` MUST be one of the listed enum values.
- `actions` may have 0–4 `<action>` children. Empty action list is OK
  ("nothing to do, things look stable").
- Numeric fields are mg/dL unless noted.
- `nl` may NOT contain XML tags or markdown formatting — plain text only.
