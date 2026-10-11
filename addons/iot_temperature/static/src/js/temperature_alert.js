
/** @odoo-module **/

import { Component, onWillStart, onWillUnmount, proxy } from "@odoo/owl";
import { registry } from "@web/core/registry";

class TemperatureAlert extends Component {
    static template = "iot_temperature.TemperatureAlert";

    setup() {
        this.state = proxy({
            alert: false,
            temperature: null,
        });

        this.timer = null;

        onWillStart(async () => {
            await this.checkTemperature();

            this.timer = setInterval(
                () => this.checkTemperature(),
                5000
            );
        });

        onWillUnmount(() => {
            if (this.timer) {
                clearInterval(this.timer);
            }
        });
    }

    async checkTemperature() {
        try {
            const response = await fetch("/iot/temperature/status", {
                method: "GET",
                credentials: "same-origin",
            });

            if (!response.ok) {
                return;
            }

            const data = await response.json();

            this.state.alert = Boolean(data.alert);
            this.state.temperature = data.temperature;
        } catch (error) {
            console.error("Temperature alert check failed:", error);
        }
    }
}

registry.category("systray").add(
    "iot_temperature.TemperatureAlert",
    { Component: TemperatureAlert },
    { sequence: 1 }
);
