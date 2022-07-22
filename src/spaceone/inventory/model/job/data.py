from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, BooleanType, BaseType, DateTimeType


class HealthReport(Model):
    description = StringType(serialize_when_none=False)
    icon_class_name = StringType(deserialize_from="iconClassName", serialize_when_none=False)
    icon_url = StringType(deserialize_from="iconUrl", serialize_when_none=False)
    score = IntType(serialize_when_none=False)


class JobBuild(Model):
    url = StringType(serialize_when_none=False)
    number = IntType(serialize_when_none=False)
    result = StringType(serialize_when_none=False)
    duration = IntType(serialize_when_none=False)
    queue_id = IntType(serialize_when_none=False)
    created_at = DateTimeType(serialize_when_none=False)
    console_output = StringType(serialize_when_none=False)

class Job(Model):
    name = StringType(serialize_when_none=False)
    url = StringType(serialize_when_none=False)
    color = StringType(serialize_when_none=False)
    buildable = BooleanType(serialize_when_none=False)
    builds = ListType(ModelType(JobBuild), default=[])
    concurrent_build = BooleanType(deserialize_from="concurrentBuild", serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    disabled = BooleanType(serialize_when_none=False)
    display_name = StringType(deserialize_from="displayName", serialize_when_none=False)
    downstream_projects = ListType(BaseType, deserialize_from="downstreamProjects", default=[])
    first_build = ModelType(JobBuild, deserialize_from="firstBuild", serialize_when_none=False)
    full_display_name = StringType(deserialize_from="fullDisplayName", serialize_when_none=False)
    full_name = StringType(deserialize_from="fullName", serialize_when_none=False)
    health_report = ModelType(HealthReport, serialize_when_none=False)
    in_queue = BooleanType(deserialize_from="inQueue", serialize_when_none=False)
    keep_dependencies = BooleanType(deserialize_from="keepDependencies", serialize_when_none=False)
    label_expression = BooleanType(deserialize_from="labelExpression", serialize_when_none=False)
    last_build = ModelType(JobBuild, deserialize_from="lastBuild", serialize_when_none=False)
    last_completed_build = ModelType(JobBuild, deserialize_from="lastCompletedBuild", serialize_when_none=False)
    last_failed_build = ModelType(JobBuild, deserialize_from="lastFailedBuild", serialize_when_none=False)
    last_stable_build = ModelType(JobBuild, deserialize_from="lastStableBuild", serialize_when_none=False)
    last_successful_build = ModelType(JobBuild, deserialize_from="lastSuccessfulBuild", serialize_when_none=False)
    last_unstable_build = ModelType(JobBuild, deserialize_from="lastUnstableBuild", serialize_when_none=False)
    last_unsuccessful_build = ModelType(JobBuild, deserialize_from="lastUnsuccessfulBuild", serialize_when_none=False)
    next_build_number = IntType(deserialize_from="nextBuildNumber", serialize_when_none=False)
    property = ListType(BaseType, default=[])
    queue_item = BaseType(deserialize_from="queueItem", serialize_when_none=False)
    scm = BaseType(serialize_when_none=False)
    upstream_projects = ListType(BaseType, deserialize_from="upstreamProjects", default=[])

    def reference(self):
        return {
            "resource_id": self.url,
            "external_link": self.url
        }



