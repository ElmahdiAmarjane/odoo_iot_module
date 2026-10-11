import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

url = "http://localhost:8069/iot/temperature"

data = {
    "device_id": "ESP32_DHT11_01",
    "temperature":40.5,
    "humidity": 61.2
}

req = Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "X-Odoo-Database": "odoo_iot_db"
    },
    method="POST"
)

try:
    with urlopen(req, timeout=15) as response:
        print("HTTP :", response.status)
        print("Réponse :", response.read().decode("utf-8"))
except HTTPError as e:
    print("HTTP :", e.code)
    print("Réponse :", e.read().decode("utf-8"))
except URLError as e:
    print("Erreur de connexion :", e.reason)
