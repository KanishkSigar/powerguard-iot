export class Sidebar {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Sidebar'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

