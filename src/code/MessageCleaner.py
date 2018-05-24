import unicodedata

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from langdetect import detect

def idioma_detect(missatge):
	try:
		idioma = detect(missatge)
	except: 
		idioma = "not_detected"
	return idioma

def elimina_caracteres(text):
	caracteres = open("/Users/adriagarcia/Desktop/TFG/Codi/src/data/caracteres.txt", "r")
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
	filtered_sentence = filtered_sentence[:-1]
	return filtered_sentence

def elimina_tildes(s): #treure accents
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def stop_words(text,idioma):
	if (idioma == "es"):
		#stopwords 
		stops = set(stopwords.words('spanish'))
		stops.update(("Hola", "hola", "Gracias", "gracias", "Adios", "adios"))
		#tokenitzem el text
		word_tokens = word_tokenize(text)
		filtered_sentence = ""
		#per cada paraula a les paraules tokenitzades del text
		for w in word_tokens:
			if w not in stops:
				filtered_sentence += w + " "
		filtered_sentence = filtered_sentence[:-1]
		return filtered_sentence
	
	if (idioma == "en"):
		stops = set(stopwords.words('english'))
		stops.update(("Hello", "hello", "hi", "Hi", "thanks", "Thanks"))
		word_tokens = word_tokenize(text)
		filtered_sentence = ""
		#per cada paraula a les paraules tokenitzades del text
		for w in word_tokens:
			if w not in stops:
				filtered_sentence += w + " "
		filtered_sentence = filtered_sentence[:-1]
		return filtered_sentence

	if (idioma == "ca"):
		catalan = open("/Users/adriagarcia/Desktop/TFG/Codi/src/data/catalan.txt", "r") 
		a = []
		filtered_sentence = ""
		word_tokens = word_tokenize(text)
		for w in word_tokens:
			if w not in a:
				filtered_sentence += w + " "
		filtered_sentence = filtered_sentence[:-1]
		return filtered_sentence
	else:
		return text
