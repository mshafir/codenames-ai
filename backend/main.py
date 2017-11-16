from game.game import Game
from players.codegiver import CodeGiverHuman, CodeGiverAI
from players.guesser import GuesserHuman, GuesserAI
from utils.utils import get_words, load_distances, load_word_counts

print 'loading word counts'
counts = load_word_counts('resources/word_counts.counts')

print 'loading similarities'
distances = load_distances('resources/cached.dist.cut')

print 'loading cards'
CARDS = 'resources/codenames.txt'
cards = get_words(CARDS)
cards = [w for w in cards if w in distances]


# game start up
print 'starting game...'
game = Game(cards,
            # red team
            [CodeGiverAI('red', distances, counts, debug=True), GuesserHuman()],
            # [CodeGiverHuman(distances.keys()), GuesserAI(distances)],
            # blue team
            [CodeGiverAI('blue', distances, counts), GuesserAI(distances)]
            # [CodeGiverHuman(distances.keys()), GuesserAI(distances)]
)
game.start()
