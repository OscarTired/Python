from animal import Animal
from gato import Gato
from perro import Perro
from conejo import Conejo
from loro import Loro
from otro import Otro

class MascotaFactory:
    @staticmethod
    def create_mascota(tipo, nombre, edad, peso, dieta, tipo_atencion, extra_attr):
        if tipo == "Gato":
            return Gato(nombre, edad, peso, dieta, tipo_atencion, extra_attr)
        elif tipo == "Perro":
            return Perro(nombre, edad, peso, dieta, tipo_atencion, extra_attr)
        elif tipo == "Conejo":
            return Conejo(nombre, edad, peso, dieta, tipo_atencion, extra_attr)
        elif tipo == "Loro":
            return Loro(nombre, edad, peso, dieta, tipo_atencion, extra_attr)
        else:
            return Otro(nombre, edad, peso, dieta, tipo_atencion, extra_attr, tipo)
