from flask import jsonify
from models import Label
from app import app
from config import Config

@app.route('/api/labels', methods=['GET'])
def get_labels():
    labels = Label.query.with_entities(Label.label_name).distinct().all()
    labels = [label[0] for label in labels]
    return (jsonify({'labels': labels}), 200)