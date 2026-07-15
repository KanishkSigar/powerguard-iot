export class Navbar {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Navbar'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

