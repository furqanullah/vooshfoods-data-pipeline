const express = require("express");
const sqlite3 = require("sqlite3").verbose();
const cors = require("cors");
const path = require("path");

const app = express();
app.use(cors());

const DB_PATH = path.join(__dirname, "..", "products.db");

function getConnection() {
  return new sqlite3.Database(DB_PATH);
}

/* ---------------- PIPELINE STATUS API ---------------- */
app.get("/status", (req, res) => {
  const db = getConnection();

  db.get(
    `SELECT status, message, last_run
     FROM pipeline_status
     ORDER BY last_run DESC
     LIMIT 1`,
    [],
    (err, row) => {
      if (err) {
        res.status(500).json({
          status: "ERROR",
          message: err.message,
          last_run: null,
        });
      } else if (!row) {
        res.json({
          status: "UNKNOWN",
          message: "No pipeline runs found",
          last_run: null,
        });
      } else {
        res.json(row);
      }
    }
  );

  db.close();
});

/* ---------------- PRODUCTS API ---------------- */
app.get("/products", (req, res) => {
  const db = getConnection();

  db.all(
    `SELECT id, title, category, price_usd, price_inr, rating
     FROM products
     ORDER BY id`,
    [],
    (err, rows) => {
      if (err) {
        res.status(500).json({
          status: "error",
          message: err.message,
        });
      } else {
        res.json({
          status: "success",
          count: rows.length,
          data: rows,
        });
      }
    }
  );

  db.close();
});

/* ---------------- SERVER START ---------------- */
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`✅ Backend running at http://localhost:${PORT}`);
});
