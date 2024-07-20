import os
import csv
import random
from faker import Faker ##pip install Faker
from datetime import datetime

# Importación de módulos:
# os: Proporciona una forma de usar funcionalidades del sistema operativo, en este caso, para obtener el directorio de trabajo actual.
# csv: Permite trabajar con archivos CSV (Comma-Separated Values), para escribir los datos generados en un archivo.
# random: Permite generar números aleatorios, necesarios para generar datos aleatorios.
# Faker: Biblioteca que permite generar datos falsos, como nombres, fechas y otras informaciones aleatorias.
# datetime: Proporciona clases para manipular fechas y horas.

print("Iniciando script...")

# Imprimir el directorio de trabajo actual
current_directory = os.getcwd()
print(f"Directorio de trabajo actual: {current_directory}")
# Verificar el directorio de trabajo actual:
# os.getcwd(): Obtiene el directorio de trabajo actual.
# print(f"Directorio de trabajo actual: {current_directory}"): 
# Imprime el directorio de trabajo actual para asegurar que el script está en el lugar correcto y que tiene permisos para escribir archivos en ese directorio.

fake = Faker()
# Inicialización de Faker: Crea una instancia de Faker para generar datos falsos.

# Generar datos aleatorios CSV
data = []
rows = random.randint(10000, 15000)
print(f"Generando {rows} filas de datos...")
# Preparación para generar datos:
# data = []: Inicializa una lista vacía para almacenar los datos generados.
# rows = random.randint(10, 20): Genera un número aleatorio de filas entre 10 y 20 para decidir cuántas filas de datos se generarán.
# print(f"Generando {rows} filas de datos..."): Imprime la cantidad de filas que se van a generar.
for _ in range(rows):
    invoice_id = fake.random_int(min=1, max=1000)
    start_date = datetime.strptime('2023-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    purchase_date = fake.date_between(start_date=start_date, end_date=end_date)
    time = fake.time(pattern='%H:%M')
    while not (time >= '09:00' and time <= '21:00'):
        time = fake.time(pattern='%H:%M')
    gender = random.choice(['Male', 'Female'])
    invoice_amount = round(random.uniform(10, 1000), 2)
    payment_method = random.choice(['Credit Card', 'Cash', 'Yape'])
    city = random.choice(['Lima', 'Arequipa', 'La Libertad', 'Tacna', 'Trujillo'])

    data.append([invoice_id, purchase_date, time, gender, city, payment_method, invoice_amount])
# Generación de datos aleatorios:
# Se ejecuta un bucle para generar una cantidad de filas de datos (definida por rows).
# invoice_id = fake.random_int(min=1, max=1000): Genera un ID de factura aleatorio entre 1 y 1000.
# start_date y end_date: Define el rango de fechas.
# purchase_date = fake.date_between(start_date=start_date, end_date=end_date): Genera una fecha de compra aleatoria dentro del rango.
# time = fake.time(pattern='%H:%M'): Genera una hora aleatoria.
# while not (time >= '09:00' and time <= '21:00'): Asegura que la hora está entre las 9:00 y las 21:00.
# gender = random.choice(['Male', 'Female']): Selecciona aleatoriamente un género.
# invoice_amount = round(random.uniform(10, 1000), 2): Genera un monto de factura aleatorio entre 10 y 1000, redondeado a dos decimales.
# payment_method = random.choice(['Credit Card', 'Cash', 'PayPal']): Selecciona aleatoriamente un método de pago.
# city = random.choice(['Torremolinos', 'Fuengirola', 'Malaga', 'Marbella', 'Benalmadena']): Selecciona aleatoriamente una ciudad.
# data.append([invoice_id, purchase_date, time, gender, city, payment_method, invoice_amount]): Agrega la fila de datos generada a la lista data.

print("Datos generados:")
for row in data:
    print(row)
# Depuración de datos: Imprime todas las filas de datos generadas para verificar que los datos se están generando correctamente.

# Escribir datos en el CSV
filename = 'data_2023.csv'
try:
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Invoice ID', 'Purchase Date', 'Time', 'Gender', 'City', 'Payment Method', 'Invoice Amount'])
        writer.writerows(data)
    print(f"Archivo CSV '{filename}' creado exitosamente en el directorio {current_directory}.")
except Exception as e:
    print(f"Error al crear el archivo CSV: {e}")

# Escribir datos en el archivo CSV:
# filename = 'data_2024.csv': Define el nombre del archivo CSV a crear.
# try...except: Maneja posibles errores durante la escritura del archivo.
# with open(filename, 'w', newline='') as file: Abre el archivo para escritura. Si el archivo no existe, lo crea; si existe, lo sobrescribe.
# writer = csv.writer(file): Crea un objeto escritor de CSV.
# writer.writerow(['Invoice ID', 'Purchase Date', 'Time', 'Gender', 'City', 'Payment Method', 'Invoice Amount']): Escribe la fila de encabezado en el archivo.
# writer.writerows(data): Escribe todas las filas de datos generadas en el archivo.
# print(f"Archivo CSV '{filename}' creado exitosamente en el directorio {current_directory}."): Confirma que el archivo CSV fue creado exitosamente.
# except Exception as e: Captura cualquier excepción que ocurra durante la escritura del archivo y imprime un mensaje de error.