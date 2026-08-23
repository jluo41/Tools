"""
The describe-medication benchmark: what is noun-specific about grading a drug.

The harness is shared -- `haipipe-norm/bench` runs B1 CONTRACT over every
member, `haipipe-norm/xbench` owns splits, circularity and weighting. What is
HERE is the three things only this noun can say: where its gold comes from,
what counts as the same drug, and at which granularities to answer.

THREE EVALUATION SETS, THREE KINDS OF GOLD
================================================================================
    E1  MEPS       192,275 US prescription fills, 2023, a public use file.
                   The dirty string is the PHARMACY's, truncated to 12
                   characters. The answer key is Multum Lexicon's, curated by a
                   different organisation against a different reference.
                   ANSWERS: is the resolver any good, in absolute terms,
                   against numbers other papers have published.

    E2  LEXICON    our own 871 MedicationIDs. 669 of their names carry the
                   generic in a parseable shape -- `losartan (COZAAR) 50 mg
                   oral tablet` -- and that name came from WellDoc's export,
                   not from the FDA Directory the resolver reads.
                   ANSWERS: does it handle the dialect it will be pointed at.

    E3  AGREEMENT  the two resolution paths against each other. SILVER.
                   ANSWERS: an upper bound, and nothing else. Two paths
                   agreeing is not two paths being right, which is precisely
                   how the NDC segmentation bug survived a measurement cycle.

Neither E1 nor E2 substitutes for the other. MEPS contains no MedicationID, no
Chinese drug column and no 'Basal Insulin'; our corpus contains no truncated
pharmacy string and has no independent answer key at product level.

TWO GRANULARITIES, NEVER ONE NUMBER
================================================================================
Copied from RxMap (JAMIA Open 2026), and it is the right split:

    ingredient   WHAT the drug is.  Partial credit, because a combination
                 product is partly right when one of two ingredients is found.
    product      WHICH product it is. Exact, at the NDC labeler+product level.

Coverage is reported with both, as a risk-coverage curve over MedConf, because
either number alone can be moved without improving anything: answer nothing and
accuracy is 1.0, answer everything and coverage is 1.0.
"""
__version__ = "0.1.0"
