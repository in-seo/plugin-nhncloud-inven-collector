import logging

import requests

from plugin.conf.cloud_service_conf import REGION
from plugin.connector.base import NHNCloudBaseConnector

_LOGGER = logging.getLogger("cloudforet")


class LoadBalancerIpACLConnector(NHNCloudBaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_ip_acls(self, secret_data: dict, region: REGION) -> dict:
        token = self.get_token(secret_data)

        url = f"https://{region.name.lower()}-api-network-infrastructure.nhncloudservice.com/v2.0/lbaas/ipacl-groups"
        headers = {"X-Auth-Token": token}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            _LOGGER.error(f"Failed to get LB IP ACLS. {response.json()}")
            raise Exception(f"Failed to get LB IP ACLS. {response.json()}")

        return response.json().get("ipacl_groups", [])