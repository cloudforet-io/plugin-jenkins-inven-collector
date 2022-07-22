import time
import logging
import json

from spaceone.core.service import *
from spaceone.inventory.manager.jenkins_manager import JenkinsManager
from spaceone.inventory.libs.schema.cloud_service import ErrorResourceResponse
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)
        self.execute_managers = []

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        capability = {
            'filter_format': FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE,
            'supported_features': SUPPORTED_FEATURES,
            'supported_schedules': SUPPORTED_SCHEDULES
        }
        return {'metadata': capability}

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})
        if secret_data != {}:
            jenkins_manager: JenkinsManager = self.locator.get_manager('JenkinsManager')
            active = jenkins_manager.verify({}, secret_data)

        return {}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def collect(self, params):
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
        """

        start_time = time.time()

        _LOGGER.debug(f'EXECUTOR START')
        jenkins_manager: JenkinsManager = self.locator.get_manager('JenkinsManager')

        try:
            for result in jenkins_manager.collect_resources(params):
                yield result.to_primitive()
        except Exception as e:
            _LOGGER.error(f'[collect] failed to yield result => {e}', exc_info=True)
            error_resource_response = self.generate_error_response(e, '', 'inventory.Error')
            yield error_resource_response.to_primitive()

        _LOGGER.debug(f'TOTAL TIME : {time.time() - start_time} Seconds')

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
