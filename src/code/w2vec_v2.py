import gensim
import numpy as np
import simplejson as json
from scipy import spatial

from gensim import models
from pymongo import MongoClient
import DataCollection as datacollection
import MongoController as mongoController
import MessageCleaner as messageCleaner

def vectorize(sentence, model, num_features, index2word_set):
    words = sentence.split()
    feature_vec = np.zeros((num_features, ), dtype='float32')
    n_words = 0
    for word in words:
        if word in index2word_set:
            n_words += 1
            feature_vec = np.add(feature_vec, model[word])
    if (n_words > 0):
        feature_vec = np.divide(feature_vec, n_words)
    return feature_vec

#model, source_doc = query, target_docs = missatges anteriors
def extract_context(model, source_doc, target_docs, threshold=0.0):
	index2word_set = set(model.wv.index2word)
	s1_afv = vectorize(source_doc, model=model, num_features=100, index2word_set=index2word_set)
	results = []
	for doc in target_docs:
		equip_resolutor = doc[1]
		producte = doc[2]
		assumpte = doc[3]
		serveiTipus = doc[4]
		subservei = doc[5]
		_id = doc[6]
		docAux = doc[0]
		s2_afv = vectorize(docAux, model=model, num_features=100, index2word_set=index2word_set)
		sim_score = 1 - spatial.distance.cosine(s1_afv, s2_afv)
		if sim_score >= threshold:
			results.append({
				'Similitud': str(sim_score),
				'Missatge': str(docAux),
				'Equip resolutor': str(equip_resolutor),
				'Producte': str(producte),
				'Servei Tipus': str(serveiTipus),
				'Subservei': str(subservei)
			})
	for i in range (0, len(results)):
		results[i]['Similitud'] = float(results[i]['Similitud'])
	results.sort(key=lambda k: k['Similitud'], reverse=True)
	nova = json.loads(json.dumps(results))
	return nova



def run(query):
	collection = mongoController.connection_messages()
	cursor = collection.find()
	query = datacollection.query_cleaner(query)

	ticket_complete = []
	for ticket in cursor:
		ticket_n = []
		ticket_n.append(ticket.get("missatge"))
		ticket_n.append(ticket.get("equipResolutor"))
		ticket_n.append(ticket.get("producte"))
		ticket_n.append(ticket.get("assumpte"))
		ticket_n.append(ticket.get("serveiTipus"))
		ticket_n.append(ticket.get("subservei"))
		ticket_n.append(ticket.get("Id"))
		ticket_complete += [ticket_n]

	sentences = []
	for i in range(0, len(ticket_complete)):
		sentenceAux = ticket_complete[i][0].split(" ") 
		sentences += [sentenceAux]

	model = models.Word2Vec(sentences, min_count=1)

	result = extract_context(model, query, ticket_complete)
	if len(result) < 1:
		result = []
		result.append({
			'Equip resolutor': "No s'ha trobat cap similitud",
			'Producte': "",
			'Servei Tipus': "",
			'Subservei':""}
			)
		nova = json.loads(json.dumps(results))
		return (nova[0]) 
	else: 
		return (result[0])