import pymongo
from pymongo import MongoClient

def connection_tickets():
	client = MongoClient('mongodb://localhost:27017/ticketsdb')
	db = client.ticketsdb
	collection = db.tickets
	return collection

def connection_messages():
	client = MongoClient('mongodb://localhost:27017/ticketsdb')
	db = client.ticketsdb
	collection = db.Messages
	return collection

def insert_new_ticket(idTiquet, missatge, equipResolutor, producte, assumpte,
			serveiTipus, subservei):
	client = MongoClient('mongodb://localhost:27017/ticketsdb')
	db = client.ticketsdb
	db.Messages.insert({ "Id": idTiquet, "missatge": missatge, "equipResolutor": equipResolutor, "producte": producte,
			"assumpte": assumpte, "serveiTipus": serveiTipus, "subservei": subservei})