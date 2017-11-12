import Controller from '@ember/controller';

export default Controller.extend({
	queryParams: [ 'numPlayers', 'humanRole', 'difficulty' ],
	numPlayers: 1,
	humanRole: 'guessing',
	difficulty: 'easy'
});
