import {html, LitElement} from 'lit'
import {customElement, state} from 'lit/decorators.js'
import '../assets/mui.js'
import {elrsState, saveConfig} from '../utils/state.js'

@customElement('rover-osd-panel')
class RoverOsdPanel extends LitElement {
    @state() accessor enabled
    @state() accessor craftName
    @state() accessor cellCount

    createRenderRoot() {
        this.enabled = elrsState.config['rover-osd-enabled'] ?? true
        this.craftName = elrsState.config['rover-craft-name'] ?? 'RZGX ROVER'
        this.cellCount = elrsState.config['rover-cell-count'] ?? 2
        return this
    }

    render() {
        return html`
            <div class="mui-panel mui--text-title">RZGX Rover OSD</div>
            <div class="mui-panel">
                <div class="mui-checkbox">
                    <input id="rover-osd-enabled" type="checkbox"
                           ?checked="${this.enabled}"
                           @change="${(e) => this.enabled = e.target.checked}" />
                    <label for="rover-osd-enabled">Enable Rover OSD</label>
                </div>

                <div class="mui-textfield">
                    <input id="rover-craft-name" type="text" maxlength="16"
                           .value="${this.craftName}"
                           @input="${this.updateCraftName}" />
                    <label for="rover-craft-name">Craft Name (maximum 16 characters)</label>
                </div>

                <div class="mui-textfield">
                    <input id="rover-cell-count" type="number" min="1" max="8" step="1"
                           .value="${this.cellCount}"
                           @input="${this.updateCellCount}" />
                    <label for="rover-cell-count">Battery Cell Count (1-8 cells)</label>
                </div>

                <button class="mui-btn mui-btn--small mui-btn--primary"
                        ?disabled="${!this.checkChanged()}"
                        @click="${this.save}">Save</button>
            </div>

            <div class="mui-panel mui--text-title">MVP Sources</div>
            <div class="mui-panel">
                <table class="mui-table mui-table--bordered">
                    <thead><tr><th>OSD item</th><th>Source</th></tr></thead>
                    <tbody>
                        <tr><td>Steering</td><td>CH1</td></tr>
                        <tr><td>Gas</td><td>CH2</td></tr>
                        <tr><td>Arming</td><td>Receiver arming state</td></tr>
                        <tr><td>Battery voltage</td><td>Filtered receiver analog VBAT, average per cell</td></tr>
                        <tr><td>RSSI / LQ</td><td>Receiver link statistics</td></tr>
                    </tbody>
                </table>
            </div>

            <div class="mui-panel info-bg">
                <b>Supported PWM receivers:</b> DJI serial communication uses Output 2 as UART TX
                and Output 3 as UART RX. These outputs cannot provide PWM while serial mode is active.
            </div>
        `
    }

    updateCraftName(e) {
        const cleaned = e.target.value.toUpperCase().replace(/[^A-Z0-9 _-]/g, '')
        e.target.value = cleaned
        this.craftName = cleaned
    }

    updateCellCount(e) {
        const parsed = Number.parseInt(e.target.value, 10)
        this.cellCount = Number.isNaN(parsed) ? 2 : Math.min(8, Math.max(1, parsed))
    }

    checkChanged() {
        return this.enabled !== (elrsState.config['rover-osd-enabled'] ?? true) ||
            this.craftName !== (elrsState.config['rover-craft-name'] ?? 'RZGX ROVER') ||
            this.cellCount !== (elrsState.config['rover-cell-count'] ?? 2)
    }

    save(e) {
        e.preventDefault()
        saveConfig({
            'rover-osd-enabled': this.enabled,
            'rover-craft-name': this.craftName || 'RZGX ROVER',
            'rover-cell-count': this.cellCount
        }, () => this.requestUpdate())
    }
}
