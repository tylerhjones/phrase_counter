import unittest
from phrase_counter.strategies import default_normalizer

class TestNormalizer(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(default_normalizer('dog cat bird'), 'dog cat bird')
        self.assertEqual(default_normalizer('dog-man'), 'dogman')
        self.assertEqual(default_normalizer('dog😀'), 'dog')
        self.assertEqual(default_normalizer('dog(#@&$)!cat'), 'dogcat')
        self.assertEqual(default_normalizer('Dog'), 'dog')