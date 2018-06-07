#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
from flask_pymongo import PyMongo

import w2v as w2v
import w2vec_v2 as w2vec_v2
import difflib_version as difflib_version
import cosine_similarity as cosine_similarity
import DataCollection as dataCollection

app = Flask(__name__)

@app.route('/api/similitud/', methods=['POST'])
def create_task():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    w2vResult = w2v.run(request.json['message'])
    tutorialResult = difflib_version.run(request.json['message'])
    w2vecNewResult = w2vec_v2.run(request.json['message'])
    cosine_similarityResult = cosine_similarity.run(request.json['message'])
    return jsonify("Assumpte: " + str(request.json['assumpte']), "w2v: " + str(w2vResult),  "w2vecNew: " + str(w2vecNewResult), 
        "cosine_similarity: " + str(cosine_similarityResult), "tutorial: " + str(tutorialResult))

@app.route('/api/new_ticket/', methods=['POST'])
def new_ticket():
    if not request.json or not '_id' or not 'descripcio' or not 'equipResolutorNom' or not 'producte' or not 'assumpte' or not 'serveiTipus' or not 'subservei' in request.json:
        abort(405)
    return jsonify(dataCollection.take_ticket(request.json))
    #return jsonify(str(request.json)) 

#Metode POST per crear un nou post de message
"""
{
	"book": {
		"subtitle": "Read a second book"
	}
}
"""

@app.route('/api/prova/', methods=['GET'])
def prova():
    return ("Esteu accedint a la vostra API")

@app.route("/api/startdb/",methods=["GET"])
def api_post():
	dataCollection.run()
	return "BD iniciada"

@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_found(error):
	return make_response(jsonify({'error': 'Faltan valors Json'}), 404)

if __name__ == '__main__':
	app.run(debug=True)