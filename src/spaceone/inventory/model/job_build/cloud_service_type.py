import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField, DateTimeDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_server_conf = os.path.join(current_dir, 'widget/count_by_server.yml')
count_by_job_conf = os.path.join(current_dir, 'widget/count_by_job.yml')
count_by_result_conf = os.path.join(current_dir, 'widget/count_by_result.yml')


cst_job = CloudServiceTypeResource()
cst_job.name = 'Build'
cst_job.provider = 'jenkins'
cst_job.group = 'Jenkins'
cst_job.is_primary = True
cst_job.is_major = True
cst_job.labels = ['Application Integration']
cst_job.tags = {
    'spaceone:icon': 'https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/jenkins.svg',
}

cst_job._metadata = CloudServiceTypeMeta.set_meta(
    fields=[
        TextDyField.data_source('ID', 'data.id', options={
            'is_optional': True
        }),
        EnumDyField.data_source('Result', 'data.result', default_state={
            'safe': ['SUCCESS'],
            'alert': ['FAILURE']
        }),
        TextDyField.data_source('Queue ID', 'data.queue_id', options={
            'is_optional': True
        }),
        TextDyField.data_source('Duration', 'data.duration', options={
            'is_optional': True
        }),
        TextDyField.data_source('Estimated Duration', 'data.estimated_duration', options={
            'is_optional': True
        }),
        TextDyField.data_source('Keep Log', 'data.keep_log', options={
            'is_optional': True
        }),
        TextDyField.data_source('URL', 'data.url', options={
            'is_optional': True
        }),
        TextDyField.data_source('Executor', 'data.executor', options={
            'is_optional': True
        }),
        TextDyField.data_source('Description', 'data.description', options={
            'is_optional': True
        }),
        TextDyField.data_source('Job URL', 'data.job_url', options={
            'is_optional': True
        }),
        TextDyField.data_source('Job Name', 'data.job_name', options={
            'is_optional': True
        }),
        DateTimeDyField.data_source('Created At', 'data.created_at', options={
            'is_optional': True
        })
    ],
    search=[
        SearchField.set(name='ID', key='data.id'),
        SearchField.set(name='Name', key='data.full_display_name'),
        SearchField.set(name='Result', key='data.result'),
        SearchField.set(name='Queue ID', key='data.queue_id'),
        SearchField.set(name='Duration', key='data.duration', data_type='integer'),
        SearchField.set(name='Estimated Duration', key='data.estimated_duration', data_type='integer'),
        SearchField.set(name='Keep Log', key='data.keep_log', data_type='boolean'),
        SearchField.set(name='URL', key='data.url'),
        SearchField.set(name='Description', key='data.description'),
        SearchField.set(name='Job Name', key='data.job_name'),
        SearchField.set(name='Job URL', key='data.job_url'),
        SearchField.set(name='Building', key='data.building', data_type='boolean'),
        SearchField.set(name='Created At', key='data.created_at', data_type='datetime')
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_server_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_job_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_result_conf))
    ]
)

BUILD_CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_job}),
]
