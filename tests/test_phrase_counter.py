import unittest
import io
from phrase_counter.phrase_counter import PhraseCounter


class TestPhraseCounter_default_strategies(unittest.TestCase):
    def test_min_words(self):
        result = PhraseCounter().count_phrases(io.StringIO('dog cat'))
        self.assertEqual(result, [])

    def test_one_sentence(self):
        result = PhraseCounter().count_phrases(io.StringIO('dog cat bird'))
        self.assertEqual(result, [('dog cat bird', 1)])

    def test_two_sentences(self):
        result = PhraseCounter().count_phrases(io.StringIO('dog cat bird. dog cat bird'))
        self.assertEqual(result, [('dog cat bird', 2), ('cat bird dog', 1), ('bird dog cat', 1)])
    
    def test_max_results(self):
        result = PhraseCounter(max_phrase_count=1).count_phrases(io.StringIO('dog cat bird. dog cat bird'))
        self.assertEqual(result, [('dog cat bird', 2)])
    
    def test_sequential_spaces(self):
        result = PhraseCounter(max_phrase_count=1).count_phrases(
            io.StringIO('dog     and   cat   '))
        self.assertEqual(result, [('dog and cat', 1)])

    def test_title(self):
        result = PhraseCounter(max_phrase_count=3).count_phrases(
        io.StringIO('''
            Chapter 1

            The beginning

            the cats end.''')
        )
        self.assertEqual(result, [('the cats end', 1)])
    
    def test_book_page(self):
        with open('tests/texts/book_sample.txt', 'r') as reader:
            result = PhraseCounter(max_phrase_count=3).count_phrases(reader)
        self.assertEqual(result, 
            [('these cats could', 3), ('in the beginning', 2), ('the beginning there', 1)])