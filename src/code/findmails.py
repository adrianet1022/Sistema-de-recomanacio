from bs4 import BeautifulSoup
import html
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re

text = "Hola bon dia, www.aixoesunalocura.com A través de la Vicedegana d'Estudiantat M. Teresa Abad, la DEFIB ens demana donar d'alta els següents emails institucionals: delegat.centre@fib.upc.edu junta.defib@fib.upc.edu (Para secretario y tesorero) defib@fib.upc.edu Ja em direu alguna cosa, salutacions, Lluïsa."
text = BeautifulSoup(text,"html.parser").text 
match = re.findall(r'[\w\.-]+@[\w\.-]+', text)
text = text.split(" ")
missatge = ""
for word in text:
	#si la paraula es un correu la escric be
	if word in match:
		missatge += word + " "
	#si la paraula no es un correu pero es més petita que 14 
	elif not word in match and len(word) > 15:
		missatge += "webormail "
	else:
		missatge += word + " "
print (str(missatge))
