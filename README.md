# 📦 Real-Time E-commerce Analytics Pipeline on AWS

This project demonstrates a complete **real-time data pipeline** for ingesting, processing, storing, and analyzing product event data from an e-commerce platform using fully managed **AWS serverless services**.

## 🧱 Components

### 1. **Real-Time Ingestion**

- **Data Source**: Static product event data (`product_events.json`) hosted on a public S3 bucket.
- **Producer Lambda**:
  - Fetches and sends records to Amazon Kinesis Data Stream.
  - Implemented using Python and Boto3.
  - Handles batching and stream throttling.

### 2. **Stream Processing & Deduplication**

- **Kinesis Data Stream**:
  - Collects streaming events.
  - Triggered by consumer Lambda.

- **Consumer Lambda**:
  - Invoked by Kinesis.
  - Performs **deduplication** using DynamoDB (transaction_id as key).
  - Stores clean records into S3 **Bronze layer** in JSON format.

- **DynamoDB Table**:
  - `ecommerce_dedup_table` with transaction_id as partition key.
  - Ensures each event is processed only once.

### 3. **Data Lake Storage & Cataloging**

- **Amazon S3**:
  - Raw JSON data stored at `s3://ecommerce-product-data-bhaskar/bronze/raw-events/`.

- **AWS Glue Crawler**:
  - Crawls raw S3 data and populates metadata to the **Glue Data Catalog**.
  - Creates Athena-readable table: `ecommerce_raw_events_flat`.

### 4. **Query Layer**

- **Amazon Athena**:
  - Queries the `ecommerce_raw_events_flat` table.
  - Example analytics: Top 10 products by quantity sold.

- **AWS Wrangler (Python SDK)**:
  - Used from Jupyter Notebook to query Athena and visualize insights via Matplotlib/Seaborn.

---

## 📊 Sample Query: Top-Selling Products

```sql
SELECT product_name, SUM(quantity) AS total_quantity
FROM ecommerce_raw_events_flat
GROUP BY product_name
ORDER BY total_quantity DESC
LIMIT 10;
```

---

## 🔐 Security & IAM

- Lambda functions use **least-privilege IAM roles** with:
  - Kinesis put/consume permissions
  - DynamoDB read/write access
  - S3 write permissions
- CloudWatch logging is enabled for both Lambdas.

---

## ✅ Status

- ✔️ Producer Lambda tested and deployed
- ✔️ Deduplication working via DynamoDB
- ✔️ S3 Bronze layer operational
- ✔️ Glue Crawler setup and cataloging completed
- ✔️ Athena querying and Python visualization successful

---

## 📌 Future Enhancements

- Add Glue job for Silver → Gold layer ETL
- Enable Athena views for business teams
- Integrate QuickSight (optional – not used due to cost)

### Thanks 
