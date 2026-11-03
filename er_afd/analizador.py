"""Analizador sencillo para las expresiones regulares del proyecto."""

import string


class ErrorExpresion(Exception):
    pass


class Analizador:
    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0

    def analizar(self):
        if self.texto == "":
            self.error("La expresión regular está vacía")

        resultado = self.leer_union()

        if not self.termino():
            self.error("Se encontró un símbolo inesperado")

        return resultado

    def leer_union(self):
        opciones = []
        opciones.append(self.leer_concatenacion())

        while self.actual() == "|":
            self.avanzar()

            if self.termino() or self.actual() == "|" or self.actual() == ")":
                self.error("Falta una expresión después de |")

            opciones.append(self.leer_concatenacion())

        if len(opciones) == 1:
            return opciones[0]

        return {
            "tipo": "union",
            "hijos": opciones
        }

    def leer_concatenacion(self):
        partes = []

        while not self.termino() and self.actual() != "|" and self.actual() != ")":
            partes.append(self.leer_repeticion())

        if len(partes) == 0:
            self.error("Se esperaba una expresión")

        if len(partes) == 1:
            return partes[0]

        return {
            "tipo": "concatenacion",
            "hijos": partes
        }

    def leer_repeticion(self):
        nodo = self.leer_elemento()

        while self.actual() == "*":
            self.avanzar()
            nodo = {
                "tipo": "kleene",
                "hijo": nodo
            }

        return nodo

    def leer_elemento(self):
        if self.termino():
            self.error("Se esperaba un símbolo")

        caracter = self.avanzar()

        if caracter == "(":
            if self.actual() == ")":
                self.error("Los paréntesis están vacíos")

            contenido = self.leer_union()

            if self.actual() != ")":
                self.error("Falta cerrar el paréntesis")

            self.avanzar()
            return contenido

        if caracter == "[":
            return self.leer_conjunto()

        if caracter == "\\":
            return self.leer_escape()

        if caracter == ".":
            return {"tipo": "cualquiera"}

        if caracter == "ε":
            return {"tipo": "epsilon"}

        if caracter == "*" or caracter == "|" or caracter == ")":
            self.error("El operador no tiene un elemento antes", self.posicion - 1)

        return {
            "tipo": "literal",
            "valor": caracter
        }

    def leer_conjunto(self):
        negado = False
        caracteres = []

        if self.actual() == "^":
            negado = True
            self.avanzar()

        if self.termino():
            self.error("Falta cerrar el conjunto con ]")

        if self.actual() == "]":
            self.error("El conjunto no puede estar vacío")

        while not self.termino() and self.actual() != "]":
            izquierda = self.leer_caracter_conjunto()

            if self.actual() == "-" and self.siguiente() != "]" and self.siguiente() is not None:
                posicion_guion = self.posicion
                self.avanzar()
                derecha = self.leer_caracter_conjunto()

                if len(izquierda) != 1 or len(derecha) != 1:
                    self.error("El rango debe tener un carácter a cada lado", posicion_guion)

                inicio = ord(izquierda[0])
                final = ord(derecha[0])

                if inicio > final:
                    self.error("El rango está escrito al revés", posicion_guion)

                izquierda = []
                numero = inicio

                while numero <= final:
                    izquierda.append(chr(numero))
                    numero = numero + 1

            self.agregar_sin_repetir(caracteres, izquierda)

        if self.actual() != "]":
            self.error("Falta cerrar el conjunto con ]")

        self.avanzar()

        return {
            "tipo": "conjunto",
            "caracteres": caracteres,
            "negado": negado
        }

    def leer_caracter_conjunto(self):
        if self.termino() or self.actual() == "]":
            self.error("Se esperaba un carácter dentro del conjunto")

        caracter = self.avanzar()

        if caracter == "\\":
            return self.leer_valores_escape()

        return [caracter]

    def leer_escape(self):
        valores = self.leer_valores_escape()

        if len(valores) == 1:
            return {
                "tipo": "literal",
                "valor": valores[0]
            }

        return {
            "tipo": "conjunto",
            "caracteres": valores,
            "negado": False
        }

    def leer_valores_escape(self):
        if self.termino():
            self.error("La secuencia de escape está incompleta")

        caracter = self.avanzar()

        if caracter == "N":
            return list(string.digits)

        if caracter == "A":
            return list(string.ascii_uppercase)

        if caracter == "a":
            return list(string.ascii_lowercase)

        if caracter == "z":
            return list(string.ascii_lowercase + string.ascii_uppercase)

        if caracter == "h":
            return [self.leer_hexadecimal()]

        return [caracter]

    def leer_hexadecimal(self):
        inicio = self.posicion
        digitos = self.texto[self.posicion:self.posicion + 2]

        if len(digitos) != 2:
            self.error("Después de \\h deben existir dos dígitos hexadecimales", inicio)

        for digito in digitos:
            if digito not in string.hexdigits:
                self.error("El código hexadecimal no es válido", inicio)

        self.posicion = self.posicion + 2
        return chr(int(digitos, 16))

    def agregar_sin_repetir(self, lista, nuevos):
        for caracter in nuevos:
            if caracter not in lista:
                lista.append(caracter)

    def actual(self):
        if self.termino():
            return None

        return self.texto[self.posicion]

    def siguiente(self):
        posicion_siguiente = self.posicion + 1

        if posicion_siguiente >= len(self.texto):
            return None

        return self.texto[posicion_siguiente]

    def avanzar(self):
        caracter = self.texto[self.posicion]
        self.posicion = self.posicion + 1
        return caracter

    def termino(self):
        return self.posicion >= len(self.texto)

    def error(self, mensaje, posicion=None):
        if posicion is None:
            posicion = self.posicion

        indicador = " " * posicion + "^"
        texto_error = mensaje + " en la posición " + str(posicion)
        texto_error = texto_error + "\n" + self.texto + "\n" + indicador
        raise ErrorExpresion(texto_error)


def analizar_expresion(texto):
    analizador = Analizador(texto)
    return analizador.analizar()


def obtener_alfabeto(nodo, alfabeto=None):
    if alfabeto is None:
        alfabeto = []

    tipo = nodo["tipo"]

    if tipo == "literal":
        agregar_simbolo(alfabeto, nodo["valor"])

    elif tipo == "cualquiera":
        agregar_simbolo(alfabeto, ".")

    elif tipo == "epsilon":
        agregar_simbolo(alfabeto, "ε")

    elif tipo == "conjunto":
        if nodo["negado"]:
            texto = "[^" + "".join(nodo["caracteres"]) + "]"
            agregar_simbolo(alfabeto, texto)
        else:
            for caracter in nodo["caracteres"]:
                agregar_simbolo(alfabeto, caracter)

    elif tipo == "kleene":
        obtener_alfabeto(nodo["hijo"], alfabeto)

    elif tipo == "concatenacion" or tipo == "union":
        for hijo in nodo["hijos"]:
            obtener_alfabeto(hijo, alfabeto)

    return alfabeto


def agregar_simbolo(alfabeto, simbolo):
    if simbolo not in alfabeto:
        alfabeto.append(simbolo)


def mostrar_arbol(nodo, nivel=0):
    espacio = "  " * nivel
    tipo = nodo["tipo"]

    if tipo == "literal":
        print(espacio + "Literal: " + repr(nodo["valor"]))

    elif tipo == "cualquiera":
        print(espacio + "Cualquier símbolo: .")

    elif tipo == "epsilon":
        print(espacio + "Épsilon: ε")

    elif tipo == "conjunto":
        contenido = "".join(nodo["caracteres"])

        if nodo["negado"]:
            print(espacio + "Conjunto negativo: [^" + contenido + "]")
        else:
            print(espacio + "Conjunto: [" + contenido + "]")

    elif tipo == "kleene":
        print(espacio + "Cerradura de Kleene: *")
        mostrar_arbol(nodo["hijo"], nivel + 1)

    elif tipo == "concatenacion":
        print(espacio + "Concatenación")

        for hijo in nodo["hijos"]:
            mostrar_arbol(hijo, nivel + 1)

    elif tipo == "union":
        print(espacio + "Unión: |")

        for hijo in nodo["hijos"]:
            mostrar_arbol(hijo, nivel + 1)
