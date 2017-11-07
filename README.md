# Codenames AI

An interactive command-line game of codenames, with an AI implementation
that can play as a code giver or guesser.

## Set up

You need to download a set of word vectors in order to run the code:

* You can download the GloVe vectors here: https://nlp.stanford.edu/projects/glove/

* LexVec is another option, can be downloaded here: https://github.com/alexandres/lexvec

Be sure to set the correct distance function `euclidean` / `cosine` depending
on the word vectors you choose

### Conda set up

1. get miniconda: https://conda.io/miniconda.html
2. `conda env create -f environment.yml --force`

## Run

`python main.py`
