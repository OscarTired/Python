#Clase base para representar una aerolinea 
class Aerolinea:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def reservar_asiento(self, vuelo, asiento):
        pass
    
#Clase derivada (Hija) que representa un vuelo de una aerolinea

class Vuelo(Aerolinea):
    def __init__(self, nombre, numero_vuelo, capacidad):
        super().__init__(nombre)
        self.numero_vuelo = numero_vuelo
        self.capacidad = capacidad
        self.asientos_disponibles = list(range(1, capacidad + 1))
        
    def reservar_asiento(self, asiento):
        if asiento in self.asientos_disponibles:
            self.asientos_disponibles.remove(asiento)
            print(f"Reserva confirmada en el vuelo {self.numero_vuelo}, asiento {asiento}.")
        else:
            print(f"El asiento {asiento} ya esta ocupado o no existe en el vuelo {self.numero_vuelo}.")
            
#Clase para representar a un pasajero
class Pasajero:
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        
    def hacer_reserva(self, vuelo, asiento):
        vuelo.reservar_asiento(asiento)
        
#EJEMPLO DE USO

#VUELO
vuelo = Vuelo("Vuelo de Prueba", "ABC123", 100)

#Pasajeros
pasajero1 = Pasajero("Jhon", "Doe")
pasajero2 = Pasajero("Jane", "Smith")
pasajero3 = Pasajero("Luis", "Garcia")

#Realizar reservas usando la instancia de Vuelo
pasajero1.hacer_reserva(vuelo, 1)
pasajero2.hacer_reserva(vuelo, 2)
pasajero2.hacer_reserva(vuelo, 1)