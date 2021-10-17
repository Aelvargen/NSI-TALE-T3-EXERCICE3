# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox
import tkinter as tk

# librairie permettant d'aller chercher un fichier dans un dossier
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
            return self.classroom[studentId]
        else:
            return None


    def ajoute_emprunt(self, studentId, book):
        if self.studentSearchById(studentId):
            # test = self.classroom[studentId]["studentBookBorrowed"]
            # test_re = test[:1] + "'" + str(booksList) + "', " + test[1:]
            self.classroom[studentId].studentBookBorrowed.append(str(book))
            return self.classroom[studentId]
            
        pass

    def del_book_borrowed(self, studentId, book):
        if self.studentSearchById(studentId):
            try:
                self.classroom[studentId].studentBookBorrowed.remove(str(book))

            except ValueError:
                exit ("Impossible de supprimer l'emprunt, {} n'a pas emprunté '{}' !".format(studentId, book))
            return self.classroom[studentId]


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

            if not all(studentId != newStudentId for studentId in self.classroom):
                raise KeyError

            datetime.strptime(newStudentDob, "%d/%m/%Y") # return ValueError if not possible to convert

        except TypeError:
            exit("Veuillez inclure chaque variable en tant que chaîne de caractères !")
        except KeyError:
            exit("Identifiant déjà existant !")
        except ValueError:
            exit("Date de naissance incorrecte, veuillez respecter la syntaxe : jj/mm/aaaa")
        else:
            self.dico[newStudentId] = {'nom': newStudentName, 'prenom' : newStudentSurname, 'date_de_naissance' : newStudentDob, 'classe' : None, 'emprunts' : []}
            return self.create_student_in_classroom(newStudentId)


    def export_class_as_csv(self):
        field_names = ['id', 'nom', 'prenom', 'date_de_naissance', 'classe', 'emprunts']
        with open('classroom.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=field_names)
            writer.writeheader()
            for k in self.dico:
                writer.writerow({field: self.dico[k].get(field) or k for field in field_names})


class MainApplication:

    def __init__(self, master):
        self.classroom = ensEleve()
        self.master = master
        self.label_title = tk.Label(master, text='Test :', fg='white', bg='#2c2c2c', font='Helvetica 14 bold')  # titre
        self.label_title.pack(pady=20, padx=10)

        self.my_listbox = Listbox(self.master)
        self.my_listbox.pack(pady=15)
        for key, value in self.classroom.dico.items():
            self.my_listbox.insert(END, key)

        self.my_button = Button(master, text="Ajouter un élève",  command=self.add_new_student)
        self.my_button.pack(pady=10)

        self.my_button2 = Button(master, text="Voir les infos de l'élève", command=self.show_student_info)
        self.my_button2.pack(pady=10)
        self.my_label = Label(master, text='')
        self.my_label.pack(pady=5)

        self.my_button3 = Button(master, text="Rafraichir la liste", command = lambda : self.refresh())
        self.my_button3.pack(pady=10)


        self.master = master
        self.frame = tk.Frame(self.master, relief=RAISED, borderwidth=1)

        # TOUS LES LOGOS UTILISÉS PROVIENNENT DU SITE: https://www.flaticon.com/

        self.frame.pack()
        self.createMenuBar(master)
        self.main_application_geometry = self.window_geometry(master, 700, 500)
        self.init_Window(master)

    
    def refresh(self):
        self.my_listbox.delete(0, 'end')
        for key, value in self.classroom.dico.items():
            self.my_listbox.insert(END, key)

    def add_new_student(self):
        self.newCreatingWindow = tk.Toplevel(self.master)
        self.app = ResultsWindow(self.newCreatingWindow, self.window_geometry, self.classroom)

    def show_student_info(self):
        self.currentSelectionValue = self.my_listbox.get(self.my_listbox.curselection())
        self.newInfoWindow = tk.Toplevel(self.master)
        self.app = showStudentInfos(
            self.newInfoWindow, self.window_geometry, self.classroom.dico, self.currentSelectionValue)



    def init_Window(self, master):  # INITIALISATION DU STYLE DE LA FENÊTRE
        self.title = master.title('Tris')
        master.configure(bg='#2c2c2c')

        # UTILISATION D'UN THÈME PERSONNALISÉ
        # VOIR: https://wiki.tcl-lang.org/page/List+of+ttk+Themes ET https://sourceforge.net/projects/tcl-awthemes/
        master.tk.call('lappend', 'auto_path', 'awthemes-10.3.0/')
        master.tk.call('package', 'require', 'awlight')
        self.style = Style()
        self.style_theme_used = self.style.theme_use('awlight')

        # Logo stocké dans le dossier /images
        self.favicon = master.iconbitmap(r'images/favicon.ico')
        self.menu = tk.Menu()

    # DÉFINITION DE LA TAILLE ET DU CENTRAGE DE LA FENÊTRE
    # Le but de cette fonction est de centrer notre fenêtre quelque soit la résolution de l'écran. Les dimensions s'adaptent également.

    def window_geometry(self, master, app_width, app_height):

        # On récupère la longueur et la largeur de l'écran de l'utilisateur
        self.screen_width = master.winfo_screenwidth()
        self.screen_height = master.winfo_screenheight()

        # On calcule les coordoonées du centre de l'écran en prenant compte de la taille de la fenêtre
        self.x = (self.screen_width / 2) - (app_width / 2)
        self.y = (self.screen_height / 2) - (app_height / 2)

        # On fait apparaître la fenêtre
        self.geometry = master.geometry(
            f'{app_width}x{app_height}+{int(self.x)}+{int(self.y)}')

    def createMenuBar(self, master):  # MENU SUPÉRIEUR

        self.var = IntVar()
        menuBar = tk.Menu(master)
        menuFile = tk.Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label='Fichier', menu=menuFile)

        self.photo_save = PhotoImage(file=r'images/floppy-disk.png')
        self.photoimage_save = self.photo_save.subsample(30, 30)
        menuFile.add_command(label='Sauvegarder les résultats', image=self.photoimage_save, compound=LEFT, command= lambda : self.classroom.export_class_as_csv())


        menuHelp = tk.Menu(menuBar, tearoff=0)
        # Énoncé de l'exercice
        self.photo_link = PhotoImage(file=r'images/link.png')  # logo
        self.photoimage_link = self.photo_link.subsample(30, 30)
        menuHelp.add_command(label='Cours et énoncé de l\'exercice', image=self.photoimage_link, compound=LEFT, command=lambda: [webbrowser.open('exercices_poo.html')])  # titre et redirection vers le .html de cours

        self.photo_about = PhotoImage(file=r'images/about.png')  # logo
        self.photoimage_about = self.photo_about.subsample(30, 30)
        # titre et enclenchement de la fonction "do_about" ligne 127
        
        menuHelp.add_command(
            label='À propos', image=self.photoimage_about, compound=LEFT, command=self.do_about)

        menuBar.add_cascade(label='Aide', menu=menuHelp)
        master.config(menu=menuBar)

    # Pop-up fenêtre "à propos"

    def do_about(self):
        self.msg = tkinter.messagebox.showinfo(
            'À propos', '---------------------------------------\n Tri par récursivité pour piles et files en OOP.\n Réalisé par Alexis SARRA \n\n Classe de Terminale d\'enseignement Numérique et Sciences Informatiques \n\n Lycée Privé Ensemble Scolaire Jean-XXIII - 57958 Montigny-lès-Metz \n ---------------------------------------'
        )


class ResultsWindow:
    def __init__(self, master, window_geometry, classroom):
        self.classroom = classroom
        self.test = window_geometry(master, 600, 250)
        self.master = master
        self.frame = tk.Frame(self.master)
        master.configure(bg='#2c2c2c')

        self.newStudentIdLabel = tk.Label(master, text='Identifiant du nouvel élève:', fg='white', bg='#2c2c2c', font='Helvetica')
        self.newStudentIdLabel.pack()
        self.newStudentIdInput = tk.Entry(master, width=30, font='Helvetica')
        self.newStudentIdInput.pack(pady=5, padx=10)


        self.newStudentNameLabel = tk.Label(master, text='Prénom du nouvel élève:', fg='white', bg='#2c2c2c', font='Helvetica')
        self.newStudentNameLabel.pack()
        self.newStudentNameInput = tk.Entry(master, width=30, font='Helvetica')
        self.newStudentNameInput.pack(pady=5, padx=10)


        self.newStudentSurnameLabel = tk.Label(master, text='Nom de famille du nouvel élève:', fg='white', bg='#2c2c2c', font='Helvetica')
        self.newStudentSurnameLabel.pack()
        self.newStudentSurnameInput = tk.Entry(master, width=30, font='Helvetica')
        self.newStudentSurnameInput.pack(pady=5, padx=10)

        self.newStudentDobLabel = tk.Label(master, text='Date d\'anniversaire du nouvel élève:', fg='white', bg='#2c2c2c', font='Helvetica')
        self.newStudentDobLabel.pack()
        self.newStudentDobInput = tk.Entry(master, width=30, font='Helvetica')
        self.newStudentDobInput.pack(pady=5, padx=10)
    

        self.addButton = tk.Button(self.frame, text = 'Ajouter', width = 25, command = self.add_new_student)
        self.addButton.pack()

        self.quitButton = tk.Button(self.frame, text = 'Quitter', width = 25, command = self.close_window)
        self.quitButton.pack()

        self.frame.pack()

    def add_new_student(self):
        self.classroom.ajoute_eleve(self.newStudentIdInput.get(), self.newStudentNameInput.get(), self.newStudentSurnameInput.get(), self.newStudentDobInput.get())
        

    def close_window(self):
        self.master.destroy()


class showStudentInfos():
    def __init__(self, master, window_geometry, classroom, curseselection):
        self.classroom = classroom
        self.test = window_geometry(master, 600, 250)
        self.master = master
        self.frame = tk.Frame(self.master)
        master.configure(bg='#2c2c2c')


        self.studentName = tk.Label(master, text=classroom[curseselection]['prenom'], fg='white', bg='#2c2c2c', font='Helvetica')
        self.studentName.pack()

        self.studentSurname = tk.Label(master, text=classroom[curseselection]['nom'], fg='white', bg='#2c2c2c', font='Helvetica')
        self.studentSurname.pack()

        self.studentDob = tk.Label(master, text=classroom[curseselection]['date_de_naissance'], fg='white', bg='#2c2c2c', font='Helvetica')
        self.studentDob.pack()

        self.studentGrade = tk.Label(master, text=classroom[curseselection]['classe'], fg='white', bg='#2c2c2c', font='Helvetica')
        self.studentGrade.pack()

        self.studentBooksBorrowed = tk.Label(master, text=classroom[curseselection]['emprunts'], fg='white', bg='#2c2c2c', font='Helvetica')
        self.studentBooksBorrowed.pack()




















def main():
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop()

if __name__ == '__main__':


    main()


