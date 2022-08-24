# Top Word Phrases

This program takes a list of one or more files as arguments, or stdin if no arguments are given.
It then prints to stdout the top 100 most common three word phrases in the format `<phrase>  - <count>` sorted by count descending.

Program will ignore punctuation and treat all case insensitively.

`python app.py -h` for help.

## Design Overview

The project is split between interaction and fulfillment. `app.py` handles user input, while phrase_counter.py handles the actual counting.

Phrase counter uses a strategy pattern to change out behavior based on future needs. Presently this project only supports a default behavior, but could easily add new sorting, character normalization, etc.

Phrases are defined as N number of consecutive words within a sentence.
We count the phrases via a sliding window of size N. example for N=2, with `[]` denoting the window.
```
[I love sandwiches] for lunch
I [love sandwiches for] lunch
I love [sandwiches for lunch]
```

Multiple newlines are considered as a page divide. This was to avoid counting things like chapter headings as separate phrases.

## Execution

Local
```bash
$ python app.py -h
$ python phrases.py texts/moby-dick.txt texts/brothers-karamazov.txt
```

Docker
```bash
$ docker run -it -v $(pwd):/app -w /app python:3.10 python app.py texts/moby-dick.txt texts/brothers-karamazov.txt
```

## Testing

This program is written in python and uses the unittest module. You may manually invoke tests via
```bash
$ python -m unittest discover -s tests
```
or via docker
```bash
$ docker run -it -v $(pwd):/app -w /app python:3.10 python -m unittest discover -s tests
```

## Known Issues
- Secondary sorting is not consistent. If two phrases have equal count, insertion order from file is used rather than secondary sorting.
- If multiple files are specfied, the top results are extended, not combined. This means if the two lists have the same phrases, the equivalent phrases counts will not be added. (a debatable behavior)
- There is no timeout for stdin if supplied. This means the program will hang indefinitely if no input is given. (also a debatable behavior)
- Some repetitious phrases which would not be considered as 'phrases' are counted. eg. page footers.

## Future Work and Feature Goals
[ ]: build pkg and push to pypi
[ ]: build as standalone executable (avoid python app.py)
[ ]: add unicode support via a new normalization strategy
[ ]: brew recipe, because everyone loves a recipe
[ ]: improve primary content recognition (avoid page footers)

## Notes from the Author
