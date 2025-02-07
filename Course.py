from Examination import Examination

# Klasse Course (Kurs) erstellen
class Course:
    def __init__(self, name, description, examination):
        # Sicherstellen, dass es sich bei examination auch wirklich um eine Instanz der Klasse Examination handelt
        if not isinstance(examination, Examination):
            # Andernfalls Fehler ausgeben und Nutzer darauf hinweisen
            raise ValueError("Bei examination muss es sich um eine Instanz von Examination handeln")
        # Kurs besitzt folgende Variablen
        self.name = name
        self.description = description
        self.examination = examination