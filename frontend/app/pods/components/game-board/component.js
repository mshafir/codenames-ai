import Component from '@ember/component';

export default Component.extend({
	actions: {
		selectedCard(card) {
			this.sendAction('selectedCard', card);
		}
	}
});
