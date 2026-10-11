
{
    "name": "IoT Temperature Monitoring",
    "version": "1.0.0",
    "category": "Technical",
    "summary": "Monitor temperature and humidity from IoT sensors",
    "depends": ["base", "web"],
    "data": [
        "security/ir.access.csv",
        "views/temperature_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "iot_temperature/static/src/js/temperature_alert.js",
            "iot_temperature/static/src/xml/temperature_alert.xml",
            "iot_temperature/static/src/css/temperature_alert.css",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    "author": "ENSIASD",
}
