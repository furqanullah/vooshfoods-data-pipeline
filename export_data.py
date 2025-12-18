import json
from database import get_connection

def export_products():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch products
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    # Get column names
    columns = [desc[0] for desc in cursor.description]

    product_list = [dict(zip(columns, row)) for row in products]

    # Save to JSON
    with open("products.json", "w") as f:
        json.dump(product_list, f, indent=4)

    # Fetch last pipeline status
    cursor.execute("SELECT * FROM pipeline_status ORDER BY id DESC LIMIT 1")
    status_row = cursor.fetchone()
    status_columns = [desc[0] for desc in cursor.description]
    pipeline_status = dict(zip(status_columns, status_row)) if status_row else {}

    with open("pipeline_status.json", "w") as f:
        json.dump(pipeline_status, f, indent=4)

    conn.close()
    print("Exported products and pipeline status to JSON")

if __name__ == "__main__":
    export_products()
