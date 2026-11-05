import unittest

from pruebas_precision import CASOS, ejecutar_caso


class PruebasPrecision(unittest.TestCase):
    def test_todos_los_casos(self):
        for expresion, cadena, esperado in CASOS:
            with self.subTest(expresion=expresion, cadena=cadena):
                obtenido = ejecutar_caso(expresion, cadena)
                self.assertEqual(obtenido, esperado)


if __name__ == "__main__":
    unittest.main()
