import Component from '@ember/component';
import set from 'ember-metal/set';
import get from 'ember-metal/get';
import { A } from '@ember/array';
import { computed } from '@ember/object';
import { inject as service } from '@ember/service';
import { later } from '@ember/runloop';

export default Component.extend({
	mode: '', // ai or human
	turn: 'red', // red or blue
	phase: 'codegiving', // codegiving or guessing
	guesses: 0,
	assassinGuessed: false,
	history: A(),

	codenames: service(),
	messaging: service(),

	redLeft: computed('board', 'guesses', function() {
		return A(this.get('board')).filter(c => {
			return get(c, 'type') === 'red' && !get(c, 'found');
		}).get('length');
	}),

	blueLeft: computed('board', 'guesses', function() {
		return A(this.get('board')).filter(c => {
			return get(c, 'type') === 'blue' && !get(c, 'found');
		}).get('length');
	}),

	gameEnd: computed('redLeft', 'blueLeft', 'assassinGuessed', function() {
		return this.get('redLeft') === 0 || this.get('blueLeft') === 0 || this.get('assassinGuessed');
	}),

	getHint() {
		return this.get('codenames').getHint(this.get('turn'), this.get('board'), this.get('history')).then((hint) => {
			this.set('hintWord', hint.word);
			this.set('hintNum', hint.num);
			this.get('history').pushObject(hint.word);
			this.set('guesses', parseInt(hint.num) + 1);
			if (this.get('difficulty') === 'easy') {
				this.set('quality', 200);
			} else if (this.get('difficulty') === 'hard') {
				this.set('quality', 100);
			} else {
				this.set('quality', 0);
			}
			return hint;
		});
	},

	performGuess(board, word) {
		let card = A(board).find(c => get(c,'word') === word);
		if (this.makeGuess(card)) {
			if (this.get('guesses') > 1) {
				later(this, this.executeTurn, 2000);
			} else {
				this.nextPhase();
			}
		}
	},

	guess() {
		let board = this.get('board');
		return this.get('codenames').guess(
			this.get('hintWord'), this.get('quality'), board).then((guess) => {
				this.get('messaging').displayMessage(this.get('turn') + ' guesses '+guess.word);
				later(this, this.performGuess, board, guess.word, 2000);
			});
	},

	executeTurn() {
		if (this.get('gameEnd')) {
			return;
		}
		if (this.get('mode') === 'ai') {
			if (this.get('phase') === 'codegiving') {
				this.set('thinking', true);
				this.getHint().then(() => {
					this.set('thinking', false);
					this.nextPhase();
				});
			} else {
				later(this, this.guess, 2000);
			}
		}
	},

	nextPhase() {
		if (this.get('gameEnd')) {
			return;
		}
		if (this.get('phase') === 'codegiving') {
			this.set('phase', 'guessing');
		} else {
			this.set('phase', 'codegiving');
			this.set('hintWord', '');
			this.set('hintNum', '');
			this.set('turn', this.get('turn') === 'red' ? 'blue' : 'red');
		}
		let turn = this.get('turn');
		let numPlayers = this.get('numPlayers');
		if (turn === 'red' || parseInt(numPlayers) === 2) {
			this.set('mode', this.get('phase') === this.get('humanRole') ? 'human' : 'ai');
		} else {
			this.set('mode', 'ai');
		}
		this.executeTurn();
	},

	makeGuess(card) {
		let turn = this.get('turn');
		let type = get(card, 'type');

		set(card, 'found', true);
		if (type === turn) {
			this.get('messaging').displayMessage(`${turn} gets it right!`);
			// right!
			this.set('guesses', this.get('guesses') - 1);
			if (this.get('guesses') === 0) {
				this.nextPhase();
				return false;
			}
			return true;
		} else {
			this.get('messaging').displayMessage(`${turn} guessed a ${type} card.`);
			// wrong!
			this.set('guesses', 0);
			if (type === 'assassin') {
				this.set('assassinGuessed', turn);
			} else {
				this.nextPhase();
			}
			return false;
		}
	},

	actions: {
		playAgain() {
			this.set('mode', '');
			this.set('turn', 'red');
			this.set('assassinGuessed', false);
			this.set('phase', 'codegiving');
			this.set('guesses', 0);
			this.set('hintWord', '');
			this.set('hintNum', '');
			this.set('history', A());
		},
		start(option) {
			if (this.get('mode') === '') {
				this.set('humanRole', option);
				this.set('mode', 'chooseDifficulty');
			} else {
				this.get('codenames').makeBoard().then((board) => {
					this.set('board', board);
					this.set('difficulty', option);
					this.set('mode', this.get('phase') === this.get('humanRole') ? 'human' : 'ai');
					this.executeTurn();
				});
			}
		},
		submitHint(num) {
			this.set('hintNum', num);
			this.set('guesses', num + 1);
			this.set('quality', 100);
			this.nextPhase();
		},
		selectedCard(card) {
			let phase = this.get('phase');
			let mode = this.get('mode');
			let end = this.get('gameEnd');
			if (phase === 'guessing' && mode === 'human' && !end) {
				this.makeGuess(card);
			}
		},
		pass() {
			this.nextPhase();
		}
	}
});
