import sys
from datetime import date, datetime
import codecs
import csv

class ensEleves:
    def __init__(self, dico):
        self.dico = dico

    def charger_eleves(self, file):
        donnee = []
        with codecs.open(file, encoding="utf-8") as csvfile:  # Ouverture du fichier
            # codecs.open pour forcer le lecture en utf-8
            spam = csv.reader(csvfile, delimiter=';')
            for rang in spam:
                donnee.append(rang)
        for i in range(0, len(donnee)):
            self.dico[donnee[i][0]] = {'nom': donnee[i][1], 'prénom': donnee[i][2],
                                       'anniv': donnee[i][3], 'classe': donnee[i][4], 'emprunts': donnee[i][5]}
        return self.dico

    def classe(self, eleve, classe):
        self.dico[eleve]['classe'] = classe
        return self.dico

    def ajoute_emprunts(self, eleve, livre):
        self.dico[eleve].emprunts.append(livre)
            
        # self.dico[eleve].emprunts.append(livre)
        return self.dico


dico = {}
instance = ensEleves(dico)
print(instance.charger_eleves("eleves.csv"))
print(instance.classe('elv1', 'classe3'))
print(instance.ajoute_emprunts('elv1', 'cc'))
