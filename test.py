#Import tkinter library
from tkinter import *
#Create an instance of Tkinter frame or window
win = Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Make the window sticky for every case
win.grid_rowconfigure(0, weight=1)
win.grid_columnconfigure(0, weight=1)
#Create a Label
label = Label(win, text="This is a Centered Text", font=('Aerial 15 bold'))
label.grid(row=2, column=0)
label.grid_rowconfigure(1, weight=1)
label.grid_columnconfigure(1, weight=1)
win.mainloop()


'''
if self.addStudentBookEntry.get() is not None:
            self.classroom.ajoute_emprunt(self.curseselection, self.addStudentBookEntry.get())

        if self.delStudentBookEntry.get() is not None:
            print(self.classroom.dico[self.curseselection])
            if self.classroom.del_book_borrowed(self.curseselection, str(self.delStudentBookEntry.get())):
                return True
            else:
                return (tkinter.messagebox.showerror('Erreur', 'Le livre indiqué n\'est pas actuellement emprunté par l\'élève !'))
                '''