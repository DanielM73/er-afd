import string
import unittest

from er_afd.analizador import ErrorExpresion
from er_afd.analizador import analizar_expresion, obtener_alfabeto


class PruebasAnalizador(unittest.TestCase):
    def test_union_concatenacion_y_kleene(self):
        arbol = analizar_expresion("a|bc*")

        self.assertEqual(arbol["tipo"], "union")
        self.assertEqual(arbol["hijos"][0]["valor"], "a")
        self.assertEqual(arbol["hijos"][1]["tipo"], "concatenacion")
        self.assertEqual(arbol["hijos"][1]["hijos"][1]["tipo"], "kleene")

    def test_parentesis(self):
        arbol = analizar_expresion("(a|b)c")

        self.assertEqual(arbol["tipo"], "concatenacion")
        self.assertEqual(arbol["hijos"][0]["tipo"], "union")

    def test_punto_y_epsilon(self):
        arbol = analizar_expresion("ε.")

        self.assertEqual(arbol["hijos"][0]["tipo"], "epsilon")
        self.assertEqual(arbol["hijos"][1]["tipo"], "cualquiera")
        self.assertEqual(obtener_alfabeto(arbol), ["ε", "."])

    def test_conjunto_y_rango(self):
        arbol = analizar_expresion("[a-cx]")

        self.assertEqual(arbol["caracteres"], ["a", "b", "c", "x"])

    def test_conjunto_negativo(self):
        arbol = analizar_expresion("[^abc]")

        self.assertTrue(arbol["negado"])
        self.assertEqual(arbol["caracteres"], ["a", "b", "c"])

    def test_escapes_especiales(self):
        casos = [
            (r"\N", list(string.digits)),
            (r"\A", list(string.ascii_uppercase)),
            (r"\a", list(string.ascii_lowercase)),
            (r"\z", list(string.ascii_lowercase + string.ascii_uppercase))
        ]

        for expresion, esperado in casos:
            with self.subTest(expresion=expresion):
                arbol = analizar_expresion(expresion)
                self.assertEqual(arbol["caracteres"], esperado)

    def test_hexadecimal(self):
        arbol = analizar_expresion(r"\h41\h20")

        self.assertEqual(arbol["hijos"][0]["valor"], "A")
        self.assertEqual(arbol["hijos"][1]["valor"], " ")

    def test_escape_normal(self):
        arbol = analizar_expresion(r"\*\p\\")
        valores = []

        for hijo in arbol["hijos"]:
            valores.append(hijo["valor"])

        self.assertEqual(valores, ["*", "p", "\\"])

    def test_espacio(self):
        arbol = analizar_expresion("hola mundo")

        self.assertEqual(arbol["tipo"], "concatenacion")
        self.assertIn(" ", obtener_alfabeto(arbol))

    def test_orden_del_alfabeto(self):
        arbol = analizar_expresion("ba(b|c)ε")

        self.assertEqual(obtener_alfabeto(arbol), ["b", "a", "c", "ε"])

    def test_expresiones_invalidas(self):
        expresiones = [
            "",
            "|a",
            "a|",
            "a||b",
            "()",
            "(ab",
            "ab)",
            "[]",
            "[a",
            "[z-a]",
            "\\",
            r"\h4G"
        ]

        for expresion in expresiones:
            with self.subTest(expresion=expresion):
                with self.assertRaises(ErrorExpresion):
                    analizar_expresion(expresion)


if __name__ == "__main__":
    unittest.main()
