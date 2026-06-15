#!/usr/bin/env python3
"""
Build MetaFn - Model Metadata Function for CGM Databricks Deployment

Creates MetaFn for CGM glucose forecasting model deployed to Databricks Model Serving:
- Returns model metadata for API responses
- Provides MLflow signature schema (inputSchema/outputSchema) for Unity Catalog
- Defines Databricks dataframe_records payload format

================================================================================
TEMPLATE GUIDE:
================================================================================

[BOILERPLATE] - Standard code, copy as-is
[CUSTOMIZE]   - Change for your specific MetaFn

STRUCTURE:
  1. CONFIGURATION - Define MetaFn name
  2. FUNCTION - Define MetaFn logic (always named MetaFn)
  3. SAVE - Save to production using Base utility
  4. SUMMARY - Display results and usage examples

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

print("="*80)
print("Building MetaFn: Model Metadata Function for CGM Databricks Deployment")
print("="*80)

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
META_FN_NAME = 'CGMDecoder_DBR_v260101'

print(f"\nBuilding MetaFn: {META_FN_NAME}")
print("="*80)

# -------- FUNCTION --------
def MetaFn(SPACE):
    """
    Model metadata function for CGM Databricks Model Serving endpoint.

    Returns model registry information, prediction type, and MLflow signature schema
    for Databricks Unity Catalog deployment with dataframe_records payload format.

    Parameters
    ----------
    SPACE : dict
        Workspace configuration with MODEL_ENDPOINT

    Returns
    -------
    dict
        Meta results with:
        - Local_to_External_ModelSeries: Model name mapping
        - External_to_Local_ModelSeries: Reverse mapping
        - modelMetadata: Model metadata for API response
        - metadata_response: Full metadata response structure
        - inputSchema: MLflow/Unity Catalog input schema (NEW)
        - outputSchema: MLflow/Unity Catalog output schema (NEW)
    """
    ENDPOINT_NAME = SPACE['MODEL_ENDPOINT']
    Local_to_External_ModelSeries = {ENDPOINT_NAME: ENDPOINT_NAME}
    External_to_Local_ModelSeries = {v:k for k,v in Local_to_External_ModelSeries.items()}

    modelMetadata = []
    d = {}
    d['modelName'] = ENDPOINT_NAME
    d['predictionType'] = 'glucose_forecast'
    d['forecastHorizon'] = 12  # 12 timesteps (1 hour with 5-min intervals)
    d['unit'] = 'mg/dL'
    modelMetadata.append(d)

    # Input schema for MLflow/Unity Catalog signature
    # Defines what inputs the endpoint accepts (matches dataframe_records format)
    inputSchema = [
        {
            'name': 'TriggerName_to_CaseTriggerList',
            'type': 'string',
            'required': True,
            'description': 'Trigger configuration with PatientID, ObsDT_UTC, TimezoneOffset (JSON string)'
        },
        {
            'name': 'inference_form',
            'type': 'string',
            'required': True,
            'description': 'Patient data in inference format with ElogBGEntry, Diet, Exercise, Medication (JSON string)'
        },
        {
            'name': 'models',
            'type': 'string',
            'required': True,
            'description': 'List of requested model endpoints as JSON array (e.g., ["endpoint_cgm_decoder_ohio/v0001"])'
        },
        {
            'name': '_metadata',
            'type': 'string',
            'required': False,
            'description': 'Optional metadata for the request (e.g., example_id for testing)'
        }
    ]

    # Output schema for MLflow/Unity Catalog signature
    # Defines what outputs the endpoint returns
    outputSchema = [
        {
            'name': 'predictions',
            'type': 'string',
            'description': 'Glucose forecast predictions as JSON string with timestamps and predicted values'
        }
    ]

    metadata_response = {
        "body": {
            "modelMetadata": modelMetadata
        },
        "contentType": "application/json",
        "invokedProductionVariant": "AllTraffic"
    }

    meta_results = {
        'Local_to_External_ModelSeries': Local_to_External_ModelSeries,
        'External_to_Local_ModelSeries': External_to_Local_ModelSeries,
        'modelMetadata': modelMetadata,
        'metadata_response': metadata_response,
        'inputSchema': inputSchema,      # NEW: For MLflow signature
        'outputSchema': outputSchema,    # NEW: For MLflow signature
    }
    return meta_results


# Attach function string for reloading
MetaFn.fn_string = inspect.getsource(MetaFn)

# -------- SAVE --------
# Generate Python code using Base utility
prefix = []
fn_variables = [MetaFn]
pycode = Base.convert_variables_to_pystirng(fn_variables=fn_variables, prefix=prefix)

# Add docstring at the top
pycode = f'"""\n{META_FN_NAME} - MetaFn\n\n' + \
         'Model metadata function for CGM Databricks Model Serving endpoint.\n"""\n\n' + \
         pycode

# Save to file
pypath = os.path.join(META_FN_PATH, f'{META_FN_NAME}.py')
with open(pypath, 'w') as f:
    f.write(pycode)

print(f"✓ Saved {META_FN_NAME} to: {pypath}")

# endregion


# region Testing
# ============================================================================
# [BOILERPLATE] Test MetaFn
# ============================================================================
print("\n" + "="*80)
print("Testing MetaFn")
print("="*80)

# Set test MODEL_ENDPOINT if not already set
if 'MODEL_ENDPOINT' not in SPACE:
    SPACE['MODEL_ENDPOINT'] = 'cgm-decoder-v1'
    print(f"Using test MODEL_ENDPOINT: {SPACE['MODEL_ENDPOINT']}")

meta_results = MetaFn(SPACE)

print(f"\n✓ MetaFn executed successfully!")
print(f"\nModel metadata:")
print(f"  Endpoint: {SPACE.get('MODEL_ENDPOINT', 'N/A')}")
print(f"  Prediction Type: {meta_results['modelMetadata'][0]['predictionType']}")
print(f"  Forecast Horizon: {meta_results['modelMetadata'][0]['forecastHorizon']} timesteps")
print(f"  Unit: {meta_results['modelMetadata'][0]['unit']}")

# endregion


# region Summary
# ============================================================================
# [BOILERPLATE] Summary
# ============================================================================
print("\n" + "="*80)
print("✅ COMPLETE: MetaFn Built")
print("="*80)
print(f"\nCreated MetaFn: {META_FN_NAME}")
print(f"✓ Saved to: {pypath}")
print(f"✓ Ready for deployment")

print("\n" + "="*80)
print("Usage in Endpoint Pipeline")
print("="*80)
print(f"""
from haipipe.endpoint_base.builder.metafn import MetaFn

# Load MetaFn
metafn = MetaFn('{META_FN_NAME}', SPACE)
meta_results = metafn.MetaFn(SPACE)

# Returns model metadata for API responses
print(meta_results['modelMetadata'])
""")

print("="*80)

# endregion
