export class Breadcrumb {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Breadcrumb'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

