import difflib
import numpy as np
import simplejson as json

from pymongo import MongoClient
import DataCollection as datacollection
import MongoController as mongoController
import MessageCleaner as messageCleaner
from difflib import SequenceMatcher as SM

def run(query):
	collection = mongoController.connection_messages()
	cursor = collection.find()
	query = [datacollection.query_cleaner(query)]

	ticket_complete=[]
	for ticket in cursor:
		ticket_n = []
		ticket_n.append(ticket.get("missatge"))
		ticket_complete += ticket_n

	d = difflib.Differ()

	for search in query:
		matches = difflib.get_close_matches(search, possibilities = ticket_complete, n = 1, cutoff = 0.5)
		if len(matches) == 0:
			return("no hay matches")
		else: 
			s1 = str(matches[0])
			s2 = str(query[0])
			cursor = collection.find({"missatge": str(matches[0])})
			for ticket in cursor:
				equipResolutor = ticket.get("equipResolutor")
				producte = ticket.get("producte")
				assumpte = ticket.get("assumpte")
				serveiTipus = ticket.get("serveiTipus")
				subservei = ticket.get("subservei")
			return ("Equip resolutor: " + str(equipResolutor), 
				"Producte: " + str(producte), "Servei Tipus: " + str(serveiTipus),
				"Subservei: " + str(subservei))


