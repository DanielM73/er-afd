"""Evaluación de una cadena utilizando el AFD."""


def validar_cadena(cadena):
    for caracter in cadena:
        es_ascii = caracter.isascii()
        es_permitido = caracter.isalnum() or caracter == " "

        if not es_ascii or not es_permitido:
            return False

    return True


def evaluar_cadena(afd, cadena):
    estado_actual = afd["inicial"]
    recorrido = []

    for caracter in cadena:
        destino = buscar_destino(afd, estado_actual, caracter)

        recorrido.append({
            "origen": estado_actual,
            "simbolo": caracter,
            "destino": destino
        })

        if destino is None:
            return {
                "aceptada": False,
                "recorrido": recorrido
            }

        estado_actual = destino

    aceptada = estado_actual in afd["finales"]

    return {
        "aceptada": aceptada,
        "recorrido": recorrido
    }


def buscar_destino(afd, estado, caracter):
    destino_exacto = None
    destino_negado = None
    destino_cualquiera = None

    for transicion in afd["transiciones"]:
        if transicion["origen"] != estado:
            continue

        simbolo = transicion["simbolo"]

        if simbolo == caracter:
            destino_exacto = transicion["destino"]

        elif es_conjunto_negativo(simbolo):
            if acepta_conjunto_negativo(simbolo, caracter):
                destino_negado = transicion["destino"]

        elif simbolo == ".":
            destino_cualquiera = transicion["destino"]

    if destino_exacto is not None:
        return destino_exacto

    if destino_negado is not None:
        return destino_negado

    return destino_cualquiera


def es_conjunto_negativo(simbolo):
    return simbolo.startswith("[^") and simbolo.endswith("]")


def acepta_conjunto_negativo(simbolo, caracter):
    excluidos = simbolo[2:-1]
    return caracter not in excluidos


def mostrar_resultado(resultado):
    for paso in resultado["recorrido"]:
        origen = "Q" + str(paso["origen"])

        if paso["destino"] is None:
            destino = "∅"
        else:
            destino = "Q" + str(paso["destino"])

        print(origen + "|" + paso["simbolo"] + "|" + destino)

    if resultado["aceptada"]:
        print("Cadena aceptada")
    else:
        print("Cadena rechazada")
