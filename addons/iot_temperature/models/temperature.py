
from odoo import models, fields, api


class IoTTemperature(models.Model):
    _name = "iot.temperature"
    _description = "IoT Temperature Measurement"
    _order = "measurement_date desc"

    device_id = fields.Char(
        string="Device ID",
        required=True,
        default="ESP32_DHT11_01",
    )

    temperature = fields.Float(
        string="Temperature (°C)",
        required=True,
    )

    humidity = fields.Float(
        string="Humidity (%)",
        required=True,
    )

    measurement_date = fields.Datetime(
        string="Measurement Date",
        required=True,
        default=fields.Datetime.now,
    )

    temperature_status = fields.Selection(
        [
            ("normal", "Normal"),
            ("alert", "High Temperature"),
        ],
        string="Temperature Status",
        compute="_compute_temperature_status",
        store=True,
    )

    @api.depends("temperature")
    def _compute_temperature_status(self):
        for record in self:
            if record.temperature > 35:
                record.temperature_status = "alert"
            else:
                record.temperature_status = "normal"
