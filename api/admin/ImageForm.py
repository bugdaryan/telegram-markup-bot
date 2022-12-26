from flask_wtf import FlaskForm
from wtforms import MultipleFileField

class ImageForm(FlaskForm):
    image_byte = MultipleFileField("Image")