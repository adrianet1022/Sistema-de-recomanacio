import gensim
import numpy as np
import simplejson as json
import re, math

from gensim import models
from pymongo import MongoClient
import DataCollection as datacollection
import MongoController as mongoController
import MessageCleaner as messageCleaner
from collections import Counter

WORD = re.compile(r'\w+')

def vectorize(text):
	words = WORD.findall(text)
	return Counter(words)


def _cosine_sim(vec1, vec2):
	intersection = set(vec1.keys()) & set(vec2.keys())
	numerator = sum([vec1[x] * vec2[x] for x in intersection])

	vector1 = sum([vec1[x]**2 for x in vec1.keys()])
	vector2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(vector1) * math.sqrt(vector2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

#model, source_doc = query, target_docs = missatges anteriors
def extract_context(source_doc, target_docs, threshold=0.3):
		source_vec = vectorize(str(source_doc))
		results = []
		for doc in target_docs:
			equip_resolutor = doc[1]
			producte = doc[2]
			assumpte = doc[3]
			serveiTipus = doc[4]
			subservei = doc[5]
			_id = doc[6]
			docAux = doc[0].split(" ")
			target_vec = vectorize(str(docAux))
			sim_score = _cosine_sim(source_vec, target_vec)
			if sim_score >= threshold:
				results.append({
					'Missatge': str(doc[0]),
					'Similitud': str(sim_score),
					'Equip resolutor': str(equip_resolutor),
					'Producte': str(producte),
					'Servei Tipus': str(serveiTipus),
					'Subservei': str(subservei)
				})
		for i in range (0, len(results)):
			results[i]['Similitud'] = float(results[i]['Similitud'])
		results.sort(key=lambda k: k['Similitud'], reverse=True)
		#if len(results) > 0:
		#	del results[0]['Similitud']
		nova = json.loads(json.dumps(results))
		return nova

def run(query):
	collection = mongoController.connection_messages()
	cursor = collection.find()
	query = datacollection.query_cleaner(query)
	query = query.split(" ")

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

	result = extract_context(query, ticket_complete)
	if len(result) < 1:
		return ("No hi ha cap similitud")
	else: 
		return (str(result[0]))