# Conversión del AFND a AFD

El AFND se convierte en AFD mediante la construcción de subconjuntos. Un estado del AFD representa un conjunto de estados del AFND.

## Cierre épsilon

El cierre épsilon de un estado contiene ese mismo estado y todos los estados que se pueden alcanzar utilizando solamente transiciones `ε`. El programa usa una lista y la recorre hasta que ya no aparecen estados nuevos.

## Movimiento por símbolo

Para cada símbolo del alfabeto se buscan las transiciones que salen de los estados del conjunto actual. Después se calcula el cierre épsilon de los estados alcanzados.

Si el conjunto todavía no existe, se agrega como un nuevo estado del AFD. Los estados se nombran `Q0`, `Q1`, `Q2` y así sucesivamente. `Q0` siempre corresponde al cierre épsilon del estado inicial del AFND.

Un estado del AFD es final cuando su conjunto contiene al estado final del AFND. Épsilon no se incluye en el alfabeto del AFD.

La salida utiliza el formato:

```text
Q0|símbolo|Q1
```
