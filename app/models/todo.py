from flask_sqlalchemy import SQLAlchemy
from . import db


class TodoModel(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "task": self.task}
