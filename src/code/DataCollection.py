import re
import html

import MongoController as mongoController
import MessageCleaner as messageCleaner
from bs4 import BeautifulSoup



def text_cleaner(raw_html):
	cleantext = BeautifulSoup(raw_html,"html.parser").text
	cleantext = cleantext.lower()
	cleantext = messageCleaner.modifica_correus(cleantext)
	cleantext = messageCleaner.elimina_tildes(cleantext)
	cleantext = messageCleaner.elimina_caracteres(cleantext)
	cleantext = messageCleaner.elimina_letras_sueltas(cleantext)
	cleantext = messageCleaner.stop_words(cleantext)
	return cleantext

def query_cleaner(raw_html):
	cleantext = BeautifulSoup(raw_html,"html.parser").text
	cleantext = cleantext.lower()
	cleantext = messageCleaner.modifica_correus(cleantext)
	cleantext = messageCleaner.elimina_tildes(cleantext)
	cleantext = messageCleaner.elimina_caracteres(cleantext)
	cleantext = messageCleaner.elimina_letras_sueltas(cleantext)
	cleantext = messageCleaner.stop_words(cleantext)
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

		missatge = text_cleaner(missatge)

		mongoController.insert_new_ticket(idTiquet, missatge, equipResolutor, producte, assumpte,
			serveiTipus, subservei)

def take_ticket(jsonRequest):
	idTiquet = jsonRequest['_id']
	missatge = jsonRequest['descripcio']
	missatge = query_cleaner(str(missatge))
	equipResolutor = jsonRequest['equipResolutorNom']
	producte = jsonRequest['producte']
	assumpte = jsonRequest['assumpte']
	serveiTipus = jsonRequest['serveiTipus']
	subservei = jsonRequest['subservei']
	mongoController.insert_new_ticket(idTiquet, missatge, equipResolutor, producte, assumpte,
			serveiTipus, subservei)
	return "Ha guardat be"

def run():
	collection = mongoController.connection_tickets()
	take_data(collection)
	return ("Ha guardat be")

