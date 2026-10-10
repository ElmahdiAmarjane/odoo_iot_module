from odoo import models, fields


class IoTTemperature(models.Model):
    _name = "iot.temperature"
    _description = "IoT Temperature Measurement"
    _order = "measurement_date desc"

    device_id = fields.Char(
        string="Device ID",
        required=True,
        default="ESP32_DHT11_01"
    )

    temperature = fields.Float(
        string="Temperature (°C)",
        required=True
    )

    humidity = fields.Float(
        string="Humidity (%)",
        required=True
    )

    measurement_date = fields.Datetime(
        string="Measurement Date",
        required=True,
        default=fields.Datetime.now
    )