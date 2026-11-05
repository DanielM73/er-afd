# ER-AFD

Proyecto para convertir expresiones regulares a un AFND mediante Thompson, transformar el AFND a AFD con construcción de subconjuntos y evaluar cadenas.

## Estado actual

El primer módulo está implementado:

- analizador descendente recursivo sin librerías de regex;
- representación sencilla con diccionarios y detección del alfabeto;
- operadores, conjuntos, rangos y escapes solicitados;
- programa provisional desde la terminal, Makefile y pruebas.

También está implementada la construcción del AFND mediante Thompson:

- estados `q0`, `q1`, ...;
- transiciones épsilon;
- unión, concatenación y cerradura de Kleene;
- conjuntos, rangos y escapes;
- tabla de transiciones con el formato solicitado.

La conversión del AFND a AFD también está implementada:

- cierre épsilon;
- movimiento por símbolo;
- construcción de subconjuntos;
- estados `Q0`, `Q1`, ...;
- tabla determinista sin transiciones épsilon.

El módulo de simulación todavía debe agregarse.

## Uso en Linux

```bash
make build
make test
make run ER='(a|b)*abb' CADENA='abb'
```

También puede ejecutarse directamente:

```bash
.venv/bin/er-afd '(a|b)*abb' 'abb'
```

Las explicaciones de los módulos se encuentran dentro de la carpeta `doc`.
