import unittest

from er_afd.afd import convertir_a_afd
from er_afd.afnd import construir_afnd
from er_afd.analizador import analizar_expresion
from er_afd.simulador import evaluar_cadena, validar_cadena


class PruebasSimulador(unittest.TestCase):
    def crear_afd(self, expresion):
        arbol = analizar_expresion(expresion)
        afnd = construir_afnd(arbol)
        return convertir_a_afd(afnd)

    def test_cadena_aceptada(self):
        afd = self.crear_afd("(a|b)*abb")
        resultado = evaluar_cadena(afd, "abb")

        self.assertTrue(resultado["aceptada"])

    def test_cadena_rechazada(self):
        afd = self.crear_afd("(a|b)*abb")
        resultado = evaluar_cadena(afd, "aba")

        self.assertFalse(resultado["aceptada"])

    def test_recorrido(self):
        afd = self.crear_afd("ab")
        resultado = evaluar_cadena(afd, "ab")

        self.assertEqual(len(resultado["recorrido"]), 2)
        self.assertEqual(resultado["recorrido"][0]["simbolo"], "a")
        self.assertIsNotNone(resultado["recorrido"][1]["destino"])

    def test_cadena_vacia_con_kleene(self):
        afd = self.crear_afd("a*")
        resultado = evaluar_cadena(afd, "")

        self.assertTrue(resultado["aceptada"])

    def test_punto_acepta_cualquier_alfanumerico(self):
        afd = self.crear_afd(".")

        self.assertTrue(evaluar_cadena(afd, "a")["aceptada"])
        self.assertTrue(evaluar_cadena(afd, "7")["aceptada"])

    def test_conjunto_negativo(self):
        afd = self.crear_afd("[^abc]")

        self.assertTrue(evaluar_cadena(afd, "d")["aceptada"])
        self.assertFalse(evaluar_cadena(afd, "a")["aceptada"])

    def test_numero_especial(self):
        afd = self.crear_afd(r"\N\N")

        self.assertTrue(evaluar_cadena(afd, "25")["aceptada"])
        self.assertFalse(evaluar_cadena(afd, "2a")["aceptada"])

    def test_espacios(self):
        afd = self.crear_afd("hola mundo")

        self.assertTrue(evaluar_cadena(afd, "hola mundo")["aceptada"])

    def test_validacion_ascii(self):
        self.assertTrue(validar_cadena("Hola 123"))
        self.assertFalse(validar_cadena("á"))
        self.assertFalse(validar_cadena("hola!"))

    def test_literal_y_punto_pueden_coincidir(self):
        afd = self.crear_afd("aX|.Y")

        self.assertTrue(evaluar_cadena(afd, "aX")["aceptada"])
        self.assertTrue(evaluar_cadena(afd, "aY")["aceptada"])
        self.assertTrue(evaluar_cadena(afd, "bY")["aceptada"])

    def test_literal_y_conjunto_negativo_pueden_coincidir(self):
        afd = self.crear_afd("aX|[^b]Y")

        self.assertTrue(evaluar_cadena(afd, "aX")["aceptada"])
        self.assertTrue(evaluar_cadena(afd, "aY")["aceptada"])
        self.assertFalse(evaluar_cadena(afd, "bY")["aceptada"])


if __name__ == "__main__":
    unittest.main()
