from game import Game
from codegiver import CodeGiverHuman, CodeGiverAI
from guesser import GuesserHuman, GuesserAI
from scipy.spatial import distance
from utils import get_words, load_vectors


# potential sources
GLOVE_VECTORS = 'resources/glove.6B.300d.vectors'
GLOVE2_VECTORS = 'resources/glove.42B.300d.vectors'
LEXVEC_VECTORS = 'resources/lexvec.enwiki+newscrawl.300d.W.pos.vectors'
DEP_VECTORS = 'resources/deps.vectors'
GOOGLE_VECTORS = 'resources/GoogleNews-vectors-negative300.bin'

SMALL_WORDS = 'resources/wordlist.10000.words'
LARGE_WORDS = 'resources/words_alpha.words'

CARDS = 'resources/codenames.txt'

# loading routine
print 'loading smarts...'
common_words = set([w for w in get_words(LARGE_WORDS) if len(w) > 2])
vectors = load_vectors(GLOVE2_VECTORS, common_words)
common_words = vectors.keys()
dist_func = distance.cosine


cards = get_words(CARDS)
cards = [w for w in cards if w in vectors]

# game start up
print 'starting game...'
game = Game(cards,
            # red team
            [CodeGiverAI('red', vectors, dist_func, words=common_words, debug=True), GuesserHuman()],
            # blue team
            [CodeGiverHuman(common_words), GuesserAI(vectors, dist_func, words=common_words)])
game.start()


