import time
import datetime
import logging
from spaceone.inventory.libs.manager import CollectManager
from spaceone.inventory.libs.schema.base import ReferenceModel
from spaceone.inventory.connector.jenkins import JenkinsConnector
from spaceone.inventory.model.job.cloud_service import Job, JobResource, JobResponse
from spaceone.inventory.model.job_build.cloud_service import Build, BuildResource, BuildResponse
from spaceone.inventory.model.job_build.cloud_service_type import BUILD_CLOUD_SERVICE_TYPES
from spaceone.inventory.model.job.cloud_service_type import JOB_CLOUD_SERVICE_TYPES

_LOGGER = logging.getLogger(__name__)


class JenkinsManager(CollectManager):
    cloud_service_types = BUILD_CLOUD_SERVICE_TYPES + JOB_CLOUD_SERVICE_TYPES

    def collect_cloud_service(self, params):
        _LOGGER.debug(f'[collect_cloud_service] START')
        start_time = time.time()
        """
        Args:
            params:
                - options
                - schema
                - secret_data
                - filter
                - zones
        Response:
            CloudServiceResponse/ErrorResourceResponse
        """
        secret_data = params['secret_data']
        collected_cloud_services = []
        error_responses = []

        job_id = ''
        jenkins_conn: JenkinsConnector = self.locator.get_connector('JenkinsConnector', **params)
        jobs = jenkins_conn.get_all_jobs()
        jobs_info = [jenkins_conn.get_job_info(_job.get('name', '')) for _job in jobs]

        build_vos = []
        for _job in jobs_info:
            try:
                job_id = _job['url']

                if _job.get('healthReport'):
                    _job['health_report'] = _job['healthReport'][0]

                for build in _job.get('builds', []):
                    build_info = jenkins_conn.get_build_info(_job['name'], build.get('number'))
                    console_output = jenkins_conn.get_build_console_output(_job['name'], build.get('number'))

                    build.update({
                        'result': build_info.get('result'),
                        'duration': build_info.get('duration'),
                        'queue_id': build_info.get('queueId'),
                        'console_output': console_output
                    })

                    if created_at := self.convert_timestamp_to_datetime(build_info.get('timestamp')):
                        build.update({'created_at': created_at})
                        build_info['created_at'] = created_at

                    build_info.update({
                        'job_url': job_id,
                        'job_name': _job.get('fullDisplayName', ''),
                        'console_output': console_output
                    })

                    build_vos.append(Build(build_info, strict=False))

                job_vo = Job(_job, strict=False)
                job_name = job_vo.name

                job_resource = JobResource({
                    'name': job_name,
                    'account': secret_data.get('endpoint'),
                    'data': job_vo,
                    'reference': ReferenceModel(job_vo.reference())
                })

                collected_cloud_services.append(JobResponse({'resource': job_resource}))
            except Exception as e:
                _LOGGER.error(f'[collect_cloud_service] => {e}', exc_info=True)
                error_response = self.generate_resource_error_response(e, 'BigQuery', 'SQLWorkspace', job_id)
                error_responses.append(error_response)

        for build_vo in build_vos:
            build_resource = BuildResource({
                'name': build_vo.full_display_name,
                'account': secret_data.get('endpoint'),
                'data': build_vo,
                'reference': ReferenceModel(build_vo.reference())
            })
            collected_cloud_services.append(BuildResponse({'resource': build_resource}))

        _LOGGER.debug(f'** Job Finished {time.time() - start_time} Seconds **')
        return collected_cloud_services, error_responses

    @staticmethod
    def convert_timestamp_to_datetime(timestamp):
        created_at = None

        if timestamp:
            created_at = datetime.datetime.fromtimestamp(timestamp/1000)

        return created_at
