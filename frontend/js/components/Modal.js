export class Modal {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Modal'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

