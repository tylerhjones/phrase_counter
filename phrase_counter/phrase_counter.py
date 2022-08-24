from threading import Thread
from collections import deque
from phrase_counter.strategies import default_normalizer, default_sorting

class PhraseCounter:
    """
    Phrase Counter takes input as a filepath or string, and returns a sorted list of tuples.
    The tuples are sorted by the count of the phrases, with the most common phrases first.
    Phrases must be three words. Two word phrases are not counted. Phrases may overlap.
    """
    def __init__(self, 
        normalizer_strategy=default_normalizer, 
        sorting_strategy=default_sorting,
        max_phrase_count=100,
        phrase_length=3) -> None:
        self.big_map = {}
        self.normalizer_strategy = normalizer_strategy
        self.sorting_strategy = sorting_strategy
        self.window = deque(maxlen=phrase_length)
        self.phrase_length = phrase_length
        self.max_phrase_count = max_phrase_count

    def sort_map(self) -> list[tuple[str, int]]:
        return self.sorting_strategy(self.big_map)[:self.max_phrase_count]

    def count_phrases(self, reader):
        self.window.clear()
        for sentence in reader:
            sentence = self.normalizer_strategy(sentence)
            words = sentence.split()

            # minimal phrase length required for sentences to be counted.
            if len(words) < self.phrase_length:
                continue

            for word in words:
                self.window.append(word)

                if len(self.window) == self.phrase_length: 
                    key = ' '.join(self.window)
                    if key in self.big_map:
                        self.big_map[key] += 1
                    else:
                        self.big_map[key] = 1
        return self.sort_map()