from flask import jsonify
from models import Label
from app import app
from config import Config

@app.route('/api/labels', methods=['GET'])
def get_labels():
    labels = Label.query.with_entities(Label.name, Label.id).distinct().all()
    labels_dict = {'label': [label[0] for label in labels], 'id':[label[1] for label in labels]}
    return (jsonify(labels_dict), 200)