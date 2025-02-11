import sqlite3
import tkinter
from tkinter import ttk, messagebox
from Dashboard import Dashboard
from Student import Student


class Login(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pyhton Project")
        self.dashboard = Dashboard(self, self)

        # Definierte Auswahl an möglichen Studiengängen (der einfachheit halber nur 2)
        # Diese werden die voreingestellten Kurse im Dashboard beeinflussen
        courses_of_study = ["Software Engineering", "Mathematics"]

        # Datenbank öffnen
        conn = sqlite3.connect('study_database.db')
        # Cursor erstellen
        cursor = conn.cursor()

        # Alle Daten aus finished courses auswählen
        cursor.execute("SELECT *, oid FROM students")
        records = cursor.fetchall()

        # Darstellung der Login-Seite muss davon abhängig sein, ob bereits Einträge vom Studenten in der Datenbank existieren.
        # In diesem Prototyp wird es nicht erlaubt, mehr als einen Studenten zu erstellen
        if records:
            # Wenn ein Eintrag vom Student existiert, so soll wieder das Objekt student erzeugt werden
            student = Student(records[0][0],records[0][1],records[0][2])

            # study (Studiengang) wurde nur als String in der Datenbank gespeichert.
            # Wie in Phase 2 beschrieben, wurde keine Klasse für den Studiengang erstellt
            study = records[0][3]
            #Debug der Angaben in der Konsole
            print(f"Name: {student.surname} {student.lastname}, Student ID: {student.id}, Studiengang: {records[0][3]}")

            # Login-Seite
            self.login_page = tkinter.Frame(self)
            self.login_page.pack(fill="both",expand=True)
            tkinter.Label(self.login_page, text="Willkommen zurück!").grid(row=0, column=0, columnspan=2, pady=20, padx=20)

            # Button zum Erstellen des Dashboards
            create_dashboard_button = tkinter.Button(self.login_page, text="Zum Dashboard", command= lambda: self.show_dashboard(student,study))
            create_dashboard_button.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

            # Eingabefeld für den Vornamen
            surname_label = tkinter.Label(self.login_page, text="Vorname: " + records[0][0])
            surname_label.grid(row=1, columnspan=2, pady=10, padx=20)

            # Eingabefeld für den Nachnamen
            lastname_label = tkinter.Label(self.login_page, text="Nachname: " + records[0][1])
            lastname_label.grid(row=2, columnspan=2, pady=10, padx=20)

            # Auswahl vom Studiengang mit drop box
            studies_label = tkinter.Label(self.login_page, text="Studiengang: " + records[0][3])
            studies_label.grid(row=3, columnspan=2, pady=10, padx=20)
        else:
            # Login-Seite
            self.login_page = tkinter.Frame(self)
            self.login_page.pack(fill="both",expand=True)
            tkinter.Label(self.login_page, text="Willkommen! Du kannst hier dein neues Dashboard erstellen.").grid(row=0, column=0, columnspan=2, pady=20, padx=20)

            # Button zum Erstellen des Dashboards
            create_dashboard_button = tkinter.Button(self.login_page, text="Dashboard erstellen",command=self.init_dashboard)
            create_dashboard_button.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

            # Eingabefeld für den Vornamen
            surname_label = tkinter.Label(self.login_page, text="Vorname: ")
            surname_label.grid(row=1, column=0, pady=10, padx=20)
            self.surname_input = tkinter.Entry(self.login_page, width=30)
            self.surname_input.grid(row=1, column=1, pady=10, padx=20)

            # Eingabefeld für den Nachnamen
            lastname_label = tkinter.Label(self.login_page, text="Nachname: ")
            lastname_label.grid(row=2, column=0, pady=10, padx=20)
            self.lastname_input = tkinter.Entry(self.login_page, width=30)
            self.lastname_input.grid(row=2, column=1, pady=10, padx=20)

            # Auswahl vom Studiengang mit drop box
            studies_label = tkinter.Label(self.login_page, text="Studiengang: ")
            studies_label.grid(row=3, column=0, pady=10, padx=20)
            self.studies_drop_box = ttk.Combobox(self.login_page, values=courses_of_study)
            self.studies_drop_box.current(0)
            self.studies_drop_box.grid(row=3, column=1, pady=10, padx=20)



        # Änderungen speichern
        conn.commit()
        # Schließen der Verbindung
        conn.close()


        # Button zum Zurücksetzen des Dashboards (Achtung dies wird auch den Namen und Studiengang löschen)
        reset_dashboard_button = tkinter.Button(self.login_page, text="Alles zurücksetzen", command=self.reset_all)
        reset_dashboard_button.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="ew")



        self.login_page.pack(fill="both", expand=True)

    # Methode, die zur Erstellung vom Dashboard verwendet wird und mit den Eingaben des Nutzers arbeitet
    def init_dashboard(self):
        # Namen vom Studenten erhalten
        surname = self.surname_input.get()
        lastname = self.lastname_input.get()

        # Warnung, wenn Eingabe fehlt
        if not surname or not lastname:
            messagebox.showinfo("Eingabe fehlt", "Bitte geben deinen/einen Namen an!")
            return

        # Student Objekt erzeugen lassen (dies ist vor allem wichtig, damit eine ID erstellt wird)
        student = Student(surname, lastname)
        # Studiengang erhalten
        study = self.studies_drop_box.get()

        # Datenbank öffnen
        conn = sqlite3.connect('study_database.db')
        # Cursor erstellen
        cursor = conn.cursor()

        # Daten vom Studenten und den Studiengang einpflegen
        cursor.execute("INSERT INTO students VALUES (:student_surname, :student_lastname, :student_it, :study)",
                       {
                           'student_surname': student.surname,
                           'student_lastname': student.lastname,
                           'student_it': student.id,
                           'study': study
                       })

        #Basierend auf dem Studiengang werden hier einige Kurse als Beispiel initalisiert
        if study == "Software Engineering":
            predefined_courses = [
                ("Requirements Engineering", "Platzhalter für Kursbeschreibung", 0, "Klausur"),
                ("Python Projekt", "Platzhalter für Kursbeschreibung", 0, "Projekt")
            ]
            #Hinzufügen der voreingestellten Kurse in die Datenbank
            for course_name, course_description, course_grade, course_examination  in predefined_courses:
                cursor.execute("INSERT INTO courses VALUES (:course_name, :course_description, :course_grade, :course_examination)",
                               {
                                   'course_name': course_name,
                                   'course_description': course_description,
                                   'course_grade': course_grade,
                                   'course_examination': course_examination
                               })
        elif study == "Mathematics":
            predefined_courses = [
                ("Stochastik", "Platzhalter für Kursbeschreibung", 0, "Klausur"),
                ("Lineare Algebra", "Platzhalter für Kursbeschreibung", 0, "Klausur"),
                ("Analysis", "Platzhalter für Kursbeschreibung", 0, "Klausur"),
            ]
            # Hinzufügen der voreingestellten Kurse in die Datenbank
            for course_name, course_description, course_grade, course_examination in predefined_courses:
                cursor.execute("INSERT INTO courses VALUES (:course_name, :course_description, :course_grade, :course_examination)",
                               {
                                   'course_name': course_name,
                                   'course_description': course_description,
                                   'course_grade': course_grade,
                                   'course_examination': course_examination
                               })

        # Änderungen speichern
        conn.commit()
        # Schließen der Verbindung
        conn.close()

        # Dashboard mit den Eingaben initialisieren und aufrufen
        self.show_dashboard(student, study)

    # Methode, die mit dem Zurücksetzen-Button aufgerufen werden kann, um alle Daten zu löschen (inklusive Name und Studiengang)
    def reset_all(self):
        # Datenbank öffnen
        conn = sqlite3.connect('study_database.db')
        # Cursor erstellen
        cursor = conn.cursor()

        # Alle Einträge aus den Tabellen entfernen
        cursor.execute("DELETE FROM students")
        cursor.execute("DELETE FROM courses")
        cursor.execute("DELETE FROM finished_courses")

        # Änderungen speichern
        conn.commit()
        # Schließen der Verbindung
        conn.close()

        # Aktuelles Fenster schließen und erneut starten
        self.destroy()
        self.__init__()

    # Methode für das Aufrufen des Dashboards
    def show_dashboard(self, student: Student, study):
        self.dashboard = Dashboard(self, self)
        # Die initialize-Methode in der Klasse Dashboard wird aufgerufen
        self.dashboard.initialize(student, study)
        # Alle anderen Seiten schließen
        self.login_page.pack_forget()

        # Dashboard verpacken
        self.dashboard.pack(fill="both", expand=True)


# Es soll immer zuerst die Login-Seite gestartet werden bei der Ausführung
if __name__ == "__main__":
    app = Login()
    app.mainloop()
