Worked example: OptTime v2 fu7d datapoint description
=======================================================

The canonical "good" instance of SKILL.md's mandatory datapoint
description. Project-specific by nature (an SMS follow-up send-time
RCT); use it as a filled-in model, not as content to copy verbatim.

Worked example — OptTime v2 fu7d (the template's canonical "good" instance)
---------------------------------------------------------------------------

   A datapoint is one specific patient who was enrolled in the
   "2026_Optimal_Timing_Personalization" experiment, who received an
   initial SMS invitation at time `ObsDT` (`invitation_type=N/A`, the
   LINKMESSAGE type), who did NOT click the initial within the
   cancellation window so a follow-up SMS was queued, who was then
   UNIFORMLY RANDOMLY assigned (`π(T|X) = 1/20`) to one of 20 follow-up
   send-time arms `T ∈ {FT_08_00, FT_08_30, ..., FT_17_30}` (column
   `experiment_config`, every 30 min from 08:00 to 17:30 local), and
   for whom the follow-up was actually delivered (`minutes_to_followup > 0`,
   `follow_up_invitation_id` set, `follow_up_deliver_on_date` recorded);
   the binary outcome `Y = clicked_follow_up_7d` answers "did the patient
   click any link in the FOLLOW-UP message within 7 days of
   `follow_up_deliver_on_date`" (verified by checking
   `first_follow_up_clicked_date` falls inside that window), with
   population mean Y ≈ 0.459 on test.

   The input features X are 12 CaseFn groups encoded as one 1,995-dim
   sparse vector with ~58 non-zero entries per row:
     - PAge5                 — age in 5-yr buckets, from DfPtt.ageBucketBy5
     - Pgender               — M/F/U, from DfPtt.gender
     - PZip3FixedLen         — first-3 zip digits, from DfPtt.zipcode3
     - InvCrntTimeFixedLen   — ★ THE TREATMENT — one-hot of FT_HH_MM from
                               DfInv.experiment_config (S-Learner pattern:
                               treatment folded into X; for counterfactual
                               inference this slot is re-set to other arms)
     - PhmFixedLen           — patient's pharmacy NCPDP code
     - NPIFixedLen           — prescribing provider NPI
     - NPITraitFixedLen      — provider attributes (specialty, taxonomy)
     - RxCrntNDCRxFixedLen   — current Rx (NDC + dosage form + refill bucket)
     - Zip3EngFixedLen       — HISTORICAL engagement aggregated by zip3
     - NcpdpEngFixedLen      — HISTORICAL engagement by pharmacy
     - NpiEngFixedLen        — HISTORICAL engagement by provider
     - NdcEngFixedLen        — HISTORICAL engagement by drug

   (The 4 *Eng* features are HISTORICAL, not contemporaneous, so they
   do not leak the current invitation's click.)

   Selection filters (Stage 4 SplitArgs.Split_to_Selection, applied to
   BOTH train and test):
     1. messaged == 1                          — SMS was actually sent
     2. experiment_config in {20 FT_HH_MM arms} — valid OptTime arm
     3. minutes_to_followup > 0                 — FU was actually delivered
                                                  (not cancelled because the
                                                  patient clicked the initial
                                                  inside the cancel window)

   INTENTIONALLY NOT FILTERED ON:
     - `clicked` (whether they ever clicked the original invitation) —
       deliberately KEPT IN the cohort. The label clicked_follow_up_7d
       is specifically about the FU message, not the original, so filtering
       on `clicked` would be selection-on-a-correlated-outcome and is bias-
       inducing. Two patients can have clicked=1 AND clicked_follow_up_7d=1
       (clicked both) or clicked=1 AND clicked_follow_up_7d=0 (clicked only
       the original) or clicked=0 AND clicked_follow_up_7d=1 (FU-only) —
       all three are valid datapoints in this cohort.

   Split policy:
     SplitMethod = RandomByStratum
     Stratification columns: [experiment_config, clicked_follow_up_7d,
                              authenticated_follow_up_7d]
     Ratio = 80/20, seed = 42
     Train: 99,206 rows  |  Test: 24,845 rows
     Per-arm test counts: 1,193 - 1,297 (verified uniform-random)
     Label positive rate: ≈ 45.9% in both splits

   Worked example row (test idx 0):
     PID 10000000012, Male, age 70.  ObsDT = 2026-04-06 17:21.
     T = FT_10_30 (arm idx 5).  FU delivered 2026-04-07 13:55 (~20.6 hrs later).
     7-day window: 2026-04-07 13:55 → 2026-04-14 13:55.
     first_follow_up_clicked_date = NaT → Y = 0.


