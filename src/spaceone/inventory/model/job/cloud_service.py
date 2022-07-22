from schematics.types import PolyModelType

from spaceone.inventory.model.job.data import *
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout, TableDynamicLayout, ListDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


job_meta = ItemDynamicLayout.set_fields('Job', fields=[
    TextDyField.data_source('Name', 'data.name'),
    EnumDyField.data_source('Disabled', 'data.disabled', default_badge={
        'indigo.500': ['false'], 'coral.600': ['true']
    }),
    TextDyField.data_source('Description', 'data.description'),
    TextDyField.data_source('Buildable', 'data.buildable'),
    TextDyField.data_source('URL', 'data.url'),
    TextDyField.data_source('Keep Dependencies', 'data.keep_dependencies'),
    TextDyField.data_source('In Queue', 'data.in_queue'),
    TextDyField.data_source('Concurrent Build', 'data.concurrent_build')
])

build_summary_meta = ItemDynamicLayout.set_fields('Build Summary', fields=[
    TextDyField.data_source('First Build Number', 'data.first_build.number'),
    TextDyField.data_source('First Build URL', 'data.first_build.url'),
    TextDyField.data_source('Last Build Number', 'data.last_build.number'),
    TextDyField.data_source('Last Build URL', 'data.last_build.url'),
    TextDyField.data_source('Last Completed Build Number', 'data.last_completed_build.number'),
    TextDyField.data_source('Last Completed Build URL', 'data.last_completed_build.url'),
    TextDyField.data_source('Last Failed Build Number', 'data.last_failed_build.number'),
    TextDyField.data_source('Last Failed Build URL', 'data.last_failed_build.url')
])

health_report_meta = ItemDynamicLayout.set_fields('Health Report', fields=[
    TextDyField.data_source('Description', 'data.health_report.description'),
    TextDyField.data_source('Score', 'data.health_report.score'),
])

job = ListDynamicLayout.set_layouts('Job', layouts=[job_meta, build_summary_meta, health_report_meta])

build = TableDynamicLayout.set_fields('Build', root_path='data.builds', fields=[
    TextDyField.data_source('ID', 'number'),
    EnumDyField.data_source('Result', 'result', default_state={
        'safe': ['SUCCESS'],
        'alert': ['FAILURE']
    }),
    TextDyField.data_source('Duration', 'duration'),
    DateTimeDyField.data_source('Created At', 'created_at')
])


job_template_meta = CloudServiceMeta.set_layouts([job, build])


class JenkinsResource(CloudServiceResource):
    cloud_service_group = StringType(default='Jenkins')


class JobResource(JenkinsResource):
    cloud_service_type = StringType(default='Job')
    data = ModelType(Job)
    _metadata = ModelType(CloudServiceMeta, default=job_template_meta, serialized_name='metadata')


class JobResponse(CloudServiceResponse):
    resource = PolyModelType(JobResource)
