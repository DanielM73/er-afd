"""Casos completos para calcular la precisión del programa."""

from er_afd.afd import convertir_a_afd
from er_afd.afnd import construir_afnd
from er_afd.analizador import analizar_expresion
from er_afd.simulador import evaluar_cadena


CASOS = [
    ("a", "a", True),
    ("a", "b", False),
    ("ab", "ab", True),
    ("ab", "a", False),
    ("a|b", "a", True),
    ("a|b", "b", True),
    ("a|b", "c", False),
    ("a*", "", True),
    ("a*", "aaaa", True),
    ("a*", "aaab", False),
    ("(ab)*", "abab", True),
    ("(a|b)c", "ac", True),
    ("(a|b)c", "bc", True),
    ("(a|b)c", "abc", False),
    ("[abc]", "b", True),
    ("[a-c]", "c", True),
    ("[a-c]", "d", False),
    ("[^abc]", "d", True),
    ("[^abc]", "a", False),
    (r"\N", "7", True),
    (r"\N\N", "42", True),
    (r"\A", "Z", True),
    (r"\A", "z", False),
    (r"\a", "z", True),
    (r"\z", "A", True),
    (r"\h41", "A", True),
    (".", "8", True),
    ("hola mundo", "hola mundo", True),
    ("aεb", "ab", True),
    ("(a|b)*abb", "ababb", True),
    ("(a|b)*abb", "ababa", False),
    ("aX|.Y", "aY", True),
    ("aX|.Y", "bY", True),
    ("aX|[^b]Y", "aY", True),
    ("aX|[^b]Y", "bY", False),
    (r"[a-z]\N", "m5", True)
]


def ejecutar_caso(expresion, cadena):
    arbol = analizar_expresion(expresion)
    afnd = construir_afnd(arbol)
    afd = convertir_a_afd(afnd)
    resultado = evaluar_cadena(afd, cadena)
    return resultado["aceptada"]


def texto_resultado(valor):
    if valor:
        return "Aceptada"

    return "Rechazada"


def main():
    correctos = 0
    numero = 1

    print("PRUEBAS DE PRECISIÓN")
    print("No. | ER | Cadena | Esperado | Obtenido | Estado")

    for expresion, cadena, esperado in CASOS:
        obtenido = ejecutar_caso(expresion, cadena)

        if obtenido == esperado:
            estado = "OK"
            correctos = correctos + 1
        else:
            estado = "FALLO"

        fila = str(numero) + " | " + expresion + " | " + repr(cadena)
        fila = fila + " | " + texto_resultado(esperado)
        fila = fila + " | " + texto_resultado(obtenido)
        fila = fila + " | " + estado
        print(fila)
        numero = numero + 1

    total = len(CASOS)
    precision = correctos * 100 / total
    print()
    print("Casos correctos: " + str(correctos) + " de " + str(total))
    print("Precisión: " + format(precision, ".2f") + "%")

    if correctos == total:
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
