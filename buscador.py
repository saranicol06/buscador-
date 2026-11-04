import math
import time 
#ARBOL
class NodoTrie:
    #representa una letra dentro de un camino de palabras
    __slots__ = ("hijos", "posiciones")  #atributos del arbol 

    def __init__(self): #constructor, se ejecuta cada vez que creamos un nodo4
     #crea un diccionario vacio  donde se gurada los nodos que estan conectados al nodo actual 
        self.hijos = {}
     #crea una lista vacia donde se guardan las posiciones donde aparecen las palabras que terminan en ese nodo
        self.posiciones =[]


def construir_trie(indice_simple):
     raiz = NodoTrie()

     for palabra_min, posiciones in indice_simple.items():
        nodo = raiz
        for letra in palabra_min:
            if letra not in nodo.hijos:
                 nodo.hijos[letra] = NodoTrie()
            nodo = nodo.hijos[letra]

        nodo.posiciones = posiciones 

     return raiz


def posiciones_con_prefijo(raiz, prefijo):
    nodo = raiz
    for letra in prefijo:
        nodo = nodo.hijos.get(letra)
        if nodo is None:
            return[]


    posiciones = []
    pila = [nodo]
    while pila:
        actual = pila.pop()
        posiciones.extend(actual.posiciones)
        pila.extend(actual.hijos.values())


    posiciones.sort()
    return posiciones
        

 

def cargar_archivo(ruta):
    # lista para guardar las palabras en orden
    palabras = []

    # diccionario para guardar las líneas de cada palabra
    apariciones = {}

    #diccionario que usamos para las busquedas que no distinguen por mayusculab  
    apariciones_simple = {}

    #lista para saber en que linea esta cada palabara para mostrar la primera y ultima coincidencia con su numero de linea
    lineas_palabras = []

    #diccionario con las posiciones de cada palabra (en minusculas), para el trie
    posiciones_simple = {}

    try:
        #abrimos el archivo en modo lectura
        with open(ruta, "r", encoding="utf-8") as archivo:

            # leemos el archivo línea por línea
            for numero_linea, linea in enumerate(archivo, start=1):

                #separamos la línea en palabras
                palabras_linea = linea.split()

                # revisamos cada palabra de la línea
                for palabra in palabras_linea:

                    # guardamos el índice antes de agregar la palabra
                    indice = len(palabras)

                    # guardamos la palabra en la lista
                    palabras.append(palabra)

                    # si la palabra no está en el diccionario, creamos una lista vacía para sus líneas
                    if palabra not in apariciones:
                        apariciones[palabra] = []

                    # guardamos la línea donde aparece
                    apariciones[palabra].append(numero_linea)

                    # convertimos la palabra a minúsculas
                    palabra_minuscula = palabra.lower()

                    if palabra_minuscula not in posiciones_simple:
                          posiciones_simple[palabra_minuscula] = []

                    posiciones_simple[palabra_minuscula].append(indice)

                    # si no existe, creamos su lista de líneas
                    if palabra_minuscula not in apariciones_simple:
                        apariciones_simple[palabra_minuscula] = []

                    # guardamos la línea donde aparece
                    apariciones_simple[palabra_minuscula].append(numero_linea)

                    #lista que guarda los numeros de linea donde aparecen 
                    lineas_palabras.append(numero_linea)

        # comprobamos si el archivo tenía palabras
        if len(palabras) == 0:
            print("El archivo está vacío.")
            return None
        
        raiz_trie = construir_trie(posiciones_simple)    

        # devolvemos las estructuras creadas incluyendo las convertidas a minusculas para tener ambas versiones del diccionario y tambien la lista con el numero de linea de las palabras
        return palabras, apariciones, apariciones_simple, lineas_palabras, raiz_trie

    except FileNotFoundError:
        print("Error: el archivo no existe.")

    except PermissionError:
        print("Error: no tienes permiso para leer el archivo.")

    except UnicodeDecodeError:
        print("Error: el archivo tiene un formato de texto no compatible.")

    except OSError:
        print("Error al intentar leer el archivo.")

    return None


def buscar_exacta(palabra, apariciones):

    inicio = time.perf_counter()

    #si la palabra existe como clave en el diccionario y guarda en lineas donde aparece la palabra
    if palabra in apariciones:
        lineas = apariciones[palabra]

        print("La palabra fue encontrada.")
        print("Cantidad de apariciones:", len(lineas)) #cantidad de veces que aparece la palabra
        print("Primera línea:", lineas[0])
        print("Última línea:", lineas[-1])

    else:
        print("La palabra no fue encontrada.")

    fin = time.perf_counter()

    tiempo = (fin - inicio) * 1000
    print("Tiempo de búsqueda:", tiempo, "milisegundos")

def buscar_simple(palabra, apariciones_simple):

    # convertimos lo que escribió el usuario a minúsculas
    palabra = palabra.lower()

    inicio = time.perf_counter()

    # revisamos si la palabra existe en el diccionario
    if palabra in apariciones_simple:

        lineas = apariciones_simple[palabra]

        print("La palabra fue encontrada.")
        print("Cantidad de apariciones:", len(lineas))
        print("Primera línea:", lineas[0])
        print("Última línea:", lineas[-1])

    else:
        print("La palabra no fue encontrada.")

    fin = time.perf_counter()

    tiempo = (fin - inicio) * 1000
    print("Tiempo de búsqueda:", tiempo, "milisegundos")


def buscar_prefijo(prefijo, raiz_trie, palabras, lineas_palabras):
    # evitamos prefijos vacíos (devolverían todas las palabras)
    if prefijo.strip() == "":
        print("Error: debe ingresar un prefijo.")
        return
    
    # convertimos el prefijo a minúsculas
    prefijo = prefijo.strip().lower()

    inicio = time.perf_counter()

    #buscamos en el trie las posicones de las palabras que comienzan con el prefijo indicado
    indices = posiciones_con_prefijo(raiz_trie, prefijo)

    if len(indices) > 0:

        #mostrar cada palabra y la linea en la que aparece
        for indice in indices:
            print(palabras[indice], "- Línea:", lineas_palabras[indice])



        # mostramos la primera coincidencia
        print("Primera palabra:", palabras[indices[0]])
        print("Primera línea:", lineas_palabras[indices[0]])

        # mostramos la última coincidencia
        print("Última palabra:", palabras[indices[-1]])
        print("Última línea:", lineas_palabras[indices[-1]])

    else:
        print("No se encontraron palabras con ese prefijo.")

    fin = time.perf_counter()

    tiempo = (fin - inicio) * 1000
    print("Tiempo de búsqueda:", tiempo, "milisegundos")


def mostrar_estadisticas(palabras):

    # contamos la cantidad total de palabras
    total = len(palabras)

    # comprobamos que existan palabras
    if total == 0:
        print("No hay palabras para mostrar estadísticas.")

    else:

        # obtenemos la primera palabra
        primera = palabras[0]

        # obtenemos la última palabra
        ultima = palabras[-1]

        # calculamos la posición central, math.ceil redondea un numero decimal hacia arriba del entero mas pequeno que ¿s amyor o igual a ese numerko
        posicion_central = math.ceil(total / 2)

        # convertimos la posición a un índice de Python
        indice_central = posicion_central - 1

        # obtenemos la palabra central
        central = palabras[indice_central]

        # mostramos los resultados
        print("ESTADÍSTICAS DEL ARCHIVO")
        print("Total de palabras:", total)
        print("Primera palabra:", primera)
        print("Última palabra:", ultima)
        print("Palabra central:", central)
        print("Posición central:", posicion_central)


def buscar_por_posicion(palabras, lineas_palabras):
    while True:
        posicion = input("Ingrese la posición de la palabra que desea buscar: ")

        inicio = time.perf_counter()

        # intentamos convertir el dato a un número entero
        try:
            posicion = int(posicion)

        except ValueError:
            print("Error: debe ingresar un número entero.")
            continue

        # comprobamos que la posición esté dentro del rango
        if posicion < 1 or posicion > len(palabras):
            print("Error: la posición está fuera del rango del archivo.")
            print("El archivo tiene", len(palabras), "palabras.")
            continue

        # convertimos la posición del usuario a un índice de Python
        indice = posicion - 1

        # obtenemos la palabra que está en esa posición
        palabra = palabras[indice]

        # obtenemos la línea donde aparece esa palabra
        linea = lineas_palabras[indice]

        # mostramos el resultado
        print("Palabra encontrada:", palabra)
        print("Posición:", posicion)
        print("Línea:", linea)

        fin = time.perf_counter()

        tiempo = (fin - inicio) * 1000
        print("Tiempo de búsqueda:", tiempo, "milisegundos")

        break


def comparar_busquedas(palabras, apariciones, lineas_palabras):

    palabra = input("Ingrese la palabra que desea buscar: ")

    # BUSQUEDA OPTIMIZADA CON DICCIONARIO

    inicio = time.perf_counter()

    resultados_optimizados = apariciones.get(palabra, [])

    print("\nVERSION OPTIMIZADA")

    print("Cantidad de apariciones:", len(resultados_optimizados))

    if len(resultados_optimizados) > 0:
        print("Primera línea:", resultados_optimizados[0])
        print("Última línea:", resultados_optimizados[-1])
    else:
        print("La palabra no fue encontrada.")

    fin = time.perf_counter()

    tiempo_optimizado = (fin - inicio) * 1000

    print("Tiempo optimizado:", tiempo_optimizado, "milisegundos")


    # BUSQUEDA LENTA CON LISTA

    resultados_lineales = []

    inicio = time.perf_counter()

    for i in range(len(palabras)):

        if palabras[i] == palabra:
            resultados_lineales.append(lineas_palabras[i])

    print("\nVERSION LENTA")

    print("Cantidad de apariciones:", len(resultados_lineales))

    if len(resultados_lineales) > 0:
        print("Primera línea:", resultados_lineales[0])
        print("Última línea:", resultados_lineales[-1])
    else:
        print("La palabra no fue encontrada.")

    fin = time.perf_counter()

    tiempo_lineal = (fin - inicio) * 1000

    print("Tiempo lineal:", tiempo_lineal, "milisegundos")


    # COMPARACION

    diferencia = abs(tiempo_lineal - tiempo_optimizado)

    print("\nRESULTADOS DE LA COMPARACION")

    if resultados_optimizados == resultados_lineales:
        print("Las dos búsquedas obtuvieron los mismos resultados.")
    else:
        print("Error: los resultados son diferentes.")

    print("Diferencia de tiempo:", diferencia, "milisegundos")
def menu():

    # variable para guardar las estructuras del archivo
    resultado = None

    # variable para controlar el menú
    opcion = ""

    while opcion != "0":

        print("\n========== BUSCADOR DE PALABRAS ==========")
        print("1. Cargar archivo")

        # solo mostramos las opciones si ya se cargó un archivo
        if resultado is not None:

            print("2. Búsqueda exacta")
            print("3. Búsqueda simple")
            print("4. Búsqueda por prefijo")
            print("5. Mostrar estadísticas")
            print("6. Buscar palabra por posición")
            print("7. Comparar búsquedas")

        print("0. Salir")
        print("==========================================")

        opcion = input("Seleccione una opción: ")

        # OPCION 0: SALIR
        if opcion == "0":
            break

        # OPCION 1: CARGAR ARCHIVO

        elif opcion == "1":

            # comprobamos si ya existe un archivo cargado
            if resultado is not None:

                respuesta = input("Ya hay un archivo cargado. ¿Desea reemplazarlo? (si/no): ")

                if respuesta.strip().lower() != "si":
                    print("Se conserva el archivo actual.")
                    continue

            ruta = input("Ingrese la ruta del archivo: ")

            nuevo_resultado = cargar_archivo(ruta)

            # solo reemplazamos si la carga fue exitosa
            if nuevo_resultado is not None:
                resultado = nuevo_resultado
                print("Archivo cargado correctamente.")

        # comprobamos que exista un archivo cargado
        elif resultado is None:
            print("Primero debe cargar un archivo.")

        else:

            # recuperamos las estructuras del archivo
            palabras, apariciones, apariciones_simple, lineas_palabras, raiz_trie = resultado

            # OPCION 2: BUSQUEDA EXACTA

            if opcion == "2":

                palabra = input("Ingrese la palabra que desea buscar: ")
                buscar_exacta(palabra, apariciones)

            # OPCION 3: BUSQUEDA SIMPLE

            elif opcion == "3":

                palabra = input("Ingrese la palabra que desea buscar: ")
                buscar_simple(palabra, apariciones_simple)

            # OPCION 4: BUSQUEDA POR PREFIJO

            elif opcion == "4":

                prefijo = input("Ingrese el prefijo que desea buscar: ")
                buscar_prefijo(prefijo, raiz_trie, palabras, lineas_palabras)

            # OPCION 5: ESTADISTICAS

            elif opcion == "5":

                mostrar_estadisticas(palabras)

            # OPCION 6: BUSCAR POR POSICION

            elif opcion == "6":

                buscar_por_posicion(palabras, lineas_palabras)

            # OPCION 7: COMPARAR BUSQUEDAS

            elif opcion == "7":

                comparar_busquedas(palabras, apariciones, lineas_palabras)

            else:
                print("Opción no válida.")




    print("Gracias por utilizar el programa.")




# iniciamos el programa
if __name__ == "__main__":

    menu()