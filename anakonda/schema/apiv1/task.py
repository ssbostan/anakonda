from anakonda.anakonda import ma
from anakonda.model import Task


class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field()
    namespace = ma.auto_field()
    runtime = ma.auto_field()
    created_at = ma.auto_field(dump_only=True)
    last_update_at = ma.auto_field(dump_only=True)
    image = ma.auto_field()
    script = ma.auto_field()
    result = ma.auto_field(dump_only=True)
    status = ma.auto_field(dump_only=True)
