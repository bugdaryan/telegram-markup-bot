from app import app, db, auth
from config import Config
from models import User, Image, Label
from api import register, get_token, get_labels, post_annotation, get_image
from flask_admin import Admin
from admin import ImageModelView, MyAdminIndexView, LoginForm, MyModelView, LabelStatisticsView
from flask import redirect, url_for, send_file, make_response, g
import flask_login as login
import zipfile
import io
from flask_login import login_required, current_user

def init_login():
    login_manager = login.LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(User).get(user_id)


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('admin.index'))

@app.route('/download_images_labels')
@login_required
def download_images_labels():
    if not current_user.is_admin:
        return 'Error: You do not have permission to access this endpoint.'

    images_labels = [{'image_name': f'{image.id}.jpg', 'image_data': image.image_byte, 'label': image.label.name} for image in Image.filter(Image.label_id != None).all()]

    csv_data = 'image_name,label\n'
    for image_label in images_labels:
        csv_row = f'{image_label["image_name"]},{image_label["label"]}\n'
        csv_data += csv_row
    
    fileobj = io.BytesIO()
    with zipfile.ZipFile(fileobj, 'w') as zf:
        zf.writestr('images_labels.csv', csv_data)

        for image_label in images_labels:
            zf.writestr(image_label['image_name'], image_label['image_data'])

    fileobj.seek(0)

    response = make_response(send_file(fileobj, mimetype='application/zip'))
    response.headers['Content-Disposition'] = 'attachment; filename=images_labels.zip'
    return response

app.app_context().push()
db.create_all()
with open(Config.SQL_INIT_FILE, 'r') as f:
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
admin.add_view(MyModelView(Label, db.session))
admin.add_view(ImageModelView(Image, db.session))
admin.add_view(LabelStatisticsView(name='Label Statistics'))

if __name__ == '__main__':
    app.debug = Config.DEBUG
    app.run(host="0.0.0.0", port=Config.PORT)