import requests
import time
import random
from datetime import datetime

def simulate_sensor_data(panel_id):
    hour = datetime.now().hour
    if 10 <= hour < 16:
        base_output = random.uniform(200, 300)
    else:
        base_output = random.uniform(10, 50)

    data = {
        "panel_id": panel_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "energy_wh": round(base_output, 2),
        "voltage": random.uniform(220, 240),
        "temperature": random.uniform(20, 45)
    }
    return data

def send_data_to_oracle(sensor_data):
    print(f"[IoT Simulator] Sending data: {sensor_data}")
    return True

if __name__ == "__main__":
    print("🌞 Simulating Solar Panel IoT Sensor...")
    while True:
        data = simulate_sensor_data("SOL-PANEL-001")
        send_data_to_oracle(data)
        time.sleep(5)