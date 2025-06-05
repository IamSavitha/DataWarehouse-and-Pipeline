# 🚍 Public Transit Performance Analytics

This project implements a real-time data pipeline to monitor and analyze public transit performance using live data from public transportation APIs. The pipeline leverages **Apache Airflow**, **dbt**, and **Snowflake** to ingest, transform, and store data. The insights are visualized using **Power BI** to support operational planning and service optimization for transit agencies.

---

## 🔧 Technologies Used

- **Apache Airflow** – Workflow orchestration
- **Python** – Data ingestion and API interaction
- **dbt (Data Build Tool)** – Data transformation and modeling
- **Snowflake** – Cloud data warehouse
- **Power BI** – Data visualization

---

## 📊 Project Goals

- Ingest real-time and historical GTFS-RT data from transit APIs
- Clean and transform data for analytics
- Calculate key metrics such as average delay, on-time performance, and congestion patterns
- Enable transit planners to optimize routes and scheduling based on data

---

## 📁 Project Structure

Public_Transit_Performance_Analytics/
│
├── dags/
│ └── transit_etl_dag.py # Airflow DAG for ETL orchestration
│
├── scripts/
│ └── ingest_gtfs_rt.py # Python script to pull GTFS-RT data
│
├── dbt_transit/
│ ├── models/
│ │ ├── staging/
│ │ │ └── stg_trip_updates.sql # Cleaned raw trip updates
│ │ └── marts/
│ │ └── fct_route_performance.sql # Final performance metrics
│ └── dbt_project.yml # dbt project configuration
│
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🔁 ETL Pipeline Overview

### Ingestion:
- Collects data from a public GTFS-RT API endpoint
- Parses trip updates, delay data, and metadata
- Stores the raw data into a Snowflake table: `raw_trip_updates`

### Transformation:
- dbt is used to transform the raw data:
  - `stg_trip_updates`: Standardizes and flattens the raw feed
  - `fct_route_performance`: Aggregates performance metrics

### Visualization:
- Power BI connects to Snowflake to create dashboards showing:
  - Average delay per route
  - On-time rate over time
  - Congestion trends by hour and day

---

## ✅ Key Metrics

- **Average Delay** (in minutes)
- **On-Time Performance** (% trips delayed ≤ 5 minutes)
- **Trip Volume** (by route, date, and hour)
- **Congestion Heatmaps**

---

## 🚀 How to Run This Project

### 1. Clone the Repository

```bash
git clone https://github.com/IamSavitha/Public_Transit_Performance_Analytics.git
cd Public_Transit_Performance_Analytics

---

### 2. Install Python Dependencies
bash
Copy
Edit
pip install -r requirements.txt

---

### 3. Configure Airflow
Add transit_etl_dag.py to your Airflow DAGs folder

Set up a scheduler and webserver to run the pipeline

---

### 4. Snowflake Setup
Create a Snowflake database and table raw_trip_updates

Update credentials in ingest_gtfs_rt.py or use Airflow connections

---

### 5. Run dbt Models
bash
Copy
Edit
cd dbt_transit
dbt run

---

### 6. Power BI Dashboard
Connect Power BI to Snowflake

Use fct_route_performance for reports and metrics

📬 Contact
Savitha Vijayarangan
GitHub • LinkedIn

📌 Future Enhancements
Integrate GTFS static data for route and stop mapping

Include weather or event-based delay factors

Add streaming ingestion using Kafka or AWS Kinesis