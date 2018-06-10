import unicodedata
import re

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect

"""
def idioma_detect(missatge):
	try:
		idioma = detect(missatge)
	except: 
		idioma = "not_detected"
	return idioma
"""
def elimina_caracteres(text):
	caracteres = open("/Users/adriagarcia/Desktop/TFG/Codigo/src/data/caracteres.txt", "r")
	#EN A PONGO LOS CARACTERES QUE NO QUIERO
	a = []
	for line in caracteres:
		a.append(line.strip())

	#FILTERED SENTENCE ACABARA SIENDO MI FRASE SIN CARACTERES
	filtered_sentence = ""
	#POR CADA PALABRA EN EL MENSAJE ENTRO
	for word in text:
		#POR CADA LETRA EN PALABRA ENTRO
		filtered_word = ""
		for letter in word:
			#SI LA LETRA NO ESTA EN a
			if letter not in a:
				#la palabra filtrada sera la suma de las letras
				filtered_word += letter
		filtered_sentence += filtered_word
	return filtered_sentence

def elimina_letras_sueltas(text):
	letters = open("/Users/adriagarcia/Desktop/TFG/Codigo/src/data/letters.txt", "r") 
	a = []
	for line in letters:
		a.append(line.strip())

	filtered_sentence = ""
	word_tokens = word_tokenize(text)
	for w in word_tokens:
		if w not in a: 
			filtered_sentence += w + " "
	filtered_sentence = filtered_sentence[:-1]
	return filtered_sentence

def elimina_tildes(s): #treure accents
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def stop_words(text):
	#stopwords  en tots els idiomes per evitar errors en detecció de llenguatge
	stops = set(stopwords.words('spanish'))
	stops.update(("Hola", "hola", "Gracias", "gracias", "Adios", "adios"))
	stops.update((stopwords.words('english')))
	stops.update(("Hello", "hello", "hi", "Hi", "thanks", "Thanks"))
	catalan = open("/Users/adriagarcia/Desktop/TFG/Codigo/src/data/catalan.txt", "r") 
	a = []
	for line in catalan:
		a.append(line.strip())
	stops.update((a))
	#tokenitzem el text
	word_tokens = word_tokenize(text)
	filtered_sentence = ""
	#per cada paraula a les paraules tokenitzades del text
	for w in word_tokens:
		if w not in stops:
			filtered_sentence += w + " "
	filtered_sentence = filtered_sentence[:-1]
	return filtered_sentence

def modifica_correus(text):
	match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
	text = text.split(" ")
	missatge = ""
	for word in text:
		if word in match:
			missatge += word + " " 
		elif not word in match and len(word) > 15:
			missatge += "webormail "
		else:
			missatge += word + " "
	missatge = missatge[:-1]
	return missatge

def elimina_paraules_llargues(text):
	text = text.split(" ")
	missatge = ""
	for word in text:
		if len(word) > 15:
			missatge += ""
		else:
			missatge += word + " "
	missatge = missatge[:-1]
	return missatge



