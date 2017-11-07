import numpy as np
from tqdm import tqdm
from collections import defaultdict


# aka. fathomability
SIMILARITY_THRESHOLD = 0.7
DISTINCTNESS_THRESHOLD = 0.05


def legal_word(w, words):
    if w in words:
        return False
    for w2 in words:
        if w in w2 or w2 in w:
            return False
    return True


class CodeGiverHuman:
    def __init__(self, words):
        self.words = words  # allowed words

    def give_hint(self, board):
        fout = open('board_answers.txt', 'w')
        fout.write(board.get_answers())
        fout.close()
        print 'Check board_answers.txt for the answers to the current board, but do not let the others see'
        clue = ''
        while clue == '' or clue not in self.words:
            clue = raw_input('What is your clue?\n > ')
            if clue not in self.words:
                print 'Unknown word '+clue
        num = raw_input('How many words is your clue for? \n > ')
        return clue, int(num)


class Hint:
    def __init__(self, word, num=0, similarity=0., distinctness=0., intended=None):
        self.word = word
        self.num = num
        self.similarity = similarity
        self.distinctness = distinctness
        self.intended = intended

    def __str__(self):
        return "%s for %i (similarity: %f, distinctness: %f, intended: %s)" % \
              (self.word, self.num, self.similarity, self.distinctness, ', '.join(self.intended))


class CodeGiverAI:
    def __init__(self, team, vectors, similarity_func, words=None, debug=False):
        self.team = team
        if words is None:
            self.words = vectors.keys()
        else:
            self.words = words
        self.vectors = vectors
        self.debug = debug
        self.similarity_func = similarity_func
        self.history = set()
        self.cache = defaultdict(float)

    def give_hint(self, board):
        print 'thinking...'
        hints = self.score_hints(board)
        best_hint = hints[0]
        if self.debug:
            for i in range(10):
                print hints[i]
        self.history.add(best_hint.word)
        return best_hint.word, best_hint.num

    def evaluate_hint(self, hint):
        if hint.distinctness > DISTINCTNESS_THRESHOLD:
            return hint.num
        return hint.distinctness - hint.similarity

    def score_hints(self, board):
        hints = [self.score_word(w, board) for w in tqdm(self.words) if legal_word(w, board.words) and not w in self.history]
        hints = [hint for hint in hints if hint.num > 0]
        return sorted(hints, key=self.evaluate_hint, reverse=True)

    def score_word(self, word, board):
        similarity = sorted(self.board_similarity(word, board), key=lambda w: w[2])

        team_words = []
        first_non_team_word = None
        first_non_team_type = None
        for w, type, score in similarity:
            if type == self.team:
                team_words.append((w, score))
            else:
                first_non_team_word = (w, score)
                first_non_team_type = type
                break

        # number of guessable words
        guessable_words = [w for w in team_words if w[1] < SIMILARITY_THRESHOLD]
        if len(guessable_words) == 0 or first_non_team_word is None:
            return Hint(word, 0, 0, 0, [])

        # the number to give and how distinct the clue is from other words on the board
        num = len(guessable_words)
        distinctness = first_non_team_word[1] - guessable_words[-1][1]

        # penalty to distinctness depending on type
        if first_non_team_type == 'assassin':
            distinctness -= 0.2
        elif first_non_team_type != 'neutral':
            distinctness -= 0.1

        similarity = np.mean([w[1] for w in guessable_words])

        return Hint(word, num, similarity, distinctness, [t[0] + ' (' + str(t[1]) + ')' for t in guessable_words])

    def board_similarity(self, word, board):
        return [(w, board.word_type(w), self.word_similarity(word, w)) for w in board.remaining_words()]

    def word_similarity(self, word1, word2):
        if word1 + '.' + word2 in self.cache:
            return self.cache[word1 + '.' + word2]
        score = self.similarity_func(self.vectors[word1], self.vectors[word2])
        self.cache[word1+'.'+word2] = score
        self.cache[word2+'.'+word1] = score
        return score
