"""Construcción básica de un AFND con el algoritmo de Thompson."""

from er_afd.analizador import obtener_alfabeto


def construir_afnd(arbol):
    contador = {"numero": 0}
    fragmento = construir_fragmento(arbol, contador)

    estados = []
    numero = 0

    while numero < contador["numero"]:
        estados.append(numero)
        numero = numero + 1

    alfabeto = obtener_alfabeto(arbol)

    if "ε" not in alfabeto:
        alfabeto.append("ε")

    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "transiciones": fragmento["transiciones"],
        "inicial": fragmento["inicio"],
        "finales": [fragmento["fin"]]
    }


def construir_fragmento(nodo, contador):
    tipo = nodo["tipo"]

    if tipo == "literal":
        return fragmento_simbolo(nodo["valor"], contador)

    if tipo == "cualquiera":
        return fragmento_simbolo(".", contador)

    if tipo == "epsilon":
        return fragmento_simbolo("ε", contador)

    if tipo == "conjunto":
        return fragmento_conjunto(nodo, contador)

    if tipo == "union":
        return fragmento_union(nodo, contador)

    if tipo == "concatenacion":
        return fragmento_concatenacion(nodo, contador)

    if tipo == "kleene":
        return fragmento_kleene(nodo, contador)

    raise ValueError("No se reconoce el tipo de nodo: " + tipo)


def fragmento_simbolo(simbolo, contador):
    inicio = nuevo_estado(contador)
    fin = nuevo_estado(contador)

    transiciones = []
    transiciones.append(crear_transicion(inicio, simbolo, fin))

    return {
        "inicio": inicio,
        "fin": fin,
        "transiciones": transiciones
    }


def fragmento_conjunto(nodo, contador):
    inicio = nuevo_estado(contador)
    fin = nuevo_estado(contador)
    transiciones = []

    if nodo["negado"]:
        simbolo = "[^" + "".join(nodo["caracteres"]) + "]"
        transiciones.append(crear_transicion(inicio, simbolo, fin))
    else:
        for caracter in nodo["caracteres"]:
            transiciones.append(crear_transicion(inicio, caracter, fin))

    return {
        "inicio": inicio,
        "fin": fin,
        "transiciones": transiciones
    }


def fragmento_union(nodo, contador):
    inicio = nuevo_estado(contador)
    fin = nuevo_estado(contador)
    transiciones = []

    for hijo in nodo["hijos"]:
        parte = construir_fragmento(hijo, contador)
        transiciones.append(crear_transicion(inicio, "ε", parte["inicio"]))
        transiciones.extend(parte["transiciones"])
        transiciones.append(crear_transicion(parte["fin"], "ε", fin))

    return {
        "inicio": inicio,
        "fin": fin,
        "transiciones": transiciones
    }


def fragmento_concatenacion(nodo, contador):
    partes = nodo["hijos"]
    primera = construir_fragmento(partes[0], contador)

    inicio = primera["inicio"]
    fin_anterior = primera["fin"]
    transiciones = list(primera["transiciones"])

    posicion = 1

    while posicion < len(partes):
        siguiente = construir_fragmento(partes[posicion], contador)
        transiciones.append(crear_transicion(fin_anterior, "ε", siguiente["inicio"]))
        transiciones.extend(siguiente["transiciones"])
        fin_anterior = siguiente["fin"]
        posicion = posicion + 1

    return {
        "inicio": inicio,
        "fin": fin_anterior,
        "transiciones": transiciones
    }


def fragmento_kleene(nodo, contador):
    inicio = nuevo_estado(contador)
    fin = nuevo_estado(contador)
    parte = construir_fragmento(nodo["hijo"], contador)

    transiciones = []
    transiciones.append(crear_transicion(inicio, "ε", parte["inicio"]))
    transiciones.append(crear_transicion(inicio, "ε", fin))
    transiciones.extend(parte["transiciones"])
    transiciones.append(crear_transicion(parte["fin"], "ε", parte["inicio"]))
    transiciones.append(crear_transicion(parte["fin"], "ε", fin))

    return {
        "inicio": inicio,
        "fin": fin,
        "transiciones": transiciones
    }


def nuevo_estado(contador):
    estado = contador["numero"]
    contador["numero"] = contador["numero"] + 1
    return estado


def crear_transicion(origen, simbolo, destino):
    return {
        "origen": origen,
        "simbolo": simbolo,
        "destino": destino
    }


def agrupar_transiciones(transiciones):
    filas = []

    for transicion in transiciones:
        fila_encontrada = None

        for fila in filas:
            mismo_origen = fila["origen"] == transicion["origen"]
            mismo_simbolo = fila["simbolo"] == transicion["simbolo"]

            if mismo_origen and mismo_simbolo:
                fila_encontrada = fila
                break

        if fila_encontrada is None:
            nueva_fila = {
                "origen": transicion["origen"],
                "simbolo": transicion["simbolo"],
                "destinos": [transicion["destino"]]
            }
            filas.append(nueva_fila)
        elif transicion["destino"] not in fila_encontrada["destinos"]:
            fila_encontrada["destinos"].append(transicion["destino"])

    return filas


def formatear_afnd(afnd):
    lineas = []
    lineas.append("AFND")
    lineas.append("Q={" + unir_estados(afnd["estados"], "q") + "}")
    lineas.append("Σ={" + ",".join(afnd["alfabeto"]) + "}")
    lineas.append("F={" + unir_estados(afnd["finales"], "q") + "}")

    filas = agrupar_transiciones(afnd["transiciones"])

    for fila in filas:
        origen = "q" + str(fila["origen"])
        simbolo = fila["simbolo"]
        destinos = unir_estados(fila["destinos"], "q")
        lineas.append(origen + "|" + simbolo + "|{" + destinos + "}")

    return "\n".join(lineas)


def unir_estados(estados, prefijo):
    nombres = []

    for estado in estados:
        nombres.append(prefijo + str(estado))

    return ",".join(nombres)


def mostrar_afnd(afnd):
    print(formatear_afnd(afnd))
