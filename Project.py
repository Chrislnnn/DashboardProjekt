from Examination import Examination
# Unterklasse von Examination (Prüfungsleistung) erstellen
class Project(Examination):
    def __init__(self, grade, deadline):
        # Die Variable grade (Note) wird von der Klasse Examination geerbt
        super().__init__(grade)
        # Das Projekt soll über die Note hinaus noch eine deadline besitzen und den festgelegten Namen Projekt
        self.deadline = deadline
        self.name = "Projekt"