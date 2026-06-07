# Motor de Consultas sobre Datos Comprimidos por Rangos
### Proyecto Final — Análisis y Diseño de Algoritmos I
**Universidad del Valle Sede Tuluá — 2025**

Integrantes:
- Paula Jimena Bohórquez Bermúdez – 202459409
- Manuela Delgado Aguirre – 202459640
- Juan Camilo Gil Agudelo – 202459531

---

## Descripción

Sistema que almacena y consulta eficientemente una secuencia de valores representada
mediante rangos comprimidos. Opera directamente sobre la representación comprimida
sin expandir la secuencia completa, lo que permite manejar dominios de hasta 10⁹ posiciones.

---

## Requisitos

- **Python 3.8 o superior**
- No se requieren librerías externas ni instalaciones adicionales.

Para verificar la versión de Python instalada:

```
python3 --version
```

---

## Archivos del proyecto

```
proyecto/
├── main.py             # Punto de entrada, dispatcher y operaciones VALUE, COUNT_RANGES, MERGE
├── lista_rangos.py     # Estructura ListaRangos, MergeSort y búsqueda binaria
├── rango.py            # Clase Rango
├── consultas.py        # Operaciones SUM, FREQUENCY, MAX_RANGE, MIN_RANGE, DECOMPRESS
├── modificaciones.py   # Operación UPDATE
├── entrada.txt         # Archivo de entrada con los datos y operaciones
└── README.md           # Este archivo
```

Todos los archivos deben estar en la **misma carpeta** para que el programa funcione correctamente.

---

## Instrucciones de ejecución

### Paso 1 — Preparar el archivo de entrada

El archivo `entrada.txt` debe tener el siguiente formato:

```
N
valor inicio fin
valor inicio fin
...
Q
OPERACION parametros
OPERACION parametros
...
```

Donde:
- `N` es la cantidad de rangos iniciales.
- Cada una de las `N` líneas siguientes define un rango con tres enteros: `valor inicio fin`.
- `Q` es la cantidad de operaciones a procesar.

**Ejemplo de entrada.txt:**

```
5
1 1 5
3 6 8
2 9 14
8 15 16
4 17 20
7
VALUE 10
SUM 1 10
UPDATE 6 8 5
FREQUENCY 2
MAX_RANGE 1 20
DECOMPRESS 1 12
COUNT_RANGES
```

### Paso 2 — Ejecutar el programa

Abrir una terminal en la carpeta del proyecto y ejecutar:

**En Linux / macOS:**
```
python3 main.py
```

**En Windows:**
```
python main.py
```

### Paso 3 — Ver los resultados

El programa genera automáticamente el archivo `salida.txt` en la misma carpeta.
La salida correspondiente al ejemplo anterior sería:

```
VALUE 10 = 2
SUM 1 10 = 21
UPDATE 6 8 5 = OK
FREQUENCY 2 = 6
MAX_RANGE 1 20 = 8
DECOMPRESS 1 12 = 1 1 1 1 1 5 5 5 2 2 2 2
COUNT_RANGES = 5
```

---

## Operaciones disponibles

| Operación | Parámetros | Descripción |
|---|---|---|
| `VALUE` | posicion | Retorna el valor en esa posición |
| `SUM` | inicio fin | Suma de valores en el intervalo |
| `FREQUENCY` | valor | Cantidad de posiciones con ese valor |
| `MAX_RANGE` | inicio fin | Valor máximo en el intervalo |
| `MIN_RANGE` | inicio fin | Valor mínimo en el intervalo |
| `DECOMPRESS` | inicio fin | Expande el intervalo posición a posición |
| `UPDATE` | inicio fin valor | Reemplaza el valor en el intervalo |
| `MERGE` | _(ninguno)_ | Fusiona rangos consecutivos con igual valor |
| `COUNT_RANGES` | _(ninguno)_ | Cantidad de rangos actuales |

---

## Notas importantes

- El programa **no requiere compilación**. Python es un lenguaje interpretado.
- El archivo `entrada.txt` debe estar en la misma carpeta que `main.py`.
- El archivo `salida.txt` se **sobreescribe** cada vez que se ejecuta el programa.
- Los rangos en `entrada.txt` pueden venir en cualquier orden; el sistema los ordena internamente.
- No se debe modificar ningún archivo `.py` para cambiar los datos de entrada; solo editar `entrada.txt`.
