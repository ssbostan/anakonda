from anakonda.anakonda import db
from anakonda.util import now, uuidgen


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.String(64), primary_key=True, default=uuidgen)
    name = db.Column(db.String(256), index=True, nullable=False)
    namespace = db.Column(db.String(64), index=True, nullable=False)
    runtime = db.Column(db.String(32), index=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=now)
    last_update_at = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String(256), index=True, nullable=False)
    script = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), nullable=False)

    def __repr__(self):
        return f"<Task id='{self.id}' name='{self.name}'>"
