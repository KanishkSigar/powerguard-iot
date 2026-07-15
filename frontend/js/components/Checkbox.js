export class Checkbox {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Checkbox'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

