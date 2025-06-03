import tkinter
from tkinter import *
import sqlite3

# Klasse Subpage (Unterseite) wird erstellt
class Subpage(tkinter.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Methode, die aufgerufen wird, wenn der Nutzer auf den Dashboard-Button klickt
        def main_page_click(self):
            self.pack_forget()
            self.controller.dashboard.pack(fill="both", expand=True)

        # Methode, die aufgerufen wird, wenn der Nutzer auf einen Unterseiten-Button klickt
        def subpage_click(self):
            navigate_to_subpage_label = Label(self, text="Dieser Button könnte an eine andere Unterseite weiterleiten!")
            navigate_to_subpage_label.pack()

        # Methode, die die aktiven und abgeschlossen Kurse aus den Tabellen in der Datenbank ausgeben soll
        def query(self):
            # Datenbank öffnen
            conn = sqlite3.connect('study_database.db')
            # Cursor erstellen
            cursor = conn.cursor()

            # Alle Daten aus courses auswählen
            cursor.execute("SELECT *, oid FROM courses")
            records = cursor.fetchall()

            # Alle Daten aus courses ausgeben
            print_records = ''
            for record in records:
                print_records += str(record[0]) + "\n"

            # Erstellten String im Label ausgeben
            current_courses.configure(text=print_records)

            # Alle Daten aus finished courses auswählen
            cursor.execute("SELECT *, oid FROM finished_courses")
            records = cursor.fetchall()

            # Alle Daten aus finished courses ausgeben
            print_records = ''
            for record in records:
                print_records += str(record[0] + ", Note: " + str(record[2])) + "\n"

            # Erstellten String im Label ausgeben
            finished_courses.configure(text=print_records)

            # Änderungen speichern
            conn.commit()
            # Schließen der Verbindung
            conn.close()

        def update(self):
            query(self)

        # Frame für die Darstellung der Navigationselemente erstellen
        navigation_frame = LabelFrame(self, text="Navigationsleiste", padx=0, pady=50)
        navigation_frame.pack(padx=10, pady=10)

        # Buttons für das Öffnen der Unterseiten erstellen
        subpage_button_1 = Button(navigation_frame, text="Dashboard", command=lambda: main_page_click(self), fg="black", bg="grey",padx=40, pady=20)
        subpage_button_2 = Button(navigation_frame, text="Unterseite 1", command=lambda: subpage_click(self), fg="black", bg="grey",padx=40, pady=20)
        subpage_button_3 = Button(navigation_frame, text="Unterseite 2", command=lambda: subpage_click(self), fg="black", bg="grey",padx=40, pady=20)
        subpage_button_4 = Button(navigation_frame, text="Unterseite 3", command=lambda: subpage_click(self), fg="black", bg="grey",padx=40, pady=20)
        subpage_button_5 = Button(navigation_frame, text="Unterseite 4", command=lambda: subpage_click(self), fg="black", bg="grey",padx=40, pady=20)

        # Positionierung der Buttons für die Unterseite
        subpage_button_1.grid(row=0, column=0, padx=50)
        subpage_button_2.grid(row=0, column=1, padx=50)
        subpage_button_3.grid(row=0, column=2, padx=50)
        subpage_button_4.grid(row=0, column=3, padx=50)
        subpage_button_5.grid(row=0, column=4, padx=50)

        # Erstelle ein Frame für die Darstellung der aktuellen Kurse und der abgeschlossenen Kurse
        course_frame = LabelFrame(self, text="Kurse", padx=0, pady=50)
        course_frame.pack(padx=10, pady=10)

        # Label für die aktiven Kurse (Überschrift)
        current_courses_label = Label(course_frame, text="Aktuelle Kurse")
        current_courses_label.grid(row=0, column=0, pady=10, padx=10)
        # Label für die aktiven Kurse (Für die Ausgabe der Liste an Kursen)
        current_courses = Label(course_frame, text="")
        current_courses.grid(row=1, column=0, pady=10, padx=10)

        # Label für die abgeschlossenen Kurse (Überschrift)
        finished_courses_label = Label(course_frame, text="Abgeschlossene Kurse")
        finished_courses_label.grid(row=0, column=1, pady=10, padx=10)
        # Label für die abgeschlossenen Kurse (Für die Ausgabe der Liste an Kursen)
        finished_courses = Label(course_frame, text="")
        finished_courses.grid(row=1, column=1, pady=10, padx=10)

        # Hinweis
        info_text = Label(course_frame, text="Die Liste wird erst nach einem Neustart aktualisiert!")
        info_text.grid(row=2, columnspan=2, pady=10, padx=10)

        # Alle aktiven und abgeschlossenen Kurse aus der Datenbank ausgeben
        query(self)