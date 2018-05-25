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
	print("Vectoriza la query")
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
				'Document': doc
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

collection = mongoController.connection_messages()
query = "no funciona el enlace para colgar practicas en atenea"
#busquem l'idioma de la query per a agafar els missatges unicament que son en el mateix idioma
#idioma_query = messageCleaner.idioma_detect(query)
cursor = collection.find()
#netejem la query per treballar igual que amb la DB
print("Query" + str(query))
query = datacollection.query_cleaner(query)
query = query.split(" ")
print("Query" + str(query))
#creem les els tiquets només amb les dades que voldrem mostrar mes tard

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

a = open("ticket_complete.txt","w+")
a.write(str(ticket_complete))
"""
sentence = ['recoger nino', 'Que tiempo hace', 'Donde estas', 'Cuando vienes a casa', 'Comprar comida', 'Comer juntos',
             'Esta lloviendo', 'Esta nevando', 'Hace mucho viento', 'Hay mucha niebla', 'Llueve mucho',
             'Donde andas', 'Por donde estas', 'Cuando llegas', 'Pasa por el supermercado', 'Cenamos juntos',
             'Desayunamos juntos', 'Compra algo para la cena', 'La nevera esta vacia', 'Cuando piensas llegar',
             'Hace mucho frio', 'Ves a comprar', 'Estas en casa', 'Estas en el trabajo', 'Estoy llegando',
             'Donde nos vemos', 'Cuando nos vemos', 'Cuando hemos quedado', 'Donde hemos quedado',
             'Los niños te estan esperando', 'Recoge a tu hijo', 'Comer con padres', 'Comemos en casa', 'Comemos fuera',
             'Llegas tarde', 'Hay que hacer la compra', 'Hace mucho calor', 'Hace mucho sol',
             'Han llamado de la escuela puedes recogerlos', 'Esta tapado el dia', 'Vas con retraso','Dnd estas']
"""
#creem les frases per a crear un model correctament
sentences = []
for i in range(0, len(ticket_complete)):
	sentenceAux = ticket_complete[i][0].split(" ") #sentenceAux = sentence[i][0].split(" ")
	sentences += [sentenceAux]
f = open("sentences.txt","w+")
f.write(str(sentences))

#print (str(sentences))

model = models.Word2Vec(sentences, min_count=10)
#print("Vocabulari: "+ str(model.wv.vocab))

result = extract_context(model, query, ticket_complete)
#print("Aixo es el que mes triga")
if len(result) < 1:
	print ("No hi ha cap similitud")
else: 
	print ("El millor resultat es: " + str(result[0])) #result de 0 perque nomes volem tornar el int no la llista
	print ("El segon millor resultat es: " + str(result[1]))
	print ("El tercer millor resultat es: " + str(result[2]))
	print ("El quart millor resultat es: " + str(result[3]))
	print ("El cinque millor resultat es: " + str(result[4]))
	print ("El sise millor resultat es: " + str(result[5]))
	print ("El sete millor resultat es: " + str(result[6]))
	print ("El vuite millor resultat es: " + str(result[7]))

