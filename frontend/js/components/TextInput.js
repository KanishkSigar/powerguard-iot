export class TextInput {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'TextInput'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

