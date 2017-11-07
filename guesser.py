import time
from scipy.spatial import distance

class GuesserHuman:
    def guess(self, clue, board, tries_left):
        word = raw_input('What is your guess? (or pass)\n > ')
        if word == 'pass' or word in board.remaining_words():
            return word
        else:
            print 'Word not on board'
            self.guess(word, board)

class GuesserAI:
    def __init__(self, vectors, debug=False):
        self.words = vectors.keys()
        self.vectors = vectors
        self.debug = debug

    def guess(self, clue, board, tries_left):
        # realistic delay
        time.sleep(2)
        if tries_left == 1:
            return 'pass'
        board_scores = [(w, self.word_similarity(clue, w)) for w in board.remaining_words()]
        best = min(board_scores, key=lambda x: x[1])
        print best[0] + '!'
        return best[0]

    def word_similarity(self, word1, word2):
        return distance.euclidean(self.vectors[word1], self.vectors[word2])
