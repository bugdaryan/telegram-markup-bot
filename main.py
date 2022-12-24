from app import app, db
from config import Config
from models import User, Image, Annotation, Label
from api import register, get_token, get_labels
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from admin import ImageModelView


if __name__ == '__main__':
    app.app_context().push()
    db.create_all()


    with open(Config.INIT_SQL_FILE, 'r') as f:
        sql_script = f.readlines()
    sql_script = '\n'.join(sql_script)
    with app.app_context():
        db.create_all()
        for script in sql_script.split(';'):
            script = script.replace('\n', '')
            if len(script):
                db.session.execute(script)
                db.session.commit()

    admin = Admin(app, name='saitama', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Annotation, db.session))
    admin.add_view(ModelView(Label, db.session))
    admin.add_view(ImageModelView(Image, db.session, name='Image'))
    
    app.debug = Config.DEBUG
    app.run(port=Config.PORT)