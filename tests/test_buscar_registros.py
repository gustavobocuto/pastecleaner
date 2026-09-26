import unittest
from core.text_records import buscar_registros_duplicados


class TestBuscarRegistros(unittest.TestCase):
    def test_buscar_registros_duplicados(self):
        resultado = buscar_registros_duplicados(__file__)
        self.assertIsInstance(resultado, dict)


if __name__ == "__main__":
    unittest.main()
