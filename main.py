from app import app, db
from config import Config
from models import User, Image, Annotation, Label
from api import register, get_token, get_labels
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from admin import ImageModelView, MyAdminIndexView, LoginForm, MyModelView
from flask import redirect, url_for
import flask_login as login

def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin.index'))

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
    init_login()

    admin = Admin(app, name='admin', template_mode='bootstrap4', index_view=MyAdminIndexView(),  base_template='my_master.html')
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Annotation, db.session))
    admin.add_view(MyModelView(Label, db.session))
    admin.add_view(ImageModelView(Image, db.session))

    app.debug = Config.DEBUG
    app.run(port=Config.PORT)