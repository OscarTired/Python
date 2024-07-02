from animal import Animal

class Gato(Animal):
    def __init__(self, nombre, edad, peso, dieta, tipo_atencion, cantidad_maullidos):
        super().__init__(nombre, edad, peso, dieta, tipo_atencion)
        self._cantidad_maullidos = cantidad_maullidos
        self._tipo_atencion = tipo_atencion

    def realizar_atencion(self):
        return f"{self.nombre} - Atención de Gato: Maullidos -> {self._cantidad_maullidos}"
