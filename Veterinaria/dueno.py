class Dueño:
    def __init__(self, nombres, apellidos, dni):
        self._nombres = nombres
        self._apellidos = apellidos
        self._dni = dni
        self._mascota = None

    def asignar_mascota(self, mascota):
        self._mascota = mascota
