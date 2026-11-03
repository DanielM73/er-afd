"""Inicio del programa desde la terminal."""

import sys

from er_afd.analizador import ErrorExpresion, analizar_expresion
from er_afd.analizador import mostrar_arbol, obtener_alfabeto


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

    print("ER válida")
    print("Alfabeto:", obtener_alfabeto(arbol))
    mostrar_arbol(arbol)
    print("Cadena recibida:", repr(cadena))
    print("Todavía falta construir el AFND y el AFD.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

