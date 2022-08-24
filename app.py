import concurrent.futures
import sys
import os
from phrase_counter.phrase_counter import PhraseCounter
import argparse

def file_exists(file_path):
    return os.path.isfile(file_path)

def print_usage():
    print('''Usages: 
    python app.py <file_path> <file_path> ...
    cat <file_path> | python app.py
    ''')

def do_count(reader, max_results, phrase_size):
        pc = PhraseCounter(
            max_phrase_count=max_results, 
            phrase_length=phrase_size)
        return pc.count_phrases(reader)

def count_file(file_path, max_results, phrase_size):
    with open(file_path, 'r') as reader:
        return do_count(reader, max_results, phrase_size)

def main(files: list[str], max_results: int, phrase_size: int):
    top_phrases = []
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for filepath in files:
            if not file_exists(filepath):
                print(f'ERR: {filepath} is not found.', file=sys.stderr)
                sys.exit(1)

            future = executor.submit(count_file, filepath, max_results, phrase_size)
            futures.append(future)

        # Step 2: read from stdin
        if not sys.stdin.isatty():
            future = executor.submit(do_count, sys.stdin, max_results, phrase_size)
            futures.append(future)

        if len(futures) == 0:
            print(f'ERR: no inputs given. see usage --help, -h', file=sys.stderr)
            sys.exit(1)
        
        # Step 3: wait and print results
        for future in futures:
            top_phrases.extend(future.result())
        top_phrases.sort(key=lambda x: x[1], reverse=True)

        for phrase, count in top_phrases[:max_results]:
            print(f'{phrase} - {count}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Phrase Counter
    Accpts files as arguments or stdin, and prints the top phrases and number of occurrences.''')

    parser.add_argument('files', type=str, nargs='*', help='Input files to be counted and sorted into a single result list.')
    parser.add_argument('-m', '--max', dest='max_results', default=100, type=int,
                        help='Maximum number of records to print (default: 100)')
    parser.add_argument('-s', '--size', dest='phrase_size', default=3, type=int,
                        help='Size of the phrase to consider (default: 3)')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    main(args.files, args.max_results, args.phrase_size)