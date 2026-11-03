# ER-AFD

Proyecto para convertir expresiones regulares a un AFND mediante Thompson, transformar el AFND a AFD con construcción de subconjuntos y evaluar cadenas.

## Estado actual

El primer módulo está implementado:

- analizador descendente recursivo sin librerías de regex;
- representación sencilla con diccionarios y detección del alfabeto;
- operadores, conjuntos, rangos y escapes solicitados;
- programa provisional desde la terminal, Makefile y pruebas.

Los módulos Thompson, subconjuntos y simulación todavía deben agregarse. Por ahora se puede comprobar el módulo de entrada.

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

La explicación de este módulo se encuentra en `doc/01_modulo_entrada_er.md`.
