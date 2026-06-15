#!/usr/bin/env python3
"""
Build MetaFn - Model Metadata Function for MIMIC-IV Mortality Prediction

Creates MetaFn for MIMIC-IV in-hospital mortality prediction endpoint:
- Returns model metadata for API responses
- Provides MLflow signature schema (inputSchema/outputSchema) for Unity Catalog
- Defines model name mapping (local endpoint name ↔ model series name)

================================================================================
TEMPLATE GUIDE:
================================================================================

[BOILERPLATE] - Standard code, copy as-is
[CUSTOMIZE]   - Change for your specific MetaFn

STRUCTURE:
  1. CONFIGURATION - Define MetaFn name
  2. FUNCTION - Define MetaFn logic (always named MetaFn)
  3. SAVE - Save to production using Base utility
  4. TEST - Verify MetaFn output structure
  5. SUMMARY - Display results and usage examples

================================================================================
"""

# region Setup
# ============================================================================
# [BOILERPLATE] Imports & Path Setup
# ============================================================================
import os
import sys
import inspect

# Add workspace to path
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.abspath(os.path.join(script_dir, '../../..'))
sys.path.insert(0, os.path.join(workspace_dir, 'code'))

from haipipe import setup_workspace
from haipipe.base import Base
from haipipe.endpoint_base.builder.metafn import FN_META_PATH

print("=" * 80)
print("Building MetaFn: Model Metadata for MIMIC-IV Mortality Prediction")
print("=" * 80)

# ============================================================================
# [BOILERPLATE] Workspace Setup
# ============================================================================
WORKSPACE_PATH, SPACE, logger = setup_workspace()

META_FN_PATH = os.path.join(SPACE['CODE_FN'], FN_META_PATH)
os.makedirs(META_FN_PATH, exist_ok=True)

# endregion


# region MetaFn Definition
# ============================================================================
# [CUSTOMIZE] MetaFn Configuration
# ============================================================================
META_FN_NAME = 'MimicMortality_v260611'

print(f"\nBuilding MetaFn: {META_FN_NAME}")
print("=" * 80)


# ============================================================================
# [CUSTOMIZE] Main MetaFn Function
# ============================================================================
def MetaFn(SPACE):
    """
    Model metadata function for MIMIC-IV in-hospital mortality endpoint.

    Returns model registry information, prediction type, and MLflow signature
    schema. Binary classification: predicts probability of in-hospital death
    at admission time using demographics + clinical data (labs, vitals, meds,
    diagnoses, procedures).

    Parameters
    ----------
    SPACE : dict
        Workspace configuration. Must contain MODEL_ENDPOINT (the endpoint
        name used for routing, e.g. 'mimic.mortality.xgb/v0001').

    Returns
    -------
    dict
        Meta results with:
        - Local_to_External_ModelSeries: {endpoint_name: model_series_name}
        - External_to_Local_ModelSeries: {model_series_name: endpoint_name}
        - modelMetadata: List of model metadata dicts for API response
        - metadata_response: Full metadata response structure (SageMaker format)
        - inputSchema: MLflow/Unity Catalog input schema
        - outputSchema: MLflow/Unity Catalog output schema
    """
    ENDPOINT_NAME = SPACE['MODEL_ENDPOINT']

    # [CUSTOMIZE] Model name mapping
    modelName = 'MimicIV31_MortalityXGB'
    Local_to_External_ModelSeries = {ENDPOINT_NAME: modelName}
    External_to_Local_ModelSeries = {v: k for k, v in Local_to_External_ModelSeries.items()}

    # [CUSTOMIZE] Model metadata — describes what the model does
    modelMetadata = [{
        'modelName': modelName,
        'predictionType': 'in_hospital_mortality',
        'description': 'Predicts probability of in-hospital death at admission time',
        'dataset': 'MIMIC-IV 3.1',
        'algorithm': 'XGBoost S-Learner (single default action)',
        'performance': {'auc_roc': 0.887, 'auc_pr': 0.203, 'accuracy': 0.976},
        'predictions': ['mortality_risk'],
    }]

    # [CUSTOMIZE] Input schema — columns of dataframe_records[0]
    # Describes the Databricks Model Serving wire format.
    # Each field is a column in the dataframe_records payload.
    # Complex data (clinical tables) is JSON-encoded as a string column.
    #
    # Databricks payload format:
    #   {"dataframe_records": [{"patient_id": "...", "source_tables": "{...}", ...}]}
    #
    # Follows CGM pattern: routing fields + one JSON-string field for all clinical data.
    inputSchema = [
        {'name': 'patient_id',    'type': 'string', 'required': True,
         'description': 'MIMIC patient identifier (numeric string, e.g. "10001")'},
        {'name': 'admission_id',  'type': 'string', 'required': True,
         'description': 'Hospital admission ID (HadmID, e.g. "21001")'},
        {'name': 'admit_time',    'type': 'string', 'required': True,
         'description': 'Admission time (ISO timestamp, e.g. "2150-01-01T12:00:00")'},
        {'name': 'source_tables', 'type': 'string', 'required': True,
         'description': 'All clinical source tables as JSON string: '
                        '\'{"Ptt": [...], "Admission": [...], "LabEvent": [...], ...}\'. '
                        'Contains 29 MIMIC-IV table types. Parsed by Input2SrcFn.'},
        {'name': 'models',        'type': 'string', 'required': True,
         'description': 'Model name to invoke (e.g. "MimicIV31_MortalityXGB")'},
        {'name': '_metadata',     'type': 'string', 'required': False,
         'description': 'Optional metadata for request tracking (JSON string)'},
    ]

    # [CUSTOMIZE] Output schema — what the endpoint returns
    outputSchema = [
        {'name': 'predictions', 'type': 'string',
         'description': 'Mortality risk prediction as JSON with mortality_risk (0-1), risk_level, threshold_alerts'},
    ]

    # [BOILERPLATE] Standard response structure
    metadata_response = {
        'body': {'modelMetadata': modelMetadata},
        'contentType': 'application/json',
        'invokedProductionVariant': 'AllTraffic',
    }

    return {
        'Local_to_External_ModelSeries': Local_to_External_ModelSeries,
        'External_to_Local_ModelSeries': External_to_Local_ModelSeries,
        'modelMetadata': modelMetadata,
        'metadata_response': metadata_response,
        'inputSchema': inputSchema,
        'outputSchema': outputSchema,
    }


# [BOILERPLATE] Attach function string for reloading
MetaFn.fn_string = inspect.getsource(MetaFn)

# endregion


# region Save
# ============================================================================
# [BOILERPLATE] Save MetaFn to production
# ============================================================================
prefix = []
fn_variables = [MetaFn]
pycode = Base.convert_variables_to_pystirng(fn_variables=fn_variables, prefix=prefix)

pycode = (
    f'"""\n{META_FN_NAME} - MetaFn\n\n'
    f'MIMIC-IV in-hospital mortality prediction endpoint metadata.\n'
    f'Binary classification: mortality_risk probability at admission time.\n"""\n\n'
    + pycode
)

pypath = os.path.join(META_FN_PATH, f'{META_FN_NAME}.py')
with open(pypath, 'w') as f:
    f.write(pycode)

print(f"✓ Saved {META_FN_NAME} to: {pypath}")

# endregion


# region Test
# ============================================================================
# [BOILERPLATE] Test MetaFn
# ============================================================================
print("\n" + "=" * 80)
print("Testing MetaFn")
print("=" * 80)

# Set test MODEL_ENDPOINT if not already set
if 'MODEL_ENDPOINT' not in SPACE:
    SPACE['MODEL_ENDPOINT'] = 'mimic.mortality.xgb/v0001'
    print(f"Using test MODEL_ENDPOINT: {SPACE['MODEL_ENDPOINT']}")

meta_results = MetaFn(SPACE)

# Validate return structure
assert 'Local_to_External_ModelSeries' in meta_results, "Missing Local_to_External_ModelSeries"
assert 'External_to_Local_ModelSeries' in meta_results, "Missing External_to_Local_ModelSeries"
assert 'modelMetadata' in meta_results, "Missing modelMetadata"
assert 'metadata_response' in meta_results, "Missing metadata_response"
assert 'inputSchema' in meta_results, "Missing inputSchema"
assert 'outputSchema' in meta_results, "Missing outputSchema"

mm = meta_results['modelMetadata'][0]
print(f"\n✓ MetaFn executed successfully!")
print(f"\nModel metadata:")
print(f"  Endpoint:        {SPACE.get('MODEL_ENDPOINT', 'N/A')}")
print(f"  Model Name:      {mm['modelName']}")
print(f"  Prediction Type: {mm['predictionType']}")
print(f"  Dataset:         {mm['dataset']}")
print(f"  Predictions:     {mm['predictions']}")
print(f"  Performance:     AUC-ROC={mm['performance']['auc_roc']}, AUC-PR={mm['performance']['auc_pr']}")
print(f"\nSchema:")
print(f"  Input fields:    {len(meta_results['inputSchema'])} ({sum(1 for f in meta_results['inputSchema'] if f['required'])} required)")
print(f"  Output fields:   {len(meta_results['outputSchema'])}")
print(f"\nMapping:")
print(f"  Local→External:  {meta_results['Local_to_External_ModelSeries']}")
print(f"  External→Local:  {meta_results['External_to_Local_ModelSeries']}")

# endregion


# region Summary
# ============================================================================
# [BOILERPLATE] Summary
# ============================================================================
print("\n" + "=" * 80)
print("✅ COMPLETE: MetaFn Built")
print("=" * 80)
print(f"\nCreated MetaFn: {META_FN_NAME}")
print(f"✓ Saved to: {pypath}")
print(f"✓ Ready for deployment")

print("\n" + "=" * 80)
print("Usage in Endpoint Pipeline")
print("=" * 80)
print(f"""
from haipipe.endpoint_base.builder.metafn import MetaFn

# Load MetaFn
metafn = MetaFn('{META_FN_NAME}', SPACE)
meta_results = metafn.MetaFn(SPACE)

# Returns model metadata for API responses
print(meta_results['modelMetadata'])
print(meta_results['inputSchema'])

# In endpoint config YAML:
#   MetaFn: "{META_FN_NAME}"
""")

print("=" * 80)

# endregion
