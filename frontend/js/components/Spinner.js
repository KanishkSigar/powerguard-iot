export class Spinner {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Spinner'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

