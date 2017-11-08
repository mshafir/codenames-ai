from tqdm import tqdm
import numpy as np
from gensim.models import KeyedVectors
from collections import defaultdict


def file_lines(file):
    return sum(1 for line in open(file))


def get_words(file):
    fin = open(file)
    words = list()
    for l in fin:
        words.append(l[:-1].strip().lower())
    fin.close()
    return words


def load_vectors(file, common_words, abort=None):
    if file.endswith('.bin'):
        return KeyedVectors.load_word2vec_format(file, binary=True)
    vectors = dict()
    lines = file_lines(file)
    fin = open(file)
    i = 0
    last_amount = 0
    with tqdm(total=lines) as pbar:
        for l in fin:
            i += 1
            parts = l[:-1].split(' ')
            word = parts[0].lower()
            if word not in common_words and len(common_words) > 0:
                continue
            if abort is not None and i > abort:
                break
            vectors[word] = np.array([float(n) for n in parts[1:]])
            pbar.update(i-last_amount)
            last_amount = i
    fin.close()
    return vectors


def load_distances(file):
    lines = file_lines(file)
    fin = open(file)
    distances = defaultdict(lambda: defaultdict(lambda: 2))
    with tqdm(total=lines) as pbar:
        for l in fin:
            word,card,score = l[:-1].split(' ')
            distances[word][card] = float(score)
            pbar.update()
    fin.close()
    return distances


def load_word_counts(file):
    lines = file_lines(file)
    fin = open(file)
    counts = defaultdict(int)
    with tqdm(total=lines) as pbar:
        for l in fin:
            word,c = l[:-1].split('\t')
            counts[word] = int(c)
            pbar.update()
    fin.close()
    return counts