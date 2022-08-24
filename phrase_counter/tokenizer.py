import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Tokenizer:
    """
    Iterates on input returning a sentence at a time.
    Sequential newlines are considered to be the end of a sentence.
    """
    def __init__(self, reader):
        self.buffer = ''
        self.reader = reader
        self.started = False

    def _next(self):
        if not self.started:
            self.cur = self.reader.read(1)
            self.nxt = self.reader.read(1)
            self.started = True
            return self.cur, self.nxt
        else:
            self.cur = self.nxt
            self.nxt = self.reader.read(1)
            return self.cur, self.nxt
    
    def _return_buffer(self):
        tmp = self.buffer
        self.buffer = ''
        return tmp.strip()
    
    def __next__(self):
        while True:
            # exit condition 1: end of input
            cur, nxt = self._next()

            if not cur:
                if len(self.buffer) > 0:
                    return self._return_buffer()
                else:
                    raise StopIteration
        
            # exit condition 2: end of sentence
            # This assumes proper usage of English punctuation. TODO: Make this configurable.
            if cur in ['?', '.', '!']:
                self.buffer += cur
                return self._return_buffer()
            
            # exit condition 3: block of text
            # We consider blocks of text like chapter\n\nfoo not to be a phrase.
            # Blocks of text are delimited by two newlines.
            if cur == '\n' and '\n' == nxt:
                return self._return_buffer()
            
            self.buffer += cur