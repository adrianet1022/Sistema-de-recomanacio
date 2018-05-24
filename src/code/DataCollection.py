import re
import html

import MongoController as mongoController
import MessageCleaner as messageCleaner


def cleanhtml(raw_html):
	cleantext = html.unescape(raw_html) #treure els codis html i deixar els accents
	cleantext = cleantext.lower()
	cleantext = messageCleaner.elimina_tildes(cleantext)
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', cleantext)
	cleantext = messageCleaner.elimina_caracteres(cleantext)
	idioma = messageCleaner.idioma_detect(cleantext)
	cleantext = messageCleaner.stop_words(cleantext, idioma)
	cleantext = " ".join(cleantext.split())
	return cleantext

def take_data(collection):
	cursor = collection.find()
	for ticket in collection.find():
		idTiquet = ticket.get("_id")
		missatge = ticket.get("descripcio")
		equipResolutor = ticket.get("equipResolutorNom")
		producte = ticket.get("producte")
		assumpte = ticket.get("assumpte")
		serveiTipus = ticket.get("serveiTipus")
		subservei = ticket.get("subservei")

		missatge = cleanhtml(missatge)
		idioma = messageCleaner.idioma_detect(missatge)
		#missatge_NET = messageCleaner.stop_words(missatge, idioma)

		mongoController.insert_new_ticket(idTiquet, missatge, missatge_NET, idioma, equipResolutor, producte, assumpte,
			serveiTipus, subservei)


def run():
	collection = mongoController.connection_tickets()
	take_data(collection)
	print ("Ha guardat be")

