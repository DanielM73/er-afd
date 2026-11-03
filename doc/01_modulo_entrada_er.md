# Módulo de entrada de expresiones regulares

Este módulo recibe la expresión regular escrita por el usuario y revisa que su estructura sea válida. Se hizo con un analizador descendente recursivo sencillo y no utiliza la librería `re` de Python.

El programa lee la expresión de izquierda a derecha. Para guardar el resultado utiliza diccionarios, listas y cadenas. Estas estructuras son suficientes para que después el algoritmo de Thompson pueda construir el AFND.

## Elementos reconocidos

- Concatenación implícita, por ejemplo `ab`.
- Unión con `|`.
- Cerradura de Kleene con `*`.
- Paréntesis para cambiar la precedencia.
- Punto `.` para cualquier símbolo.
- Épsilon `ε`.
- Conjuntos como `[abc]`.
- Conjuntos negativos como `[^abc]`.
- Rangos como `[a-z]`.
- Caracteres escapados como `\*`, `\p` y `\\`.
- Dígitos con `\N`.
- Caracteres ASCII hexadecimales con `\h`, por ejemplo `\h20` y `\h41`.
- Letras mayúsculas con `\A`.
- Letras minúsculas con `\a`.
- Letras mayúsculas o minúsculas con `\z`.

## Orden de las operaciones

Primero se resuelven los paréntesis. Después se aplica la cerradura de Kleene, luego la concatenación y al final la unión. Con esto una expresión como `a|bc*` se interpreta como la unión entre `a` y la concatenación de `b` con `c*`.

## Errores revisados

El módulo detecta expresiones vacías, paréntesis sin cerrar, conjuntos vacíos, conjuntos sin cerrar, rangos escritos al revés, uniones incompletas y escapes hexadecimales incorrectos. Cuando encuentra un problema muestra la posición aproximada del error.

## Ejecución actual

```bash
make build
make test
make run ER='(a|b)*abb' CADENA='abb'
```

En esta etapa el programa valida la expresión y muestra la estructura encontrada. La construcción del AFND y del AFD se agregará en los siguientes módulos.
