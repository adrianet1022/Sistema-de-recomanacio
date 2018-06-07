import re, math

from collections import Counter

WORD = re.compile(r'\w+')

def text_to_vector(text):
	words = WORD.findall(text)
	return Counter(words)

def _cosine_sim(vec1, vec2):
	"""Find the cosine similarity distance between two vectors."""
	intersection = set(vec1.keys()) & set(vec2.keys())
	#Agafa la intersecció dels dos vectors
	print("INTERSECTION: " + str(intersection))
	#1a it: una: 1 * una: 1 = 1
	#2a it: aixo: 1 * aixo: 1 = 1
	#3a it: proba: 2 * proba: 1 = 2
	#4a it: es: 1 * es: 1 = 1
	#numerator = 1+1+2+1 = 5
	#calcula el numerador (Part d'adalt) per calcular despres el resultat de la similitud final
	#Tinc la formula descarregada
	numerator = sum([vec1[x] * vec2[x] for x in intersection])
	print ("NUMERATOR: " + str(numerator))

	sum1 = sum([vec1[x]**2 for x in vec1.keys()])
	sum2 = sum([vec2[x]**2 for x in vec2.keys()])
	denominator = math.sqrt(sum1) * math.sqrt(sum2)

	if not denominator:
		return 0.0
	else:
		return float(numerator) / denominator

query = "aixo es una proba proba"
query2 = "aixo tambe es una proba"

#fica a 1 les paraules que surten
proba = text_to_vector(query)
proba2 = text_to_vector(query2)
result = _cosine_sim(proba,proba2)
print(str(proba) + "Proba 2 "+ str(proba2) + "Result " + str(result) )