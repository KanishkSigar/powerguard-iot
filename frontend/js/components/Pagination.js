export class Pagination {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Pagination'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

