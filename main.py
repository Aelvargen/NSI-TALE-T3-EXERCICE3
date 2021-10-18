# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox

# librairie permettant d'aller chercher un fichier dans un dossier
import webbrowser
from classes import ensEleve

class MainApplication:

    def __init__(self, master):
        self.classroom = ensEleve()
        self.master = master

        self.students_Box = LabelFrame(self.master,text='Liste des identifiants élèves',relief=GROOVE, labelanchor='n', width=850, height=180)
        self.students_Box.grid_propagate(0)

        self.students_Box.pack(pady=15)

        self.scrollbar = Scrollbar(self.students_Box)
        self.scrollbar.pack(side=RIGHT, fill=Y)

       
        self.listbox = Listbox(self.students_Box, width=90, bg='azure', font=('Consolas', 10, ''))  # 'TkDefaultFont 11')
        self.listbox.pack(padx=5, pady=10)

        for key in self.classroom.dico.keys():
            self.listbox.insert(END,'%s' % ((key)))
        
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.listbox.yview)

        self.my_button = Button(master, text="Ajouter un élève",  command=self.add_new_student)
        self.my_button.place(x=25, y=250)

        self.my_button2 = Button(master, text="Voir les infos de l'élève", command=self.show_student_info)
        self.my_button2.place(x=150, y=250)

        self.my_button3 = Button(master, text="Rafraichir la liste", command = lambda : self.refresh())
        self.my_button3.place(x=550, y=250)
        self.master = master
        self.frame = Frame(self.master, relief=RAISED, borderwidth=1)

        self.agedOrOlderThan18StudentsButton = Button(master, text="Liste des élèves majeurs", command=self.show_aged_or_older_than_18_students)
        self.agedOrOlderThan18StudentsButton.place(x=400, y=250)

        # TOUS LES LOGOS UTILISÉS PROVIENNENT DU SITE: https://www.flaticon.com/
        self.refresh()
        self.frame.pack()
        self.createMenuBar(master)
        self.main_application_geometry = self.window_geometry(master, 700, 500)
        self.init_Window(master)

    
    def refresh(self):
        for key in self.classroom.dico.keys():
            if key not in self.listbox.get(0, 'end'):
                self.listbox.insert(END, '%s' % ((key)))

    def add_new_student(self):
        self.newCreatingWindow = Toplevel(self.master)
        self.app = addNewStudentWindow(self.newCreatingWindow, self.window_geometry, self.classroom)

    def show_student_info(self):
        try:
            self.currentSelectionValue = self.listbox.get(self.listbox.curselection())
            
        except TclError:
            return (tkinter.messagebox.showerror('Erreur', 'Veuillez sélectionner un élève !'))
        else:
            self.newInfoWindow = Toplevel(self.master)
            self.app = showStudentInfos(self.newInfoWindow, self.window_geometry, self.classroom, self.currentSelectionValue)

    def show_aged_or_older_than_18_students(self):
        self.newStudentsListWindow = Toplevel(self.master)
        self.app = showAgedOrOlderThan18Students(self.newStudentsListWindow, self.window_geometry, self.classroom)


    def init_Window(self, master): 
        self.title = master.title('Liste des élèves')
        master.configure(bg='#FFF')

        
        master.tk.call('lappend', 'auto_path', 'awthemes-10.3.0/')
        master.tk.call('package', 'require', 'awlight')
        self.style = Style()
        self.style_theme_used = self.style.theme_use('awlight')

        # Logo stocké dans le dossier /images
        self.favicon = master.iconbitmap(r'images/favicon.ico')
        self.menu = Menu()

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
        menuBar = Menu(master)
        menuFile = Menu(menuBar, tearoff=0)

        menuBar.add_cascade(label='Fichier', menu=menuFile)

        self.photo_save = PhotoImage(file=r'images/floppy-disk.png')
        self.photoimage_save = self.photo_save.subsample(30, 30)
        menuFile.add_command(label='Sauvegarder les résultats', image=self.photoimage_save, compound=LEFT, command= lambda : self.classroom.export_class_as_csv())


        menuHelp = Menu(menuBar, tearoff=0)
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
            'À propos', '---------------------------------------\n Gestion d\'une liste d\'élève.\n Réalisé par Alexis SARRA \n\n Classe de Terminale d\'enseignement Numérique et Sciences Informatiques \n\n Lycée Privé Ensemble Scolaire Jean-XXIII - 57958 Montigny-lès-Metz \n ---------------------------------------'
        )


class addNewStudentWindow:
    def __init__(self, master, window_geometry, classroom):
        self.classroom = classroom
        self.test = window_geometry(master, 600, 375)
        self.master = master
        self.frame = Frame(self.master)
        master.configure(bg='#FFF')
        master.attributes('-topmost', True)

        self.students_Box = LabelFrame(self.master,text='Nouvel Élève', relief=GROOVE, labelanchor='n', width=850, height=180)
        self.students_Box.grid_propagate(0)
        self.students_Box.pack(pady=15)

        self.newStudentIdLabel = Label(self.students_Box, text='Identifiant du nouvel élève:', foreground='#151414', font='Consolas')
        self.newStudentIdLabel.pack()
        self.newStudentIdInput = Entry(self.students_Box, width=30, font='Consolas')
        self.newStudentIdInput.pack(pady=5, padx=10)


        self.newStudentNameLabel = Label(self.students_Box, text='Prénom du nouvel élève:', foreground='#151414', font='Consolas')
        self.newStudentNameLabel.pack()
        self.newStudentNameInput = Entry(self.students_Box, width=30, font='Consolas')
        self.newStudentNameInput.pack(pady=5, padx=10)


        self.newStudentSurnameLabel = Label(self.students_Box, text='Nom de famille du nouvel élève:', foreground='#151414', font='Consolas')
        self.newStudentSurnameLabel.pack()
        self.newStudentSurnameInput = Entry(self.students_Box, width=30, font='Consolas')
        self.newStudentSurnameInput.pack(pady=5, padx=10)

        self.newStudentDobLabel = Label(self.students_Box, text='Date d\'anniversaire du nouvel élève:', foreground='#151414', font='Consolas')
        self.newStudentDobLabel.pack()
        self.newStudentDobInput = Entry(self.students_Box, width=30, font='Consolas')
        self.newStudentDobInput.pack(pady=5, padx=10)
    

        self.addButton = Button(self.frame, text = 'Ajouter', width = 25, command = self.add_new_student)
        self.addButton.pack()

        self.quitButton = Button(self.frame, text = 'Quitter', width = 25, command = self.close_window)
        self.quitButton.pack()

        self.frame.pack()

    def add_new_student(self):

        if self.classroom.ajoute_eleve(self.newStudentIdInput.get(), self.newStudentNameInput.get(), self.newStudentSurnameInput.get(), self.newStudentDobInput.get()) == KeyError:
            self.master.attributes('-topmost', False)
            return (tkinter.messagebox.showerror('Erreur', "Identifiant déjà existant !")), self.master.attributes('-topmost', True)

        elif self.classroom.ajoute_eleve(self.newStudentIdInput.get(), self.newStudentNameInput.get(), self.newStudentSurnameInput.get(), self.newStudentDobInput.get()) == ValueError:
            self.master.attributes('-topmost', False)
            return (tkinter.messagebox.showerror('Erreur', "Date de naissance incorrecte, veuillez respecter la syntaxe : jj/mm/aaaa")), self.master.attributes('-topmost', True)

        elif self.classroom.ajoute_eleve(self.newStudentIdInput.get(), self.newStudentNameInput.get(), self.newStudentSurnameInput.get(), self.newStudentDobInput.get()) == TypeError:
            self.master.attributes('-topmost', False)
            return (tkinter.messagebox.showerror('Erreur', "Veuillez inclure chaque variable en tant que chaîne de caractères !")), self.master.attributes('-topmost', True)


        else:
            self.close_window()
            return (tkinter.messagebox.showinfo('Confirmation', "Enregistrement fait !"))

    def close_window(self):
        self.master.destroy()


class showStudentInfos():
    def __init__(self, master, window_geometry, classroom, curseselection):
        self.curseselection = curseselection
        self.classroom = classroom
        self.test = window_geometry(master, 600, 500)
        self.master = master
        self.frame = Frame(self.master)
        master.configure(bg='#FFF')
        master.attributes('-topmost', True)

        self.students_Box = LabelFrame(self.master,text='Fiche Élève : {}'.format(self.curseselection), relief=GROOVE, labelanchor='n', width=850, height=180)
        self.students_Box.grid_propagate(0)
        self.students_Box.pack(pady=15)

        self.studentNameTitle = Label(self.students_Box, text="Prénom", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.studentNameTitle.grid(row=0, sticky=E)
        self.studentNameTitle.grid_rowconfigure(1, weight=1)
        self.studentNameTitle.grid_columnconfigure(1, weight=1)

        self.studentName = Label(self.students_Box, text=' ' + classroom.dico[curseselection]['prenom'], foreground='#151414', font='Consolas')
        self.studentName.grid(row=0, column=1, sticky=W)
    
        self.studentSurnameTitle = Label(self.students_Box, text="Nom de famille", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.studentSurnameTitle.grid(row=1, sticky=E)
        self.studentSurname = Label(self.students_Box, text=' ' + classroom.dico[curseselection]['nom'], foreground='#151414', font='Consolas')
        self.studentSurname.grid(row=1, column=1, sticky=W)

        self.studentDobTitle = Label(self.students_Box, text="Date de naissance", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.studentDobTitle.grid(row=2, sticky=E)
        self.studentDob = Label(self.students_Box, text=' ' + classroom.dico[curseselection]['date_de_naissance'], foreground='#151414', font='Consolas')
        self.studentDob.grid(row=2, column=1, sticky=W)

        self.studentGradeTitle = Label(self.students_Box, text="Classe", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.studentGradeTitle.grid(row=3, sticky=E)
        self.studentGrade = Label(self.students_Box, text=' ' + str(classroom.dico[curseselection]['classe']), foreground='#151414', font='Consolas')
        self.studentGrade.grid(row=3, column=1, sticky=W)

        self.studentBooksBorrowedTitle = Label(self.students_Box, text="Livres empruntés", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.studentBooksBorrowedTitle.grid(row=4, sticky=E)
        self.studentBooksBorrowed = Label(self.students_Box, text=' ' + str(classroom.dico[curseselection]['emprunts']), foreground='#151414', font='Consolas')
        self.studentBooksBorrowed.grid(row=4, column=1, sticky=W)

        self.changeStudentGradeLabel = Label(self.master, text="Changer la classe de l'élève", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.changeStudentGradeLabel.pack()
        self.changeStudentGradeInput = Entry(self.master, width=10, font='Consolas')
        self.changeStudentGradeInput.pack()

        self.addStudentBookLabel = Label(self.master, text="Ajouter un livre", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.addStudentBookLabel.pack()
        self.addStudentBookEntry = Entry(self.master, width=10, font='Consolas')
        self.addStudentBookEntry.pack()

        self.delStudentBookLabel = Label(self.master, text="Supprimer un livre", foreground='#151414', font=('Consolas', 11, 'normal', 'underline'))
        self.delStudentBookLabel.pack()
        self.delStudentBookEntry = Entry(self.master, width=10, font='Consolas')
        self.delStudentBookEntry.pack()

        self.applyChanges = Button(self.master, text="Appliquer les modifications", command = self.apply_changes)
        self.applyChanges.pack()

    def apply_changes(self):

        if len(self.changeStudentGradeInput.get()) != 0:
                if self.classroom.classe(self.curseselection, self.changeStudentGradeInput.get()):
                    self.close_window()
                    return (tkinter.messagebox.showinfo('Confirmation', 'Modification(s) enregistrée(s) avec succès !'))
                else:
                    self.master.attributes('-topmost', False)
                    return (tkinter.messagebox.showerror('Erreur', 'Le classe indiquée n\'est pas attribuable.')), self.master.attributes('-topmost', True)
        if len(self.addStudentBookEntry.get()) != 0:
            if self.classroom.ajoute_emprunt(self.curseselection, self.addStudentBookEntry.get()):
                self.close_window()
                return (tkinter.messagebox.showinfo('Confirmation', 'Modification(s) enregistrée(s) avec succès !'))

        if len(self.delStudentBookEntry.get()) != 0:
            if self.classroom.del_book_borrowed(self.curseselection, self.delStudentBookEntry.get()):
                self.close_window()
                return (tkinter.messagebox.showinfo('Confirmation', 'Modification(s) enregistrée(s) avec succès !'))
            else:
                self.master.attributes('-topmost', False)
                return (tkinter.messagebox.showerror('Erreur', 'Le classe indiquée n\'est pas attribuable.')), self.master.attributes('-topmost', True)

    def close_window(self):
        self.master.destroy()

class showAgedOrOlderThan18Students():
    def __init__(self, master, window_geometry, classroom):
        self.classroom = classroom
        self.test = window_geometry(master, 600, 200)
        self.master = master
        self.frame = Frame(self.master)
        master.configure(bg='#FFF')
        master.attributes('-topmost', True)

        self.students_Box = LabelFrame(self.master,text='Liste des élèves majeurs par identifiant',relief=GROOVE, labelanchor='n', width=850, height=180)
        self.students_Box.grid_propagate(0)
        self.students_Box.pack(pady=15)

        self.scrollbar = Scrollbar(self.students_Box)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox = Listbox(self.students_Box, width=90, bg='azure', font=('Consolas', 10, ''))  # 'TkDefaultFont 11')
        self.listbox.pack(padx=5, pady=10)

        for element in classroom.liste_eleves_majeurs():
            self.listbox.insert(END,'%s' % ((element)))
        
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.listbox.yview)

        


def main():
    root = Tk()
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = MainApplication(root)

    root.mainloop()

if __name__ == '__main__':


    main()


