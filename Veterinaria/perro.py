from animal import Animal

class Perro(Animal):
    def __init__(self, nombre, edad, peso, dieta, tipo_atencion, cantidad_ladridos):
        super().__init__(nombre, edad, peso, dieta, tipo_atencion)
        self._cantidad_ladridos = cantidad_ladridos
        self._tipo_atencion = tipo_atencion

    def realizar_atencion(self):
        return f"{self.nombre} - Atención de Perro: Ladridos -> {self._cantidad_ladridos}"
