import re
ASCII_PATTERN = re.compile('[^A-Za-z\ ]')

def default_normalizer(sentence: str) -> str:
    sentence = sentence.replace('\n', ' ')
    # remove non-ASCII characters and convert to lowercase
    return ASCII_PATTERN.sub('', sentence).lower() 

def default_sorting(results):
    if type(results) == dict:
        return sorted(results.items(), key=lambda x: x[1], reverse=True)
    if type(results) == list:
        return sorted(results, key=lambda x: x[1], reverse=True)
    else:
        raise ValueError(f'unsupported type given to sorting strategy {type(results)}')