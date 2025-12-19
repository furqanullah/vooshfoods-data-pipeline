# End-to-End Data Pipeline with Monitoring & Dashboard

## 📌 Project Overview
This project implements a **simple yet production-style end-to-end data pipeline** that:

* Extracts data from a **public API**
* Transforms and enriches the data
* Stores it in a **SQL database**
* Exposes the data via a backend API
* Displays pipeline health and data in a **React dashboard**
* Includes **monitoring, logging, and Slack alerting** for failures

  ## 🖥️ Running the Project Locally
### 🔹 Prerequisites
* Python 3.9+
* Node.js 18+
* npm
* SQLite
### 🔹 Backend (Pipeline)
```bash
cd backend
pip install -r requirements.txt
python pipeline.py
```
### 🔹 Backend API (Node.js)
```bash
cd backend
npm install
node server.js

API runs at:
```
http://localhost:5000

## 🔹 Frontend Dashboard (React)
```bash
cd dashboard
npm install
npm start
```
Dashboard runs at:
```
http://localhost:3000
```

## 🔗 API Used
**Fake Store API**
[https://fakestoreapi.com/products](https://fakestoreapi.com/products)

**Why this API?**
* Public & free (no authentication)
* Realistic e-commerce data
* Suitable for testing reliability, transformations, and rerunnable pipelines

## 🏗️ Architecture
Public API
   ↓
Python ETL Pipeline
   ↓
SQLite Database
   ↓
Node.js Backend API
   ↓
React Dashboard

## ⚙️ Tech Stack
| Layer                            | Technology              |
| -------------------------------- | ----------------------- |
| Data Extraction & Transformation | Python                  |
| Database                         | SQLite                  |
| Backend API                      | Node.js (Express)       |
| Frontend Dashboard               | React                   |
| Monitoring                       | SQL status table + logs |
| Alerting                         | Slack Webhook           |


## 🔄 Data Pipeline Flow
### 1️⃣ Extraction
* Fetches product data from Fake Store API
* Handles timeouts, HTTP errors, and failures using try/except
* Logs failures and triggers Slack alerts

### 2️⃣ Transformation
* Normalizes fields
* Adds calculated column:
* `price_inr = price_usd × 83`
* Adds `updated_at` timestamp

### 3️⃣ Storage
* Stores data in SQLite
* Uses **idempotent inserts** (`INSERT OR REPLACE`)
* Pipeline can be safely re-run without duplication

### 4️⃣ Monitoring & Reliability
* Pipeline execution status stored in `pipeline_status` table
* Logs:

* `SUCCESS` or `FAILED`
* * Error message
* Timestamp
* Slack alert sent on failure
* Previous successful data is retained to avoid breaking downstream systems

### 5️⃣ Dashboard
* React UI displays:
* Pipeline status (SUCCESS / FAILED)
* Last run time and message
* Product table
* Aggregate metrics (total products, average price)

* On failure:
* Dashboard remains visible
  * Shows last successful data
  * Clearly indicates pipeline failure

## 📊 Database Schema
### products
* id (PRIMARY KEY)
* title
* price_usd
* price_inr
* category
* rating
* updated_at

### pipeline_status
* last_run
* status
* message

---
## 🚨 Monitoring & Alerts
* Pipeline failures are:

  * Logged in database
  * Written to log files
  * Sent to Slack via webhook
* Dashboard reflects real pipeline health
* Uses **graceful degradation** (last good data remains visible)

---
## 🚀  ✅ Implemented Slack notifications for pipeline failures.
  - Sends a message to the configured Slack channel whenever a job fails.

---
## 🚀 Improvements & Scaling (Future)
If this system were in production:
* Schedule pipeline using **cron / Azure Functions**
* Add authentication for APIs
* login and register page before redirecting Dashboard
* Deployement of front-end and backend
* Centralized logging & monitoring

---
## ✅ Key Takeaway
This project demonstrates:
* Reliable data pipelines
* Operational monitoring
* Clear system visibility


## Links

- **GitHub Repository:** https://github.com/furqanullah/vooshfoods-data-pipeline
- **Deployed Application:** https://vooshfoods-data-pipeline.netlify.app/
