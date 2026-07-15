export class Dropdown {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Dropdown'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

