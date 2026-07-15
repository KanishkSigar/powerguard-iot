export class ToggleSwitch {
    constructor() {
        this.element = document.createElement('div');
        this.element.className = 'ToggleSwitch'.toLowerCase();
    }
    render() {
        return this.element;
    }
}

