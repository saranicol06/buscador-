"""
Taller Final - BUSCADOR DE PALABRAS
Por: Sara Zuluaga y Axel Bedoya 

DESCRIPCIÓN: 
Programa de consola que carga un archivo de texto y permite buscar palabras de forma eficiente 

ESTRUCTURAS DE DATOS UTILIZADAS
- Listas: almacenan las palabras y sus líneas en orden de aparición.
- Diccionarios: guardan las apariciones de cada palabra para búsquedas rápidas.
- Trie: árbol implementado desde cero para realizar búsquedas por prefijo.


OPCIONES DEL MENÚ

1. Cargar archivo             5. Mostrar estadísticas
2. Búsqueda exacta            6. Buscar por posición
3. Búsqueda simple             7. Comparar búsquedas
4. Búsqueda por prefijo        0. Salir

MEDICIÓN DE TIEMPOS

Se utiliza time.perf_counter() para medir las búsquedas en milisegundos,
sin contar el tiempo que tarda el usuario en escribir.

 """
import math
import time 



class NodoTrie:
    """
    Nodo del Trie. Representa una letra dentro de un camino de palabras.

    Atributos:
    hijos (dict): guarda los nodos que siguen después de cada letra.
    posiciones (list): guarda las posiciones de las palabras que terminan en este nodo.

    """
    
    __slots__ = ("hijos", "posiciones")

    def __init__(self): 
        """ 
        constructor: se ejecuta cada vez que creamos un nodo.
        
        """
        self.hijos = {}
        self.posiciones =[]


def construir_trie(indice_simple):
     """
     Construye el Trie a partir de las palabras unicas y en minusculas 

     PARAMETROS:
      - indice_simple (dict): palabra en minuscula por ende la lista de posiciones donde aparece
          Retorna:
          NodoTrie: La raiz del arbol construido.
          Complejidad O(U*L)  = U: Palabras unicas y L= largo promedio de una palabra 
     
     """
     raiz = NodoTrie()

     for palabra_min, posiciones in indice_simple.items():
        nodo = raiz

        #Bajamos letra por letra, creando los nodos que no existen
        for letra in palabra_min:
            if letra not in nodo.hijos:
                 nodo.hijos[letra] = NodoTrie()
            nodo = nodo.hijos[letra]

        #el ultimo nodo marca el final de la palabra y guarda sus posiciones 
        
        nodo.posiciones = posiciones 

     return raiz


def posiciones_con_prefijo(raiz, prefijo):

    """
    Busca en el Trie todas las palabras que comienzan con el prefijo dado.

    PARAMETROS: 
    raiz (NodoTrie): Raiz del Trie
    Prefijo (str):  prefijo ya convertido en minuscula 

    RETORNA:
    list[int]: posiciones 

    
    """
    nodo = raiz
    for letra in prefijo:
        nodo = nodo.hijos.get(letra) 
    
        if nodo is None:
            return[]

    #Recolectar apariciones 
    posiciones = []
    pila = [nodo]
    while pila:
        actual = pila.pop()
        posiciones.extend(actual.posiciones)
        pila.extend(actual.hijos.values())


    posiciones.sort()
    return posiciones
        

 

def cargar_archivo(ruta):
    """
    Opción 1: Carga del archivo 
    Lee un archivo de texto y construye todas las estructuras de datos

    PARAMETROS:
    ruta (str): nombre o ruta del archivo.

    RETORNA:
    tuple: (palabras, apariciones, apariciones_simple,
            lineas_palabras, raiz_trie) si es exitoso; None si ocurre un error.
    """
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
        with open(ruta, "r", encoding="utf-8") as archivo:

            for numero_linea, linea in enumerate(archivo, start=1):

                palabras_linea = linea.split()

                for palabra in palabras_linea:

                    indice = len(palabras)

                    palabras.append(palabra)


                    if palabra not in apariciones:
                        apariciones[palabra] = []

                    apariciones[palabra].append(numero_linea)



                    palabra_minuscula = palabra.lower()

                    if palabra_minuscula not in posiciones_simple:
                          posiciones_simple[palabra_minuscula] = []

                    posiciones_simple[palabra_minuscula].append(indice)

                    if palabra_minuscula not in apariciones_simple:
                        apariciones_simple[palabra_minuscula] = []

                    apariciones_simple[palabra_minuscula].append(numero_linea)

                    lineas_palabras.append(numero_linea)

        if len(palabras) == 0:
            print("El archivo está vacío.")
            return None

        raiz_trie = construir_trie(posiciones_simple)    

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

    """
    Opción 2. Busqueda exacta
    Distingue mayusculas y minusculas y no acepta coincidencias parciales
     
    PARAMETROS:
    palabra (str): palabra que se desea buscar.
    apariciones (dict): palabra, lista de líneas donde aparece.

    RETORNA:
    None. Imprime las apariciones, primera y última línea, y tiempo de búsqueda.
    """

    inicio = time.perf_counter()

    if palabra in apariciones:
        lineas = apariciones[palabra]

        print("La palabra fue encontrada.")
        print("Cantidad de apariciones:", len(lineas))
        print("Primera línea:", lineas[0])
        print("Última línea:", lineas[-1])

    else:
        print("La palabra no fue encontrada.")

    fin = time.perf_counter()

    tiempo = (fin - inicio) * 1000
    print("Tiempo de búsqueda:", tiempo, "milisegundos")

def buscar_simple(palabra, apariciones_simple):
    """
    Opción 3: Búsqueda simple
    Igula que la exacta pero no disitngue de mayusculas y minusculas 

    PARAMETROS:
    palabra (str): palabra a buscar, sin importar mayúsculas o minúsculas.
    apariciones_simple (dict): palabra en minúsculas,  lista de líneas.

    RETORNA:
    None. Imprime la cantidad de apariciones, primera y última línea.
    """

    palabra = palabra.lower()

    inicio = time.perf_counter()

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
    """
    Opcion 4: Buscar por prefijo
    Muestra todas las palabras que cominezan con el prefijo, ain diatinguir minusculas o mayusculas.

    PARAMETROS:
    prefijo (str): prefijo que se desea buscar.
    raiz_trie (NodoTrie): raíz del Trie.
    palabras (list): palabras del archivo en orden.
    lineas_palabras (list): línea correspondiente a cada palabra.

    RETORNA:
    None. Imprime las palabras encontradas y sus líneas
    """
    # evitamos prefijos vacíos (devolverían todas las palabras)
    if prefijo.strip() == "":
        print("Error: debe ingresar un prefijo.")
        return
    
    prefijo = prefijo.strip().lower()

    inicio = time.perf_counter()

    indices = posiciones_con_prefijo(raiz_trie, prefijo)

    if len(indices) > 0:

        for indice in indices:
            print(palabras[indice], "- Línea:", lineas_palabras[indice])



        print("Primera palabra:", palabras[indices[0]])
        print("Primera línea:", lineas_palabras[indices[0]])

        print("Última palabra:", palabras[indices[-1]])
        print("Última línea:", lineas_palabras[indices[-1]])

    else:
        print("No se encontraron palabras con ese prefijo.")

    fin = time.perf_counter()

    tiempo = (fin - inicio) * 1000
    print("Tiempo de búsqueda:", tiempo, "milisegundos")


def mostrar_estadisticas(palabras):
    """
    Opción 5: Mostrar estadisticos 
    Muestra el total de palabras, la primera, la ultima y la del centro.

    PARAMETROS:
    palabras (list): palabras del archivo en orden de aparición.

    RETORNA:
    None. Imprime las estadísticas del archivo.
    """
    total = len(palabras)

    if total == 0:
        print("No hay palabras para mostrar estadísticas.")

    else:

        primera = palabras[0]

        ultima = palabras[-1]

        # calculamos la posición central, math.ceil redondea un numero decimal hacia arriba del entero mas pequeno que ¿s amyor o igual a ese numerko
        posicion_central = math.ceil(total / 2)

        indice_central = posicion_central - 1

        central = palabras[indice_central]

        print("ESTADÍSTICAS DEL ARCHIVO")
        print(f"El archivo contiene {total} palabras.")
        print(f"La palabra No1 es: {primera}")
        print(f"La palabra No{total} es: {ultima}")
        print(f"La palabra del centro (No{posicion_central}) es: {central}")


def buscar_por_posicion(palabras, lineas_palabras):
    """
    Opción 6: Buscar por posicion
    Pide un numero entero X y muestra la figura que esta en la posicion X del texto

    PARAMETRO:
    palabras (list): palabras del archivo en orden.
    lineas_palabras (list): línea correspondiente a cada palabra.

    RETORNA:
    None. Imprime cada palabra, su posición y su línea.
    
    """
    while True:
        posicion = input("Ingrese la posición de la palabra que desea buscar: ")

        inicio = time.perf_counter()

        try:
            posicion = int(posicion)

        except ValueError:
            print("Error: debe ingresar un número entero.")
            continue

        if posicion < 1 or posicion > len(palabras):
            print("Error: la posición está fuera del rango del archivo.")
            print("El archivo tiene", len(palabras), "palabras.")
            continue

        indice = posicion - 1

        palabra = palabras[indice]

        linea = lineas_palabras[indice]

        print("Palabra encontrada:", palabra)
        print("Posición:", posicion)
        print("Línea:", linea)

        fin = time.perf_counter()

        tiempo = (fin - inicio) * 1000
        print("Tiempo de búsqueda:", tiempo, "milisegundos")

        break


def comparar_busquedas(palabras, apariciones, lineas_palabras):

    """
    Opción 7: Comparar busquedad 
    Compara la busquedad optimizada con diccionario y la busqueda lineal con lista 
    PARAMETROS:
        palabras (list): palabras del archivo.
        apariciones (dict): palabra -> lista de líneas.
        lineas_palabras (list): línea correspondiente a cada palabra.

    RETORNA:
        None. Imprime los resultados y tiempos de ambas búsquedas
    """

    palabra = input("Ingrese la palabra que desea buscar: ")

    # BUSQUEDA OPTIMIZADA CON DICCIONARIO

    inicio = time.perf_counter()

    resultados_optimizados = apariciones.get(palabra, [])
   
    fin = time.perf_counter()

    tiempo_optimizado = (fin - inicio) * 1000

    

    print("\nVERSION OPTIMIZADA")

    print("Cantidad de apariciones:", len(resultados_optimizados))

    if len(resultados_optimizados) > 0:
        print("Primera línea:", resultados_optimizados[0])
        print("Última línea:", resultados_optimizados[-1])
    else:
        print("La palabra no fue encontrada.")

    print("Tiempo optimizado:", tiempo_optimizado, "milisegundos")


    # BUSQUEDA LENTA CON LISTA

    inicio = time.perf_counter()
    resultados_lineales = []

    for i in range(len(palabras)):

        if palabras[i] == palabra:
            resultados_lineales.append(lineas_palabras[i])
  
    fin = time.perf_counter()

    tiempo_lineal = (fin - inicio) * 1000

    print("\nVERSION LENTA")

    print("Cantidad de apariciones:", len(resultados_lineales))

    if len(resultados_lineales) > 0:
        print("Primera línea:", resultados_lineales[0])
        print("Última línea:", resultados_lineales[-1])
    else:
        print("La palabra no fue encontrada.")

    print("Tiempo lineal:", tiempo_lineal, "milisegundos")


    # COMPARACION

    diferencia = abs(tiempo_lineal - tiempo_optimizado)

    print("\nRESULTADOS DE LA COMPARACION")

    if resultados_optimizados == resultados_lineales:
        print("Las dos búsquedas obtuvieron los mismos resultados.")
    else:
        print("Error: los resultados son diferentes.")

    print("Diferencia de tiempo:", diferencia, "milisegundos")

    if tiempo_optimizado > 0:
        print(f"La versión optimizada fue {tiempo_lineal / tiempo_optimizado:.1f} veces más rápida.")

def menu():

    """
    Ciclo principal del programa. Muestra el menú, lee la opción del usuario y
    llama a la función correspondiente. Solo termina cuando el usuario elige
    la opción 0 (Salir); después de cada operación vuelve al menú.
 
 
    """
    resultado = None

    opcion = ""

    while opcion != "0":

        print("\n========== BUSCADOR DE PALABRAS ==========")
        print("1. Cargar archivo")

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

        elif resultado is None:
            print("Primero debe cargar un archivo.")

        else:

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




if __name__ == "__main__":

    menu()
