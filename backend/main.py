from app import app, db
from config import Config
from models import User

if __name__ == '__main__':
    app.app_context().push()
    db.create_all()

    app.debug = Config.DEBUG
    app.run(port=Config.PORT)