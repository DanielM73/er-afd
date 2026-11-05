# Simulación y evaluación de la cadena

La evaluación inicia en `Q0` y lee la cadena de izquierda a derecha. Por cada carácter se busca una transición que salga del estado actual.

El recorrido se guarda en una lista para mostrarlo después con el formato solicitado:

```text
Q0|a|Q1
Q1|b|Q2
```

Después de consumir toda la cadena se revisa si el último estado pertenece al conjunto de estados finales. El programa muestra `Cadena aceptada` o `Cadena rechazada`.

La cadena solamente puede contener caracteres alfanuméricos ASCII y espacios. El punto funciona como cualquier símbolo y un conjunto negativo acepta cualquier carácter que no esté dentro de los excluidos.

El programa retorna el código `1` cuando la cadena es aceptada y `0` cuando es rechazada, siguiendo la indicación del proyecto.
