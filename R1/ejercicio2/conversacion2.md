# Conversación – Ejercicio 2 (B2: Gestión de trabajos de impresión)

**Concurso:** Prompt & Code Challenge 2026 – Ronda 1 – Categoría Básica  
**Equipo:** Bit-Master  
**Archivo de código asociado:** `codigo2.py`

> **Estado de evidencia:** este documento registra el análisis del enunciado y la estrategia de implementación disponible hasta el momento. A diferencia de B1, todavía no se han comunicado resultados de experimentos propios con la caja negra B2. No se presentan hipótesis como reglas confirmadas.

## 1. Enunciado analizado

La impresora recibe Q órdenes:

- `ADD id p`: agrega un trabajo pendiente con identificador y prioridad. Los identificadores no se repiten en ADD.
- `BOOST id x`: si el trabajo sigue pendiente, incrementa su prioridad e imprime `OK`; si no, imprime `NO`.
- `CANCEL id`: si el trabajo sigue pendiente, lo elimina e imprime `OK`; si no, imprime `NO`.
- `PRINT k`: imprime hasta k trabajos pendientes en orden de prioridad descendente, los elimina y muestra sus identificadores separados por espacios. Si no hay trabajos, imprime `VACIA`.

La salida contiene una línea por cada `BOOST`, `CANCEL` y `PRINT`. Los límites son Q hasta 10^6, id hasta 2·10^6, prioridad p hasta 10^9, incremento x hasta 10^18 y k hasta 10^6. El tiempo límite es 10 segundos y la memoria 256 MB.

## 2. Reglas que el enunciado deja por descubrir

El enunciado pide investigar con la caja negra:

1. Cómo se desempata cuando dos trabajos tienen la misma prioridad.
2. Si `BOOST` modifica algo además de la prioridad.
3. Si las prioridades cambian automáticamente con el tiempo.

Estas reglas deben verificarse experimentalmente antes de considerarlas confirmadas.

## 3. Hipótesis algorítmica inicial

Se propone una cola de prioridad (heap) para extraer el trabajo con mayor prioridad, junto con un diccionario para localizar rápidamente los trabajos pendientes por identificador.

Para evitar recorrer el heap al ejecutar `BOOST` o `CANCEL`, se utiliza eliminación diferida (*lazy deletion*):
- `BOOST` actualiza la prioridad en el diccionario y agrega una nueva entrada al heap.
- `CANCEL` elimina el trabajo del diccionario.
- Al ejecutar `PRINT`, se descartan entradas del heap que ya no correspondan a un trabajo pendiente o que tengan una versión antigua.

Complejidad esperada: O(Q log Q) en el peor caso, con operaciones de heap logarítmicas.

## 4. Política provisional de desempate

La implementación candidata conserva el orden original de llegada (`ADD`) como segundo criterio cuando dos prioridades son iguales. Esto equivale a FIFO entre trabajos con la misma prioridad.

**Importante:** es una hipótesis de implementación, no una regla confirmada por la caja negra. Debe probarse con dos o más trabajos de igual prioridad y con un caso donde `BOOST` provoque un empate.

## 5. Tratamiento provisional de BOOST

La implementación candidata aumenta la prioridad del trabajo pendiente y conserva su orden original de llegada para desempates. Se utiliza un contador de versión para invalidar entradas anteriores del heap.

**Importante:** aún falta comprobar si `BOOST` conserva el orden de llegada o si altera el orden de desempate, y si existe envejecimiento u otro cambio automático de prioridades.

## 6. Código candidato

El archivo `codigo2.py` implementa:
- Lectura desde entrada estándar.
- Escritura a salida estándar.
- Heap de prioridad descendente.
- Diccionario de trabajos pendientes.
- Actualización diferida para `BOOST`.
- Cancelación lógica para `CANCEL`.
- Impresión y eliminación de trabajos en `PRINT`.

## 7. Pruebas pendientes con la caja negra B2

Se deben ejecutar, como mínimo, estos experimentos pequeños:

### B2-P01: desempate de trabajos agregados en orden
```text
5
ADD 10 7
ADD 20 7
ADD 30 7
PRINT 3
PRINT 1
```
Permite observar el orden entre prioridades iguales.

### B2-P02: BOOST que produce empate
```text
4
ADD 10 5
ADD 20 8
BOOST 10 3
PRINT 2
```
Permite observar cómo se resuelve un empate después de BOOST.

### B2-P03: BOOST a trabajo inexistente o ya impreso
```text
4
ADD 10 5
PRINT 1
BOOST 10 2
CANCEL 10
```
Permite verificar que un trabajo deja de estar pendiente después de imprimirse.

### B2-P04: cancelación
```text
5
ADD 10 5
CANCEL 10
PRINT 1
BOOST 10 1
CANCEL 10
```
Permite verificar las respuestas y la eliminación del trabajo cancelado.

### B2-P05: posible cambio de prioridad con el tiempo
```text
6
ADD 10 1
ADD 20 2
PRINT 1
PRINT 1
ADD 30 1
PRINT 1
```
Este caso ayuda a observar el orden de impresión, aunque para demostrar envejecimiento se requieren experimentos diseñados con más precisión.

## 8. Estado de entrega

- [x] Enunciado B2 analizado.
- [x] Estrategia de heap y diccionario diseñada.
- [x] Código candidato `codigo2.py` generado.
- [x] Conversación/registro inicial `conversacion2.md` generado.
- [ ] Ejecutar los experimentos anteriores con la caja negra B2.
- [ ] Ajustar la regla de desempate y BOOST según resultados reales.
- [ ] Ejecutar los dos ejemplos oficiales B2.
- [ ] Confirmar el commit definitivo de `R1/ejercicio2/codigo2.py` y `conversacion2.md`.

