import $ from 'jquery';
import { A } from '@ember/array';
import Service from '@ember/service';
import config from '../config/environment';
import { later } from '@ember/runloop';

export default Service.extend({
	message: '',
	showMessage: false,
	displayMessage(message, timeout = 2000) {
		this.set('message', message);
		this.set('showMessage', true);
		later(this, this.hideMessage, timeout);
	},
	hideMessage(message) {
		this.set('showMessage', false);
	}
});
