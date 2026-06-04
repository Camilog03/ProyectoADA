# =============================================================================
# lista_rangos.py — Estructura ListaRangos + MergeSort + Búsqueda Binaria
# Proyecto ADA I — Problema 4: Motor de consultas sobre datos comprimidos
# Universidad del Valle Sede Tuluá
# =============================================================================
#
# Este archivo contiene:
#   - ListaRangos : lista dinámica propia, arreglo base de Rango
#   - ordenar_lista_rangos() : MergeSort sobre ListaRangos - D&V #1
#   - buscar_primer_rango_que_llega() : búsqueda binaria - D&V #2
# =============================================================================

from rango import Rango

# =============================================================================
# CLASE ListaRangos
# =============================================================================

class ListaRangos:
    
    """
    Lista dinámica propia de objetos Rango, mantenida ordenada por .inicio.

    Usa una lista de Python SOLO como almacenamiento interno (arreglo base).
    No se usa sorted(), bisect, dict, set ni ninguna estructura prohibida.

    El atributo 'total' permite que COUNT_RANGES sea O(1) sin recorrer nada.
    """

    def __init__(self):

        self.datos = []   # arreglo base — solo almacenamiento
        self.total = 0    # contador de rangos actuales

    # ------------------------------------------------------------------
    # Operaciones básicas sobre el arreglo interno
    # ------------------------------------------------------------------

    def agregar_al_final(self, rango):
        """
        Agrega un Rango al final del arreglo.
        Usado exclusivamente durante la construcción inicial (leer_entrada),
        antes de ordenar con MergeSort.
        Complejidad: O(1) amortizado.
        """
        self.datos.append(rango)
        self.total += 1

    def insertar_en(self, indice, rango):
        """
        Inserta un Rango en la posición 'indice', desplazando los siguientes.
        Usado por UPDATE al dividir rangos.
        Complejidad: O(R) en el peor caso (desplazamiento).
        """
        self.datos.insert(indice, rango)
        self.total += 1

    def eliminar_en(self, indice):
        """
        Elimina el Rango en la posición 'indice'.
        Usado por UPDATE y MERGE al fusionar o recortar rangos.
        Complejidad: O(R) en el peor caso (desplazamiento).
        """
        self.datos.pop(indice)
        self.total -= 1

    def obtener(self, indice):
        """
        Retorna el Rango en la posición 'indice' sin eliminarlo.
        Complejidad: O(1).
        """
        return self.datos[indice]

    def tamaño(self):
        """
        Retorna la cantidad de rangos actuales.
        Complejidad: O(1) gracias al contador interno.
        """
        return self.total

    def __repr__(self):
        return str(self.datos)


# =============================================================================
# DIVIDIR Y VENCER #1 — MergeSort para ordenar rangos por .inicio
# =============================================================================
#
# Problema:    Al leer entrada.txt, los rangos pueden venir en cualquier orden.
#              La búsqueda binaria REQUIERE que la lista esté ordenada por .inicio.
#              Sin orden, VALUE, SUM, MAX_RANGE, etc. retornan resultados incorrectos.
#
# Estrategia:  MergeSort divide el arreglo en mitades recursivamente hasta
#              llegar a subarreglos de tamaño 1 (caso base), luego los fusiona
#              en orden creciente de .inicio.
#
# Caso base:   izq >= der → subarreglo de 0 o 1 elemento, ya está "ordenado".
# División:    mitad = (izq + der) // 2
#              Ordenar recursivamente [izq..mitad] y [mitad+1..der]
# Combinación: Mezclar los dos subarreglos ordenados en el arreglo auxiliar,
#              comparando .inicio de cada elemento.
#
# Complejidad: O(R log R) tiempo,  O(R) espacio auxiliar.
# Comparación con solución ingenua (inserción): O(R²) → MergeSort es mucho
#              mejor cuando R es grande (hasta 1,000,000 rangos según enunciado).
# =============================================================================

def ordenar_lista_rangos(lista):
    """
    Ordena en el lugar la ListaRangos por .inicio usando MergeSort.
    Debe llamarse una sola vez al terminar leer_entrada(), antes de cualquier
    operación de consulta.
    """
    _mergesort(lista.datos, 0, lista.tamaño() - 1)


def _mergesort(datos, izq, der):
    """
    MergeSort recursivo sobre el arreglo interno 'datos' (lista de Rangos).
    Ordena el subarreglo datos[izq..der] por .inicio de forma creciente.
    """
    # Caso base: subarreglo de tamaño 0 o 1 → ya ordenado
    if izq >= der:
        return

    # División: calcular el índice del punto medio
    mitad = (izq + der) // 2

    # Conquistar: ordenar cada mitad de forma independiente
    _mergesort(datos, izq, mitad)
    _mergesort(datos, mitad + 1, der)

    # Combinar: fusionar las dos mitades ya ordenadas
    _merge(datos, izq, mitad, der)


def _merge(datos, izq, mitad, der):
    """
    Fusiona dos subarreglos contiguos ya ordenados:
        datos[izq..mitad]   y   datos[mitad+1..der]
    El resultado queda ordenado en datos[izq..der].

    Usa un arreglo auxiliar temporal para la mezcla.
    """
    # Construir arreglo auxiliar copiando ambas mitades
    auxiliar = []
    for k in range(izq, der + 1):
        auxiliar.append(datos[k])

    # Índices para recorrer la mitad izquierda y la derecha del auxiliar
    i = 0                        # recorre auxiliar[0..mitad-izq]
    j = (mitad - izq) + 1        # recorre auxiliar[mitad-izq+1..der-izq]
    limite_izq = mitad - izq     # último índice válido de la mitad izquierda
    limite_der = der - izq       # último índice válido del auxiliar completo
    k = izq                      # posición de escritura en datos[]

    # Mezclar comparando .inicio de cada elemento
    while i <= limite_izq and j <= limite_der:
        if auxiliar[i].inicio <= auxiliar[j].inicio:
            datos[k] = auxiliar[i]
            i += 1
        else:
            datos[k] = auxiliar[j]
            j += 1
        k += 1

    # Copiar elementos restantes de la mitad izquierda (si quedan)
    while i <= limite_izq:
        datos[k] = auxiliar[i]
        i += 1
        k += 1

    # Copiar elementos restantes de la mitad derecha (si quedan)
    while j <= limite_der:
        datos[k] = auxiliar[j]
        j += 1
        k += 1


# =============================================================================
# DIVIDIR Y VENCER #2 — Búsqueda binaria sobre rangos ordenados
# =============================================================================
#
# Problema:    Localizar el primer rango relevante para una posición dada,
#              en O(log R) en vez de O(R) con búsqueda lineal.
#
# Estrategia:  Sobre la lista ya ordenada por .inicio, buscar el primer rango
#              cuyo .fin >= posicion. Ese es el primer rango que podría contener
#              o solaparse con la posición buscada.
#
# Caso base:   izq > der → no quedan candidatos, retornar 'resultado'.
# División:    mitad = (izq + der) // 2
# Decisión:    rango[mitad].fin >= posicion → candidato válido, anotar y buscar
#                                             más a la izquierda (puede haber uno antes)
#              rango[mitad].fin < posicion  → rango termina antes, ir a la derecha
# Combinación: retornar el índice del candidato más a la izquierda encontrado.
#
# Complejidad: O(log R) vs O(R) de búsqueda lineal.
# =============================================================================

def buscar_primer_rango_que_llega(lista, posicion):
    """
    Retorna el índice del primer rango cuyo .fin >= posicion.

    Este índice es el punto de entrada para todas las operaciones que
    necesitan recorrer rangos desde una posición: VALUE, SUM, MAX_RANGE,
    MIN_RANGE, DECOMPRESS y UPDATE.

    Si ningún rango llega hasta 'posicion', retorna lista.tamaño()
    (señal de que no hay ningún rango relevante).

    Precondición: la lista debe estar ordenada por .inicio (garantizado
                  después de llamar a ordenar_lista_rangos en leer_entrada).
    """
    izq      = 0
    der      = lista.tamaño() - 1
    resultado = lista.tamaño()   # valor por defecto: "no encontrado"

    while izq <= der:
        mitad       = (izq + der) // 2
        rango_mitad = lista.obtener(mitad)

        if rango_mitad.fin >= posicion:
            resultado = mitad    # posible candidato
            der = mitad - 1     # buscar si hay uno más a la izquierda
        else:
            izq = mitad + 1     # este rango termina antes → ir a la derecha

    return resultado
