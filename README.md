# IoT Sensor Data Ingestion & Monitoring API

A scalable backend system designed to ingest, cache, and retrieve real-time data streams from IoT devices. The project demonstrates modern backend architecture and performance optimization.

## Tech Stack
* **Framework:** *Django* & *Django REST Framework* (DRF)
* **Database:** *PostgreSQL* (for persistent historical data)
* **Caching:** *Redis* (for instant retrieval of real-time data)
* **Infrastructure:** *Docker & Docker Compose*

## Key Features
1. **Automated API Documentation:** Interactive Swagger UI provided via `drf-spectacular`.
2. **High-Performance Caching:** The `/latest_reading/` endpoint bypasses PostgreSQL entirely, fetching the most recent sensor data directly from Redis RAM in milliseconds.
3. **Database Optimization:** Django models are configured with composite indexes (`device`, `-timestamp`) to ensure historical time-series queries remain fast as the dataset grows to millions of rows.
4. **Live Data Simulation:** Includes a standalone Python script to simulate real-world IoT network traffic continuously hitting the API.

## Quick Start Guide

**1. Clone the repository and navigate to the directory:**
```bash
git clone https://github.com/your-username/iot-dashboard.git
cd iot-dashboard
```

**2. Spin up the infrastructure using Docker**
```bash
docker-compose up --build -d
```

**3. Run the initial database migrations:**
```bash
docker-compose exec web python manage.py migrate
```

**4. View the Interactive API Documentation:
Navigate to http://127.0.0.1:8000/api/docs/ in your browser.**


## Simulating IoT Traffic
To see the system in action, run the included simulation script. This will register a mock device and begin streaming temperature and humidity data to the database every 3 seconds.

(Ensure you have the requests library installed locally) 

```bash
pip install requests
```

**Run the IoT data simulation script**
```bash
python simulate_data.py
```

*While the script is running, grab the Device ID from the terminal output and hit the caching endpoint (e.g., http://127.0.0.1:8000/api/devices/{id}/latest_reading/) to see real-time data being served directly from Redis. (Replace id with digit which can be found http://127.0.0.1:8000/api/devices)*

**P.S. For the local demonstration, the application endpoints are mapped to localhost. You can access the base API and Swagger UI at http://127.0.0.1:8000/**