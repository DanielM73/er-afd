"""Inicio del programa desde la terminal."""

import sys

from er_afd.analizador import ErrorExpresion, analizar_expresion
from er_afd.afnd import construir_afnd, mostrar_afnd
from er_afd.afd import convertir_a_afd, mostrar_afd
from er_afd.simulador import evaluar_cadena, mostrar_resultado, validar_cadena


def main():
    if len(sys.argv) != 3:
        print("Uso: er-afd <ER> <cadena>")
        return 2

    expresion = sys.argv[1]
    cadena = sys.argv[2]

    try:
        arbol = analizar_expresion(expresion)
    except ErrorExpresion as error:
        print("ER inválida")
        print(error)
        return 2

    if not validar_cadena(cadena):
        print("Cadena inválida: use solamente caracteres alfanuméricos ASCII y espacios")
        return 2

    afnd = construir_afnd(arbol)
    afd = convertir_a_afd(afnd)
    resultado = evaluar_cadena(afd, cadena)

    mostrar_afnd(afnd)
    mostrar_afd(afd)
    mostrar_resultado(resultado)

    if resultado["aceptada"]:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

