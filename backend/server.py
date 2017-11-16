import random

from flask import Flask
from flask import jsonify, request

from game.board import Board
from players.codegiver import CodeGiverAI
from players.guesser import GuesserAI
from utils.utils import get_words, load_distances, load_word_counts

print 'loading word counts'
counts = load_word_counts('resources/word_counts.counts')

print 'loading similarities'
distances = load_distances('resources/cached.dist.cut')

print 'loading cards'
CARDS = 'resources/codenames.txt'
cards = get_words(CARDS)
cards = [w for w in cards if w in distances]

app = Flask(__name__)


def board_to_json(board):
    return [{
        "word": word,
        "type": board.word_type(word),
        "found": word in board.found
    } for word in board.words]

def json_to_board(board_json):
    words = [w['word'] for w in board_json]
    board = Board(words)
    board.red = set([w['word'] for w in board_json if w['type'] == 'red'])
    board.blue = set([w['word'] for w in board_json if w['type'] == 'blue'])
    board.neutral = set([w['word'] for w in board_json if w['type'] == 'neutral'])
    board.assassin = [w['word'] for w in board_json if w['type'] == 'assassin'][0]
    board.found = set([w['word'] for w in board_json if w['found']])
    return board

@app.route('/board')
def create_board():
    random.shuffle(cards)
    board = Board(cards[:25])
    random.shuffle(board.words)
    return jsonify(board_to_json(board))

@app.route('/hint/<team>', methods=['POST'])
def give_hint(team):
    board = json_to_board(request.get_json().get('board'))
    history = request.get_json().get('history')
    codegiver = CodeGiverAI(team, distances, counts, debug=True)
    codegiver.history = set(history)
    word, num = codegiver.give_hint(board)
    return jsonify({
        "word": word,
        "num": num
    })

@app.route('/guess/<clue>/<quality>', methods=['POST'])
def guess(clue, quality):
    board = json_to_board(request.get_json().get('board'))
    guesser = GuesserAI(distances, debug=True)
    word = guesser.guess(clue, board, 2, int(quality))
    return jsonify({
        "word": word
    })
