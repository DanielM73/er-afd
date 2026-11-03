import unittest

from er_afd.afnd import construir_afnd, formatear_afnd
from er_afd.analizador import analizar_expresion


class PruebasAFND(unittest.TestCase):
    def test_literal(self):
        arbol = analizar_expresion("a")
        afnd = construir_afnd(arbol)

        self.assertEqual(afnd["inicial"], 0)
        self.assertEqual(afnd["finales"], [1])
        self.assertEqual(afnd["alfabeto"], ["a", "ε"])
        self.assertEqual(afnd["transiciones"][0]["simbolo"], "a")

    def test_concatenacion(self):
        afnd = construir_afnd(analizar_expresion("ab"))

        self.assertEqual(len(afnd["estados"]), 4)
        self.assertEqual(afnd["transiciones"][1]["simbolo"], "ε")
        self.assertEqual(afnd["finales"], [3])

    def test_union(self):
        afnd = construir_afnd(analizar_expresion("a|b"))
        salida = formatear_afnd(afnd)

        self.assertIn("q0|ε|{q2,q4}", salida)
        self.assertEqual(afnd["inicial"], 0)

    def test_kleene(self):
        afnd = construir_afnd(analizar_expresion("a*"))
        salida = formatear_afnd(afnd)

        self.assertIn("q0|ε|{q2,q1}", salida)
        self.assertIn("q3|ε|{q2,q1}", salida)

    def test_conjunto(self):
        afnd = construir_afnd(analizar_expresion("[a-c]"))
        simbolos = []

        for transicion in afnd["transiciones"]:
            simbolos.append(transicion["simbolo"])

        self.assertEqual(simbolos, ["a", "b", "c"])

    def test_conjunto_negativo(self):
        afnd = construir_afnd(analizar_expresion("[^abc]"))

        self.assertEqual(afnd["transiciones"][0]["simbolo"], "[^abc]")

    def test_epsilon_conserva_su_posicion(self):
        afnd = construir_afnd(analizar_expresion("aεb"))

        self.assertEqual(afnd["alfabeto"], ["a", "ε", "b"])

    def test_formato_solicitado(self):
        afnd = construir_afnd(analizar_expresion("a"))
        salida = formatear_afnd(afnd)

        self.assertIn("AFND", salida)
        self.assertIn("Q={q0,q1}", salida)
        self.assertIn("Σ={a,ε}", salida)
        self.assertIn("F={q1}", salida)
        self.assertIn("q0|a|{q1}", salida)


if __name__ == "__main__":
    unittest.main()
