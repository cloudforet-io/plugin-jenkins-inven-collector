import logging
import jenkins
from spaceone.core.connector import BaseConnector
from spaceone.inventory.error.custom import *

_LOGGER = logging.getLogger(__name__)


class JenkinsConnector(BaseConnector):

    def __init__(self, **kwargs):
        super().__init__(transaction=None, config=None)

        secret_data = kwargs.get('secret_data')
        endpoint = secret_data.get('endpoint')
        username = secret_data.get('username')
        password = secret_data.get('password')

        if not endpoint:
            raise ERROR_SECRET(key='endpoint')
        if not username:
            raise ERROR_SECRET(key='username')
        if not password:
            raise ERROR_SECRET(key='password')

        self.client = jenkins.Jenkins(endpoint, username=username, password=password)

    def verify(self):
        self.client.get_whoami()

    def get_all_jobs(self):
        return self.client.get_all_jobs()

    def get_job_info(self, job_name):
        return self.client.get_job_info(job_name)

    def get_build_info(self, job_name, build_number):
        return self.client.get_build_info(job_name, build_number)


