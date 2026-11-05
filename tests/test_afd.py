import unittest

from er_afd.afd import cierre_epsilon, convertir_a_afd, formatear_afd
from er_afd.afnd import construir_afnd
from er_afd.analizador import analizar_expresion


class PruebasAFD(unittest.TestCase):
    def crear_automatas(self, expresion):
        arbol = analizar_expresion(expresion)
        afnd = construir_afnd(arbol)
        afd = convertir_a_afd(afnd)
        return afnd, afd

    def test_cierre_epsilon(self):
        afnd, afd = self.crear_automatas("a|b")
        cierre = cierre_epsilon([afnd["inicial"]], afnd)

        self.assertEqual(cierre, afd["conjuntos"][0])
        self.assertGreater(len(cierre), 1)

    def test_estado_inicial(self):
        afnd, afd = self.crear_automatas("ab")

        self.assertEqual(afd["inicial"], 0)
        self.assertEqual(afd["conjuntos"][0], [0])

    def test_afd_no_tiene_epsilon(self):
        afnd, afd = self.crear_automatas("aεb")

        self.assertNotIn("ε", afd["alfabeto"])
        self.assertEqual(afd["alfabeto"], ["a", "b"])

    def test_kleene_inicial_es_final(self):
        afnd, afd = self.crear_automatas("a*")

        self.assertIn(0, afd["finales"])

    def test_union_acepta_dos_caminos(self):
        afnd, afd = self.crear_automatas("a|b")
        destinos_desde_inicio = []

        for transicion in afd["transiciones"]:
            if transicion["origen"] == 0:
                destinos_desde_inicio.append(transicion["destino"])

        self.assertEqual(len(destinos_desde_inicio), 2)

        for destino in destinos_desde_inicio:
            self.assertIn(destino, afd["finales"])

    def test_un_destino_por_simbolo(self):
        afnd, afd = self.crear_automatas("(a|b)*abb")
        pares = []

        for transicion in afd["transiciones"]:
            par = (transicion["origen"], transicion["simbolo"])
            self.assertNotIn(par, pares)
            pares.append(par)

    def test_estado_vacio(self):
        afnd, afd = self.crear_automatas("a")

        self.assertIn([], afd["conjuntos"])

    def test_formato_solicitado(self):
        afnd, afd = self.crear_automatas("a")
        salida = formatear_afd(afd)

        self.assertIn("AFD", salida)
        self.assertIn("Q={Q0,Q1,Q2}", salida)
        self.assertIn("Σ={a}", salida)
        self.assertIn("F={Q1}", salida)
        self.assertIn("Q0|a|Q1", salida)


if __name__ == "__main__":
    unittest.main()
