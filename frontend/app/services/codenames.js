import $ from 'jquery';
import { A } from '@ember/array';
import Service from '@ember/service';
import config from '../config/environment';

export default Service.extend({
	makeBoard() {
		return $.get(`${config.backend}/board`);
	},
	getHint(team, board, history) {
		return $.post({
			url: `${config.backend}/hint/${team}`,
			data: JSON.stringify({ board, history }),
			contentType: 'application/json'
		});
	},
	guess(clue, quality, board){
		return $.post({
			url: `${config.backend}/guess/${clue}/${quality}`,
			data: JSON.stringify({ board }),
			contentType: 'application/json'
		});
	}
});
