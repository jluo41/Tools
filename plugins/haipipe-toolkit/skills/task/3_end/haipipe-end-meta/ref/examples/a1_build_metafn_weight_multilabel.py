#!/usr/bin/env python3
"""
Build MetaFn - Weight Loss Multi-Label Prediction Endpoint

WellDoc 2023 CVS-DeRx weight prediction endpoint.
Predicts probability of achieving 2/4/6/8/10/12% weight loss
within 60 days (WeightAf2M horizon).

[BOILERPLATE] - Standard code, copy as-is
[CUSTOMIZE]   - Change for your specific MetaFn
"""

# region Setup
# ============================================================================
# [BOILERPLATE] Imports & Path Setup
# ============================================================================
import os
import sys
import inspect

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.abspath(os.path.join(script_dir, '../../..'))
sys.path.insert(0, os.path.join(workspace_dir, 'code'))

from haipipe import setup_workspace
from haipipe.base import Base
from haipipe.endpoint_base.builder.metafn import FN_META_PATH

WORKSPACE_PATH, SPACE, logger = setup_workspace()
META_FN_PATH = os.path.join(SPACE['CODE_FN'], FN_META_PATH)
os.makedirs(META_FN_PATH, exist_ok=True)
# endregion


# region MetaFn Definition
# ============================================================================
# [CUSTOMIZE] MetaFn for weight loss multi-label prediction
# ============================================================================
META_FN_NAME = 'WeightLossMultiLabel_v260305'

print(f"Building MetaFn: {META_FN_NAME}")

def MetaFn(SPACE):
    """
    Model metadata for WellDoc weight-loss multi-label prediction endpoint.

    Predicts probability of achieving each weight-loss tier (2/4/6/8/10/12%)
    within 60 days of the trigger date (WeightAf2M horizon).
    """
    ENDPOINT_NAME = SPACE['MODEL_ENDPOINT']

    modelName = 'WellDocWeightLossMultiLabel'
    Local_to_External_ModelSeries = {ENDPOINT_NAME: modelName}
    External_to_Local_ModelSeries = {v: k for k, v in Local_to_External_ModelSeries.items()}

    modelMetadata = [{
        'modelName': modelName,
        'predictionType': 'weight_loss_probability',
        'horizon': 'WeightAf2M',
        'horizon_description': 'target +60d, window [+50d, +70d]',
        'predictions': [
            'loss_gt2pct',
            'loss_gt4pct',
            'loss_gt6pct',
            'loss_gt8pct',
            'loss_gt10pct',
            'loss_gt12pct',
        ]
    }]

    inputSchema = [
        {'name': 'patient_id',          'type': 'string', 'required': True,
         'description': 'Patient identifier'},
        {'name': 'observation_dt',      'type': 'string', 'required': True,
         'description': 'Trigger date (ISO timestamp, weight-log day)'},
        {'name': 'models',              'type': 'string', 'required': True,
         'description': 'Requested models as JSON array string'},
        {'name': 'ptt',                 'type': 'string', 'required': True,
         'description': 'Patient demographics as JSON string (single record)'},
        {'name': 'weight_entries',      'type': 'string', 'required': True,
         'description': 'Weight history as JSON array (up to 90d lookback)'},
        {'name': 'cgm_entries',         'type': 'string', 'required': False,
         'description': 'CGM readings as JSON array (up to 90d lookback)'},
        {'name': 'diet_entries',        'type': 'string', 'required': False,
         'description': 'Diet logs as JSON array (up to 90d lookback)'},
        {'name': 'exercise_entries',    'type': 'string', 'required': False,
         'description': 'Exercise logs as JSON array (up to 90d lookback)'},
        {'name': 'medication_entries',  'type': 'string', 'required': False,
         'description': 'Medication records as JSON array (up to 90d lookback)'},
        {'name': 'height_entries',      'type': 'string', 'required': False,
         'description': 'Height measurements as JSON array'},
        {'name': 'step_entries',        'type': 'string', 'required': False,
         'description': 'Step count records as JSON array'},
        {'name': 'sleep_entries',       'type': 'string', 'required': False,
         'description': 'Sleep records as JSON array'},
    ]

    outputSchema = [
        {'name': 'predictions', 'type': 'string',
         'description': 'JSON with ranked weight-loss tier probabilities (0-100 scale)'}
    ]

    metadata_response = {
        'body': {'modelMetadata': modelMetadata},
        'contentType': 'application/json',
        'invokedProductionVariant': 'AllTraffic'
    }

    return {
        'Local_to_External_ModelSeries': Local_to_External_ModelSeries,
        'External_to_Local_ModelSeries': External_to_Local_ModelSeries,
        'modelMetadata': modelMetadata,
        'metadata_response': metadata_response,
        'inputSchema': inputSchema,
        'outputSchema': outputSchema,
    }


MetaFn.fn_string = inspect.getsource(MetaFn)
# endregion


# region Save + Test
prefix = []
fn_variables = [MetaFn]
pycode = Base.convert_variables_to_pystirng(fn_variables=fn_variables, prefix=prefix)
pycode = f'"""\n{META_FN_NAME} - MetaFn\n\nWeight loss multi-label prediction endpoint metadata.\n"""\n\n' + pycode

pypath = os.path.join(META_FN_PATH, f'{META_FN_NAME}.py')
with open(pypath, 'w') as f:
    f.write(pycode)
print(f"Saved: {pypath}")

# Test
if 'MODEL_ENDPOINT' not in SPACE:
    SPACE['MODEL_ENDPOINT'] = 'endpoint_weight_af2m_multilabel/v0001'
result = MetaFn(SPACE)
print(f"modelName:   {result['modelMetadata'][0]['modelName']}")
print(f"predictions: {result['modelMetadata'][0]['predictions']}")
print(f"DONE: {META_FN_NAME}")
# endregion
