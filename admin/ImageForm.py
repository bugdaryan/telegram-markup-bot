from flask_wtf import FlaskForm
from wtforms import FileField, MultipleFileField

class ImageForm(FlaskForm):
    image_byte = MultipleFileField("Image")