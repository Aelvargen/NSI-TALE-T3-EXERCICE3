import webbrowser
from datetime import date, datetime
import codecs
import csv

class Eleve:
    def __init__(self, studentName, studentSurname, studentDob):
        self.studentName = studentName
        self.studentSurname = studentSurname
        self.studentDob = datetime.strptime(studentDob, "%d/%m/%Y")
        self.studentAge = self.age()
        self.studentGrade = None
        self.studentBookBorrowed = []


    def __str__(self):
        return "{} {} {} {} {}".format(self.studentName, self.studentSurname, self.studentDob, self.studentGrade, self.studentBookBorrowed)


    def age(self):
            today = date.today()
            return today.year - self.studentDob.year - ((today.month, today.day) < (self.studentDob.month, self.studentDob.day))


    def agedOrOlderThan18(self):
        return True if self.studentAge >= 18 else False


class ensEleve:
    def __init__(self) -> None:
        self.classroom = {}
        self.studentsList = self.charger_eleves("eleves.csv")
        self.studentsOverTheAgeOfMajority = self.liste_eleves_majeurs()

    def __str__(self) -> str:
        return str(self.classroom)

    def charger_eleves(self, csvFileName):
        self.dico = {}
        e = 0
        with codecs.open(csvFileName, encoding="utf-8") as csvfile: # Ouverture du fichier
            # codecs.open pour forcer le lecture en utf-8
            spam = csv.reader(csvfile, delimiter=';') 
            for rang in spam :
                self.dico[rang[0]] = {'nom': rang[1], 'prenom': rang[2], 'date_de_naissance': rang[3], 'classe': rang[4], 'emprunts': (rang[5].split(','))}
                self.create_student_in_classroom(list(self.dico)[e])
                e = e + 1
        return self.classroom

    def create_student_in_classroom(self, studentId):
        liste = []
        for key, value in self.dico[studentId].items():
            liste.append(value)
        student = Eleve(liste[0], liste[1], liste[2])
        student.studentGrade = liste[3]
        student.studentBookBorrowed = liste[4]
        self.classroom[studentId] = student

        return self.classroom
            


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
            # test = self.classroom[studentId]["studentBookBorrowed"]
            # test_re = test[:1] + "'" + str(booksList) + "', " + test[1:]
            self.classroom[studentId].studentBookBorrowed.append(str(book))
            return True
        else:
            return False
            
        pass

    def del_book_borrowed(self, studentId, book):
        if self.studentSearchById(studentId):
            if book in self.classroom[studentId].studentBookBorrowed:
                print(self.classroom[studentId].studentBookBorrowed)
                self.classroom[studentId].studentBookBorrowed.remove(book)
                print(self.classroom[studentId].studentBookBorrowed)
                return True
            else:
                return None


    def liste_eleves_majeurs(self):
        listOfAdultsStudents = []
        for studentId in self.classroom:
            if self.classroom[studentId].agedOrOlderThan18():
                listOfAdultsStudents.append(studentId)
        return listOfAdultsStudents

    def ajoute_eleve(self, newStudentId, newStudentName, newStudentSurname, newStudentDob):

        try:

            if not all(isinstance(element, str) for element in [newStudentId, newStudentName, newStudentSurname, newStudentDob]):
                raise TypeError

            if not all(studentId != newStudentId for studentId in self.classroom.keys()):
                raise KeyError

            datetime.strptime(newStudentDob, "%d/%m/%Y") # return ValueError if not possible to convert


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
