from flask import jsonify, g, request
from models import User, Label, Image
from app import db, app, auth
from config import Config
import random
import base64

@app.route('/api/images', methods=['GET'])
@auth.login_required
def get_image():
    images = db.session.query(Image).filter(Image.label_id == None).all()
    res = {
        'image': None,
        'image_id': None
    }
    if len(images):
        image = random.choice(images)
        image_data = base64.b64encode(image.image_byte).decode('utf-8')
        res['image'] = image_data
        res['image_id'] = image.id

    return (jsonify(res), 200)