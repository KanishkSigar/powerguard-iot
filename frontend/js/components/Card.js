export class Card {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Card'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

