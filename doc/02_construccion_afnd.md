# Construcción del AFND con Thompson

Después de validar la expresión regular, el programa recorre la estructura obtenida y crea un AFND utilizando el algoritmo de Thompson.

Cada parte de la expresión produce un fragmento con un estado de inicio, un estado final y una lista de transiciones. Los estados se numeran con un contador sencillo para obtener `q0`, `q1`, `q2` y así sucesivamente.

## Casos utilizados

- Un símbolo crea dos estados y una transición entre ellos.
- Un conjunto crea una transición por cada carácter permitido.
- La unión crea un nuevo inicio y un nuevo final, conectados con transiciones épsilon.
- La concatenación conecta el final de un fragmento con el inicio del siguiente mediante épsilon.
- La cerradura de Kleene permite repetir el fragmento o pasar directamente al estado final.

El alfabeto conserva el orden en el que aparecen los símbolos en la expresión. Si épsilon no aparece escrito, se agrega al final del alfabeto del AFND, tal como solicita el proyecto.

La salida utiliza el formato:

```text
q0|símbolo|{q1,q2}
```
