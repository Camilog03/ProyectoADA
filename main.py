# =============================================================================
# main.py — Lector de entrada, VALUE, dispatcher y escritura de salida
# Proyecto ADA I — Problema 4: Motor de consultas sobre datos comprimidos
# Universidad del Valle Sede Tuluá
# =============================================================================
# Persona 1: leer_entrada, value, procesar_y_escribir, punto de entrada
# Persona 2: sum_rango, frequency, max_range, min_range  ← en consultas.py
# Persona 3: update, merge, count_ranges, decompress     ← en modificaciones.py
# =============================================================================

from lista_rangos import ListaRangos, ordenar_lista_rangos, buscar_primer_rango_que_llega
from rango import Rango
from consultas import sum_rango, frequency, max_range, min_range, decompress
from modificaciones import update


# =============================================================================
# FUNCIONES AUXILIARES DE LECTURA
# =============================================================================

def _siguiente_linea_no_vacia(lineas, i):
    """
    Avanza el índice 'i' hasta la próxima línea no vacía.
    Retorna el nuevo valor de i.
    """
    while i < len(lineas) and lineas[i].strip() == '':
        i += 1
    return i


def _leer_entero(lineas, i):
    """
    Lee un entero de la línea 'i' y retorna (valor, i+1).
    Auxiliar para mantener leer_entrada sin duplicar lógica de conversión.
    """
    return int(lineas[i].strip()), i + 1


# =============================================================================
# LEER ENTRADA
# =============================================================================

def leer_entrada(nombre_archivo):
    """
    Lee entrada.txt, construye la ListaRangos inicial y la ordena.
    También retorna las operaciones como lista de strings.

    Formato esperado:
        N
        valor inicio fin       ← N líneas, pueden venir en cualquier orden
        ...
        Q
        OPERACION parametros   ← Q líneas
        ...

    IMPORTANTE: los rangos pueden venir desordenados en el archivo.
    Después de leer todos los rangos se aplica ordenar_lista_rangos()
    (MergeSort, O(R log R)) para garantizar el orden por .inicio que
    requieren la búsqueda binaria y todas las operaciones de consulta.

    Retorna: (lista_rangos, operaciones)
    """
    lista = ListaRangos()
    operaciones = []

    with open(nombre_archivo, 'r') as f:
        lineas = f.read().split('\n')

    i = 0

    # --- Leer cantidad de rangos iniciales ---
    i = _siguiente_linea_no_vacia(lineas, i)
    n, i = _leer_entero(lineas, i)

    # --- Leer los N rangos (sin asumir orden) ---
    for _ in range(n):

        i = _siguiente_linea_no_vacia(lineas, i)
        partes = lineas[i].strip().split()
        valor = int(partes[0])
        inicio = int(partes[1])
        fin = int(partes[2])
        lista.agregar_al_final(Rango(valor, inicio, fin))
        i += 1

    # --- Ordenar por .inicio con MergeSort antes de cualquier consulta ---
   
    ordenar_lista_rangos(lista)

    # --- Leer cantidad de operaciones ---
    i = _siguiente_linea_no_vacia(lineas, i)
    q, i = _leer_entero(lineas, i)

    # --- Leer las Q operaciones ---
    for _ in range(q):
        i = _siguiente_linea_no_vacia(lineas, i)
        if i < len(lineas):
            operaciones.append(lineas[i].strip())
            i += 1
    return lista, operaciones


# =============================================================================
# OPERACIÓN VALUE
# =============================================================================
#
# Dado una posición, retorna el valor que tiene en la secuencia comprimida.
# Usa buscar_primer_rango_que_llega() para llegar al candidato en O(log R)
# y luego verifica con .contiene() que la posición esté dentro del rango.
#
# Complejidad: O(log R)
# =============================================================================

def value(lista, posicion):
    """
    Retorna el valor en la posición dada, o None si ningún rango la cubre.

    Ejemplo:
        lista = [Rango(1,1,5), Rango(3,6,8), Rango(2,9,14), ...]
        value(lista, 10) → 2   (Rango(2,9,14) contiene pos 10)
        value(lista, 7)  → 3   (Rango(3,6,8) contiene pos 7)
        value(lista, 25) → None (ningún rango llega ahí)
    """
    idx = buscar_primer_rango_que_llega(lista, posicion)

    if idx < lista.tamaño():
        rango = lista.obtener(idx)
        if rango.contiene(posicion):
            return rango.valor

    return None   # posición fuera de todos los rangos


# =============================================================================
# FUNCIÓN AUXILIAR DE ESCRITURA
# =============================================================================

def _escribir(salida, texto):
    """
    Escribe una línea en el archivo de salida.
    Centraliza la escritura para evitar repetir salida.write(...+ '\n').
    """
    salida.write(texto + '\n')


# =============================================================================
# FUNCIÓN AUXILIAR DE PARSEO DE PARÁMETROS
# =============================================================================

def _dos_enteros(partes):
    """
    Extrae dos enteros de partes[1] y partes[2].
    Usada por SUM, MAX_RANGE, MIN_RANGE, DECOMPRESS para evitar duplicar
    la misma conversión en cada rama del dispatcher.
    Retorna: (ini, fin)
    """
    return int(partes[1]), int(partes[2])


# =============================================================================
# PROCESADOR CENTRAL Y ESCRITURA DE SALIDA
# =============================================================================

# COUNT_RANGES y MERGE usan directamente la ListaRangos (Persona A)
def count_ranges(lista):
    return lista.tamaño()
 
def merge(lista):
    """
    Fusiona rangos consecutivos que tengan el mismo valor.
    Recorre la lista una vez de izquierda a derecha.
    Complejidad: O(R)
    """
    i = 0
    while i < lista.tamaño() - 1:
        actual    = lista.obtener(i)
        siguiente = lista.obtener(i + 1)
        # Si son consecutivos y tienen el mismo valor → fusionar
        if actual.fin + 1 == siguiente.inicio and actual.valor == siguiente.valor:
            actual.fin = siguiente.fin   # extender el rango actual
            lista.eliminar_en(i + 1)     # eliminar el siguiente
            # NO incrementar i: revisar de nuevo con el nuevo siguiente
        else:
            i += 1


def procesar_y_escribir(lista, operaciones, nombre_salida):
    """
    Procesa todas las operaciones en el orden del archivo y escribe
    los resultados en salida.txt.
    """
    with open(nombre_salida, 'w') as salida:

        for linea in operaciones:
            partes  = linea.strip().split()
            if not partes:
                continue
            comando = partes[0]

            # ----------------------------------------------------------------
            # VALUE
            # ----------------------------------------------------------------
            if comando == "VALUE":
                pos = int(partes[1])
                res = value(lista, pos)
                _escribir(salida, f"VALUE {pos} = {res if res is not None else 'NONE'}")

            # ----------------------------------------------------------------
            # SUM — Persona 2
            # ----------------------------------------------------------------
            elif comando == "SUM":
                ini, fin = _dos_enteros(partes)
                res = sum_rango(lista, ini, fin)
                _escribir(salida, f"SUM {ini} {fin} = {res}")

            # ----------------------------------------------------------------
            # FREQUENCY — Persona 2
            # ----------------------------------------------------------------
            elif comando == "FREQUENCY":
                val = int(partes[1])
                res = frequency(lista, val)
                _escribir(salida, f"FREQUENCY {val} = {res}")

            # ----------------------------------------------------------------
            # MAX_RANGE — Persona 2
            # ----------------------------------------------------------------
            elif comando == "MAX_RANGE":
                ini, fin = _dos_enteros(partes)
                res = max_range(lista, ini, fin)
                _escribir(salida, f"MAX_RANGE {ini} {fin} = {res}")

            # ----------------------------------------------------------------
            # MIN_RANGE — Persona 2
            # ----------------------------------------------------------------
            elif comando == "MIN_RANGE":
                ini, fin = _dos_enteros(partes)
                res = min_range(lista, ini, fin)
                _escribir(salida, f"MIN_RANGE {ini} {fin} = {res}")

            # ----------------------------------------------------------------
            # UPDATE — Persona 3
            # ----------------------------------------------------------------
            elif comando == "UPDATE":
                ini, fin = _dos_enteros(partes)
                val = int(partes[3])
                update(lista, ini, fin, val)
                _escribir(salida, f"UPDATE {ini} {fin} {val} = OK")

            # ----------------------------------------------------------------
            # MERGE — Persona 3
            # ----------------------------------------------------------------
            elif comando == "MERGE":
                merge(lista)
                _escribir(salida, "MERGE = OK")

            # ----------------------------------------------------------------
            # COUNT_RANGES — Persona 3
            # ----------------------------------------------------------------
            elif comando == "COUNT_RANGES":
                res = count_ranges(lista)
                _escribir(salida, f"COUNT_RANGES = {res}")

            # ----------------------------------------------------------------
            # DECOMPRESS — Persona 3
            # ----------------------------------------------------------------
            elif comando == "DECOMPRESS":
                ini, fin = _dos_enteros(partes)
                vals = decompress(lista, ini, fin)
                _escribir(salida, f"DECOMPRESS {ini} {fin} = " +
                          " ".join(str(v) for v in vals))

            else:
                _escribir(salida, f"OPERACION DESCONOCIDA: {linea}")


# =============================================================================
# PUNTO DE ENTRADA PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    lista, operaciones = leer_entrada("entrada.txt")
    procesar_y_escribir(lista, operaciones, "salida.txt")
    print("Procesamiento completo. Ver salida.txt")

    with open("salida.txt", "r") as f:
        print(f.read())
