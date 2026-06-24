# Sensors Dfrobots - Weather Station Monitoring System

This repository contains the core code, scripts, configurations, and flows for the **DFRobot Weather Station** environmental monitoring system.

---

## Repository Structure

```
Sensors-Dfrobots/
├── Sensor Weather/
│   ├── log_weather_data.py# Daemon script to log weather telemetry
│   ├── train1_model.py    # Python machine learning/prediction script
│   └── new/
│       ├── flows.json     # Node-RED orchestrator flow (Dashboard layout)
│       └── weather_clean.py # Clean sensor reading script
└── README.md
```

---

## 🛠 Features

* **Data Ingestion:** `weather_clean.py` reads telemetry (wind, rain, temperature, etc.) from DFRobot sensors.
* **Orchestration:** Node-RED is used to manage scheduled reads and layout the dashboard interface.
* **Storage:** Telemetry is written directly to an InfluxDB database (`1.x` version) via Node-RED.

---

## 🚀 Getting Started

### Prerequisites

* Python 3
* Pip dependencies:
  ```bash
  pip install pymodbus pyserial
  ```
* A running **Node-RED** instance with InfluxDB and MQTT node packages installed.

### Setup

1. Run the clean weather script:
   ```bash
   python3 "Sensor Weather/new/weather_clean.py"
   ```
2. Import the `Sensor Weather/new/flows.json` flow directly into your Node-RED editor.
