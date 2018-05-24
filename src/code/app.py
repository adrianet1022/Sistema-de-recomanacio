#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
from flask_pymongo import PyMongo

import w2v as w2v
import DataCollection as dataCollection

app = Flask(__name__)


#Metode POST per crear un nou post de message
@app.route('/api/similitud/', methods=['POST'])
def create_task():
    if not request.json or not 'message' in request.json:
        abort(400)
    return jsonify(w2v.run(request.json['message'])), 201

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)