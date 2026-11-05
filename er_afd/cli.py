"""Inicio del programa desde la terminal."""

import sys

from er_afd.analizador import ErrorExpresion, analizar_expresion
from er_afd.afnd import construir_afnd, mostrar_afnd
from er_afd.afd import convertir_a_afd, mostrar_afd


def main():
    if len(sys.argv) != 3:
        print("Uso: er-afd <ER> <cadena>")
        return 0

    expresion = sys.argv[1]
    cadena = sys.argv[2]

    try:
        arbol = analizar_expresion(expresion)
    except ErrorExpresion as error:
        print("ER inválida")
        print(error)
        return 0

    afnd = construir_afnd(arbol)
    afd = convertir_a_afd(afnd)

    mostrar_afnd(afnd)
    mostrar_afd(afd)
    print("Cadena recibida:", repr(cadena))
    print("Todavía falta evaluar la cadena con el AFD.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

