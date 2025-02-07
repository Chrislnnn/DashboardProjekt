class Student:
    # Die Klasse Student hat einen id_counter (Zähler).
    # Damit kann sichergestellt werden, dass jeder Student eine einzigartige ID erhält (wichtig für Eintragung in die Datenbank)
    id_counter = 1
    def __init__(self, surname_input, lastname_input, stored_id=None):
        # Jeder Student muss mit einem Vor- und Nachnamen erstellt werden
        self.surname = surname_input
        self.lastname = lastname_input
        # ID wird erstellt, wenn nicht bereits eine existiert.
        if stored_id is None:
            self.id = Student.id_counter
            Student.id_counter += 1
        # Eine ID liegt bereits vor, wenn der Eintrag vom Student aus der Datenbank entnommen wird
        else:
            self.id = stored_id