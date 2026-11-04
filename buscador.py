import math

def cargar_archivo(ruta):
    # lista para guardar las palabras en orden
    palabras = []

    # diccionario para guardar las líneas de cada palabra
    apariciones = {}

    #diccionario que usamos para las busquedas que no distinguen por mayusculab  
    apariciones_simple = {}

    #lista para saber en que linea esta cada palabara para mostrar la primera y ultima coincidencia con su numero de linea
    lineas_palabras = []

    try:
        #abrimos el archivo en modo lectura
        with open(ruta, "r", encoding="utf-8") as archivo:

            # leemos el archivo línea por línea
            for numero_linea, linea in enumerate(archivo, start=1):

                #separamos la línea en palabras
                palabras_linea = linea.split()

                # revisamos cada palabra de la línea
                for palabra in palabras_linea:

                    # guardamos la palabra en la lista
                    palabras.append(palabra)

                    # si la palabra no está en el diccionario, creamos una lista vacía para sus líneas
                    if palabra not in apariciones:
                        apariciones[palabra] = []

                    # guardamos la línea donde aparece
                    apariciones[palabra].append(numero_linea)

                    # convertimos la palabra a minúsculas
                    palabra_minuscula = palabra.lower()

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

        # devolvemos las estructuras creadas incluyendo las convertidas a minusculas para tener ambas versiones del diccionario y tambien la lista con el numero de linea de las palabras
        return palabras, apariciones, apariciones_simple, lineas_palabras

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

    #si la palabra existe como clave en el diccionario y guarda en lineas donde aparece la palabra
    if palabra in apariciones:
        lineas = apariciones[palabra]

        print("La palabra fue encontrada.")
        print("Cantidad de apariciones:", len(lineas)) #cantidad de veces que aparece la palabra
        print("Líneas donde aparece:", lineas) #lineas donde aparece la palabra

    else:
        print("La palabra no fue encontrada.")


def buscar_simple(palabra, apariciones_simple):

    # convertimos lo que escribió el usuario a minúsculas
    palabra = palabra.lower()

    # revisamos si la palabra existe en el diccionario
    if palabra in apariciones_simple:

        lineas = apariciones_simple[palabra]

        print("La palabra fue encontrada.")
        print("Cantidad de apariciones:", len(lineas))
        print("Líneas donde aparece:", lineas)

    else:
        print("La palabra no fue encontrada.")


def buscar_prefijo(prefijo, palabras, lineas_palabras):

    # convertimos el prefijo a minúsculas
    prefijo = prefijo.lower()

    # lista para guardar las coincidencias
    coincidencias = []

    # recorremos todas las palabras del archivo
    for i in range(len(palabras)):

        # obtenemos la palabra en minúsculas
        palabra = palabras[i].lower()

        # comprobamos si comienza con el prefijo
        if palabra.startswith(prefijo):

            # guardamos la palabra y su línea
            coincidencias.append((palabras[i], lineas_palabras[i]))

    # comprobamos si encontramos coincidencias
    if len(coincidencias) > 0:

        print("Palabras encontradas:")

        # mostramos todas las coincidencias
        for palabra, linea in coincidencias:
            print(palabra, "- Línea:", linea)

        # mostramos la primera coincidencia
        print("Primera palabra:", coincidencias[0][0])
        print("Primera línea:", coincidencias[0][1])

        # mostramos la última coincidencia
        print("Última palabra:", coincidencias[-1][0])
        print("Última línea:", coincidencias[-1][1])

    else:
        print("No se encontraron palabras con ese prefijo.")


import math

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

    posicion = input("Ingrese la posición de la palabra que desea buscar: ")

    # intentamos convertir el dato a un número entero
    try:
        posicion = int(posicion)

    except ValueError:
        print("Error: debe ingresar un número entero.")
        return

    # comprobamos que la posición esté dentro del rango
    if posicion < 1 or posicion > len(palabras):
        print("Error: la posición está fuera del rango del archivo.")
        print("El archivo tiene", len(palabras), "palabras.")
        return

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


import time

def comparar_busquedas(palabras, apariciones, lineas_palabras):

    # pedimos la palabra que queremos buscar
    palabra = input("Ingrese la palabra que desea buscar: ")

    # busqueda optimizada

    inicio = time.perf_counter()

    # buscamos directamente en el diccionario
    resultados_optimizados = apariciones.get(palabra, [])

    fin = time.perf_counter()

    # calculamos el tiempo en milisegundos
    tiempo_optimizado = (fin - inicio) * 1000

    # busqueda lineal

    resultados_lineales = []

    inicio = time.perf_counter()

    # recorremos todas las palabras
    for i in range(len(palabras)):

        if palabras[i] == palabra:
            resultados_lineales.append(lineas_palabras[i])

    fin = time.perf_counter()

    tiempo_lineal = (fin - inicio) * 1000

    # mostramos resultados

    print("\nRESULTADOS DE LA COMPARACION")

    if resultados_optimizados == resultados_lineales:
        print("Las dos búsquedas obtuvieron los mismos resultados.")
    else:
        print("Los resultados son diferentes.")

    print("Cantidad de apariciones:", len(resultados_optimizados))

    if len(resultados_optimizados) > 0:
        print("Primera línea:", resultados_optimizados[0])
        print("Última línea:", resultados_optimizados[-1])
    else:
        print("La palabra no fue encontrada.")

    print("\nTIEMPOS DE EJECUCION")
    print("Búsqueda optimizada:", tiempo_optimizado, "milisegundos")
    print("Búsqueda lineal:", tiempo_lineal, "milisegundos")

def menu():

    # variable para guardar las estructuras del archivo
    resultado = None

    # variable para controlar el menú
    opcion = -1

    while opcion != 0:

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

        # OPCION 1: CARGAR ARCHIVO

        if opcion == "1":

            # comprobamos si ya existe un archivo cargado
            if resultado is not None:

                respuesta = input("Ya hay un archivo cargado. ¿Desea reemplazarlo? (si/no): ")

                if respuesta.lower() != "si":
                    print("Se conserva el archivo actual.")
                    continue

            ruta = input("Ingrese la ruta del archivo: ")

            nuevo_resultado = cargar_archivo(ruta)

            # solo reemplazamos si la carga fue exitosa
            if nuevo_resultado is not None:
                resultado = nuevo_resultado
                print("Archivo cargado correctamente.")

        # comprobamos que exista un archivo cargado
        elif resultado is not None:

            # recuperamos las estructuras del archivo
            palabras, apariciones, apariciones_simple, lineas_palabras = resultado

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
                buscar_prefijo(prefijo, palabras, lineas_palabras)

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

        else:
            print("Primero debe cargar un archivo.")

    print("Gracias por utilizar el programa.")


# iniciamos el programa
menu()