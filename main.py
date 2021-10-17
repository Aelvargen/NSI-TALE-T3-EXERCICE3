# -*- coding: utf-8 -*-

from datetime import date, datetime
import codecs
import csv

class Eleve:
    def __init__(self, studentName, studentSurname, studentDob):
        self.studentName = studentName
        self.studentSurname = studentSurname
        self.studentDob = studentDob
        # self.studentAge = self.age()
        self.studentGrade = None
        self.studentBookBorrowed = []


    def __str__(self):
        return "{} {} {} {} {}".format(self.studentName, self.studentSurname, self.studentDob, self.studentGrade, self.studentBookBorrowed)


    def age(self):
        self.studentAge = (datetime.now().date() - self.studentDob) / 365 # On calcule l'âge de l'élève en jours que nous divisons par 365 pour obtenir le nombre d'années
        return self.studentAge.days # .days car le nombre d'années est stocké dans notre type <datetime> comme un nombre de jours


    def agedOrOlderThan18(self):
        return True if self.studentAge >= 18 else False


class ensEleve:
    def __init__(self) -> None:
        self.classroom = {}
        self.studentsList = self.charger_eleves("eleves.csv")

    def __str__(self) -> str:
        return str(self.classroom)

    def charger_eleves(self, csvFileName):
        self.dico = {}
        self.donnee=["nom", "prenom", "date_de_naissance", "classe", "emprunts"]
        with codecs.open(csvFileName, encoding="utf-8") as csvfile: # Ouverture du fichier
            # codecs.open pour forcer le lecture en utf-8
            spam = csv.reader(csvfile, delimiter=';') 
            for rang in spam :
                self.test = {}
                e = 0
                for i in self.donnee:
                    e += 1
                    self.test[i] = rang[e]
                self.dico[rang[0]] = self.test

        return self.create_class()

    def create_class(self):
        for key, value in self.dico.items():
            liste = []
            for item in value.values():
                liste.append(item)
            student = Eleve(liste[0], liste[1], liste[2])
            self.classroom[key] = student
        return self.classroom
            


    def studentSearchById(self, studentId):
        for student in self.classroom:
            if student == studentId:
                return self.classroom[student]
        return None

    def classe(self, studentId, newClassGroup):
        if self.studentSearchById(studentId):
            self.classroom[studentId].studentGrade = newClassGroup
            return self.classroom[studentId]
        else:
            return None

        pass

    def ajoute_emprunt(self, studentId, book):
        if self.studentSearchById(studentId):
            # test = self.classroom[studentId]["studentBookBorrowed"]
            # test_re = test[:1] + "'" + str(booksList) + "', " + test[1:]
            self.classroom[studentId].studentBookBorrowed.remove(str(book))
            return self.classroom[studentId]
            
        pass

    def del_book_borrowed(self, studentId, book):
        if self.studentSearchById(studentId):
            self.classroom[studentId].studentBokBorrowed.delete(str(book))
            return self.classroom[studentId]
    def liste_eleves_majeurs(self):

        pass

    def ajoute_eleve(self):

        pass


class createCsv:

    def __init__(self) -> None:
        pass

    def __str__(self) -> str:
        pass

    pass


# instance = Eleve("Adrien", "Grom", date(2003, 10, 20))

# print(instance)
# print(instance.agedOrOlderThan18())

instance2 = ensEleve()

# print(instance2.studentsList)
print(instance2.classroom["elv1"])

instance2.classe("elv1", "cinquième")


print(instance2.classroom["elv1"])

instance2.ajoute_emprunt("elv1", "Mein Kampf")
print(instance2.classroom["elv1"])

instance2.ajoute_emprunt("elv1", "Mein Kampf")
print(instance2.classroom["elv1"])


instance2.del_book_borrowed("elv1", "Mein Kampf")
print(instance2.classroom["elv1"])
# print(instance2.studentSearchById("elv1"))
# print(instance2.classe("elv1", "test"))

# print(instance2.ajoute_emprunt("elv1", "test"))

# print(instance2.define_students())
# Arrêt : Grand B, 2 : il faut ajouter les clés du dictionnaire pour chaque valeur

