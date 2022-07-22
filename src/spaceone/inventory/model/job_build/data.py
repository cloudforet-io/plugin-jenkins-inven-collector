from schematics import Model
from schematics.types import ModelType, ListType, StringType, IntType, DateTimeType, BooleanType, BaseType


class BuildActionCauses(Model):
    short_description = StringType(deserialize_from="shortDescription", serialize_when_none=False)
    use_id = StringType(deserialize_from="userId", serialize_when_none=False)
    user_name = StringType(deserialize_from="userName", serialize_when_none=False)


class BuildAction(Model):
    causes = ListType(ModelType(BuildActionCauses), default=[])


class BuildChangeSet(Model):
    items = ListType(BaseType, default=[])
    kind = BaseType(deserialize_from=False)


class Build(Model):
    job_url = StringType(serialize_when_none=False)
    job_name = StringType(serialize_when_none=False)
    id = StringType(serialize_when_none=False)
    display_name = StringType(deserialize_from="displayName", serialize_when_none=False)
    full_display_name = StringType(deserialize_from="fullDisplayName", serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    executor = BaseType(serialize_when_none=False)
    duration = IntType(serialize_when_none=False)
    estimated_duration = IntType(deserialize_from="estimatedDuration", serialize_when_none=False)
    url = StringType(serialize_when_none=False)
    actions = ListType(ModelType(BuildAction), default=[])
    artifacts = ListType(BaseType, default=[])
    building = BooleanType(serialize_when_none=False)
    change_set = ModelType(BuildChangeSet, serialize_when_none=False)
    culprits = ListType(BaseType, default=[])
    keep_log = BooleanType(deserialize_from="keepLog", serialize_when_none=False)
    number = IntType(serialize_when_none=False)
    queue_id = StringType(deserialize_from="queueId", serialize_when_none=False)
    result = StringType(serialize_when_none=False)
    console_output = StringType(serialize_when_none=False)
    created_at = DateTimeType(serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.url,
            "external_link": self.url
        }
