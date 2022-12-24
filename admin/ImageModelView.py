from flask_admin.form import ImageUploadField
from flask_admin.model.template import macro
from flask_admin.model import BaseModelView
from markupsafe import Markup
from admin.ImageForm import ImageForm
from models import Image
from sqlalchemy import func
from flask import request
import base64
from flask import redirect, url_for


class ImageModelView(BaseModelView):
    def __init__(self, model, session, **kwargs):
        # Pass the session object to the model view constructor
        super().__init__(model, **kwargs)

        # Set the session as an instance variable
        self.session = session

    form_extra_fields = {
        'image_byte': ImageUploadField('Image', render_kw={"multiple": True})
    }

    def render_image(self, context, model, name):
        # return Markup(f'<img src="data:image/png;base64,{model.image_byte} " width="100" height="100">')
        image_data = base64.b64encode(model.image_byte).decode('utf-8')

        # Construct the data URI for the image
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
        self.session.add(model)

        self.session.commit()
        return redirect(url_for('.index_view'))


    def scaffold_list_columns(self):
        return ['id', 'image_byte']

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

        # Apply any filters and search terms to the count query
        if filters:
            count_query = self.apply_filters(count_query, filters)
        if search:
            count_query = self.apply_search(count_query, search)

        # Execute the count query and retrieve the count
        count = count_query.scalar()


        # Query the database for all the records for the Image model
        query = self.model.query

        # Apply any filters and search terms to the query
        if filters:
            query = self.apply_filters(query, filters)
        if search:
            query = self.apply_search(query, search)

        # Apply the sort and pagination to the query
        if sort_field:
            query = self.apply_sort(query, sort_field, sort_desc)
        if page and page_size:
            query = self.apply_pagination(query, page, page_size)

        # Return the list of records for the query
        return count, query.all()
