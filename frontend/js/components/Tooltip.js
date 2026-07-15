export class Tooltip {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Tooltip'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

