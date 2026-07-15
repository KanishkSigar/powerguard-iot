export class Accordion {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Accordion'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

