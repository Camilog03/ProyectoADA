# =============================================================================
# rango.py — Clase Rango
# Proyecto ADA I — Problema 4: Motor de consultas sobre datos comprimidos
# Universidad del Valle Sede Tuluá
# =============================================================================


class Rango:
    """
    Representa un rango comprimido de la secuencia.

    Un rango indica que cierto 'valor' ocupa todas las posiciones
    entre 'inicio' y 'fin' (inclusive).

    Ejemplo:
        Rango(3, 6, 8) → el valor 3 ocupa las posiciones 6, 7 y 8.
        Rango(1, 1, 5) → el valor 1 ocupa las posiciones 1, 2, 3, 4 y 5.
    """

    def __init__(self, valor, inicio, fin):
        self.valor  = valor
        self.inicio = inicio
        self.fin    = fin

    def longitud(self):
        """
        Retorna cuántas posiciones ocupa este rango.
        Ejemplo: Rango(3, 6, 8).longitud() → 3
        """
        return self.fin - self.inicio + 1

    def contiene(self, posicion):
        """
        Retorna True si la posición dada cae dentro de este rango.
        Ejemplo: Rango(3, 6, 8).contiene(7) → True
        """
        return self.inicio <= posicion <= self.fin

    def __repr__(self):
        return f"Rango({self.valor}, {self.inicio}-{self.fin})"
