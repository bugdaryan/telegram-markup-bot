from flask import jsonify, g, request
from models import User, Label, Image
from app import db, app, auth
from config import Config

@app.route('/api/annotations', methods=['POST'])
@auth.login_required
def post_annotation():
    user = g.user
    if user.participate_in_markup == False:
        return (jsonify({'message':'You are not allowed to participate in markup.'}), 403)
    label_id = request.json.get('label_id')
    image_id = request.json.get('image_id')

    image = Image.query.filter(Image.id == image_id).first()
    label = Label.query.filter(Label.id == label_id).first()
    if not image:
        return (jsonify({}), 400)
    if not label:
        return (jsonify({}), 400)
    image.label_id = label_id
    image.user_id = user.id
    db.session.add(image)
    db.session.commit()

    return (jsonify({}), 201)