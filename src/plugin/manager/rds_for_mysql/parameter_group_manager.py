import logging

from spaceone.inventory.plugin.collector.lib import *

from plugin.conf.cloud_service_conf import AUTH_TYPE, ASSET_URL, REGION
from plugin.connector.rds_for_mysql.parameter_group_connector import ParameterGroupConnector
from plugin.manager.base import NHNCloudBaseManager

_LOGGER = logging.getLogger("cloudforet")


class ParameterGroupManager(NHNCloudBaseManager):
    auth_type = AUTH_TYPE.APP_KEY
    AVAILABLE_REGIONS = [REGION.KR1, REGION.KR2, REGION.JP1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloud_service_group = "RDS for MySQL"
        self.cloud_service_type = "Parameter Group"
        self.metadata_path = f"metadata/{self.cloud_service_group.replace(' ', '_').lower()}/{self.cloud_service_type.replace(' ', '_').lower()}.yaml"

    def create_cloud_service_type(self):
        cloud_service_type = make_cloud_service_type(
            name=self.cloud_service_type,
            group=self.cloud_service_group,
            provider=self.provider,
            metadata_path=self.metadata_path,
            is_primary=False,
            is_major=False,
            tags={
                "spaceone:icon": f"{ASSET_URL}/rds_for_mysql.png"
            },
            labels=["Management"]
        )

        return cloud_service_type

    def create_cloud_service(self, secret_data):
        parameter_group_connector = ParameterGroupConnector()
        
        parameter_groups = []
        for AVAILABLE_REGION in self.AVAILABLE_REGIONS:
            if (secret_data.get("user_access_key_id") is not None and 
                secret_data.get("secret_access_key") is not None):
                parameter_groups = parameter_group_connector.list_parameter_groups(secret_data.get("app_key"), secret_data.get("user_access_key_id"), secret_data.get("secret_access_key"), AVAILABLE_REGION)
            for parameter_group in parameter_groups:
                reference = {
                    "resource_id": parameter_group.get("parameterGroupId"),
                    "external_link": ""
                }
                
                cloud_service = make_cloud_service(
                    name=parameter_group["parameterGroupName"],
                    cloud_service_type=self.cloud_service_type,
                    cloud_service_group=self.cloud_service_group,
                    provider=self.provider,
                    data=parameter_group,
                    account=secret_data.get("project_id"),
                    reference=reference,
                    region_code=AVAILABLE_REGION.name
                )

                yield cloud_service