from game import Game
from codegiver import CodeGiverHuman, CodeGiverAI
from guesser import GuesserHuman, GuesserAI
import numpy as np
from scipy.spatial import distance
from tqdm import tqdm


def file_lines(file):
    return sum(1 for line in open(file))


def get_words(file):
    fin = open(file)
    words = list()
    for l in fin:
        words.append(l[:-1].strip().lower())
    fin.close()
    return words


def load_vectors(file, common_words):
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
            if word not in common_words:
                continue
            vectors[word] = np.array([float(n) for n in parts[1:]])
            pbar.update(i-last_amount)
            last_amount = i
    fin.close()
    return vectors


print 'loading smarts...'
GLOVE_VECTORS = 'resources/glove.6B.300d.vectors'
LEXVEC_VECTORS = 'resources/lexvec.enwiki+newscrawl.300d.W.pos.vectors'
common_words = set([w for w in get_words('resources/wordlist.10000.txt') if len(w) > 2])
vectors = load_vectors(GLOVE_VECTORS, common_words)
dist_func = distance.cosine


cards = get_words('resources/codenames.txt')
cards = [w for w in cards if w in vectors]


print 'starting game...'
game = Game(cards,
            # red team
            [CodeGiverAI('red', vectors, dist_func, debug=False), GuesserHuman()],
            # blue team
            [CodeGiverHuman(), GuesserAI(vectors, dist_func)])
game.start()


