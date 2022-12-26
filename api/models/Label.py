from app import db, app
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Label(db.Model):
    __tablename__ = 'labels'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(32), index=True, unique=True)
    images = relationship('Image', backref='label', lazy=True)

    def __repr__(self):
        return '<Label {}>'.format(self.name)