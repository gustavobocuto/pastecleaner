import unittest
from duplicados.calcular_hash import calcular_hash_arquivo

class TestCalcularHash(unittest.TestCase):
    def test_calcular_hash_arquivo(self):
        # Testes básicos para calcular_hash_arquivo
        self.assertEqual(len(calcular_hash_arquivo(__file__)), 32)

if __name__ == "__main__":
    unittest.main()
