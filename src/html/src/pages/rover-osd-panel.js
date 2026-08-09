import {html, LitElement} from 'lit'
import {customElement, state} from 'lit/decorators.js'
import '../assets/mui.js'
import {elrsState, saveConfig} from '../utils/state.js'

@customElement('rover-osd-panel')
class RoverOsdPanel extends LitElement {
    @state() accessor enabled
    @state() accessor craftName
    @state() accessor cellCount
    @state() accessor lowBatteryEnabled
    @state() accessor lowBatteryThresholdCentivolts
    @state() accessor lowBatteryDelayMs

    createRenderRoot() {
        this.enabled = elrsState.config['rover-osd-enabled'] ?? true
        this.craftName = elrsState.config['rover-craft-name'] ?? 'RZGX ROVER'
        const configuredCellCount = Number.parseInt(elrsState.config['rover-cell-count'] ?? 2, 10)
        this.cellCount = Number.isNaN(configuredCellCount) ? 2 : Math.min(8, Math.max(0, configuredCellCount))
        this.lowBatteryEnabled = this.cellCount !== 0 && (elrsState.config['rover-low-battery-enabled'] ?? false)
        this.lowBatteryThresholdCentivolts = elrsState.config['rover-low-battery-threshold-cv'] ?? 350
        this.lowBatteryDelayMs = elrsState.config['rover-low-battery-delay-ms'] ?? 3000
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

                <div class="mui-select">
                    <select id="rover-voltage-mode" @change="${this.updateVoltageMode}">
                        <option value="0" ?selected=${this.cellCount === 0}>RX</option>
                        ${[1, 2, 3, 4, 5, 6, 7, 8].map((cells) => html`
                            <option value="${cells}" ?selected=${this.cellCount === cells}>${cells}S</option>
                        `)}
                    </select>
                    <label for="rover-voltage-mode">Voltage Mode</label>
                </div>

                <div class="mui-panel info-bg">
                    <b>Physical sensing still matters.</b> Selecting a mode only changes how firmware interprets
                    the analog reading; it does not switch the voltage source electrically. Choose <b>RX</b> only
                    when the external VBAT sensing lead is disconnected and the receiver is reading its BEC supply.
                    For 1S-8S, connect the sensing lead to the verified positive whole-pack terminal and select the
                    actual series cell count. Wrong wiring, mode, or cell count will produce a misleading voltage.
                </div>

                <div class="mui-checkbox">
                    <input id="rover-low-battery-enabled" type="checkbox"
                           .checked=${this.lowBatteryEnabled}
                           .disabled=${this.cellCount === 0}
                           @change="${(e) => this.lowBatteryEnabled = e.target.checked}" />
                    <label for="rover-low-battery-enabled">Enable Low-Battery Warning</label>
                </div>

                ${this.cellCount !== 0 && this.lowBatteryEnabled ? html`
                    <div class="mui-textfield">
                        <input id="rover-low-battery-threshold" type="number" min="2.50" max="4.50" step="0.01"
                               .value="${(this.lowBatteryThresholdCentivolts / 100).toFixed(2)}"
                               @input="${this.updateLowBatteryThreshold}" />
                        <label for="rover-low-battery-threshold">Low-Battery Threshold (V/cell)</label>
                    </div>

                    <div class="mui-select">
                        <select id="rover-low-battery-delay"
                                @change="${(e) => this.lowBatteryDelayMs = Number.parseInt(e.target.value, 10)}">
                            <option value="0" ?selected=${this.lowBatteryDelayMs === 0}>Immediate</option>
                            <option value="1000" ?selected=${this.lowBatteryDelayMs === 1000}>1 second</option>
                            <option value="3000" ?selected=${this.lowBatteryDelayMs === 3000}>3 seconds</option>
                            <option value="5000" ?selected=${this.lowBatteryDelayMs === 5000}>5 seconds</option>
                            <option value="10000" ?selected=${this.lowBatteryDelayMs === 10000}>10 seconds</option>
                        </select>
                        <label for="rover-low-battery-delay">Warning Delay</label>
                    </div>
                ` : ''}

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
                        <tr><td>Battery voltage</td><td>Filtered analog voltage: RX supply or average per cell</td></tr>
                        <tr><td>Low battery</td><td>User threshold and continuous delay, 1S-8S only</td></tr>
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

    updateVoltageMode(e) {
        const parsed = Number.parseInt(e.target.value, 10)
        this.cellCount = Number.isNaN(parsed) ? 2 : Math.min(8, Math.max(0, parsed))
        if (this.cellCount === 0)
            this.lowBatteryEnabled = false
    }

    updateLowBatteryThreshold(e) {
        const parsed = Number.parseFloat(e.target.value)
        if (!Number.isNaN(parsed))
            this.lowBatteryThresholdCentivolts = Math.round(Math.min(4.50, Math.max(2.50, parsed)) * 100)
    }

    checkChanged() {
        return this.enabled !== (elrsState.config['rover-osd-enabled'] ?? true) ||
            this.craftName !== (elrsState.config['rover-craft-name'] ?? 'RZGX ROVER') ||
            this.cellCount !== (elrsState.config['rover-cell-count'] ?? 2) ||
            this.lowBatteryEnabled !== (elrsState.config['rover-low-battery-enabled'] ?? false) ||
            this.lowBatteryThresholdCentivolts !== (elrsState.config['rover-low-battery-threshold-cv'] ?? 350) ||
            this.lowBatteryDelayMs !== (elrsState.config['rover-low-battery-delay-ms'] ?? 3000)
    }

    save(e) {
        e.preventDefault()
        saveConfig({
            'rover-osd-enabled': this.enabled,
            'rover-craft-name': this.craftName || 'RZGX ROVER',
            'rover-cell-count': this.cellCount,
            'rover-low-battery-enabled': this.cellCount !== 0 && this.lowBatteryEnabled,
            'rover-low-battery-threshold-cv': this.lowBatteryThresholdCentivolts,
            'rover-low-battery-delay-ms': this.lowBatteryDelayMs
        }, () => this.requestUpdate())
    }
}
