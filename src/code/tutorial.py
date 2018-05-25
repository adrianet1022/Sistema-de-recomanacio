from gensim import models

frases= [["escribir", "tutoriales", "es", "gratificante"], ["pero", "comer", "papas", "bravas", "es", "mucho", "mejor"]]

modelo = models.Word2Vec(frases, min_count=1)

print(str(modelo.wv.vocab))