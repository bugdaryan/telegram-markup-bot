from flask_admin.form import ImageUploadField
from flask_admin.model import BaseModelView
from markupsafe import Markup
from admin.ImageForm import ImageForm
from models import Image, User, Label
from sqlalchemy import func
from flask import request
import flask_login as login
import base64
from flask import redirect, url_for


class ImageModelView(BaseModelView):
    def __init__(self, model, session, **kwargs):
        super().__init__(model, **kwargs)

        self.session = session

    form_extra_fields = {
        'image_byte': ImageUploadField('Image', render_kw={"multiple": True})
    }

    def is_accessible(self):
        return login.current_user.is_authenticated

    def render_image(self, context, model, name):
        image_data = base64.b64encode(model.image_byte).decode('utf-8')
        image_uri = 'data:image/png;base64,{}'.format(image_data)
        return Markup('<img src="{}" width="100" height="100">'.format(image_uri))

    column_formatters = {
        'image_byte': render_image
    }

    def create_model(self, form):
        for image_data in form.image_byte.data:
            image = Image()
            form.populate_obj(image)
            image.image_byte = image_data.read()
            self.session.add(image)
        self.session.commit()
        return redirect(url_for('.index_view'))


    def update_model(self, form, model):
        image_datas = form.image_byte.data
        if len(image_datas):
            model.image_byte = image_datas[0].read()
        model.user = self.session.query(User).get(form.user.data)
        model.label = self.session.query(Label).get(form.label.data)
        self.session.add(model)
        self.session.commit()
        return redirect(url_for('.index_view'))


    def scaffold_list_columns(self):
        return ['id', 'image_byte', 'user.username', 'label.name']

    def scaffold_sortable_columns(self):
        return {'id': 'asc'}

    def scaffold_form(self):
        return ImageForm

    def get_pk_value(self, model):
        return model.id

    def get_one(self, id):
        return self.session.query(self.model).get(id)

    def delete_model(self, model):
        self.session.delete(model)
        self.session.commit()
        return redirect(url_for('.index_view'))


    def is_delete_form_submitted(self):
        if request.method == 'POST':
            return 'delete' in request.form and 'confirm_delete' in request.form
        return False

    
    def get_list(self, page, sort_field, sort_desc, search, filters, page_size=None):
        count_query = self.session.query(func.count('*')).select_from(self.model)
        if filters:
            count_query = self.apply_filters(count_query, filters)
        if search:
            count_query = self.apply_search(count_query, search)
        count = count_query.scalar()
        query = self.session.query(self.model)
        if filters:
            query = self.apply_filters(query, filters)
        if search:
            query = self.apply_search(query, search)
        if sort_field:
            query = self.apply_sort(query, sort_field, sort_desc)
        if page and page_size:
            query = self.apply_pagination(query, page, page_size)
        return count, query.all()
