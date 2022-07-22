from schematics.types import PolyModelType

from spaceone.inventory.model.job_build.data import *
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.metadata.dynamic_layout import ItemDynamicLayout
from spaceone.inventory.libs.schema.cloud_service import CloudServiceResource, CloudServiceResponse, CloudServiceMeta


build_meta = ItemDynamicLayout.set_fields('Build', fields=[
    TextDyField.data_source('ID', 'data.id'),
    TextDyField.data_source('Name', 'data.full_display_name'),
    EnumDyField.data_source('Result', 'data.result', default_state={
        'safe': ['SUCCESS'],
        'alert': ['FAILURE']
    }),
    TextDyField.data_source('Job Name', 'data.job_name'),
    TextDyField.data_source('Job URL', 'data.job_url'),
    TextDyField.data_source('Queue ID', 'data.queue_id'),
    TextDyField.data_source('Duration', 'data.duration'),
    TextDyField.data_source('Estimated Duration', 'data.estimated_duration'),
    TextDyField.data_source('Keep Log', 'data.keep_log'),
    TextDyField.data_source('URL', 'data.url'),
    TextDyField.data_source('Executor', 'data.executor'),
    TextDyField.data_source('Description', 'data.description'),
    DateTimeDyField.data_source('Created At', 'data.created_at')
])


build_template_meta = CloudServiceMeta.set_layouts([build_meta])


class JenkinsResource(CloudServiceResource):
    cloud_service_group = StringType(default='Jenkins')


class BuildResource(JenkinsResource):
    cloud_service_type = StringType(default='Build')
    data = ModelType(Build)
    _metadata = ModelType(CloudServiceMeta, default=build_template_meta, serialized_name='metadata')


class BuildResponse(CloudServiceResponse):
    resource = PolyModelType(BuildResource)
