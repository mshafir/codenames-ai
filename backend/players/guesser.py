import time
import random

# shift scores so the boandary between good/bad is at a more confusing place
BASE_SCORE_SHIFT = 0.01

class GuesserHuman:
    def guess(self, clue, board, tries_left):
        word = raw_input('What is your guess? (or pass)\n > ')
        if word == 'pass' or word in board.remaining_words():
            return word
        else:
            print 'Word not on board'
            self.guess(clue, board, tries_left)

class GuesserAI:
    def __init__(self, distances, debug=False):
        self.words = distances.keys()
        self.distances = distances
        self.debug = debug

    def add_confusion(self, score, quality):
        """Adds random confusion to a similarity score for quality of 0 to 100"""
        random_shift = quality * BASE_SCORE_SHIFT * (1.0 / score)
        return score + random.uniform(-random_shift, random_shift)

    def guess(self, clue, board, tries_left, quality=100):
        # realistic delay
        time.sleep(1)
        if tries_left == 1:
            return 'pass'
        board_scores = [(w, self.add_confusion(self.word_similarity(clue, w), quality)) for w in board.remaining_words()]
        random.shuffle(board_scores)
        best = sorted(board_scores, key=lambda x: x[1])
        if self.debug:
            print best[:10]
        best_word = best[0]
        print best_word[0] + '!'
        return best_word[0]

    def word_similarity(self, word1, word2):
        return self.distances[word1][word2]
