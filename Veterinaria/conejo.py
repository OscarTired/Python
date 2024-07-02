from animal import Animal

class Conejo(Animal):
    def __init__(self, nombre, edad, peso, dieta, tipo_atencion, altura_salto):
        super().__init__(nombre, edad, peso, dieta, tipo_atencion)
        self._altura_salto = altura_salto
        self._tipo_atencion = tipo_atencion

    def realizar_atencion(self):
        return f"{self.nombre} - Atención de Conejo: Altura de Salto -> {self._altura_salto}"
