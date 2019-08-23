# Crossword Solver
## What is _Crossword Solver_?
The aim of the project is to implement an example of a backtracking algorithm (using improvements like _Forward-Checking_ and some heuristics). To do this, we've dealt with the crossword problem. Given a crossword board and using a dictionary of valid words in a language, then we have to find a valid solution for that crossword applying the rules of the popular crossword game.

### The algorithm
We'll use a *backtracking algorithm* variation: *forward-checking*, with some heuristics (_LWF_: Largest Word First, _MCV_: Most Constraining Values and _MRV_: Minimum Remaining Values) to improve the solving speed

## What can the _Crossword Solver_ do?
1. **Solve a crossword board** (read from a file)
2. **Display the solving process** the software applies while is solving the crossword. This helps us to check how the algorithm is working and introduce improvements based on its behaviour.
3. **Generate crossword puzzles** given an empty crossword. We'll look for the solutions and afterwards look for the meanings of the words in a local [_Hunspell_](http://hunspell.github.io/) dictionary or online (currently only in [_Wiktionary_](https://www.wiktionary.org/)
in Catalan language)

## Languages
The default language is Catalan; a list of words is provided in the file
`res/diccionari_CB.txt`. Their meanings are searched for in the
[_Wiktionary_](https://www.wiktionary.org/) online dictionary.

Other languages con be enabled providing a copy of an [_Hunspell_](http://hunspell.github.io/)
dictionary: words and meanings will be locally searched for in the _Hunspell_ thesaurus.

### Hunspell dictionaries
[_Hunspell_](http://hunspell.github.io/) is the spell checker of LibreOffice,
OpenOffice, Mozilla Firefox 3 & Thunderbird, and many others.

Thesaurus files can be found in LibreOffice / OpenOffice Language Packs
bundled together spellchecking and hyphenation dictionaries used for stemming
and morphological generation.

LibreOffice Language Packs download:
- https://cgit.freedesktop.org/libreoffice/dictionaries/tree/
- https://wiki.documentfoundation.org/Language_support_of_LibreOffice
- https://github.com/LibreOffice/dictionaries

Language Packs are deployed in a single `.oxt` compressed file.
If your archive manager doesn't open `.oxt` file, then rename it as `.zip`
and there you have it.

#### Thesaurus
_Hunspell_ thesaurus consists of a `.dat` structured text data file
and an optional `.idx` index file. You can find their description
[here](https://github.com/hunspell/mythes/blob/master/data_layout.txt).

The root name of LibreOffice / OpenOffice thesaurus files is prefixed by `th_`
following Language and Country Code, more an optional suffix, e.g.:
```
th_ca_ES_v3.dat
th_en_US_v2.dat th_en_US_v2.idx
th_it_IT_v2.dat th_it_IT_v2.idx
```

## About the code
The code is written in _Python 3_, and requires some libraries (available in [_PyPi_](https://pypi.python.org/pypi)):

### Libraries
#### Required
The following libraries are required for the software to run:
 - `numpy`

#### Optional
The following libraries must be present if you want to generate crossword puzzles based on an online dictionary
 - `mwapi`
 - `beautifulsoup4`

### Running the application
The application is command-line based so, open a terminal and change into the repo's root. Then, you can run the application calling to Python interpreter into main script:
```bash
python src/main.py -h
```
The `-h` argument will help you to discover how the software works and what it can do for you.

Solving the default crossword board `res/crossword_CB.txt` with English words:
```bash
python src/main.py --wordlist=directory-path-to-th_en_US_v2 --use-thesaurus
```

Generating a crossword puzzles from default `res/crossword_CB.txt` board
with English words and their meanings:
```bash
python src/main.py --wordlist=directory-path-to-th_en_US_v2 --use-thesaurus --play
```

## Credits
This is a fork of the [crossword solver](https://github.com/uab-projects/crossword)
made by @ccebrecos & @davidlj in [ETSE](https://uab.cat/enginyeria), UAB
<center><img src="http://www.uab.cat/doc/logo-UAB.png" width="100" alt="UAB Logotype"></center>

## Disclaimer
The author of this fork is not affiliated, associated, authorized,
endorsed by, or in any way officially connected with any of the companies,
organizations and individuals mentioned above.

None of them can be hold liable for any damages arising out of the use
of this software.

## License
The code is licensed under Apache Software Foundation (_ASF_) License v2.0
