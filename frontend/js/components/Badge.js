export class Badge {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'Badge'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

