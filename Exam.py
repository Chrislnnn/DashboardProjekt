from Examination import Examination
# Unterklasse von Examination (Prüfungsleistung) erstellen
class Exam(Examination):
    def __init__(self, grade, duration):
        # Die Variable grade (Note) wird von der Klasse Examination geerbt
        super().__init__(grade)
        # Die Klausur soll über die Note hinaus noch eine duration besitzen und den festgelegten Namen Klausur
        self.duration = duration
        self.name = "Klausur"