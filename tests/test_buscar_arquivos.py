import unittest
from pathlib import Path
from core.file_scanner import agrupar_por_hash


class TestAgruparPorHash(unittest.TestCase):
    def test_agrupar_por_hash_encontra_duplicata(self):
        arquivos = [Path(__file__), Path(__file__)]
        grupos = agrupar_por_hash(arquivos)
        self.assertEqual(len(grupos), 1)


if __name__ == "__main__":
    unittest.main()
