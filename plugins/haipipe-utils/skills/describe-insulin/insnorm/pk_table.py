"""
The bank: insulin product -> pharmacokinetics.

WHY THIS TABLE IS HAND-WRITTEN AND SHORT
================================================================================
Measured 260822, the 247,212 insulin administrations in 1-SourceStore carry 24
distinct drug keys and the top 12 cover 99.8% of them. There is no 100,000-row
reference to download here and no matcher worth building: a person reads twelve
package inserts once and writes them down, and every value is then citable.

WHERE THE NUMBERS COME FROM
================================================================================
FDA prescribing information for each product, cross-read against the ADA
Standards of Care insulin pharmacokinetics table. They are POPULATION values for
a typical subcutaneous dose in a typical adult. Real onset and duration move
with dose, injection site, temperature, body composition and antibody status;
a 4-hour rapid-analog duration is a 3-to-5-hour range wearing one number.

That is why nothing in this file may be stamped GOOD. GOOD is reserved for a
DIA measured on the patient in front of you -- WellDoc's MedPrescription carries
exactly that for 15.7% of prescriptions -- and the door takes it as an override.

    onset_min       time to the start of glucose-lowering effect
    peak_min        time to maximum effect. None means PEAKLESS by design:
                    glargine and degludec have no pronounced peak, and writing
                    a number there would invent a shape the drug does not have.
    duration_min    time until the effect is no longer clinically meaningful

PREMIXES ARE BIPHASIC and a single (onset, peak, duration) triple describes them
badly: 70/30 is a rapid component and an intermediate one in one injection. They
are typed `premix` and carry the ENVELOPE, and `biphasic: True` says that a
consumer modelling a single curve is approximating.
"""

RAPID = "rapid"
SHORT = "short"
INTERMEDIATE = "intermediate"
LONG = "long"
ULTRA_LONG = "ultra_long"
PREMIX = "premix"
CLASSES = (RAPID, SHORT, INTERMEDIATE, LONG, ULTRA_LONG, PREMIX)

# canonical key -> (class, onset_min, peak_min, duration_min, biphasic, note)
PK = {
    # -- rapid-acting analogues ------------------------------------------
    "insulin lispro":       (RAPID, 15, 60, 270, False, "Humalog; FDA label 3-5 h"),
    "insulin lispro-aabc":  (RAPID, 10, 57, 300, False, "Lyumjev; ultra-rapid formulation of lispro"),
    "insulin aspart":       (RAPID, 15, 60, 270, False, "NovoLog"),
    "insulin aspart faster":(RAPID, 10, 55, 270, False, "Fiasp"),
    "insulin glulisine":    (RAPID, 15, 55, 270, False, "Apidra"),
    # -- short-acting regular human --------------------------------------
    "insulin human regular":(SHORT, 30, 150, 480, False, "Novolin R / Humulin R U-100"),
    # -- intermediate ------------------------------------------------------
    "insulin human nph":    (INTERMEDIATE, 90, 300, 900, False, "Humulin N / Novolin N"),
    # -- long-acting, peakless --------------------------------------------
    "insulin glargine":     (LONG, 105, None, 1440, False, "Lantus / Basaglar U-100; peakless"),
    "insulin glargine u300":(LONG, 180, None, 1800, False, "Toujeo; flatter and longer than U-100"),
    "insulin detemir":      (LONG, 90, None, 1080, False, "Levemir; duration is dose-dependent, 12-24 h"),
    "insulin degludec":     (ULTRA_LONG, 60, None, 2520, False, "Tresiba; >42 h, steady state after 3 d"),
    # -- premixes, biphasic ------------------------------------------------
    "insulin aspart 70/30": (PREMIX, 15, 120, 1080, True, "NovoLog Mix 70/30; rapid + protamine"),
    "insulin lispro 75/25": (PREMIX, 15, 120, 1080, True, "Humalog Mix 75/25"),
    "insulin human 70/30":  (PREMIX, 30, 180, 1080, True, "Humulin 70/30 / Novolin 30R"),
    "insulin human 50/50":  (PREMIX, 30, 180, 1080, True, "Novolin 50R / Humulin 50/50"),
    # -- class-only, no product named -------------------------------------
    # A LAST RESORT, AND `basal insulin` IS THE WEAKEST ROW IN THIS FILE.
    # 'Basal' answers LONG because that is what basal means under multiple daily
    # injections. It is WRONG for a pump: in CSII there is one reservoir, the
    # basal is the same RAPID analogue as the bolus delivered at a rate, and a
    # 24-hour curve over-states its tail by a factor of five.
    #
    # The only cohort that writes these words is OhioT1DM, and OhioT1DM is
    # entirely pump -- its XML carries <temp_basal> spans and bolus-wizard
    # types, and since 260822 its rows also carry `insulin_type` (Humalog /
    # Novalog / 'Humalog 200') and `DeliveryMode`. So the fix is not to retune
    # this row for pumps and break it for the next MDI cohort: it is for the
    # CALLER to stop reaching this row when the log named a product. These two
    # stay for a log that really names nothing else.
    "bolus insulin":        (RAPID, 15, 60, 270, False, "class only; typical rapid analogue"),
    "basal insulin":        (LONG, 105, None, 1440, False,
                             "class only; MDI reading. WRONG for a pump basal, "
                             "which is the rapid analogue in the reservoir"),
}

# Everything the logs actually write -> a key in PK. Measured over all three
# dialects; 24 distinct keys, of which these are the ones that resolve.
ALIASES = {
    "insulin lispro-aabc": "insulin lispro-aabc",
    "insulin lispro": "insulin lispro",
    "humalog": "insulin lispro",
    "lyumjev": "insulin lispro-aabc",
    # Admelog is Sanofi's lispro follow-on: the same molecule, so the same
    # curve. Its absence cost 17 MEPS fills that the FDA bank could not name
    # either, and 'ADMELOG' alone only resolved because mednorm happened to.
    "admelog": "insulin lispro",
    "insulin aspart": "insulin aspart",
    "novolog": "insulin aspart",
    "fiasp": "insulin aspart faster",
    "insulin glulisine": "insulin glulisine",
    "apidra": "insulin glulisine",
    "insulin glargine": "insulin glargine",
    "lantus": "insulin glargine",
    "basaglar": "insulin glargine",
    "semglee": "insulin glargine",
    "rezvoglar": "insulin glargine",
    # The NONPROPRIETARY names of the two glargine biosimilars. A pharmacy feed
    # writes these as often as it writes the brand, and a biosimilar suffix is
    # not a different molecule.
    "insulin glargine-yfgn": "insulin glargine",
    "insulin glargine-aglr": "insulin glargine",
    "toujeo": "insulin glargine u300",
    "insulin detemir": "insulin detemir",
    "levemir": "insulin detemir",
    "insulin degludec": "insulin degludec",
    "tresiba": "insulin degludec",
    "insulin human": "insulin human regular",
    "human insulin": "insulin human regular",
    "novolin r": "insulin human regular",
    "humulin r": "insulin human regular",
    "gansulin r": "insulin human regular",
    "insulin human nph": "insulin human nph",
    "humulin n": "insulin human nph",
    "novolin n": "insulin human nph",
    "insulin aspart 70/30": "insulin aspart 70/30",
    "novolog mix 70/30": "insulin aspart 70/30",
    "humalog mix 75/25": "insulin lispro 75/25",
    "humulin 70/30": "insulin human 70/30",
    "novolin 30r": "insulin human 70/30",
    # The US brand spelling of the same premix. 'novolin 30r' is the Chinese
    # market's; both are in our data and only one was here.
    "novolin 70/30": "insulin human 70/30",
    "novolin n 70/30": "insulin human 70/30",
    "novolin 50r": "insulin human 50/50",
    "humulin 50/50": "insulin human 50/50",
    # MISSPELLINGS THAT ARE ACTUALLY IN THE DATA. Kept because the drug is
    # unambiguous and dropping them silently loses rows; a new typo does NOT get
    # added here without naming the dataset and the row count.
    #   'insulin glarigine'  WellDoc export, 6 rows
    #   'novalog'            OhioT1DM's patient tag spells NovoLog this way, in
    #                        all 22 files that name it -- 1,881 administrations.
    #                        Nothing else in insulin is one letter from it.
    "insulin glarigine": "insulin glargine",
    "novalog": "insulin aspart",
    "bolus insulin": "bolus insulin",
    "basal insulin": "basal insulin",
}

# BARE BRAND FAMILIES WE REFUSE TO RESOLVE, AND WHY THAT COSTS US A METRIC
# ============================================================================
# 'Novolin' and 'Humulin' are FAMILIES, not products: each ships as R (regular),
# N (NPH) and 70/30, three different curves. MEPS's answer key calls the bare
# string a 70/30 premix -- 182 fills of it -- so adding
#
#     "novolin": "insulin human 70/30"
#
# would raise our I1 class accuracy. It is still a guess, and it is a guess
# fitted to a corruption MEPS has and we do not: MEPS truncates RXNAME to 12
# characters, which is what turned 'Novolin 70/30' into 'NOVOLIN'. Our own logs
# write the suffix. Resolving the family name would import a distribution from
# someone else's data-entry limit.
#
# The 182 fills are therefore left wrong on purpose, and the reason is here so
# nobody 'fixes' the score without reading it.
AMBIGUOUS_FAMILIES = ("novolin", "humulin")

# CONCENTRATION, and it is BANK DATA rather than a record field
# ============================================================================
# units per mL. It does not change the PK of a bioequivalent higher strength --
# Humalog U-200 and Lyumjev U-200 are bioequivalent to their U-100 forms -- but
# it DOES change the volume delivered per unit, and for glargine it changes the
# curve outright: U-300 is flatter and longer than U-100, which is why they are
# two separate rows above.
#
# Verified 260822 against the products' own labelling:
#   Toujeo   300 U/mL. 'Each mL of TOUJEO contains 300 units of insulin
#            glargine'; SoloStar 450 U/1.5 mL, Max SoloStar 900 U/3 mL. BOTH
#            pens are U-300 -- 'Max' is a bigger pen, not a different strength,
#            which is exactly the confusion that made TOUJEO MAX resolve to the
#            U-100 row.                    products.sanofi.us/toujeo/toujeo.pdf
#   Humalog  U-100 and U-200
#   Lyumjev  U-100 and U-200
#   Tresiba  U-100 and U-200
#   everything else here: U-100 only
#
# NOT PUT IN THE RECORD. A field would have to be filled for every row, and the
# strength is knowable only when the log names the pen; most of ours do not. It
# lives here so a consumer computing VOLUME can look it up, and so the U-300
# glargine row has a stated reason to exist.
CONCENTRATION = {
    "insulin glargine u300": (300,),
    "insulin lispro": (100, 200),
    "insulin lispro-aabc": (100, 200),
    "insulin degludec": (100, 200),
}
DEFAULT_CONCENTRATION = (100,)


# HOW THE ROUTE CHANGES WHETHER THESE NUMBERS APPLY AT ALL
# ============================================================================
# Every triple above is a SUBCUTANEOUS measurement. Two logged routes break it:
#
#   intravenous   No subcutaneous depot, so no absorption phase. Onset is
#                 effectively immediate and the effect is gone in minutes to
#                 about an hour, not 4.5 h. Shanghai logs 29 of these under
#                 'Insulin dose - i.v.' and they currently receive the
#                 subcutaneous curve, which is wrong by an order of magnitude.
#                 Rule 3 says a confidently wrong value is worse than a missing
#                 one, so these get NULL and a source that says why.
#
#   pump basal    A continuous RATE in units per hour, not a bolus. The triple
#                 still describes the insulin, but a consumer convolving it as
#                 one discrete dose will misplace the whole curve. Typed, not
#                 nulled: the numbers are right, the scale is different -- which
#                 is rule 4, and it is why this noun now declares a basis.
#
# ROUTES the PK table is valid for, keyed by the DeliveryMode the log states.
PK_BASIS = {
    "mdi":           "subcutaneous_bolus",
    "pump_bolus":    "subcutaneous_bolus",
    "pump_basal":    "subcutaneous_rate",
    "pump_suspend":  "subcutaneous_rate",
    "iv":            "intravenous",
}

# WHEN THE LOG DOES NOT SAY, AND WHY THIS IS NOT A GUESS
# ---------------------------------------------------------------------------
# Most of our logs state no route: a WellDoc MedicationID is an integer and says
# nothing about a pen versus a pump. Rule 4's answer to a missing quantity is
# not to invent one, it is to REPORT ON THE REFERENCE SCALE AND SAY SO -- which
# is what describe-food does when grams are unknown and it answers per_100g.
#
# So an unstated route gets `subcutaneous_reference`: these numbers are the
# table's subcutaneous values, and that is a declared scale rather than a claim
# about this row. A consumer that needs the row's real route can test for it.
REFERENCE_BASIS = "subcutaneous_reference"
PK_BASIS["pump_suspend"] = "suspension"

# The basis values on which the table's numbers are NOT usable.
#
#   intravenous   no subcutaneous depot, so no absorption phase.
#   suspension    Shanghai logs 14 'temporarily suspend insulin delivery' rows.
#                 A suspend delivers NO insulin -- it STOPS the scheduled basal
#                 -- so an action curve for it is not merely imprecise, it is
#                 the opposite sign. The drug is still named, because which
#                 insulin was suspended is a real fact.
UNSUPPORTED_BASIS = ("intravenous", "suspension")


# A combination product whose insulin component is real but which is NOT just
# insulin. Typed, resolved to its insulin component, and flagged.
COMBINATIONS = {
    "insulin degludec and liraglutide": ("insulin degludec", "Xultophy; + GLP-1 agonist"),
    "insulin glargine and lixisenatide": ("insulin glargine", "Soliqua; + GLP-1 agonist"),
}
