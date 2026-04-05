import requests
import random
import time

# Hardcoded port to match where Dockerized Django app is running
BASE_URL = "http://127.0.0.1:8000/api"

def register_device():
    print("Attempting to register a new mock device...")
    # Generate a random MAC address ending to avoid uniqueness errors
    mac_suffix = f"{random.randint(10, 99)}"
    
    device_data = {
        "name": f"Factory_Sensor_{mac_suffix}",
        "mac_address": f"00:1B:44:11:3A:{mac_suffix}"
    }
    
    response = requests.post(f"{BASE_URL}/devices/", json=device_data)
    
    if response.status_code == 201:
        device_id = response.json()['id']
        print(f"Success! Device registered with ID: {device_id}")
        return device_id
    else:
        print(f"Failed to register device. API responded with: {response.text}")
        return None

def send_sensor_data(device_id):
    print("\nStarting continuous data transmission. Press Ctrl+C to stop.")
    try:
        while True:
            # Generate synthetic data
            payload = {
                "device": device_id,
                "temperature": round(random.uniform(22.0, 28.5), 2),
                "humidity": round(random.uniform(45.0, 55.0), 2)
            }
            
            # Send the POST request to Django API
            response = requests.post(f"{BASE_URL}/readings/", json=payload)
            
            if response.status_code == 201:
                print(f"Data Sent -> Temp: {payload['temperature']}°C | Humidity: {payload['humidity']}%")
            else:
                print(f"Error sending data: {response.text}")
                
            time.sleep(3) 
            
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    device_id = register_device()
    if device_id:
        send_sensor_data(device_id)