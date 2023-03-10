from app import db, app
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    image_byte = db.Column(db.LargeBinary, nullable=False)
    label_id = db.Column(UUID(as_uuid=True), db.ForeignKey('labels.id'), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=True)