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
    print("MESAGE: "+str(request.json['message']))
    return jsonify(w2v.run(request.json['message'])) 

#Metode POST per crear un nou post de message
"""
{
	"book": {
		"subtitle": "Read a second book"
	}
}
"""
#exemple per desenvolupar
@app.route('/api/new_ticket/', methods=['POST'])
def new_ticket():
	content = request.json
	#pasem el json a la funcio de DataCollection take_ticket i aqui es crea un ticket nou a la BD
	return jsonify(content['book']['subtitle'])

@app.route("/api/startdb/",methods=["GET"])
def api_post():
	dataCollection.run()
	return "BD iniciada"

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)