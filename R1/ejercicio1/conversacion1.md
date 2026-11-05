# Conversación – Ejercicio 1 (B1: Sensores y rachas estables)

**Concurso:** Prompt & Code Challenge 2026 – Ronda 1 – Categoría Básica  
**Equipo:** Bit-Master  
**Archivo de código asociado:** `codigo1.py`  
**Propósito:** Registrar cronológicamente el trabajo de análisis, prompting, experimentación con la caja negra y desarrollo de la solución.

> **Nota de integridad:** Este documento organiza las interacciones y resultados del trabajo de B1 que están disponibles en esta conversación. Los resultados de la caja negra se consignan tal como fueron comunicados por el participante. No se inventan salidas. Si la organización exige una exportación literal del chat completo de la plataforma, debe adjuntarse además la exportación nativa correspondiente.

---

## 1. Enunciado y estrategia inicial

### Participante
Compartió el PDF `Ronda1_Basica.pdf`, que contiene los problemas B1 y B2, ejemplos oficiales y las instrucciones para ejecutar la caja negra.

### Asistente
Identificó que B1 pide encontrar la racha más larga de sensores consecutivos y devolver longitud y posición inicial. Señaló que el enunciado deja tres reglas por descubrir:
1. Significado de “estable con tolerancia K”.
2. Tratamiento de sensores consecutivos.
3. Tratamiento de lecturas perdidas `?`.

Planteó como hipótesis inicial que la estabilidad podría depender del rango de valores de la ventana:

`máximo - mínimo <= K`

y propuso investigar la hipótesis con pruebas pequeñas antes de programar.

---

## 2. Preparación y ejecución de la caja negra

### Participante
Compartió las instrucciones oficiales para ejecutar la caja negra en Windows, Linux y macOS.

### Asistente
Explicó que, en Windows, se podía ejecutar el programa desde PowerShell con una redirección de entrada. Inicialmente se presentó un error porque PowerShell se encontraba en `C:\WINDOWS\System32` y el ejecutable no estaba en esa carpeta.

### Participante
Compartió capturas de PowerShell, Visual Studio Code y el Explorador de archivos. En ellas se observó que el ejecutable y los ejemplos estaban en:

`Downloads\Ronda1_Basica\Ronda1_Basica\B1`

Los archivos visibles incluían `caja_windows`, `ejemplo1.in`, `ejemplo1.out`, `ejemplo2.in`, `ejemplo2.out` y `enunciado`.

### Asistente
Indicó abrir PowerShell desde la carpeta `B1` y ejecutar:

```powershell
Get-Content .\ejemplo1.in | .\caja_windows.exe
Get-Content .\ejemplo1.out
Get-Content .\ejemplo2.in | .\caja_windows.exe
Get-Content .\ejemplo2.out
```

### Participante
Confirmó que las salidas de la caja negra coincidían con los archivos oficiales:

**Ejemplo 1:**
```text
2 1
6 1
2 2
```

**Ejemplo 2:**
```text
3 1
2 4
```

### Conclusión
Se verificó que el ejecutable de B1 funcionaba y que el procedimiento de entrada/salida era correcto.

---

## 3. Experimentos para descubrir las reglas ocultas

### B1-P01 – ¿Se comparan solamente sensores consecutivos?

**Entrada ejecutada:**
```text
1
3 1
1 2 3
```

**Salida comunicada por el participante:**
```text
2 1
```

**Interpretación:** si solo se compararan las diferencias entre vecinos, la secuencia completa podría mantenerse porque cada salto es 1. La salida de longitud 2 descarta esa interpretación simple y es consistente con una condición basada en el rango máximo-mínimo.

**Estado:** evidencia favorable para `máximo - mínimo <= K`; no constituye por sí sola una demostración completa.

### B1-P02 – ¿La igualdad con K está permitida?

**Entrada ejecutada:**
```text
1
2 2
1 3
```

**Salida comunicada por el participante:**
```text
2 1
```

**Interpretación:** una diferencia exactamente igual a K es aceptada. La condición candidata utiliza `<= K`, no `< K`.

**Estado:** confirmado para este caso.

### B1-P03 – ¿Qué ocurre con una lectura perdida?

**Entrada ejecutada:**
```text
1
4 10
1 2 ? 3
```

**Salida comunicada por el participante:**
```text
4 1
```

**Interpretación:** el símbolo `?` no rompe necesariamente la racha. En este caso las cuatro posiciones se cuentan dentro de la racha.

**Estado:** confirmado para este caso.

### B1-P04 – ¿Las lecturas perdidas cuentan y se ignoran al comparar?

**Entrada ejecutada:**
```text
1
3 0
1 ? 1
```

**Salida comunicada por el participante:**
```text
3 1
```

**Interpretación:** las tres posiciones cuentan para la longitud y la lectura perdida no participa en el cálculo numérico. Las dos lecturas válidas iguales forman una ventana estable con K=0.

**Estado:** evidencia fuerte para la hipótesis.

### B1-P05 – ¿Las lecturas válidas separadas por `?` siguen sujetas a K?

**Entrada ejecutada:**
```text
1
3 1
1 ? 3
```

**Salida comunicada por el participante:**
```text
2 1
```

**Interpretación:** las posiciones 1 y 2 forman una racha de longitud 2; las posiciones 2 y 3 también podrían formar una racha de longitud 2. La secuencia completa no es estable porque la diferencia entre las lecturas válidas 1 y 3 es 2, superior a K=1. La salida selecciona la posición inicial menor.

**Estado:** evidencia favorable a que las lecturas válidas de toda la ventana deben satisfacer el rango máximo-mínimo, incluso cuando hay `?` entre ellas. También es consistente con desempate por menor posición inicial.

### B1-P06 – ¿Qué ocurre si todas las lecturas se pierden?

**Entrada ejecutada:**
```text
1
4 0
? ? ? ?
```

**Salida comunicada por el participante:**
```text
4 1
```

**Interpretación:** una ventana sin ninguna lectura válida se considera estable; todas las posiciones cuentan y la longitud es 4.

**Estado:** confirmado para este caso.

---

## 4. Reglas de trabajo inferidas para B1

A partir de las pruebas anteriores se adoptó el siguiente modelo:

1. Una ventana es estable si no tiene lecturas válidas o si la diferencia entre su lectura válida máxima y mínima es menor o igual que K.
2. Los elementos `?` cuentan para la longitud de la ventana.
3. Los elementos `?` no participan en el cálculo del mínimo ni del máximo.
4. Los elementos `?` no rompen automáticamente la continuidad.
5. Se maximiza la longitud de la ventana.
6. En caso de empate, se conserva la ventana con menor posición inicial.

La condición candidata es:

`si hay lecturas válidas: max(lecturas) - min(lecturas) <= K`

Esta regla se infirió mediante las pruebas indicadas; se recomienda contrastarla con más casos si el tiempo disponible lo permite.

---

## 5. Diseño del algoritmo

### Participante
Aceptó avanzar a la implementación después de realizar las pruebas experimentales.

### Asistente
Propuso una ventana deslizante (*sliding window*) con dos deques monotónicas:
- Una deque mantiene los índices de lecturas candidatas a mínimo.
- Otra deque mantiene los índices de lecturas candidatas a máximo.
- Los `?` avanzan la ventana y cuentan en la longitud, pero no se insertan en las deques.
- Cuando `máximo - mínimo > K`, se mueve el límite izquierdo hasta recuperar estabilidad.
- Solo se actualiza la mejor respuesta cuando la longitud es estrictamente mayor, preservando así la primera posición en caso de empate.

También se propuso convertir los decimales a enteros escalados por `10^6` para evitar errores de punto flotante.

---

## 6. Implementación y corrección

Se preparó una implementación candidata en Python con:
- Lectura desde entrada estándar y escritura a salida estándar.
- Conversión decimal exacta a enteros escalados.
- Ventana deslizante.
- Deques monotónicas para mínimos y máximos.
- Arreglos compactos para reducir memoria.

El archivo final de esta iteración es `codigo1.py`.

### Validaciones locales comunicadas
Se ejecutaron pruebas locales con:
- Ejemplo oficial 1.
- Ejemplo oficial 2.
- Todas las lecturas perdidas.
- Valores negativos.
- Tolerancia cero.
- Seis decimales.
- Lectura perdida intermedia.

Las siete pruebas devolvieron las salidas esperadas en la validación local.

**Limitación:** la validación local no sustituye la comparación final ejecutando `codigo1.py` en la computadora del participante contra los archivos `.in` y `.out` originales ni la prueba de rendimiento máxima.

---

## 7. Comandos para validar en Windows

Desde la carpeta que contiene `codigo1.py`, y suponiendo que los ejemplos están en `B1`, se indicó ejecutar:

```powershell
$B1 = "$HOME\Downloads\Ronda1_Basica\Ronda1_Basica\B1"
Get-Content "$B1\ejemplo1.in" | python .\codigo1.py
Get-Content "$B1\ejemplo2.in" | python .\codigo1.py
```

Para comparar con los archivos de salida oficiales:

```powershell
$B1 = "$HOME\Downloads\Ronda1_Basica\Ronda1_Basica\B1"
$real = Get-Content "$B1\ejemplo1.in" | python .\codigo1.py
$esperado = Get-Content "$B1\ejemplo1.out"
Compare-Object $esperado $real
```

Si `Compare-Object` no muestra diferencias, las líneas comparadas coinciden.

---

## 8. Estado de entrega

- [x] Enunciado B1 analizado.
- [x] Caja negra ejecutada correctamente.
- [x] Dos ejemplos oficiales de la caja negra comprobados por el participante.
- [x] Experimentos B1-P01 a B1-P06 ejecutados.
- [x] Hipótesis algorítmica formulada.
- [x] Código Python candidato generado.
- [x] Siete pruebas locales realizadas.
- [ ] Ejecutar el archivo descargado en la computadora del participante contra ambos `.in` y comparar con ambos `.out`.
- [ ] Confirmar el commit definitivo de `R1/ejercicio1/codigo1.py`.
- [ ] Confirmar que este archivo `conversacion1.md` quedó subido al repositorio.

