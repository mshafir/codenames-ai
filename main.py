from game import Game
from codegiver import CodeGiverHuman, CodeGiverAI
from guesser import GuesserHuman, GuesserAI
import numpy as np
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


def load_vectors(file):
    vectors = dict()
    lines = file_lines(file)
    fin = open(file)
    i = 0
    with tqdm(total=lines) as pbar:
        for l in fin:
            parts = l[:-1].split(' ')
            vectors[parts[0].lower()] = np.array([float(n) for n in parts[1:]])
            i += 1
            if i % 100 == 0:
                pbar.update(100)
    fin.close()
    return vectors


print 'loading smarts...'
GLOVE_VECTORS = 'resources/glove.6B.300d.vectors'
LEXVEC_VECTORS = 'resources/lexvec.enwiki+newscrawl.300d.W.pos.vectors'
vectors = load_vectors(GLOVE_VECTORS)

cards = get_words('resources/codenames.txt')
cards = [w for w in cards if w in vectors]


print 'starting game...'
game = Game(cards,
            # red team
            [CodeGiverAI('red', vectors, True), GuesserHuman()],
            # blue team
            [CodeGiverAI('blue', vectors), GuesserAI(vectors)])
game.start()


