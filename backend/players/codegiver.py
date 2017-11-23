import random
import numpy as np
from tqdm import tqdm
from collections import defaultdict


# aka. fathomability
SIMILARITY_THRESHOLD = 0.68
TOO_SIMILAR_THRESHOLD = 0.4
DISTINCTNESS_THRESHOLD = 0.07
COUNT_MIN_THRESHOLD = 8000000
COUNT_MAX_THRESHOLD = 50000000


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
    def __init__(self, word, num=0, similarity=0., distinctness=0., first_non_team_type='neutral', intended=None):
        self.word = word
        self.num = num
        self.similarity = similarity
        self.distinctness = distinctness
        self.intended = intended
        self.first_non_team_type = first_non_team_type

    def __str__(self):
        return "%s for %i (similarity: %f, distinctness: %f, first_non_team_type: %s, intended: %s)" % \
              (self.word, self.num, self.similarity, self.distinctness, self.first_non_team_type, ', '.join(self.intended))


class CodeGiverAI:
    def __init__(self, team, distances, counts, debug=False):
        self.team = team
        self.words = distances.keys()
        self.distances = distances
        self.counts = counts
        self.debug = debug
        self.history = set()

    def give_hint(self, board):
        print 'thinking...'
        hints = self.score_hints(board)
        best_hint = hints[0]
        if self.debug:
            for i in range(min(20, len(hints)-1)):
                print str(hints[i]) + ' FINAL: ' + str(self.evaluate_hint(hints[i]))
        self.history.add(best_hint.word)
        return best_hint.word, best_hint.num

    def evaluate_hint(self, hint):
        penalty = 0
        if hint.first_non_team_type == 'assassin':
            penalty = 0.2
        elif hint.first_non_team_type != 'neutral':
            penalty = 0.1
        return hint.num + hint.distinctness - hint.similarity - penalty

    def good_word(self, word, board):
        return (self.counts[word] < COUNT_MIN_THRESHOLD or self.counts[word] > COUNT_MAX_THRESHOLD
            and legal_word(word, board.words)
            and not word in self.history
            and word in self.distances)

    def score_hints(self, board):
        print "filtering potential words..."
        potential_words = [w for w in tqdm(self.words) if self.good_word(w, board)]
        print "evaluating hints..."
        hints = [self.score_word(w, board) for w in tqdm(potential_words)]
        hints = [hint for hint in hints if hint.num > 0]
        return sorted(hints, key=self.evaluate_hint, reverse=True)

    def score_word(self, word, board):
        scores = self.board_similarity(word, board)

        # lower is better, find best non-team type and score
        team_scores = []
        best_non_team_score = SIMILARITY_THRESHOLD
        best_non_team_type = 'neutral'
        for w, type, score in scores:
            if type == self.team:
                team_scores.append((w, type, score))
            else:
                if score < best_non_team_score:
                    best_non_team_score = score
                    best_non_team_type = type

        # find team words that fit within the similarity and distinctness threshold
        # given the bes non-team score
        hint_words = []
        worst_team_score = 0
        for w, type, score in team_scores:
            if best_non_team_score - score > DISTINCTNESS_THRESHOLD and score < SIMILARITY_THRESHOLD:
                hint_words.append((w, score))
                if score > worst_team_score:
                    worst_team_score = score

        num = len(hint_words)
        if num == 0:
            return Hint(word)

        # too close it's probably cheating
        if worst_team_score < TOO_SIMILAR_THRESHOLD:
            return Hint(word)

        explanation = [t[0] + ' (' + str(t[1]) + ')' for t in hint_words]
        return Hint(word, num, worst_team_score, best_non_team_score - worst_team_score, best_non_team_type, explanation)

    def board_similarity(self, word, board):
        return [(w, board.word_type(w), self.word_similarity(word, w)) for w in board.remaining_words()]

    def word_similarity(self, word1, word2):
        return self.distances[word1][word2]
