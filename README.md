# Real-Time Sales Data Pipeline — MySQL

An end-to-end sales data engineering project that ingests CSV sales data, validates and transforms records with Python, loads the data into MySQL, performs analytical SQL queries, and exposes business insights through a Streamlit dashboard.

## 🚀 Project Overview

This project simulates a real-world sales data pipeline where incoming sales records are processed automatically and transformed into structured data for analytics.

The pipeline is designed around a simple flow:

```text
Incoming CSV
     ↓
Python ETL
     ↓
Data Validation & Transformation
     ↓
MySQL Database
     ↓
SQL Analytics
     ↓
Streamlit Dashboard
```

The project demonstrates practical skills in **Python, SQL, MySQL, ETL, data validation, database design, Linux automation, testing, and dashboard development**.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │   Incoming CSV Data │
                    │  data/incoming/     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Python ETL      │
                    │                     │
                    │ • Read CSV          │
                    │ • Validate records  │
                    │ • Transform data    │
                    │ • Handle failures   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       MySQL        │
                    │                     │
                    │ • Customers         │
                    │ • Products          │
                    │ • Stores            │
                    │ • Orders            │
                    │ • Order Items       │
                    │ • Payments          │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌─────────────────┐   ┌─────────────────┐
          │  SQL Analytics  │   │    Dashboard    │
          │                 │   │                 │
          │ • Revenue       │   │    Streamlit    │
          │ • Products      │   │   Visualization │
          │ • Customers     │   │                 │
          │ • Trends        │   │                 │
          └─────────────────┘   └─────────────────┘

                    Linux Automation
                          │
                          ▼
                    Bash + Cron
```

---

## ✨ Key Features

* **CSV-based data ingestion**
* Python ETL pipeline using Pandas
* Data validation and transformation
* Invalid-record handling
* MySQL relational database
* Batch loading into MySQL
* Duplicate protection during ingestion
* Transaction-based database loading
* Structured pipeline logging
* SQL analytics for business insights
* Streamlit dashboard
* Linux Bash automation
* Cron-based scheduled execution
* Transformation unit tests
* Environment-based database configuration

---

## 🛠️ Technology Stack

| Technology | Purpose                          |
| ---------- | -------------------------------- |
| Python     | ETL and data processing          |
| Pandas     | Data cleaning and transformation |
| MySQL      | Relational data storage          |
| SQL        | Analytics and reporting          |
| Streamlit  | Dashboard                        |
| Bash       | Pipeline automation              |
| Cron       | Scheduled execution on Linux     |
| Git/GitHub | Version control                  |
| Pytest     | Testing                          |

---

## 📂 Project Structure

```text
real-time-sales-data-pipeline/
│
├── dashboard/
│   └── app.py
│
├── data/
│   └── incoming/
│       └── sales_sample.csv
│
├── scripts/
│   └── run_pipeline.sh
│
├── sql/
│   ├── schema.sql
│   ├── indexes.sql
│   └── analytics.sql
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── generate_data.py
│   ├── pipeline.py
│   └── transform.py
│
├── tests/
│   └── test_transform.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ⚙️ How the Pipeline Works

### 1. Data Generation

A Python script generates sample sales data for development and testing.

```bash
python src/generate_data.py
```

The generated CSV is placed in:

```text
data/incoming/
```

### 2. Data Validation

The ETL pipeline reads the incoming CSV and validates the records before loading them into the database.

Validation and transformation are handled in:

```text
src/transform.py
```

Invalid records can be separated from valid records for further inspection.

### 3. Database Loading

The cleaned records are loaded into MySQL through:

```text
src/db.py
src/pipeline.py
```

The database contains separate entities for customers, products, stores, orders, order items, and payments.

### 4. SQL Analytics

Analytical queries are stored in:

```text
sql/analytics.sql
```

These queries can be used to analyze sales performance and generate business metrics.

### 5. Dashboard

The Streamlit application provides a visual layer for exploring the processed sales data.

```bash
streamlit run dashboard/app.py
```

---

## 🗄️ Database Design

The pipeline uses a relational MySQL model consisting of:

```text
Customers
    │
    └──── Orders
             │
             ├──── Order Items ──── Products
             │
             └──── Payments

Stores ───── Orders
```

This structure separates transactional data from reference data and supports analytical queries across customers, products, stores, and orders.

---

## 📊 Analytics

The SQL layer is designed to answer questions such as:

* What is the total sales revenue?
* Which products generate the most revenue?
* Which customers contribute the most sales?
* Which stores perform best?
* What is the average order value?
* What are the daily and monthly sales trends?
* Which products have the highest sales volume?
* How does sales performance change over time?
* What is the estimated profit and profit margin?

---

## 🧪 Testing

Transformation logic can be tested with:

```bash
pytest
```

Tests are located in:

```text
tests/
```

---

## 🐧 Linux Automation

The pipeline can also be executed on Linux using the Bash script:

```bash
chmod +x scripts/run_pipeline.sh
```

It can then be scheduled with cron.

Example:

```cron
0 * * * * /absolute/path/to/real-time-sales-data-pipeline/scripts/run_pipeline.sh
```

This allows the pipeline to run automatically at scheduled intervals.

---

## 🔐 Configuration

Create a local `.env` file from `.env.example`:

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sales_pipeline
DB_USER=root
DB_PASSWORD=your_mysql_password
```

**Never commit `.env` to GitHub.**

The repository intentionally excludes credentials and local virtual-environment files.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sandeep-ande23/Real_time_sales_data_pipeline.git
cd Real_time_sales_data_pipeline
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Create the database and tables using:

```text
sql/schema.sql
sql/indexes.sql
```

Then configure your local `.env` file.

### 5. Generate sample data

```bash
python src/generate_data.py
```

### 6. Run the ETL pipeline

```bash
python src/pipeline.py
```

### 7. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

---

## 📌 What This Project Demonstrates

This project demonstrates practical experience with:

* ETL pipeline development
* Relational database design
* SQL querying and analytics
* Data cleaning and validation
* Python data processing
* Batch database loading
* Transaction handling
* Automated data ingestion
* Linux command-line automation
* Scheduled jobs with cron
* Unit testing
* Data visualization
* Git and GitHub workflow

---

## 🔮 Future Improvements

Potential extensions include:

* Real-time ingestion using Kafka
* REST API-based data ingestion
* Cloud deployment
* AWS S3 data storage
* Airflow orchestration
* Docker containerization
* CI/CD with GitHub Actions
* Advanced sales forecasting
* Role-based dashboard access

---

## 👨‍💻 Author

**Sandeep Kumar**

Electrical Engineering | Data Analytics | Python | SQL | Linux

[GitHub](https://github.com/sandeep-ande23)

---

## 📄 License

This project is available for educational and portfolio purposes.
