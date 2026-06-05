from lista_rangos import buscar_primer_rango_que_llega

def frequency(lista, val):
    """
    Retorna la cantidad total de posiciones en la secuencia que tienen el valor val.
    Retorna 0 si ningún rango tiene ese valor.
    """
    contador = 0
    for i in range(lista.tamaño()):
        rango = lista.obtener(i)
        if rango.valor == val:
            contador += rango.longitud()
    return contador

def sum_rango(lista, ini, fin):
    """
    Retorna la suma de todos los valores entre las posiciones ini y fin (inclusive).
    Retorna 0 si el intervalo no cubre ningún rango.
    """
    total = 0
 
    # Saltar directamente al primer rango que podría solaparse con [ini, fin]
    i = buscar_primer_rango_que_llega(lista, ini)
 
    while i < lista.tamaño():
        rango = lista.obtener(i)
 
        # Si el rango empieza después de fin, ya no hay más solapamientos
        if rango.inicio > fin:
            break
 
        # Calcular el intersecto real entre el rango y [ini, fin]
        izq = max(rango.inicio, ini)
        der = min(rango.fin, fin)
 
        # Sumar la contribución de este rango
        total += rango.valor * (der - izq + 1)
 
        i += 1
 
    return total

def max_range(lista, ini, fin):
    """
    Retorna el valor máximo entre las posiciones ini y fin (inclusive).
    Retorna None si el intervalo no cubre ningún rango.
    """
    maximo = None
    i = buscar_primer_rango_que_llega(lista, ini)

    while i < lista.tamaño():
        rango = lista.obtener(i)

        if rango.inicio > fin:
            break

        if  maximo is None or rango.valor > maximo:
            maximo = rango.valor

        i += 1

    return maximo

def min_range(lista, ini, fin):
    """
    Retorna el valor mínimo entre las posiciones ini y fin (inclusive).
    Retorna None si el intervalo no cubre ningún rango.
    """
    minimo = None
    i = buscar_primer_rango_que_llega(lista, ini)

    while i < lista.tamaño():
        rango = lista.obtener(i)

        if rango.inicio > fin:
            break

        if  minimo is None or rango.valor < minimo:
            minimo = rango.valor

        i += 1

    return minimo

def decompress(lista, ini, fin):
    """
    Retorna una lista con los valores posición a posición entre ini y fin.
    Si una posición no está cubierta por ningún rango, se omite.
    """
    resultado = []
    i = buscar_primer_rango_que_llega(lista, ini)

    while i < lista.tamaño():
        rango = lista.obtener(i)

        if rango.inicio > fin:
            break

        # Calcular qué porción de este rango cae dentro de [ini, fin]
        izq = max(rango.inicio, ini)
        der = min(rango.fin, fin)

        # Repetir el valor tantas veces como posiciones haya en el intersecto
        for _ in range(izq, der + 1):
            resultado.append(rango.valor)

        i += 1

    return resultado

