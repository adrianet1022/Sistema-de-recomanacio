#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, request
from flask_pymongo import PyMongo

import w2v as w2v
import w2vec_v2 as w2vec_v2
import difflib_version as difflib_version
import cosine_similarity as cosine_similarity
import DataCollection as dataCollection

app = Flask(__name__)

@app.route('/api/similitud/tots/', methods=['POST'])
def create_task_tots():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    message = str(request.json['assumpte']) + " " + str(request.json['message'])
    resultW2v = w2v.run(message)
    resultCosine = cosine_similarity.run(message)
    resultDifflib = difflib_version.run(message)
    resultW2vec = w2vec_v2.run(message)

    return jsonify({
            'Similitud': resultW2v['Similitud'],
            'Missatge': resultW2v['Missatge'],
            'EquipResolutor': resultW2v['Equip resolutor'],
            'Producte': resultW2v['Producte'],
            'Servei Tipus': resultW2v['Servei Tipus'],
            'Subservei': resultW2v['Subservei']},
        {
            'Similitud': resultW2vec['Similitud'],
            'Missatge': resultW2vec['Missatge'],
            'EquipResolutor': resultW2vec['Equip resolutor'],
            'Producte': resultW2vec['Producte'],
            'Servei Tipus': resultW2vec['Servei Tipus'],
            'Subservei': resultW2vec['Subservei']},
        {
            'Similitud': resultCosine['Similitud'],
            'Missatge': resultCosine['Missatge'],
            'EquipResolutor': resultCosine['Equip resolutor'],
            'Producte': resultCosine['Producte'],
            'Servei Tipus': resultCosine['Servei Tipus'],
            'Subservei': resultCosine['Subservei']},
        {
            'Similitud': resultDifflib['Similitud'],
            'Missatge': resultDifflib['Missatge'],
            'EquipResolutor': resultDifflib['Equip resolutor'],
            'Producte': resultDifflib['Producte'],
            'Servei Tipus': resultDifflib['Servei Tipus'],
            'Subservei': resultDifflib['Subservei']}
    )


@app.route('/api/similitud/w2v/', methods=['POST'])
def create_task_w2v():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    message = str(request.json['assumpte']) + " " + str(request.json['message'])
    result = w2v.run(message)
    return jsonify({
        'EquipResolutor': result['Equip resolutor'],
        'Producte': result['Producte'],
        'Servei Tipus': result['Servei Tipus'],
        'Subservei': result['Subservei']}
    )

@app.route('/api/similitud/w2vec_new/', methods=['POST'])
def create_task_w2vnew():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    message = str(request.json['assumpte']) + " " + str(request.json['message'])
    result = w2vec_v2.run(message)
    return jsonify({
        'EquipResolutor': result['Equip resolutor'],
        'Producte': result['Producte'],
        'Servei Tipus': result['Servei Tipus'],
        'Subservei': result['Subservei']}
    )

@app.route('/api/similitud/cosine_similarity/', methods=['POST'])
def create_task_cosine():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    message = str(request.json['assumpte']) + " " + str(request.json['message'])
    result = cosine_similarity.run(message)
    return jsonify({
        'EquipResolutor': result['Equip resolutor'],
        'Producte': result['Producte'],
        'Servei Tipus': result['Servei Tipus'],
        'Subservei': result['Subservei']}
    )

@app.route('/api/similitud/difflib/', methods=['POST'])
def create_task_difflib():
    if not request.json or not 'message' or not 'assumpte'in request.json:
        abort(400)
    message = str(request.json['assumpte']) + " " + str(request.json['message'])
    result = difflib_version.run(message)
    return jsonify({
        'EquipResolutor': result['Equip resolutor'],
        'Producte': result['Producte'],
        'Servei Tipus': result['Servei Tipus'],
        'Subservei': result['Subservei']}
    )

@app.route('/api/new_ticket/', methods=['POST'])
def new_ticket():
    if not request.json or not '_id' or not 'descripcio' or not 'equipResolutorNom' or not 'producte' or not 'assumpte' or not 'serveiTipus' or not 'subservei' in request.json:
        abort(405)
    return jsonify(dataCollection.take_ticket(request.json))

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