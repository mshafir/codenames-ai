import random
import time
from board import Board

class Game:
    def __init__(self, cards, red_team, blue_team):
        self.cards = cards
        self.codegivers = {
            "red": red_team[0],
            "blue": blue_team[0]
        }
        self.guessers = {
            "red": red_team[1],
            "blue": blue_team[1]
        }

    def start(self):
        random.shuffle(self.cards)
        self.board = Board(self.cards[:25])
        self.turn = 'red'
        self.tries = 0
        print
        print 'Welcome to Codenames!'
        print
        while not self.check_game_end():
            self.take_turn()
        print 'game over!'
        print
        self.restart()

    def restart(self):
        self.board.print_answers()
        again = raw_input('Do you want to play again? (y/n):')
        if again == 'n':
            exit()
        else:
            print
            self.start()

    def end_turn(self):
        if self.turn == 'red':
            self.turn = 'blue'
        else:
            self.turn = 'red'

    def take_turn(self):
        self.print_turn()
        current_turn = self.turn
        [self.clue, self.num] = self.codegivers[current_turn].give_hint(self.board)
        self.tries = self.num + 1
        while self.turn == current_turn:
            self.board.draw()
            self.print_hint()
            print str(self.tries) + ' guesses left'
            word = self.guessers[current_turn].guess(self.clue, self.board, self.tries)
            self.check_word(word)
            time.sleep(2)


    def print_turn(self):
        self.board.draw()
        print
        print 'Scores:'
        [red, blue] = self.board.scores()
        print '  red team:  ' + str(red) + ' agents left'
        print '  blue team: ' + str(blue) + ' agents left'
        print
        print self.turn + " team's turn"

    def print_hint(self):
        print
        print self.turn + " gave hint:"
        print '%s for %i' % (self.clue, self.num)

    def check_word(self, word):
        if word == 'pass':
            print self.turn + ' passes'
            self.end_turn()
        elif self.board.has_word(word):
            type = self.board.mark_word(word)
            print
            if type == self.turn:
                print 'Nice! you got it'
                self.tries -= 1
                if self.tries == 0 or self.check_game_end():
                    self.end_turn()
            elif type == 'assassin':
                print self.turn+' team guessed the assassin and lost'
                self.end_turn()
            elif type == 'neutral':
                print 'You guessed an innocent bystander. Turn over.'
                self.end_turn()
            else:
                print "You guessed the other team's word. Turn over."
                self.end_turn()
        else:
            print str(word) + ' is not on the board'

    def check_game_end(self):
        [red, blue] = self.board.scores()
        if red == 0:
            print 'red team won'
            return True
        if blue == 0:
            print 'blue team won'
            return True
        if self.board.assassin in self.board.found:
            return True
        return False
