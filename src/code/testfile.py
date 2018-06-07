import unittest

from api.controllers import NLTController
from api.controllers import VSMDBController
from api.controllers import W2VecController
from django.test import TestCase
from mydjango.db import TLNData


class TLNTest(TestCase):
    @unittest.skip("no needed")
    def test_check_all_sentences(self):
        frases = vsmdbController.select_corpus_tln()
        iguals = 0
        maxmessages = 41
        CRED = '\033[91m'
        CEND = '\033[0m'
        CGREEN = '\033[92m'
        sentences = ['Recoger niño', 'Què tiempo hace', 'Donde estàs', 'Cuando vienes a casa', 'Comprar comida',
                     'Comer juntos']
        for i in range(0, len(frases)):
            message = frases[i]  # mensaje
            tematica = vsmdbController.select_tematica_from_message_tln(message)  # tematica
            result = W2VecController.run(frases, message)  # resultat amb el mes semblant
            if result == None:
                print(CRED + ("SMS: " + message + " Context: No context") + CEND)
            else:
                tematicaResult = vsmdbController.select_tematica_from_id_message_tln(result)
                tematicaResult = int(tematicaResult)
                tematica = int(tematica)
                if tematica == tematicaResult:
                    print(CGREEN + ("SMS: " + message + " Context: " + sentences[tematicaResult - 1]) + CEND)
                    iguals += 1
                else:
                    print(CRED + ("SMS: " + message + " Context: " + sentences[tematicaResult - 1]) + CEND)
        print("PERCENTATGE IGUALS BASE DE DADES SENSERA: " + str(iguals / maxmessages))
        self.assertEqual(iguals, maxmessages)
    """
    @unittest.skip("no needed")
    def test_check_all_equals(self):
        vsmdbController = VSMDBController.VSMDBController()
        if not vsmdbController.exists_table_tln():
            vsmdbController.create_table_tln()
            vsmdbController.save_text_to_bd_tln(TLNData.sentences, TLNData.respuestas, TLNData.tematica)
        frases = vsmdbController.select_corpus_tln()
        nltcontroller = NLTController.nltController()
        iguals = 0
        maxmessages = 500
        CRED = '\033[91m'
        CEND = '\033[0m'
        CGREEN = '\033[92m'
        sentences = ['Recoger niño', 'Què tiempo hace', 'Donde estàs', 'Cuando vienes a casa', 'Comprar comida',
                     'Comer juntos']
        for i in range(0, maxmessages):
            random = nltcontroller.randomComplete()  # missatge aleatori generat i la seva tematica
            tematica = vsmdbController.select_tematica_from_message_tln(
                random)  # tematica del missatge aleatori a la base de dades
            result = W2VecController.run(frases,
                                         random)  # resultat amb el mes semblança del missatge aleatori i la base de dades
            if result is not None:
                result = int(result)
                tematica = int(tematica)
                if tematica == result:
                    print(CGREEN + ("SMS: " + random + " Context: " + sentences[result - 1]) + CEND)
                    iguals += 1
                else:
                    print(CRED + ("SMS: " + random + " Context: " + sentences[result - 1]) + CEND)
            else:
                print(CRED + ("SMS: " + random + " Context: No context") + CEND)

        print("PERCENTATGE IGUALS AMB FRASES IGUALS: " + str(iguals / maxmessages))
        self.assertEqual(iguals, maxmessages)

    # Test missatges incomplets per comprovar la precisio
    @unittest.skip("no needed")
    def test_check_without_words(self):
        vsmdbController = VSMDBController.VSMDBController()
        if not vsmdbController.exists_table_tln():
            vsmdbController.create_table_tln()
            vsmdbController.save_text_to_bd_tln(TLNData.sentences, TLNData.respuestas, TLNData.tematica)
        frases = vsmdbController.select_corpus_tln()
        nltcontroller = NLTController.nltController()
        iguals = 0
        maxmessages = 500
        CRED = '\033[91m'
        CEND = '\033[0m'
        CGREEN = '\033[92m'
        sentences = ['Recoger niño', 'Què tiempo hace', 'Donde estàs', 'Cuando vienes a casa', 'Comprar comida',
                     'Comer juntos']

        for i in range(0, maxmessages):
            random = nltcontroller.randomIncomplete()  # missatge aleatori generat i la seva tematica
            message = random[0]
            tematica = random[1]
            result = W2VecController.run(frases, message)  # resultat amb el mes semblant
            if result is not None:
                result = int(result)
                tematica = int(tematica)
                if tematica == result:
                    print(CGREEN + ("SMS: " + message + " Context: " + sentences[result - 1]) + CEND)
                    iguals += 1
                else:
                    print(CRED + ("SMS: " + message + " Context: " + sentences[result - 1]) + CEND)
            else:
                print(CRED + ("SMS: " + message + " Context: No context") + CEND)

        print("PERCENTATGE IGUALS SENSE UNA PARAULA: " + str(iguals / maxmessages) + u"\u2588")
        self.assertGreaterEqual(iguals, 0.9)

    # Test missatges amb una nova paraula
    @unittest.skip("no needed")
    def test_check_with_new_word(self):
        vsmdbController = VSMDBController.VSMDBController()
        if not vsmdbController.exists_table_tln():
            vsmdbController.create_table_tln()
            vsmdbController.save_text_to_bd_tln(TLNData.sentences, TLNData.respuestas, TLNData.tematica)
        frases = vsmdbController.select_corpus_tln()  # obtinc totes les frases
        nltcontroller = NLTController.nltController()
        iguals = 0
        maxmessages = 500
        CRED = '\033[91m'
        CEND = '\033[0m'
        CGREEN = '\033[92m'
        sentences = ['Recoger niño', 'Què tiempo hace', 'Donde estàs', 'Cuando vienes a casa', 'Comprar comida',
                     'Comer juntos']

        for i in range(0, maxmessages):
            randomMessage = nltcontroller.randomComplete()  # missatge aleatori generat i la seva tematica
            randomWord = nltcontroller.randomComplete()  # creem un altre missatge aleatori
            randomWord = randomWord.split(" ")
            randomWord = nltcontroller.aleatori(randomWord)  # treiem una paraula aleatoria d'unaltra contexte
            message = randomMessage + " " + str(randomWord)
            tematica = vsmdbController.select_tematica_from_message_tln(randomMessage)
            result = W2VecController.run(frases, message)  # resultat amb el mes semblant
            if result is not None:
                tematicaResult = vsmdbController.select_tematica_from_id_message_tln(result)
                tematicaResult = int(tematicaResult)
                tematica = int(tematica)
                if tematica == tematicaResult:
                    print(CGREEN + ("SMS: " + message + " Context: " + sentences[tematicaResult - 1]) + CEND)
                    iguals += 1
                else:
                    print(CRED + ("SMS: " + message + " Context: " + sentences[tematicaResult - 1]) + CEND)

            else:
                print(CRED + ("SMS: " + message + " Context: No context") + CEND)
        print("PERCENTATGE IGUALS AMB UNA NOVA PARAULA: " + str(iguals / maxmessages) + u"\u2588")
        self.assertGreaterEqual(iguals, 0.9)
        """



