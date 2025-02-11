import tkinter
from tkinter import *
from tkinter import messagebox
from Course import Course
import sqlite3
from Exam import Exam
from Project import Project


class Dashboard(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # button_count zählt die Anzahl an aktiven Kursen
        self.button_count = 1
        self.semester = 1
        self.course_buttons = {}
        # Liste für die aktiven und abgeschlossenen Kurse
        self.current_courses = []
        self.finished_courses = []

        # Methode zum Initialisieren der Datenbank und den darin vorhanden Tabellen
        def initialize_databank():
            # Eine Datenbank muss erstellt werden
            conn = sqlite3.connect('study_database.db')

            # Ein Cursor wird benötigt
            cursor = conn.cursor()

            # Table für Studenten erstellen
            cursor.execute("""CREATE TABLE students (
                                            student_surname text,
                                            student_lastname text,
                                            student_it integer,
                                            study text)""")

            # Table für aktuelle Kurse erstellen
            cursor.execute("""CREATE TABLE courses (
                                course_name text,
                                course_description text,
                                course_grade integer,
                                course_examination text)""")

            # Table für abgeschlossene Kurse erstellen
            cursor.execute("""CREATE TABLE finished_courses (
                                course_name text,
                                course_description text,
                                course_grade integer,
                                course_examination text)""")

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

        # Methode zum Löschen der Tabellen in der Datenbank (dies war bei Änderungen und Testungen relevant)
        def reset_databank():
            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            #Alle Einträge aus den Tabellen entfernen
            cursor.execute("DELETE FROM students")
            cursor.execute("DELETE FROM courses")
            cursor.execute("DELETE FROM finished_courses")

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

        # Methode zum Entfernen eines Kurs-Buttons (wird aufgerufen, wenn ein Kurs abgeschlossen wird und somit nicht mehr aktiv ist)
        def removeCourseButton(self, course_name):
            # Entfernt den Button eines bestimmten Kurses
            if course_name in self.course_buttons:
                button = self.course_buttons.pop(course_name)
                # Entferne den Button aus der Anzeige
                button.grid_forget()
                # Verringere den Zähler der aktiven Kurse (Anzahl der aktiven Kurse entspricht der Anzahl der Kurs-Buttons)
                self.button_count -= 1

        # Methode zum Aufrufen eines Kurses (ein neues Fenster wird dafür erstellt)
        def openCoursePage(self, course_name):
            editor = Toplevel()
            editor.title('Kurs Darstellung')
            editor.geometry('500x500')

            # Methode zum Abschließen eines Kurses
            def finish_course():
                # Sicherstellen, dass die Eingabe auch wirklich eine sinnvolle Note ist
                if not(c_grade.get().isdigit() and 1 <= int(c_grade.get()) <= 6):
                    # Andernfalls Nutzer über inkorrekte Eingabe informieren
                    messagebox.showinfo("Eingabe inkorrekt", "Bitte gültige Note eingeben")
                    return

                # Datenbank öffnen
                conn = sqlite3.connect('study_database.db')
                # Cursor erstellen
                cursor = conn.cursor()

                # Kurs aus den aktuellen Kursen entfernen
                cursor.execute("DELETE FROM courses WHERE course_name = ?", (course_details[0],))

                # Kurs in die abgeschlossenen Kurse einpflegen
                cursor.execute("INSERT INTO finished_courses VALUES (:course_name, :course_description, :course_grade, :course_examination)",
                               {
                                   'course_name': course_details[0],
                                   'course_description': course_details[1],
                                   'course_grade': c_grade.get(),
                                   'course_examination': course_details[3],
                               })

                # Entferne Button vom Kurs
                removeCourseButton(self, course_details[0])

                # Änderungen speichern
                conn.commit()
                # Schließen der Verbindung
                conn.close()

                # Methode zur Aktualisierung des Fortschritts ausführen
                update_progress(self)
                # Methode zur Aktualisierung des Durchschnitts ausführen
                update_average(self)
                # Methode zur Aktualisierung des Semesters ausführen
                update_semester(self)

                # Fenster schließen
                editor.destroy()


            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Alle Daten extrahieren für die Eintragung in den Textfeldern
            cursor.execute("SELECT * FROM courses WHERE course_name = ?", (course_name,))
            course_details = cursor.fetchone()

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

            # Kursname Label
            c_name_label = Label(editor, text="Kursname: ")
            c_name_label.grid(row=0, column=0)
            # Der Kursname wird hier ausgegeben
            c_name = Label(editor, text=course_details[0])
            c_name.grid(row=0, column=1, padx=20)

            # Kursbeschreibung Label
            c_description_label = Label(editor, text="Kursbeschreibung: ")
            c_description_label.grid(row=1, column=0)
            # Die Kursbeschreibung wird hier ausgegeben
            c_description = Label(editor, text=course_details[1])
            c_description.grid(row=1, column=1, padx=20)

            # Prüfungsleistung Label
            c_description_label = Label(editor, text="Prüfungsleistung: ")
            c_description_label.grid(row=2, column=0)
            # Typ der Prüfungsleistung wird hier ausgegeben (Klausur oder Projekt)
            c_description = Label(editor, text=course_details[3])
            c_description.grid(row=2, column=1, padx=20)

            # Kursnote Label
            c_grade_label = Label(editor, text="Kursnote")
            c_grade_label.grid(row=3, column=0)
            # Eingabefeld für die Kursnote
            c_grade = Entry(editor, width=30)
            c_grade.grid(row=3, column=1, padx=20)

            # Button zum Abschließen des Kurses (ruft die finish_course Methode auf)
            submit_button = Button(editor, text="Kurs abschließen", command=finish_course )
            submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        # Methode die einen neuen Button erstellt (für den zu erstellenden Kurs)
        def create_course_button(course_name):
            self.button_count += 1
            # Erstelle einen neuen Button für den hinzugefügten Kurs
            newButton = Button(courseFrame, text=course_name, command=lambda: openCoursePage(self, course_name), fg="black", bg="grey", height=15, width=40)
            # Positionierung (Reihe und Spalte) des Buttons im grid mithilfe des button_count berechnen
            row = (self.button_count - 1) // 4
            column = (self.button_count - 1) % 4
            self.course_buttons[course_name] = newButton
            newButton.grid(row=row, column=column, padx=50, pady=50)

        # Methode, die alle Noten in einem neuen Fenster darstellt
        def display_grades(self):
            # Einstellungen vom Fenster
            editor = Toplevel()
            editor.title('Noten')

            # Kurse Label
            courseFrame = LabelFrame(editor, text="Kurse", padx=0, pady=0)
            courseFrame.pack()
            # Textfeld für Liste der Noten
            finished_courses = Label(courseFrame, text="")
            finished_courses.grid(row=1, column=1, pady=30, padx=30)

            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Alle Daten aus finished courses auswählen
            cursor.execute("SELECT *, oid FROM finished_courses")
            records = cursor.fetchall()

            # String mit allen Einträgen erstellen
            print_records = ''
            if records:
                for record in records:
                    # Namen, Note und Typ der Prüfungsleistung für jeden einzelnen Eintrag erhalten
                    print_records += str(record[0] + ", Note: " + str(record[2]) + " (" + str(record[3])) + ")\n" + "\n"
            else:
                print_records = "Es wurden noch keine Kurse abgeschlossen"

            # Textfeld für Liste der Noten aktualisieren
            finished_courses.configure(text=print_records)

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

        # Methoden für Erstellung eines neuen Kurses
        def addNewCourse(self):
            if (self.button_count > 7):
                # Warnung, wenn zu viele aktive Kurse vorhanden sind
                messagebox.showinfo("Übernimm dich nicht", "Bitte schließe erst mal Kurse ab, bevor du weitere startest!")
                return

            # Einstellungen vom Fenster
            editor = Toplevel()
            editor.title('Kurs hinzufügen')
            editor.geometry('500x500')

            # Methode, die aufgerufen wird, wenn Nutzer die Eingaben bestätigt und den Kurs erstellt
            def submit():
                print(exam_type.get())
                examination = None
                if exam_type.get() == "Klausur":
                    # Die Dauer wird der Einfachheit halber auf 90 Minuten festgelegt für alle Klausuren
                    # Die Note existiert noch nicht
                    examination = Exam(None, 90)
                elif exam_type.get() == "Projekt":
                    # Die Deadline wird der Einfachheit halber auf 2025 festgelegt für alle Projekte
                    # Die Note existiert noch nicht
                    examination = Project(None, "31.12.2025")

                # Objekt der Klasse Kurs mit Nutzereingaben erstellen
                course = Course(c_name.get(), c_description.get(), examination)

                #Datenbank öffnen
                conn = sqlite3.connect('study_database.db')
                #Cursor erstellen
                cursor = conn.cursor()

                # Daten in die Datenbank einpflegen.
                # Der Einfachheit halber wurde dem Nutzer nicht erlaubt spezifische Angaben zur Klausur oder Projekt zu tätigen (bspw. die duration oder deadline), da sonst eine weitere Tabelle für die Prüfungsleistungen notwendig wäre
                # und die beiden Tabellen über einen Primary Key verbunden werden müssten
                cursor.execute("INSERT INTO courses VALUES (:course_name, :course_description, :course_grade, :course_examination)",
                               {
                                   'course_name': course.name,
                                   'course_description': course.description,
                                   'course_grade': None,
                                   'course_examination': examination.name
                               })

                # Methode zum Erstellen eines Buttons für den Kurs aufrufen
                create_course_button(course.name)

                #Änderungen speichern
                conn.commit()
                # Schließen der Verbindung
                conn.close()

                # Fenster schließen
                editor.destroy()

            # Methode zum Darstellen aller aktiven Kurse
            def display_active_coures():
                # Datenbank öffnen
                conn = sqlite3.connect('study_database.db')
                # Cursor erstellen
                cursor = conn.cursor()

                #Alle Daten auswählen
                cursor.execute("SELECT *, oid FROM courses")
                records = cursor.fetchall()

                # String mit allen Einträgen erstellen
                print_records = ''
                if records:
                    for record in records:
                        # Nur den Namen des Kurses verwenden
                        print_records += str(record[0]) + "\n"

                #Textfeld für Liste der aktiven Kurse aktualisieren
                course_list.configure(text=print_records)

                # Änderungen speichern
                conn.commit()
                # Schließen der Verbindung
                conn.close()

            # Kursname Label
            c_name_label = Label(editor, text="Kursname")
            c_name_label.grid(row=0, column=0)
            # Eingabefeld für den Kursnamen
            c_name = Entry(editor, width=30)
            c_name.grid(row=0, column=1, padx=20)

            # Kursbeschreibung Label
            c_description_label = Label(editor, text="Kursbeschreibung")
            c_description_label.grid(row=1, column=0)
            # Eingabefeld für die Kursbeschreibung
            c_description = Entry(editor, width=30)
            c_description.grid(row=1, column=1, padx=20)

            # Festlegung von Klausur als Standard Prüfungsleistung
            exam_type = StringVar(value="Klausur")
            # Radiobutton ermöglichen Nutzer die Auswahl der Prüfungsleistung (zwischen Klausur und Projekt wählbar)
            Radiobutton(editor, text="Klausur", variable=exam_type, value="Klausur", command = lambda : print(exam_type.get())).grid(row=3, column=0)
            Radiobutton(editor, text="Projekt", variable=exam_type, value="Projekt", command = lambda : print(exam_type.get())).grid(row=3,column=1)

            # Button zum Speichern
            submit_button = Button(editor, text="Kurs speichern", command=submit)
            submit_button.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

            #Über diesen Button sollen die Einträge in der Datenbank angezeigt werden
            query_button = Button(editor, text="Datenbankeinträge anzeigen", command=display_active_coures)
            query_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10)

            # Label für die Ausgabe der Kurse
            course_list = Label(editor, text="")
            course_list.grid(row=6, column=0, columnspan=2, pady=10, padx=10)


        # Methode für das Öffnen der Unterseiten
        def subpage_click(self):
            # Dashboard schließen
            self.pack_forget()
            # Unterseite verpacken
            self.controller.subpage.pack(fill="both", expand=True)

        # Methode für Berechnung der Durchschnittsnote
        def calculate_average_grade(self):
            averageGrade = 0

            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Anzahl der abgeschlossenen Kurse erhalten
            cursor.execute("SELECT COUNT(*) FROM finished_courses")
            record_count = cursor.fetchone()[0]

            # Alle Noten erhalten
            cursor.execute("SELECT *, oid FROM finished_courses")
            records = cursor.fetchall()

            grade_sum = 0
            averageGrade = 0
            # Berechnung basierend auf Einträge der Noten in der Datenbank
            if records:
                for record in records:
                    grade_sum += record[2]
                averageGrade = grade_sum / record_count

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

            return averageGrade

        # Methode für Berechnung des Fortschritts
        def calculate_progress(self):

            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Anzahl der abgeschlossenen Kurse erhalten
            cursor.execute("SELECT COUNT(*) FROM finished_courses")
            record_count = cursor.fetchone()[0]

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

            # Wir gehen davon aus, dass es 6 Semester sind mit je 6 Kursen und somit insgesamt 36 Kurse
            progress_percentage = (record_count / 36) * 100

            return progress_percentage

        # Methode für Aktualisierung des Sliders mit dem Fortschritt
        def update_progress(self):
            horizontal_slider.set(calculate_progress(self))

        # Methode für Aktualisierung des Labels mit der Durchschnittsnote
        def update_average(self):
            average_display_text.configure(text=str(calculate_average_grade(self)))

        # Methode für Berechnung des Semesters (basierend auf Anzahl abgeschlossener Kurse)
        def update_semester(self):
            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Alle Daten auswählen
            cursor.execute("SELECT * FROM finished_courses")
            records = cursor.fetchall()

            # Je 6 Kurse pro Semester
            if records.__len__() > 6:
                self.semester = 2
            elif records.__len__() > 12:
                self.semester = 3
            elif records.__len__() > 18:
                self.semester = 4
            elif records.__len__() > 24:
                self.semester = 5
            elif records.__len__() > 30:
                self.semester = 6
            self.semester_information.config(text=f"{self.semester}.Semester")

            # Änderungen speichern und Verbindung schließen
            conn.close()


        # Angaben des Studenten
        student_frame = LabelFrame(self, text="Informationen", padx=0, pady=10)
        student_frame.pack(fill='x', expand=False)
        student_frame.pack(padx=10, pady=10)
        self.student_information = Label(student_frame, text="Herzlich willkommen")
        self.student_information.pack()
        self.semester_information = Label(student_frame, text=f"{self.semester}.Semester")
        self.semester_information.pack()

        # Erstelle ein Frame für die Darstellung der Navigationselemente
        navigationFrame = LabelFrame(self, text="Navigationsleiste", padx=0, pady=20)
        navigationFrame.pack(fill='x', expand=False)
        navigationFrame.pack(padx=10, pady=10)

        # Erstelle Buttons für das Öffnen der Unterseiten
        subpageButton1 = Button(navigationFrame, text="Dashboard", fg="black", bg="grey",padx=50, pady=20, height=1, width=15)
        subpageButton2 = Button(navigationFrame, text="Unterseite 1", command=lambda: subpage_click(self), fg="black", bg="grey",padx=50, pady=20, height=1, width=15)
        subpageButton3 = Button(navigationFrame, text="Unterseite 2", command=lambda: subpage_click(self), fg="black", bg="grey",padx=50, pady=20, height=1, width=15)
        subpageButton4 = Button(navigationFrame, text="Unterseite 3", command=lambda: subpage_click(self), fg="black", bg="grey",padx=50, pady=20, height=1, width=15)
        subpageButton5 = Button(navigationFrame, text="Unterseite 4", command=lambda: subpage_click(self), fg="black", bg="grey",padx=50, pady=20, height=1, width=15)

        # Positionierung der Buttons für die Unterseite
        subpageButton1.grid(row=0, column=0, padx=50)
        subpageButton2.grid(row=0, column=1, padx=50)
        subpageButton3.grid(row=0, column=2, padx=50)
        subpageButton4.grid(row=0, column=3, padx=50)
        subpageButton5.grid(row=0, column=4, padx=50)

        # Erstelle ein Frame für die Darstellung der Kurse
        courseFrame = LabelFrame(self, text="Kurse", padx=0, pady=20)
        courseFrame.pack(fill='x', expand=False)
        courseFrame.pack(padx=10, pady=10)

        # Button für das Hinzufügen von Kursen
        addCourse_button = Button(courseFrame, text="Kurs hinzufügen", command=lambda: addNewCourse(self), fg="black",bg="grey", height=15, width=40)
        # Positionierung des Buttons
        addCourse_button.grid(row=0, column=0, padx=50, pady=50)


        # Wenn Einträge in der Datenbank über aktuelle Kurse bestehen, so müssen diese ebenfalls hinzugefügt werden
        # Datenbank öffnen
        conn = sqlite3.connect('study_database.db')
        # Cursor erstellen
        cursor = conn.cursor()

        # Alle Daten auswählen
        cursor.execute("SELECT * FROM courses")
        records = cursor.fetchall()
        if records:
            for record in records:
                course_name = record[0]
                # Für jeden Kurs einen Button erstellen lassen
                create_course_button(course_name)

        # Änderungen speichern und Verbindung schließen
        conn.close()

        # Erstelle ein Frame für die Darstellung der Ziele (Studiumsdauer und Notendurchschnitt)
        goals_frame = LabelFrame(self, text="Ziele", padx=0, pady=20)
        goals_frame.pack(fill='x', expand=False)
        goals_frame.pack(padx=10, pady=10)

        # Label für den Fortschritt
        progress_text = Label(goals_frame, text="Prozentualer Fortschritt: ", padx=40, pady=10)
        # Slider, der prozentualen Fortschritt darstellen soll
        horizontal_slider = Scale(goals_frame, from_=0, to=100, orient=HORIZONTAL)

        # Label für den Notendurchschnitt
        average_text = Label(goals_frame, text="Notendurchschnitt: ", padx=40, pady=10)
        # Note wird in dieses Label eingetragen
        average_display_text = Label(goals_frame, text="", padx=40, pady=20)

        # Positionierungen der Labels im Grid
        progress_text.grid(row=0, column=0, padx=212)
        horizontal_slider.grid(row=1, column=0, padx=212)
        average_text.grid(row=0, column=1, padx=212)
        average_display_text.grid(row=1, column=1, padx=212)

        # Ein Button für die Anzeige der abeschlossenen Kurse und deren Noten
        add_course_button = Button(goals_frame, text="Bisherige Noten anzeigen", command=lambda: display_grades(self), fg="black", bg="grey", padx=40, pady=20)
        add_course_button.grid(row=0, column=2, rowspan=2, padx=50, pady=50)

        # Zu Beginn müssen Fortschritt, Durchschnittsnote und Semester aktualisiert werden
        update_progress(self)
        update_average(self)
        update_semester(self)

    # Methode die von der Login-Klasse aufgerufen wird, um Dashboard mit Information über den Studenten zu initialisieren
    def initialize(self, student, study):
        # Hier wird der Text mit dem Namen vom Studenten und dem Studiengang ausgegeben
        self.student_information.config(text=f"Herzlich willkommen, {student.surname} {student.lastname}! \n Studiengang: {study}")