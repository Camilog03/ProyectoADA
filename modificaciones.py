# =============================================================================
# modificaciones.py — UPDATE
# Proyecto ADA I — Problema 4: Motor de consultas sobre datos comprimidos
# Universidad del Valle Sede Tuluá
# =============================================================================
# Persona C: update
# =============================================================================
#
# ESTRATEGIA GENERAL DE UPDATE
# ─────────────────────────────────────────────────────────────────────────────
# UPDATE ini fin val reemplaza el valor de todas las posiciones [ini..fin]
# por val, trabajando DIRECTAMENTE sobre la lista de rangos comprimida.
#
# Para hacerlo, el algoritmo:
#   1. Localiza el primer rango relevante con búsqueda binaria  →  O(log R)
#   2. Recorre hacia la derecha todos los rangos que se solapan con [ini,fin]
#   3. Por cada rango solapado decide qué hacer:
#        a) Solapamiento parcial izquierdo  → recortar el rango existente
#        b) Solapamiento total              → eliminar el rango
#        c) Solapamiento parcial derecho   → recortar el rango existente
#   4. Inserta el nuevo rango único (val, ini, fin) en su lugar correcto
#
# Este enfoque NO expande la secuencia y opera solo sobre los R rangos.
# =============================================================================

from lista_rangos import buscar_primer_rango_que_llega
from rango import Rango


def update(lista, ini, fin, val):
    """
    Reemplaza el valor de todas las posiciones [ini..fin] por 'val'.

    Modifica la lista de rangos en el lugar sin expandir la secuencia.
    Después del update, la lista sigue ordenada por .inicio y sin solapamientos.

    Parámetros:
        lista : ListaRangos  — estructura compartida con las otras personas
        ini   : int          — posición inicial del update (inclusive)
        fin   : int          — posición final del update (inclusive)
        val   : int/float    — nuevo valor a asignar

    Complejidad: O(log R + K)  donde K = rangos solapados (K ≤ R)
    Caso peor  : O(R) cuando el update cubre todos los rangos
    """

    # ─── PASO 1: localizar el primer rango relevante con búsqueda binaria ────
    # buscar_primer_rango_que_llega retorna el índice del primer rango cuyo
    # .fin >= ini, es decir, el primero que podría solaparse con [ini, fin].
    # Costo: O(log R)  — D&V ya implementado por Persona A.
    i = buscar_primer_rango_que_llega(lista, ini)

    # ─── PASO 2: recorrer y eliminar / recortar rangos solapados ─────────────
    # Procesamos de izquierda a derecha todos los rangos que intersectan [ini,fin].
    # Usamos un índice manual porque modificamos la lista mientras la recorremos.

    while i < lista.tamaño():
        rango = lista.obtener(i)

        # Si el rango ya empieza después de fin, no hay más solapamientos
        if rango.inicio > fin:
            break

        # ── Caso A: solapamiento parcial por la IZQUIERDA ────────────────────
        # El rango empieza ANTES de ini y termina DENTRO de [ini, fin].
        # Ejemplo: rango(1, 1, 5)  con update(3, 7, val)
        #   → recortar la parte derecha: rango queda (1, 1, 2)
        #   → el rango ya NO cubre [ini..fin], pero sí sobrevive a la izquierda
        if rango.inicio < ini and rango.fin <= fin:
            rango.fin = ini - 1
            i += 1  # este rango ya fue ajustado, pasar al siguiente

        # ── Caso B: solapamiento parcial por la DERECHA ───────────────────────
        # El rango empieza DENTRO de [ini, fin] y termina DESPUÉS de fin.
        # Ejemplo: rango(2, 9, 14) con update(6, 10, val)
        #   → recortar la parte izquierda: rango queda (2, 11, 14)
        #   → el rango sobrevive a la derecha de [ini..fin]
        elif rango.inicio >= ini and rango.fin > fin:
            rango.inicio = fin + 1
            break  # este es el último rango afectado, no hay más

        # ── Caso C: solapamiento total ────────────────────────────────────────
        # El rango está completamente dentro de [ini, fin].
        # Ejemplo: rango(3, 6, 8) con update(4, 10, val)
        #   → el rango desaparece completamente
        #   → NO incrementamos i porque eliminar_en desplaza el siguiente
        elif rango.inicio >= ini and rango.fin <= fin:
            lista.eliminar_en(i)
            # i queda apuntando al siguiente rango automáticamente

        # ── Caso D: el rango CONTIENE completamente a [ini, fin] ─────────────
        # El rango empieza ANTES de ini y termina DESPUÉS de fin.
        # Ejemplo: rango(1, 1, 20) con update(5, 10, val)
        #   → hay que DIVIDIR en tres partes:
        #        (1, 1, 4)   parte izquierda que sobrevive
        #        (val, 5, 10) el nuevo rango
        #        (1, 11, 20) parte derecha que sobrevive
        else:
            # Guardar el valor original y los límites antes de modificar
            valor_original = rango.valor
            fin_original   = rango.fin

            # Recortar el rango existente → queda como parte izquierda
            rango.fin = ini - 1

            # Insertar la parte derecha justo después
            lista.insertar_en(i + 1, Rango(valor_original, fin + 1, fin_original))

            # El nuevo rango va entre los dos pedazos (se inserta en i+1,
            # pero primero ponemos la parte derecha en i+2 para preservar orden)
            # En realidad el orden correcto de inserción es:
            #   posición i   → rango recortado izquierdo  (ya existe)
            #   posición i+1 → nuevo rango (val, ini, fin)
            #   posición i+2 → rango derecho
            # Como acabamos de insertar el derecho en i+1, lo desplazamos a i+2
            # insertando el nuevo en i+1:
            lista.insertar_en(i + 1, Rango(val, ini, fin))
            return  # ya no hay más rangos que procesar

    # ─── PASO 3: insertar el nuevo rango en la posición correcta ─────────────
    # Después de eliminar/recortar todos los rangos solapados, insertamos
    # (val, ini, fin) en la posición i para mantener el orden por .inicio.
    lista.insertar_en(i, Rango(val, ini, fin))
