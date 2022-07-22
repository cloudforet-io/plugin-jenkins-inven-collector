import os
from spaceone.inventory.libs.common_parser import *
from spaceone.inventory.libs.schema.metadata.dynamic_widget import CardWidget, ChartWidget
from spaceone.inventory.libs.schema.metadata.dynamic_field import TextDyField, SearchField, EnumDyField, ListDyField
from spaceone.inventory.libs.schema.cloud_service_type import CloudServiceTypeResource, CloudServiceTypeResponse, \
    CloudServiceTypeMeta

current_dir = os.path.abspath(os.path.dirname(__file__))

total_count_conf = os.path.join(current_dir, 'widget/total_count.yml')
count_by_server_conf = os.path.join(current_dir, 'widget/count_by_server.yml')


cst_job = CloudServiceTypeResource()
cst_job.name = 'Job'
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
        TextDyField.data_source('Name', 'data.name'),
        EnumDyField.data_source('Disabled', 'data.disabled', default_badge={
            'indigo.500': ['false'], 'coral.600': ['true']
        }),
        TextDyField.data_source('Total Builds', 'data.last_build.number'),
        TextDyField.data_source('Description', 'data.description'),
        TextDyField.data_source('Buildable', 'data.buildable', options={
            'is_optional': True
        }),
        ListDyField.data_source('Health Score', 'data.health_report', options={
            'sub_key': 'score',
            'delimiter': '<br>',
            'is_optional': True
        }),
        TextDyField.data_source('URL', 'data.url', options={
            'is_optional': True
        }),
        TextDyField.data_source('Keep Dependencies', 'data.keep_dependencies', options={
            'is_optional': True
        }),
        TextDyField.data_source('In Queue', 'data.in_queue', options={
            'is_optional': True
        }),
        TextDyField.data_source('Concurrent Build', 'data.concurrent_build', options={
            'is_optional': True
        })
    ],

    search=[
        SearchField.set(name='Name', key='data.name'),
        SearchField.set(name='Disabled', key='data.disabled', data_type='boolean'),
        SearchField.set(name='Total Builds', key='data.last_build.number', data_type='integer'),
        SearchField.set(name='Description', key='data.description'),
        SearchField.set(name='Buildable', key='data.buildable', data_type='boolean'),
        SearchField.set(name='Health Score', key='data.health_report.score', data_type='integer'),
        SearchField.set(name='URL', key='data.url'),
        SearchField.set(name='Keep Dependencies', key='data.keep_dependencies', data_type='boolean'),
        SearchField.set(name='In Queue', key='data.in_queue', data_type='boolean'),
        SearchField.set(name='Concurrent Build', key='data.concurrent_build', data_type='boolean'),
    ],

    widget=[
        CardWidget.set(**get_data_from_yaml(total_count_conf)),
        ChartWidget.set(**get_data_from_yaml(count_by_server_conf))
    ]
)

JOB_CLOUD_SERVICE_TYPES = [
    CloudServiceTypeResponse({'resource': cst_job}),
]
