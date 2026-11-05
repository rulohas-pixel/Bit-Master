# Ronda 2 – Ejercicio 1 (BF: Ventas masivas)
## Registro técnico de trabajo y pruebas

> **Nota de integridad:** Este archivo es una bitácora técnica reconstruida a partir de los mensajes, capturas y resultados disponibles en la conversación. No es una exportación literal completa del historial de ChatGPT. Se registran los pasos y resultados observados; no se atribuyen pruebas que no se hayan ejecutado.

## 1. Objetivo y límites comunicados

El ejercicio de la ronda final corresponde a **BF – Ventas masivas**. En las diapositivas del concurso se comunicaron estos límites:

- Hasta 3 millones de líneas de entrada (aproximadamente 90 MB de texto).
- Memoria máxima: 64 MB.
- Tiempo máximo: 16 segundos.
- La evaluación de la ronda es independiente de la ronda 1.
- La entrega se realiza en el mismo repositorio de GitHub de la ronda 1, agregando `R2/ejercicio1/`.
- Los nombres de entrega deben ser exactamente `codigo1` y `conversacion1`; para el código se permite Python, C o C++, y la conversación puede ser `.md`, `.txt` o `.json`.
- No modificar `R1/`, porque ello podría alterar la hora de entrega de la ronda 1.

## 2. Estructura requerida

```text
nombre-equipo/
├── R1/                         # No modificar
└── R2/
    └── ejercicio1/
        ├── codigo1.py
        └── conversacion1.md
```

La carpeta `R2/ejercicio1/` debe estar en el repositorio remoto y los cambios deben enviarse con `git push`. La hora de entrega corresponde al último commit de esta carpeta.

## 3. Entorno de pruebas

Se trabajó en Windows PowerShell, desde:

```text
C:\Users\Raul\Downloads\Ronda2_Basica\Ronda2_Basica\BF
```

La caja negra utilizada fue `caja_windows.exe`. Para enviar entradas de prueba directamente desde PowerShell se utilizó el formato:

```powershell
@'
ENTRADA
'@ | .\caja_windows.exe
```

El programa Python se ejecutó con:

```powershell
@'
ENTRADA
'@ | python ".\codigo1 (1).py"
```

Durante las pruebas el archivo local se llamó `codigo1 (1).py`. Para la entrega se debe copiar/guardar su contenido como `codigo1.py` dentro de `R2/ejercicio1/`.

## 4. Reglas inferidas y contrastadas con la caja negra

Las siguientes observaciones se obtuvieron comparando la salida de `caja_windows.exe` con la salida del programa Python:

### 4.1 Acumulación por producto y cantidades negativas

Entrada probada:

```text
2028-01-01 2028-12-31
4
2028-03-01,100,7,10
2028-03-01,101,7,15
2028-03-02,102,3,8
2028-03-03,103,7,-5
```

Salida observada en la caja negra y en Python:

```text
7 20
3 8
```

La prueba confirma, para este caso, que las cantidades se acumulan por producto y que una cantidad negativa afecta el total acumulado.

### 4.2 Identificadores de venta duplicados

Entrada probada:

```text
2028-01-01 2028-12-31
5
2028-03-01,100,7,10
2028-03-02,100,7,10
2028-03-03,101,7,5
2028-03-04,102,3,8
2028-03-05,103,3,2
```

Salida de ambos programas:

```text
7 15
3 10
```

El identificador `100` no se contabilizó dos veces.

### 4.3 Qué aparición prevalece si el duplicado tiene datos distintos

Entrada probada:

```text
2028-01-01 2028-12-31
3
2028-03-01,200,7,10
2028-03-02,200,3,99
2028-03-03,201,7,5
```

Salida de ambos programas:

```text
7 15
```

La evidencia indica que se conserva la primera aparición válida del identificador `200`; la segunda aparición, aunque indique otro producto y cantidad, se ignora.

### 4.4 Duplicado cuya primera aparición está fuera del intervalo

Entrada probada:

```text
2028-03-01 2028-03-31
3
2028-02-20,300,7,100
2028-03-01,300,3,50
2028-03-02,301,3,8
```

Salida de ambos programas:

```text
3 8
```

La evidencia indica que el identificador `300` queda reservado por su primera aparición válida aunque la fecha de esa aparición esté fuera del intervalo. Por ello, la segunda aparición no se considera.

## 5. Implementación actual

La solución utiliza:

- `sys.stdin.buffer.readline` para leer desde la entrada estándar en modo binario.
- `bytearray` para marcar identificadores de venta ya utilizados.
- Una lista indexada por identificador de producto para acumular cantidades.
- Validación manual de fechas ISO `YYYY-MM-DD`, incluidos los años bisiestos.
- Comparación lexicográfica de fechas ISO para aplicar el intervalo inclusivo.
- Un recorrido de los identificadores de producto para seleccionar los tres mejores sin ordenar toda la colección.
- Desempate por identificador de producto ascendente, según la lógica implementada.

### Complejidad de la estrategia

- Procesamiento de registros: O(n), suponiendo operaciones de tamaño acotado.
- Selección de los tres mejores: O(P), donde P es el máximo identificador de producto recorrido (100 000 en el código).
- Memoria auxiliar principal: un `bytearray` de 4 000 001 bytes para los IDs de venta y una lista de 100 001 posiciones para acumulados, además de los objetos y buffers propios de Python.

Estas cotas describen la estructura del código; **no constituyen una medición de memoria máxima ni una garantía de cumplir 64 MB**.

## 6. Código entregado en este directorio

`codigo1.py` contiene la versión funcional que se comparó con la caja negra en los casos descritos. Se conserva la lógica que produjo coincidencias en las pruebas observadas.

## 7. Estado de validación y limitaciones conocidas

Pruebas pequeñas contrastadas con la caja negra:

- Ejemplos oficiales `ejemplo1.in` y `ejemplo2.in`: se reportó coincidencia de las salidas.
- Acumulación de cantidades y cantidad negativa: coincidencia.
- Duplicado del mismo identificador: coincidencia.
- Duplicado con producto/cantidad diferentes: coincidencia.
- Primera aparición fuera del intervalo y segunda dentro: coincidencia.

No se ha documentado una prueba de estrés con 3 millones de registros, una medición de tiempo de 16 segundos ni una medición de memoria de 64 MB. Por tanto, no debe afirmarse que esos límites ya están superados.

## 8. Comandos de compilación/ejecución y entrega

Desde la carpeta `BF`, la ejecución local usada fue:

```powershell
Get-Content .\ejemplo1.in | python ".\codigo1 (1).py"
Get-Content .\ejemplo2.in | python ".\codigo1 (1).py"
```

Para la carpeta de entrega, una vez copiados los archivos:

```powershell
git add R2/ejercicio1/codigo1.py R2/ejercicio1/conversacion1.md
git commit -m "Entrega R2 ejercicio 1"
git push
```

Antes de enviar, verificar en GitHub que aparezcan exactamente:

```text
R2/ejercicio1/codigo1.py
R2/ejercicio1/conversacion1.md
```

y que `R1/` permanezca sin modificaciones.
