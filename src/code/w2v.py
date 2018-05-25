import gensim
import numpy as np
import simplejson as json

from gensim import models
from pymongo import MongoClient
import DataCollection as datacollection
import MongoController as mongoController
import MessageCleaner as messageCleaner


def vectorize(model, doc):
	   """Identify the vector values for each word in the given document"""
	   word_vecs = []
	   for word in doc:
		   try:
			   vec = model[word]
			   word_vecs.append(vec)
		   except KeyError:
			   # Ignore, if the word doesn't exist in the vocabulary
			   pass
	   # Assuming that document vector is the mean of all the word vectors
	   # PS: There are other & better ways to do it.
	   vector = np.mean(word_vecs, axis=0)
	   return vector


def _cosine_sim(vecA, vecB):
	   """Find the cosine similarity distance between two vectors."""
	   csim = np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))
	   if np.isnan(np.sum(csim)):
		   return 0
	   return csim

#model, source_doc = query, target_docs = missatges anteriors
def extract_context(model, source_doc, target_docs, threshold=0.7):
		"""Calculates & returns similarity scores between given source document & all
		the target documents."""
		#source_doc: query
		#target_docs: tots els documents
		source_vec = vectorize(model, source_doc)
		results = []
		for doc in target_docs:
			equip_resolutor = doc[1]
			#equip_resolutor = datacollection.cleanhtml(equip_resolutor)
			producte = doc[2]
			assumpte = doc[3]
			serveiTipus = doc[4]
			subservei = doc[5]
			_id = doc[6]
			#print("DOC NO SPLIT: " + str(doc))
			docAux = doc[0].split(" ")
			#print("DOC SPLIT: " + str(docAux))
			target_vec = vectorize(model, docAux)
			#print("VECTORITZACIÓ " + str(target_vec))
			sim_score = _cosine_sim(source_vec, target_vec)
			if sim_score >= threshold:
				results.append({
					'Similitud': str(sim_score),
					'Document': doc,
					'Equip resolutor': str(equip_resolutor),
					'Producte': str(producte),
					'Assumpte': str(assumpte),
					'Servei Tipus': str(serveiTipus),
					'Subservei': str(subservei),
					'ID': str(_id)
				})
		#Sort results by score in desc order
		for i in range (0, len(results)):
			results[i]['Similitud'] = float(results[i]['Similitud'])
		results.sort(key=lambda k: k['Similitud'], reverse=True)
		nova = json.loads(json.dumps(results))
		return nova


def run(query):
	collection = mongoController.connection_messages()
	query = "no funciona el enlace para colgar practicas en atenea"
	cursor = collection.find()
	print("Query" + str(query))
	query = datacollection.query_cleaner(query)
	query = query.split(" ")
	print("Query" + str(query))

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

	model = models.Word2Vec(sentences, min_count=10)

	result = extract_context(model, query, ticket_complete)
	if len(result) < 1:
		return ("No hi ha cap similitud")
	else: 
		return (result[0], result[1], result[2], result[3])




