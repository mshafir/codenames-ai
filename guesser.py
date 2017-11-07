import time


class GuesserHuman:
    def guess(self, clue, board, tries_left):
        word = raw_input('What is your guess? (or pass)\n > ')
        if word == 'pass' or word in board.remaining_words():
            return word
        else:
            print 'Word not on board'
            self.guess(clue, board, tries_left)

class GuesserAI:
    def __init__(self, vectors, similarity_func, words=None, debug=False):
        if words is None:
            self.words = vectors.keys()
        else:
            self.words = words
        self.vectors = vectors
        self.debug = debug
        self.similarity_func = similarity_func

    def guess(self, clue, board, tries_left):
        # realistic delay
        time.sleep(1)
        if tries_left == 1:
            return 'pass'
        board_scores = [(w, self.word_similarity(clue, w)) for w in board.remaining_words()]
        best = min(board_scores, key=lambda x: x[1])
        print best[0] + '!'
        return best[0]

    def word_similarity(self, word1, word2):
        return self.similarity_func(self.vectors[word1], self.vectors[word2])
