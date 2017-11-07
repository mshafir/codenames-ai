# Codenames AI

An interactive command-line game of codenames, with an AI implementation
that can play as a code giver or guesser.

## Set up

### Vectors

You need to download a set of word vectors in order to run the code:

* You can download the GloVe vectors here: https://nlp.stanford.edu/projects/glove/
  * the 6B token vectors work okay
  * the 42B work better
  * I imagine the 812B work best, but haven't verrified that

* LexVec is another option, can be downloaded here: https://github.com/alexandres/lexvec

### Words

This repo comes with a sample word list

Using a larger word set, like the ones from
https://github.com/dwyl/english-words will also improve the quality of the clues

### Conda

1. get miniconda: https://conda.io/miniconda.html
2. `conda env create -f environment.yml --force`

## Run

`python main.py`
