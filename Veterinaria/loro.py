from animal import Animal

class Loro(Animal):
    def __init__(self, nombre, edad, peso, dieta, tipo_atencion, diametro_alas):
        super().__init__(nombre, edad, peso, dieta, tipo_atencion)
        self._diametro_alas = diametro_alas
        self._tipo_atencion = tipo_atencion

    def realizar_atencion(self):
        return f"{self.nombre} - Atención de Loro: Diámetro de Alas -> {self._diametro_alas}"
