export class RadioButton {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'RadioButton'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

