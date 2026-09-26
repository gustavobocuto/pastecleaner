import unittest
from core.hash_utils import hash_arquivo


class TestHashArquivo(unittest.TestCase):
    def test_hash_arquivo(self):
        self.assertEqual(len(hash_arquivo(__file__)), 32)


if __name__ == "__main__":
    unittest.main()
