# IoT Weather Sensor Data Cleaning & Telemetry Pipeline

An end-to-end data engineering pipeline built with **Python**, **Pandas**, and **SQL** designed to ingest, clean, and analyze real-world environmental sensor telemetry data (Temperature & Humidity) suffering from sensor dropouts, missing timestamps, and physical outliers.

---

## Project Overview
In industrial IoT and environmental monitoring systems, raw sensor data is notoriously messy. Hardware glitches cause extreme temperature spikes, network dropouts result in missing timestamps, and power failures leave gaps in the timeline. 

This project simulates and resolves these real-world data challenges by establishing a robust automated pipeline that:
1. **Parses & Standardizes** raw time-series telemetry logs.
2. **Detects & Handles Outliers** caused by sensor malfunction (e.g., impossible temperature/humidity readings) using statistical methods.
3. **Reindexes & Fills Temporal Gaps** to ensure a continuous, unbroken timeline for analysis.
4. **Persists Data to SQLite** and leverages **SQL Window Functions** to calculate rolling metrics for environmental trends.

---

## Tech Stack & Libraries
* **Language:** Python 3.x
* **Data Manipulation & Analysis:** Pandas, NumPy
* **Database & Querying:** SQLite, SQL Window Functions (`AVG() OVER (...)`)
* **Version Control:** Git & GitHub

---

## Pipeline Architecture & Steps

1. **Data Ingestion:** Loads raw sensor JSON/CSV logs containing erratic timestamps and faulty readings.
2. **Data Cleaning (IQR Method):** Identifies statistical outliers (values outside normal environmental thresholds) and treats them.
3. **Time-Series Reindexing:** Generates a complete hourly/daily time grid and handles missing gaps via interpolation or default baseline filling.
4. **SQL Integration:** Stores the cleaned dataset into an embedded SQLite database (`weather_sensors.db`).
5. **Analytical Queries:** Executes SQL window functions to compute rolling averages (e.g., 3-period moving averages) to smooth out short-term fluctuations
