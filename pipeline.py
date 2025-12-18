import requests
from datetime import datetime, timezone
from database import create_tables, get_connection

# -----------------------------
# CONFIG
# -----------------------------
# API_URL = "https://fakestoreapi.com/products"
USD_TO_INR = 83

# FAILURE API
API_URL = "https://fakestoreapi.com/invalid"



# Slack webhook URL
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# -----------------------------
# SLACK ALERT
# -----------------------------
def send_slack_alert(message):
    payload = {
        "text": f"🚨 Data Pipeline Alert 🚨\n{message}"
    }
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print("Failed to send Slack alert:", e)

# -----------------------------
# DATA EXTRACTION
# -----------------------------
def fetch_data():
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()
    return response.json()

# -----------------------------
# DATA TRANSFORMATION
# -----------------------------
def transform_data(raw_data):
    transformed = []
    for item in raw_data:
        transformed.append({
            "id": item.get("id"),
            "title": item.get("title"),
            "price_usd": item.get("price"),
            "price_inr": round(item.get("price", 0) * USD_TO_INR, 2),
            "category": item.get("category"),
            "rating": item.get("rating", {}).get("rate"),
            "updated_at": datetime.now(timezone.utc).isoformat()
        })
    return transformed

# -----------------------------
# DATA STORAGE
# -----------------------------
def store_data(data):
    conn = get_connection()
    cursor = conn.cursor()

    for item in data:
        cursor.execute("""
        INSERT OR REPLACE INTO products
        (id, title, price_usd, price_inr, category, rating, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            item["id"],
            item["title"],
            item["price_usd"],
            item["price_inr"],
            item["category"],
            item["rating"],
            item["updated_at"]
        ))

    conn.commit()
    conn.close()
    print(f"Stored {len(data)} records into database")

# -----------------------------
# PIPELINE STATUS LOGGING
# -----------------------------
def log_status(status, message):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO pipeline_status (last_run, status, message)
    VALUES (?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        status,
        message
    ))

    conn.commit()
    conn.close()
    print(f"Pipeline Status Logged: {status}")

# -----------------------------
# RUN PIPELINE
# -----------------------------
def run_pipeline():
    create_tables()

    try:
        raw_data = fetch_data()
        print(f"Fetched {len(raw_data)} records from API at {datetime.now()}")

        transformed_data = transform_data(raw_data)
        print("Data transformed successfully")

        store_data(transformed_data)

        log_status("SUCCESS", "Pipeline ran successfully")

    except Exception as e:
        error_message = str(e)

        # Log failure to DB
        log_status("FAILED", error_message)

        # Log failure to file
        with open("error.log", "a") as f:
            f.write(f"{datetime.now(timezone.utc)} - {error_message}\n")

        # Send Slack alert
        send_slack_alert(error_message)

        print(f"Pipeline failed: {error_message}")

# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    run_pipeline()
