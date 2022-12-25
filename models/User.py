from werkzeug.security import generate_password_hash, check_password_hash
from app import db, app
from sqlalchemy.dialects.postgresql import UUID
import uuid
import jwt
import time
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(300))
    points = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean, default=False)
    images = relationship('Image', backref='user', lazy=True)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expires_in = 3600):
        return jwt.encode(
                { 'id': str(self.id), 'exp': time.time() + expires_in},
                app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return
        return User.query.get(data['id'])
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __unicode__(self):
        return self.username