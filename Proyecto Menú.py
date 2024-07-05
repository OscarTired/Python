#NO SE OLVIDE QUE LE PUSE MI BARRA DE CARGA ORIGINAL, SUFRI PARA QUE QUEDARA BIEN, SOLO LE FALATABA UN INPUT :(
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[39m'
import os

salida1=False
general=0;global2=0;global3=0;global4=0
while not salida1:
    os.system('cls')
    print(RED+'\t|================================|')
    print(YELLOW+'\t|    RESTAURANT VOLIBEAR S.A.    |')
    print('\t|            MENÚ                |')
    print('\t|================================|')
    print('\t| A |Desayuno                    |')
    print('\t| B |Almuerzo                    |')
    print('\t| C |Cena                        |')
    print('\t| S |===========SALIR============|')
    print(RED+'\t|================================|')
    print()
    while True:
        alternativa1=input(RESET+'Ingrese Opción (A-S):')
        alternativa1=alternativa1.upper()
        if alternativa1>='A' and alternativa1<='S':break
        #uso de igual forma el break para cortar el bucle
    match alternativa1:
        #USAMOS EL MATCH PARA SIMPLIFICAR LOS ELIF
        case 'A':
            salida2=False
            while not salida2:
                print(CYAN+'\t|     |    DESAYUNO     |       |')
                print('\t|===============================|')
                print('\t| A |Café               |s/.2.50|')
                print('\t| B |Café con Leche     |s/.3.00|')
                print('\t| C |Quinua             |s/.2.00|')
                print('\t| D |Manzanilla/Anís    |s/.1.50|')
                print('\t| E |Pan con Pollo      |s/.2.00|')
                print('\t| F |Pan con Tortilla   |s/.2.00|')
                print('\t| G |Pan con Atún       |s/.2.00|')
                print('\t| S |==========SALIR============|')
                print('\t|===============================|')
                print()
                print(RESET+f'\tSubtotal1 = {global2:.2f}')
                while True:
                    alternativa2=input('\tIngrese Opción (A-S):')
                    alternativa2=alternativa2.upper()
                    if alternativa1>='A' and alternativa1<='H':break
                match alternativa2:
                    case 'A':global2=global2+2.50
                    case 'B':global2=global2+3.00
                    case 'C':global2=global2+2.00
                    case 'D':global2=global2+1.50
                    case 'E':global2=global2+2.00
                    case 'F':global2=global2+2.00
                    case 'G':global2=global2+2.00
                if alternativa2=='S':salida2=True;break
        case 'B':
            salida3=False
            while not salida3:
                print(BLUE+'\t|      |    ALMUERZO     |     |')
                print('\t|==============================|')
                print('\t| A |Pollo al Horno    |s/.7.50|')
                print('\t| B |Seco de Carne     |s/.7.50|')
                print('\t| C |Caldo de Gallina  |s/.6.50|')
                print('\t| D |Bistek a lo Pobre |s/.8.50|')
                print('\t| E |Lomo Saltado      |s/.8.50|')
                print('\t| F |Chicha Morada     |s/.5.00|')
                print('\t| G |Limonada          |s/.4.50|')
                print('\t| S |===========SALIR==========|')
                print('\t|==============================|')
                print()
                print(RESET+f'\tSubtotal = {global3:.2f}')
                while True:
                    alternativa3=input('\tIngrese opción (A-S):')
                    alternativa3=alternativa3.upper()
                    if alternativa3>='A' and alternativa3<='S':break
                match alternativa3:
                    case 'A':global3=global3+7.5
                    case 'B':global3=global3+7.5
                    case 'C':global3=global3+6.5
                    case 'D':global3=global3+8.5
                    case 'E':global3=global3+8.5
                    case 'F':global3=global3+5.0
                    case 'G':global3=global3+4.5
                if alternativa3=='S':alternativa3=True;break
        case 'C':
            salida4=False
            while not salida4:
                print(MAGENTA+'\t|      |     CENA      |       |')
                print('\t|==============================|')
                print('\t| A |Ensalada Hawaiana |s/.6.50|')
                print('\t| B |Pie de Limón      |s/.5.00|')
                print('\t| C |Caldo de Pollo    |s/.5.00|')
                print('\t| D |Frappccino        |s/.7.50|')
                print('\t| E |Queque de Naranja |s/.2.50|')
                print('\t| F |Chocolate         |s/.2.00|')
                print('\t| S |==========SALIR===========|')
                print('\t|==============================|')
                print()
                print(RESET+f'\tSubtotal = {global4:.2f}')
                while True:
                    alternativa4=input('\tIngrese opción (A-S):')
                    alternativa4=alternativa4.upper()
                    if alternativa4>='A' and alternativa4<='S':break
                match alternativa4:
                    case 'A':global4 =global4+6.5
                    case 'B':global4 =global4+5.0
                    case 'C':global4 =global4+5.0
                    case 'D':global4 =global4+7.5
                    case 'E':global4 =global4+2.5
                    case 'F':global4 =global4+2.0
                if alternativa4=='S':alternativa4=True;break
    if alternativa1 =='S':salida1=True
import time

limite = 40


def barraProgreso(segmento, total, longitud):
    porcentaje = segmento / total
    completado = int(porcentaje * longitud)
    restante = longitud - completado
    barra =YELLOW+ f"[{'©' * completado}{'~' * restante}{porcentaje: .2%}]"
    return barra


for i in range(limite + 1):
    time.sleep(0.05)
    print(barraProgreso(i, limite, 40), end="\r")

general=global2+global3+global4
igv=general*0.18
importe=general+igv
print(GREEN+'\n')
print('\t|================================|')
print('\t|        BOLETA DE VENTAS        |')
print('\t|================================|')
print(f'\t| Subtotal       : {general:.2f}         |')
print(f'\t| Igv (18%)      : {igv:.2f}          |')
print(f'\t| Pago Total     : {importe:.2f}         |')
print('\t|================================|')
print('\t|  Gracias por su Preferencia    |')
print('\t|================================|')
print(input())























