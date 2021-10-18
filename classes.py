# -*- coding: utf-8 -*-

from datetime import date, datetime
import codecs
import csv

class Eleve:
    def __init__(self, studentName, studentSurname, studentDob):
        self.studentName = studentName
        self.studentSurname = studentSurname
        self.studentDob = datetime.strptime(studentDob, "%d/%m/%Y")
        self.studentAge = self.age()
        self.studentGrade = None # classe (niveau scolaire)
        self.studentBookBorrowed = [] # liste des livres empruntés


    def __str__(self) -> str:
        return "{} {} {} {} {}".format(self.studentName, self.studentSurname, self.studentDob, self.studentGrade, self.studentBookBorrowed)


    def age(self):
            self.today = date.today()
            # Ce calcul nous permet d'avoir une précision au jour près de l'âge de l'élève
            return self.today.year - self.studentDob.year - ((self.today.month, self.today.day) < (self.studentDob.month, self.studentDob.day))


    def agedOrOlderThan18(self):
        return True if self.studentAge >= 18 else False


class ensEleve:
    def __init__(self):
        self.classroom = {}
        self.studentsList = self.charger_eleves("eleves.csv")
        self.studentsOverTheAgeOfMajority = self.liste_eleves_majeurs()

    def __str__(self) -> str:
        return str(self.classroom)

    # On charge notre fichier csv dans des dictionnaires imbriqués qui contiennent comme clef principale l'identifiant de l'élève qui ressemble à ça :
    # {'elv1': {'nom': 'Mebeaucoup', 'prenom': 'Sarah', 'date_de_naissance': '01/01/2003', 'classe': 'classe1', 'emprunts': ['emprunt_1', 'emprunt_2', 'emprunt_3']}, 'elv2': {'nom': 'Camion', 'prenom': 'Bo', 'date_de_naissance': '18/03/1954', 'classe': 'classe2', 'emprunts': ['emprunt_4']}, 'elv3': {'nom': 'Versaire', 'prenom': 'Annie', 'date_de_naissance': '19/09/1970', 'classe': 'Schmurtze classe', 'emprunts': ['emprunt_5']}} 

    def charger_eleves(self, csvFileName):
        self.dico = {}
        e = 0
        with codecs.open(csvFileName, encoding="utf-8") as csvfile: # Ouverture du fichier
            # codecs.open pour forcer le lecture en utf-8
            spam = csv.reader(csvfile, delimiter=';') 
            for rang in spam :
                self.dico[rang[0]] = {'nom': rang[1], 'prenom': rang[2], 'date_de_naissance': rang[3], 'classe': rang[4], 'emprunts': (rang[5].split(','))}
                self.create_student_in_classroom(list(self.dico)[e]) # On appelle notre fonction qui va crée une instance de la classe Eleve
                e = e + 1
        return self.classroom

    # On crée ensuite un autre dictionnaire qui lui contient toutes les instances de la classe Eleve correspondantes aux identifiants élèves qui ressemble à ça :
    # {'elv1': <classes.Eleve object at 0x0000018CA2B2A0D0>, 'elv2': <classes.Eleve object at 0x0000018CA2B20E80>, 'elv3': <classes.Eleve object at 0x0000018CA2B209A0>}
    def create_student_in_classroom(self, studentId):
        liste = []
        for value in self.dico[studentId].values():
            liste.append(value)
        student = Eleve(liste[0], liste[1], liste[2])
        student.studentGrade = liste[3]
        student.studentBookBorrowed = liste[4]
        self.classroom[studentId] = student
        return self.classroom
            

    # Vérifie si l'élève existe 
    def studentSearchById(self, studentId):
        for student in self.classroom:
            if student == studentId:
                return self.classroom[student]
        return None

    def classe(self, studentId, newClassGroup):
        if self.studentSearchById(studentId):
            self.classroom[studentId].studentGrade = newClassGroup
            self.dico[studentId]["classe"] = newClassGroup
            return True
        else:
            return None


    def ajoute_emprunt(self, studentId, book):
        if self.studentSearchById(studentId):
            self.classroom[studentId].studentBookBorrowed.append(str(book))
            return True
        else:
            return False
            

    def del_book_borrowed(self, studentId, book):
        if self.studentSearchById(studentId):
            if book in self.classroom[studentId].studentBookBorrowed:
                self.classroom[studentId].studentBookBorrowed.remove(str(book))
                return True
            else:
                raise ValueError


    def liste_eleves_majeurs(self):
        listOfAdultsStudents = []
        for studentId in self.classroom:
            if self.classroom[studentId].agedOrOlderThan18():
                listOfAdultsStudents.append(studentId)
        return listOfAdultsStudents

    def ajoute_eleve(self, newStudentId, newStudentName, newStudentSurname, newStudentDob):
        try:
            if not all(isinstance(element, str) for element in [newStudentId, newStudentName, newStudentSurname, newStudentDob]):
                # Renvoyer ce genre d'erreurs nous permet de générer des fenêtre d'erreurs spécifiques via notre interface graphique
                raise TypeError

            if not all(studentId != newStudentId for studentId in self.classroom.keys()):
                raise KeyError

            datetime.strptime(newStudentDob, "%d/%m/%Y") # Test si le format de date entré est correct, si non cela renvoit une ValueError


        except TypeError:
            return TypeError
        except KeyError:
            return KeyError
        except ValueError:
            return ValueError
        else:
            self.dico[newStudentId] = {'nom': newStudentName, 'prenom' : newStudentSurname, 'date_de_naissance' : newStudentDob, 'classe' : None, 'emprunts' : []}
            self.create_student_in_classroom(newStudentId)

            return True


    def export_class_as_csv(self):
        field_names = ['id', 'nom', 'prenom', 'date_de_naissance', 'classe', 'emprunts']
        with open('classroom.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for k in self.dico:
                writer.writerow({field: self.dico[k].get(field) or k for field in field_names})


    # Le fichier csv renvoyé ressemble à ça :
    #|------|------------|--------|-------------------|------------------|-----------------------------------------|
    #| id   | nom        | prenom | date_de_naissance | classe           | emprunts                                | --> Colonnes prédéfinies ligne 135
    #|------|------------|--------|-------------------|------------------|-----------------------------------------|
    #| elv1 | Mebeaucoup | Sarah  | 01/01/2003        | classe1          | ['emprunt_1', 'emprunt_2', 'emprunt_3'] |
    #|------|------------|--------|-------------------|------------------|-----------------------------------------|
    #| elv2 | Camion     | Bo     | 18/03/1954        | classe2          | ['emprunt_4']                           |
    #|------|------------|--------|-------------------|------------------|-----------------------------------------|
    #| elv3 | Versaire   | Annie  | 19/09/1970        | Schmurtze classe | ['emprunt_5']                           |
    #|------|------------|--------|-------------------|------------------|-----------------------------------------|

