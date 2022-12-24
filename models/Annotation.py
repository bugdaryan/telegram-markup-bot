from app import db, app
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Annotation(db.Model):
    __tablename__ = 'annotations'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    image_id = db.Column(UUID(as_uuid=True), db.ForeignKey('images.id'))
    label_id = db.Column(UUID(as_uuid=True), db.ForeignKey('labels.id'))