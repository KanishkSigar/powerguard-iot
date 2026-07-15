export class Alert {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Alert'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

