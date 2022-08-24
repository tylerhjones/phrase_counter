import unittest
import io
from phrase_counter.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    def test_one_sentence(self):
        t = Tokenizer(io.StringIO('I like dogs.'))
        self.assertEqual(next(t), 'I like dogs.')

    def test_two_sentences(self):
        t = Tokenizer(io.StringIO('I like dogs. I like cats.'))
        self.assertEqual(next(t), 'I like dogs.')
        self.assertEqual(next(t), 'I like cats.')
    
    def test_end_of_input(self):
        t = Tokenizer(io.StringIO('I like dogs'))
        self.assertEqual(next(t), 'I like dogs')
        with self.assertRaises(StopIteration):
            next(t)
    
    def test_punctuation(self):
        t = Tokenizer(io.StringIO('I like dogs! I like cats? I like birds.'))
        self.assertEqual(next(t), 'I like dogs!')
        self.assertEqual(next(t), 'I like cats?')
        self.assertEqual(next(t), 'I like birds.')
    
    def test_text_block(self):
        t = Tokenizer(io.StringIO('I like dogs\n\nI like cats'))
        self.assertEqual(next(t), 'I like dogs')
        self.assertEqual(next(t), 'I like cats')