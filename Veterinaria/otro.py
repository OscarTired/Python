from animal import Animal

class Otro(Animal):
    def __init__(self, nombre, edad, peso, dieta, tipo_atencion, extra_attr, tipo):
        super().__init__(nombre, edad, peso, dieta, tipo_atencion)
        self._tipo = tipo
        self._extra_attr = extra_attr
        self._tipo_atencion = tipo_atencion

    def realizar_atencion(self):
        return f"{self.nombre} - Atención de {self._tipo}: Atributo Extra -> {self._extra_attr}"
