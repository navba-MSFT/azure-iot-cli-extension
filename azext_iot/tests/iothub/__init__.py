# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import pytest

from time import sleep
from azext_iot.tests.helpers import (
    add_test_tag,
    assign_role_assignment,
    clean_up_iothub_device_config,
    create_storage_account,
    set_cmd_auth_type
)
from azext_iot.tests.settings import DynamoSettings, ENV_SET_TEST_IOTHUB_REQUIRED, ENV_SET_TEST_IOTHUB_OPTIONAL
from azext_iot.tests.generators import generate_generic_id
from azext_iot.tests import CaptureOutputLiveScenarioTest

from azext_iot.common.certops import create_self_signed_certificate
from azext_iot.common.shared import AuthenticationTypeDataplane
from azext_iot.tests.test_constants import ResourceTypes

DATAPLANE_AUTH_TYPES = [
    AuthenticationTypeDataplane.key.value,
    AuthenticationTypeDataplane.login.value,
    "cstring",
]

PRIMARY_THUMBPRINT = create_self_signed_certificate(
    subject="aziotcli", valid_days=1, cert_output_dir=None
)["thumbprint"]
SECONDARY_THUMBPRINT = create_self_signed_certificate(
    subject="aziotcli", valid_days=1, cert_output_dir=None
)["thumbprint"]

DEVICE_TYPES = ["non-edge", "edge"]
PREFIX_DEVICE = "test-device-"
PREFIX_EDGE_DEVICE = "test-edge-device-"
PREFIX_DEVICE_MODULE = "test-module-"
PREFIX_CONFIG = "test-config-"
PREFIX_EDGE_CONFIG = "test-edgedeploy-"
PREFIX_JOB = "test-job-"
USER_ROLE = "IoT Hub Data Contributor"
DEFAULT_CONTAINER = "devices"

settings = DynamoSettings(req_env_set=ENV_SET_TEST_IOTHUB_REQUIRED, opt_env_set=ENV_SET_TEST_IOTHUB_OPTIONAL)
ENTITY_RG = settings.env.azext_iot_testrg
ENTITY_NAME = settings.env.azext_iot_testhub or "test-hub-" + generate_generic_id()
STORAGE_ACCOUNT = settings.env.azext_iot_teststorageaccount or "hubstore" + generate_generic_id()[:4]
STORAGE_CONTAINER = settings.env.azext_iot_teststoragecontainer or DEFAULT_CONTAINER
MAX_RBAC_ASSIGNMENT_TRIES = settings.env.azext_iot_rbac_max_tries or 10
ROLE_ASSIGNMENT_REFRESH_TIME = 120


@pytest.mark.usefixtures("fixture_provision_existing_hub_role", "fixture_provision_existing_hub_device_config")
class IoTLiveScenarioTest(CaptureOutputLiveScenarioTest):
    def __init__(self, test_scenario, add_data_contributor=True):
        assert test_scenario
        self.entity_rg = ENTITY_RG
        self.entity_name = ENTITY_NAME
        super(IoTLiveScenarioTest, self).__init__(test_scenario)

        if hasattr(self, 'storage_cstring'):
            self._create_storage_account()

        if not settings.env.azext_iot_testhub:
            hubs_list = self.cmd(
                'iot hub list -g "{}"'.format(self.entity_rg)
            ).get_output_in_json()

            target_hub = None
            for hub in hubs_list:
                if hub["name"] == self.entity_name:
                    target_hub = hub
                    break

            if not target_hub:
                if hasattr(self, 'storage_cstring'):
                    self.cmd(
                        "iot hub create --name {} --resource-group {} --fc {} --fcs {} --sku S1 ".format(
                            self.entity_name, self.entity_rg,
                            self.storage_container, self.storage_cstring
                        )
                    )
                else:
                    self.cmd(
                        "iot hub create --name {} --resource-group {} --sku S1 ".format(
                            self.entity_name, self.entity_rg
                        )
                    )
                sleep(ROLE_ASSIGNMENT_REFRESH_TIME)

                target_hub = self.cmd(
                    "iot hub show -n {} -g {}".format(self.entity_name, self.entity_rg)
                ).get_output_in_json()

                if add_data_contributor:
                    self._add_data_contributor(target_hub)

        self.region = self.get_region()
        self.connection_string = self.get_hub_cstring()
        add_test_tag(
            cmd=self.cmd,
            name=self.entity_name,
            rg=self.entity_rg,
            rtype=ResourceTypes.hub.value,
            test_tag=test_scenario
        )

    def _add_data_contributor(self, target_hub):
        account = self.cmd("account show").get_output_in_json()
        user = account["user"]

        if user["name"] is None:
            raise Exception("User not found")

        assign_role_assignment(
            role=USER_ROLE,
            scope=target_hub["id"],
            assignee=user["name"],
            max_tries=MAX_RBAC_ASSIGNMENT_TRIES
        )

    def generate_device_names(self, count=1, edge=False):
        names = [
            self.create_random_name(
                prefix=PREFIX_DEVICE if not edge else PREFIX_EDGE_DEVICE, length=32
            )
            for i in range(count)
        ]
        return names

    def generate_module_names(self, count=1):
        return [
            self.create_random_name(prefix=PREFIX_DEVICE_MODULE, length=32)
            for i in range(count)
        ]

    def generate_config_names(self, count=1, edge=False):
        names = [
            self.create_random_name(
                prefix=PREFIX_CONFIG if not edge else PREFIX_EDGE_CONFIG, length=32
            )
            for i in range(count)
        ]
        return names

    def generate_job_names(self, count=1):
        return [
            self.create_random_name(prefix=PREFIX_JOB, length=32) for i in range(count)
        ]

    def _create_storage_account(self):
        """
        Create a storage account and container if a storage account was not created yet.
        Populate the following variables if needed:
          - storage_account_name
          - storage_container
          - storage_cstring
        """
        self.storage_account_name = STORAGE_ACCOUNT
        self.storage_container = STORAGE_CONTAINER

        self.storage_cstring = create_storage_account(
            cmd=self.cmd,
            account_name=self.storage_account_name,
            container_name=self.storage_container,
            rg=self.entity_rg,
            resource_name=self.entity_name,
            create_account=(not settings.env.azext_iot_teststorageaccount)
        )

    def _delete_storage_account(self):
        """
        Delete the storage account if it was created.
        """
        if not settings.env.azext_iot_teststorageaccount:
            self.cmd(
                "storage account delete -n {} -g {} -y".format(
                    self.storage_account_name, self.entity_rg
                ),
            )

        elif not settings.env.azext_iot_teststoragecontainer:
            self.cmd(
                "storage container delete -n {} --connection-string '{}'".format(
                    self.storage_account_name, self.storage_cstring
                ),
            )

    def tearDown(self):
        if not settings.env.azext_iot_testhub:
            clean_up_iothub_device_config(
                hub_name=self.entity_name,
                rg=self.entity_rg
            )

    def get_region(self):
        result = self.cmd(
            "iot hub show -n {}".format(self.entity_name)
        ).get_output_in_json()
        locations_set = result["properties"]["locations"]
        for loc in locations_set:
            if loc["role"] == "primary":
                return loc["location"]

    def get_hub_cstring(self, policy="iothubowner"):
        return self.cmd(
            "iot hub connection-string show -n {} -g {} --policy-name {}".format(
                self.entity_name, self.entity_rg, policy
            )
        ).get_output_in_json()["connectionString"]

    def set_cmd_auth_type(self, command: str, auth_type: str) -> str:
        return set_cmd_auth_type(
            command=command, auth_type=auth_type, cstring=self.connection_string
        )

    @pytest.fixture(scope='class', autouse=True)
    def tearDownSuite(self):
        yield None
        if not settings.env.azext_iot_testhub:
            self.cmd(
                "iot hub delete --name {} --resource-group {}".format(
                    ENTITY_NAME, ENTITY_RG
                )
            )
        if hasattr(self, "storage_cstring"):
            self._delete_storage_account()
