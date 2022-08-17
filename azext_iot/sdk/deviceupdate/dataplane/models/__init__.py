# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator (autorest: 3.8.4, generator: @autorest/python@5.19.0)
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from ._models_py3 import AccessCondition
from ._models_py3 import CloudInitiatedRollbackPolicy
from ._models_py3 import CloudInitiatedRollbackPolicyFailure
from ._models_py3 import ContractModel
from ._models_py3 import Deployment
from ._models_py3 import DeploymentDeviceState
from ._models_py3 import DeploymentDeviceStatesFilter
from ._models_py3 import DeploymentDeviceStatesList
from ._models_py3 import DeploymentOrderBy
from ._models_py3 import DeploymentStatus
from ._models_py3 import DeploymentsList
from ._models_py3 import Device
from ._models_py3 import DeviceClass
from ._models_py3 import DeviceClassProperties
from ._models_py3 import DeviceClassSubgroup
from ._models_py3 import DeviceClassSubgroupDeploymentStatus
from ._models_py3 import DeviceClassSubgroupFilter
from ._models_py3 import DeviceClassSubgroupUpdatableDevices
from ._models_py3 import DeviceClassSubgroupUpdatableDevicesList
from ._models_py3 import DeviceClassSubgroupsList
from ._models_py3 import DeviceClassesList
from ._models_py3 import DeviceFilter
from ._models_py3 import DeviceHealth
from ._models_py3 import DeviceHealthFilter
from ._models_py3 import DeviceHealthList
from ._models_py3 import DeviceOperation
from ._models_py3 import DeviceOperationsList
from ._models_py3 import DeviceUpdateAgentId
from ._models_py3 import DevicesList
from ._models_py3 import Error
from ._models_py3 import ErrorResponse
from ._models_py3 import FileImportMetadata
from ._models_py3 import Group
from ._models_py3 import GroupOrderBy
from ._models_py3 import GroupsList
from ._models_py3 import HealthCheck
from ._models_py3 import ImportManifestMetadata
from ._models_py3 import ImportUpdateInputItem
from ._models_py3 import InnerError
from ._models_py3 import InstallResult
from ._models_py3 import Instructions
from ._models_py3 import LogCollection
from ._models_py3 import LogCollectionDetailedStatusList
from ._models_py3 import LogCollectionList
from ._models_py3 import LogCollectionOperationDetailedStatus
from ._models_py3 import LogCollectionOperationDeviceStatus
from ._models_py3 import OperationFilter
from ._models_py3 import PatchBody
from ._models_py3 import Step
from ._models_py3 import StepResult
from ._models_py3 import StringsList
from ._models_py3 import Update
from ._models_py3 import UpdateCompliance
from ._models_py3 import UpdateFile
from ._models_py3 import UpdateFileBase
from ._models_py3 import UpdateFileDownloadHandler
from ._models_py3 import UpdateFilter
from ._models_py3 import UpdateId
from ._models_py3 import UpdateInfo
from ._models_py3 import UpdateInfoList
from ._models_py3 import UpdateList
from ._models_py3 import UpdateOperation
from ._models_py3 import UpdateOperationsList


from ._device_update_client_enums import DeploymentState
from ._device_update_client_enums import DeviceClassSubgroupDeploymentState
from ._device_update_client_enums import DeviceDeploymentState
from ._device_update_client_enums import DeviceHealthState
from ._device_update_client_enums import DeviceState
from ._device_update_client_enums import GroupType
from ._device_update_client_enums import HealthCheckResult
from ._device_update_client_enums import ImportType
from ._device_update_client_enums import OperationFilterStatus
from ._device_update_client_enums import OperationStatus
from ._device_update_client_enums import StepType
from ._patch import __all__ as _patch_all
from ._patch import *  # type: ignore # pylint: disable=unused-wildcard-import
from ._patch import patch_sdk as _patch_sdk
__all__ = [
    'AccessCondition',
    'CloudInitiatedRollbackPolicy',
    'CloudInitiatedRollbackPolicyFailure',
    'ContractModel',
    'Deployment',
    'DeploymentDeviceState',
    'DeploymentDeviceStatesFilter',
    'DeploymentDeviceStatesList',
    'DeploymentOrderBy',
    'DeploymentStatus',
    'DeploymentsList',
    'Device',
    'DeviceClass',
    'DeviceClassProperties',
    'DeviceClassSubgroup',
    'DeviceClassSubgroupDeploymentStatus',
    'DeviceClassSubgroupFilter',
    'DeviceClassSubgroupUpdatableDevices',
    'DeviceClassSubgroupUpdatableDevicesList',
    'DeviceClassSubgroupsList',
    'DeviceClassesList',
    'DeviceFilter',
    'DeviceHealth',
    'DeviceHealthFilter',
    'DeviceHealthList',
    'DeviceOperation',
    'DeviceOperationsList',
    'DeviceUpdateAgentId',
    'DevicesList',
    'Error',
    'ErrorResponse',
    'FileImportMetadata',
    'Group',
    'GroupOrderBy',
    'GroupsList',
    'HealthCheck',
    'ImportManifestMetadata',
    'ImportUpdateInputItem',
    'InnerError',
    'InstallResult',
    'Instructions',
    'LogCollection',
    'LogCollectionDetailedStatusList',
    'LogCollectionList',
    'LogCollectionOperationDetailedStatus',
    'LogCollectionOperationDeviceStatus',
    'OperationFilter',
    'PatchBody',
    'Step',
    'StepResult',
    'StringsList',
    'Update',
    'UpdateCompliance',
    'UpdateFile',
    'UpdateFileBase',
    'UpdateFileDownloadHandler',
    'UpdateFilter',
    'UpdateId',
    'UpdateInfo',
    'UpdateInfoList',
    'UpdateList',
    'UpdateOperation',
    'UpdateOperationsList',
    'DeploymentState',
    'DeviceClassSubgroupDeploymentState',
    'DeviceDeploymentState',
    'DeviceHealthState',
    'DeviceState',
    'GroupType',
    'HealthCheckResult',
    'ImportType',
    'OperationFilterStatus',
    'OperationStatus',
    'StepType',
]
__all__.extend([p for p in _patch_all if p not in __all__])
_patch_sdk()