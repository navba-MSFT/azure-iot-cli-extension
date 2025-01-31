# coding=utf-8
# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import pytest
from azext_iot.dps.providers.discovery import DPSDiscovery
from azext_iot.common._azure import parse_iot_dps_connection_string


@pytest.fixture
def get_mgmt_client(mocker, fixture_cmd):
    patched_get_raw_token = mocker.patch(
        "azure.cli.core._profile.Profile.get_raw_token"
    )
    patched_get_raw_token.return_value = (
        mocker.MagicMock(name="creds"),
        mocker.MagicMock(name="subscription"),
        mocker.MagicMock(name="tenant"),
    )
    patch = mocker.patch("azext_iot._factory.iot_service_provisioning_factory")
    patch.return_value = None

    return patch


class TestDPSDiscovery:
    def test_get_target_by_cstring(self, fixture_cmd, get_mgmt_client):
        discovery = DPSDiscovery(cmd=fixture_cmd)

        fake_login = (
            "HostName=COOLDPS.azure-devices-provisioning.net;"
            "SharedAccessKeyName=provisioningserviceowner;"
            "SharedAccessKey=AB+c/+5nm2XpDXcffhnGhnxz/TVF4m5ag7AuVIGwchj="
        )
        parsed_fake_login = parse_iot_dps_connection_string(fake_login)

        target = discovery.get_target(
            resource_name=None, resource_group_name=None, login=fake_login
        )

        # Ensure no ARM calls are made
        assert get_mgmt_client.call_count == 0

        assert target["cs"] == fake_login
        assert target["entity"] == parsed_fake_login["HostName"]
        assert target["policy"] == parsed_fake_login["SharedAccessKeyName"]
        assert target["primarykey"] == parsed_fake_login["SharedAccessKey"]

        target = discovery.get_target_by_cstring(fake_login)

        # Ensure no ARM calls are made
        assert get_mgmt_client.call_count == 0

        assert target["cs"] == fake_login
        assert target["entity"] == parsed_fake_login["HostName"]
        assert target["policy"] == parsed_fake_login["SharedAccessKeyName"]
        assert target["primarykey"] == parsed_fake_login["SharedAccessKey"]
