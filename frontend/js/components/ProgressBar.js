export class ProgressBar {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'ProgressBar'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

