export class Toast {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Toast'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

