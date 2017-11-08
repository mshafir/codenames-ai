# Codenames AI

An interactive command-line game of codenames, with an AI implementation
that can play as a code giver or guesser.

## Requirements

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

### Word Counts

Word counts help give the code giver an idea of how common or esoteric
different words are, it's configured to work against the following count
list:

http://norvig.com/ngrams/count_1w.txt

### Conda

1. get miniconda: https://conda.io/miniconda.html
2. `conda env create -f environment.yml --force`

## Execution

### Pre-compile distance matrix

You will need to compile a distance matrix to run things. This
is a one-time cost of around 30 minutes for large vectors.

`python compile_distances.py`

### Cut distance matrix

You can speed up loading and execution by getting rid of matrix
entries above a certain distance.

First argument is the distances file, second is the cutoff.

`python cut_distances.py resources/cached.dist 0.9`

### Run

You can update main.py to use the target distances and word
counts file you want. Set `debug=True` on a codegiver AI to see
the scores and what it's thinking.

Update codegiver.py to change the thresholds for clues

`python main.py`
