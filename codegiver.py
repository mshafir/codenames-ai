from scipy.spatial import distance


# aka. fathomability
SIMILARITY_THRESHOLD = 10


class CodeGiverHuman:
    def give_hint(self, board):
        clue = raw_input('What is your clue?\n > ')
        num = raw_input('How many words is your clue for? \n > ')
        return clue, int(num)


class CodeGiverAI:
    def __init__(self, team, vectors, debug=False):
        self.team = team
        self.words = vectors.keys()
        self.vectors = vectors
        self.debug = debug

    def give_hint(self, board):
        scores = self.score_words(board)
        best_score = scores[0]
        if self.debug:
            print 'distinctness: '+str(best_score[1][1])
            print 'intending: ' + ', '.join(str(best_score[1][2]))
        return best_score[0], best_score[1][0]

    def score_words(self, board):
        scores = [self.score_word(w, board) for w in self.words if w not in board.words]
        return sorted(scores, key=lambda w:w[1][1], reverse=True)

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
            return word, (0, 0, [])

        # the number to give and how distinct the clue is from other words on the board
        num = len(guessable_words)
        distinctness = guessable_words[-1][1] - first_non_team_word[1]

        # penalty to distinctness depending on type
        if first_non_team_type == 'assassin':
            distinctness -= 0.2
        elif first_non_team_type != 'neutral':
            distinctness -= 0.1

        return word, (num, distinctness, [t[0] + ' (' + str(t[1]) + ')' for t in guessable_words])

    def board_similarity(self, word, board):
        return [(w, board.word_type(w), self.word_similarity(word, w)) for w in board.remaining_words()]

    def word_similarity(self, word1, word2):
        return distance.euclidean(self.vectors[word1], self.vectors[word2])

