import json
import random
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Configuration Odoo
URL = "http://localhost:8069/iot/temperature"
DATABASE = "odoo_iot_db"
DEVICE_ID = "ESP32_DHT11_01"
INTERVAL = 5  # secondes


def simulate_dht11():
    """Simule les mesures d'un capteur DHT11."""
    temperature = round(random.uniform(22.0, 32.0), 1)
    humidity = round(random.uniform(40.0, 75.0), 1)

    return temperature, humidity


def send_measurement(temperature, humidity):
    """Envoie une mesure à l'API Odoo."""
    data = {
        "device_id": DEVICE_ID,
        "temperature": temperature,
        "humidity": humidity,
    }

    request = Request(
        URL,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Odoo-Database": DATABASE,
        },
        method="POST",
    )

    with urlopen(request, timeout=15) as response:
        result = json.loads(response.read().decode("utf-8"))
        return response.status, result


def main():
    print("=== Simulation ESP32 + DHT11 ===")
    print(f"API Odoo : {URL}")
    print(f"Intervalle : {INTERVAL} secondes")
    print("Appuyez sur Ctrl+C pour arrêter.\n")

    try:
        while True:
            temperature, humidity = simulate_dht11()
            timestamp = datetime.now().strftime("%H:%M:%S")

            try:
                status, result = send_measurement(
                    temperature, humidity
                )

                if status == 200 and result.get("success"):
                    print(
                        f"[{timestamp}] "
                        f"Température : {temperature} °C | "
                        f"Humidité : {humidity} % | "
                        f"Mesure Odoo : {result['measurement_id']}"
                    )
                else:
                    print(f"[{timestamp}] Réponse inattendue : {result}")

            except HTTPError as error:
                details = error.read().decode("utf-8", errors="replace")
                print(f"[{timestamp}] Erreur HTTP {error.code} : {details}")

            except (URLError, TimeoutError, OSError) as error:
                print(f"[{timestamp}] Erreur de connexion : {error}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\nSimulation arrêtée.")


if __name__ == "__main__":
    main()