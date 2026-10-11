import json

from odoo import http
from odoo.http import request


class IoTTemperatureController(http.Controller):

    @http.route(
        "/iot/temperature",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def receive_temperature(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)

            device_id = str(data.get("device_id", "ESP32_DHT11_01"))
            temperature = float(data["temperature"])
            humidity = float(data["humidity"])

            if not (-50 <= temperature <= 100):
                return request.make_json_response(
                    {"error": "Invalid temperature"},
                    status=400,
                )

            if not (0 <= humidity <= 100):
                return request.make_json_response(
                    {"error": "Invalid humidity"},
                    status=400,
                )

            measurement = request.env["iot.temperature"].sudo().create({
                "device_id": device_id,
                "temperature": temperature,
                "humidity": humidity,
            })

            return request.make_json_response({
                "success": True,
                "measurement_id": measurement.id,
            })

        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            return request.make_json_response(
                {"error": "Invalid JSON or missing measurement fields"},
                status=400,
            )


    @http.route(
        "/iot/temperature/status",
        type="http",
        auth="user",
        methods=["GET"],
    )
    def temperature_status(self, **kwargs):
        latest = request.env["iot.temperature"].search(
            [("device_id", "=", "ESP32_DHT11_01")],
            order="measurement_date desc, id desc",
            limit=1,
        )

        if not latest:
            return request.make_json_response({
                "alert": False,
                "temperature": None,
            })

        return request.make_json_response({
            "alert": latest.temperature > 35,
            "temperature": latest.temperature,
        })
