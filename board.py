import random
import math


def pad_left(text, size, char=' '):
    if len(text) >= size:
        return text
    else:
        return text + (size-len(text))*char


def pad_center(text, size, char=' '):
    if len(text) >= size:
        return text
    else:
        extra = float(size-len(text))
        first = int(math.floor(extra / 2))
        second = int(math.ceil(extra / 2))
        return first*char + text + second*char


class Board:
    def __init__(self, words):
        self.words = words
        self.red = set(self.words[:9])
        self.blue = set(self.words[9:17])
        self.assassin = self.words[17]
        self.neutral = set(self.words[18:])
        self.found = set()
        random.shuffle(self.words)

    def word_type(self, word):
        if word in self.red:
            return 'red'
        elif word in self.blue:
            return 'blue'
        elif word == self.assassin:
            return 'assassin'
        else:
            return 'neutral'

    def draw_word(self, word):
        text = word
        if word in self.found:
            return ' '+pad_center(self.word_type(word).upper(), 17, '~')+' '
        else:
            return ' '+pad_left(text, 18)

    def draw_line(self, words):
        print '|' + '|'.join([self.draw_word(word) for word in words]) + '|'

    def draw(self):
        print ('|' + '-'*19)*5+'|'
        for line_start in range(5):
            self.draw_line(self.words[line_start * 5:((line_start + 1) * 5)])
        print ('|' + '-' * 19) * 5 + '|'

    def print_answers(self):
        print self.get_answers()

    def get_answers(self):
        str = 'red: ' + ', '.join(self.red) + '\n'
        str += 'blue: ' + ', '.join(self.blue) + '\n'
        str += 'neutral: ' + ', '.join(self.neutral) + '\n'
        str += 'assassin: ' + self.assassin + '\n'
        return str

    def scores(self):
        return [len(self.red - self.found), len(self.blue - self.found)]

    def remaining_words(self):
        return set(self.words) - self.found

    def has_word(self, word):
        return word in self.words

    def mark_word(self, word):
        self.found.add(word)
        return self.word_type(word)



