"""Conversión básica de AFND a AFD con construcción de subconjuntos."""


def convertir_a_afd(afnd):
    alfabeto = []

    for simbolo in afnd["alfabeto"]:
        if simbolo != "ε":
            alfabeto.append(simbolo)

    inicial = cierre_epsilon([afnd["inicial"]], afnd)
    conjuntos = [inicial]
    transiciones = []
    posicion = 0

    while posicion < len(conjuntos):
        conjunto_actual = conjuntos[posicion]

        for simbolo in alfabeto:
            alcanzados = mover(conjunto_actual, simbolo, afnd)
            destino = cierre_epsilon(alcanzados, afnd)
            numero_destino = buscar_conjunto(conjuntos, destino)

            if numero_destino == -1:
                conjuntos.append(destino)
                numero_destino = len(conjuntos) - 1

            transiciones.append({
                "origen": posicion,
                "simbolo": simbolo,
                "destino": numero_destino
            })

        posicion = posicion + 1

    finales = []

    for numero in range(len(conjuntos)):
        conjunto = conjuntos[numero]

        if contiene_final(conjunto, afnd["finales"]):
            finales.append(numero)

    estados = []

    for numero in range(len(conjuntos)):
        estados.append(numero)

    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "transiciones": transiciones,
        "inicial": 0,
        "finales": finales,
        "conjuntos": conjuntos
    }


def cierre_epsilon(estados, afnd):
    cierre = []

    for estado in estados:
        if estado not in cierre:
            cierre.append(estado)

    posicion = 0

    while posicion < len(cierre):
        estado_actual = cierre[posicion]

        for transicion in afnd["transiciones"]:
            sale_del_estado = transicion["origen"] == estado_actual
            es_epsilon = transicion["simbolo"] == "ε"

            if sale_del_estado and es_epsilon:
                destino = transicion["destino"]

                if destino not in cierre:
                    cierre.append(destino)

        posicion = posicion + 1

    cierre.sort()
    return cierre


def mover(estados, simbolo, afnd):
    alcanzados = []

    for estado in estados:
        for transicion in afnd["transiciones"]:
            mismo_estado = transicion["origen"] == estado
            mismo_simbolo = simbolos_compatibles(transicion["simbolo"], simbolo)

            if mismo_estado and mismo_simbolo:
                destino = transicion["destino"]

                if destino not in alcanzados:
                    alcanzados.append(destino)

    alcanzados.sort()
    return alcanzados


def simbolos_compatibles(simbolo_transicion, simbolo_alfabeto):
    if simbolo_transicion == simbolo_alfabeto:
        return True

    if es_conjunto_negativo(simbolo_alfabeto):
        return simbolo_transicion == "."

    if simbolo_alfabeto == ".":
        return False

    if simbolo_transicion == ".":
        return True

    if es_conjunto_negativo(simbolo_transicion):
        return acepta_conjunto_negativo(simbolo_transicion, simbolo_alfabeto)

    return False


def es_conjunto_negativo(simbolo):
    return simbolo.startswith("[^") and simbolo.endswith("]")


def acepta_conjunto_negativo(simbolo, caracter):
    excluidos = simbolo[2:-1]
    return caracter not in excluidos


def buscar_conjunto(conjuntos, buscado):
    posicion = 0

    while posicion < len(conjuntos):
        if conjuntos[posicion] == buscado:
            return posicion

        posicion = posicion + 1

    return -1


def contiene_final(conjunto, finales_afnd):
    for estado in conjunto:
        if estado in finales_afnd:
            return True

    return False


def formatear_afd(afd):
    lineas = []
    lineas.append("AFD")
    lineas.append("Q={" + unir_estados(afd["estados"]) + "}")
    lineas.append("Σ={" + ",".join(afd["alfabeto"]) + "}")
    lineas.append("F={" + unir_estados(afd["finales"]) + "}")

    for transicion in afd["transiciones"]:
        origen = "Q" + str(transicion["origen"])
        simbolo = transicion["simbolo"]
        destino = "Q" + str(transicion["destino"])
        lineas.append(origen + "|" + simbolo + "|" + destino)

    return "\n".join(lineas)


def unir_estados(estados):
    nombres = []

    for estado in estados:
        nombres.append("Q" + str(estado))

    return ",".join(nombres)


def mostrar_afd(afd):
    print(formatear_afd(afd))
