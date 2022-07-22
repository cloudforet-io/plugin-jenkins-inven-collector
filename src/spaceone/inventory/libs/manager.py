import json
import logging
from spaceone.core.manager import BaseManager
from spaceone.inventory.connector.jenkins import JenkinsConnector
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse

_LOGGER = logging.getLogger(__name__)


class CollectManager(BaseManager):
    cloud_service_types = []
    response_schema = None
    collected_region_codes = []

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector = JenkinsConnector(secret_data=secret_data)
        connector.verify()

    def collect_cloud_service_type(self):
        for cloud_service_type in self.cloud_service_types:
            yield cloud_service_type

    def collect_cloud_service(self, params) -> list:
        raise NotImplemented

    def collect_resources(self, params) -> list:
        total_resources = []

        try:
            # Collect Cloud Service Type
            total_resources.extend(self.collect_cloud_service_type())

            # Collect Cloud Service
            resources, error_resources = self.collect_cloud_service(params)
            total_resources.extend(resources)
            total_resources.extend(error_resources)
        except Exception as e:
            _LOGGER.error(f'[collect_resources] {e}', exc_info=True)
            error_resource_response = self.generate_error_response(e, self.cloud_service_types[0].resource.group,
                                                                   self.cloud_service_types[0].resource.name)
            total_resources.append(error_resource_response)

        return total_resources

    @staticmethod
    def generate_error_response(e, cloud_service_group, cloud_service_type):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type
                }})

        return error_resource_response

    @staticmethod
    def generate_resource_error_response(e, cloud_service_group, cloud_service_type, resource_id):
        if type(e) is dict:
            error_resource_response = ErrorResourceResponse({
                'message': json.dumps(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type,
                    'resource_id': resource_id
                }})
        else:
            error_resource_response = ErrorResourceResponse({
                'message': str(e),
                'resource': {
                    'cloud_service_group': cloud_service_group,
                    'cloud_service_type': cloud_service_type,
                    'resource_id': resource_id
                }})
        return error_resource_response

