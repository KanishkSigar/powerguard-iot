export class Button {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Button'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

