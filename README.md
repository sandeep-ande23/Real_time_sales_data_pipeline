# Real-Time Sales Data Pipeline — MySQL Edition

A portfolio-ready Python + MySQL + Linux sales data pipeline.

## Architecture

Incoming CSV → Python ETL → Validation → MySQL → SQL Analytics → Streamlit Dashboard

Linux automation is supported through Bash + cron.

## Features

- MySQL relational database
- Python ETL pipeline
- Data validation and quarantine for bad rows
- Incremental CSV ingestion
- Duplicate-order protection
- Structured logging
- SQL analytics using CTEs and window functions
- Streamlit dashboard
- Linux cron automation
- Tests for transformations

## Windows / MySQL Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Create the database

Open MySQL Workbench or the MySQL command line and run:

```sql
SOURCE path/to/sql/schema.sql;
SOURCE path/to/sql/indexes.sql;
```

Or open both files in MySQL Workbench and execute them.

### 3. Configure credentials

Copy:

```text
.env.example → .env
```

Then set your MySQL username/password.

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=sales_pipeline
DB_USER=root
DB_PASSWORD=your_password
```

### 4. Generate sample sales data

```bash
python src/generate_data.py
```

### 5. Run the ETL pipeline

```bash
python src/pipeline.py
```

### 6. Start the dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will open in your browser.

### 7. Run tests

```bash
pytest
```

## Linux automation

On Linux:

```bash
chmod +x scripts/run_pipeline.sh
```

Example hourly cron job:

```cron
0 * * * * /absolute/path/to/sales-data-pipeline/scripts/run_pipeline.sh
```

## Project structure

```text
sales-data-pipeline/
├── data/
│   ├── incoming/
│   ├── processed/
│   └── failed/
├── src/
│   ├── config.py
│   ├── db.py
│   ├── generate_data.py
│   ├── transform.py
│   └── pipeline.py
├── sql/
│   ├── schema.sql
│   ├── indexes.sql
│   └── analytics.sql
├── scripts/
│   └── run_pipeline.sh
├── dashboard/
│   └── app.py
├── tests/
├── logs/
├── requirements.txt
├── .env.example
└── README.md
```

## Portfolio description

This project demonstrates an end-to-end sales data workflow using Python, MySQL, SQL analytics, Linux automation, validation, logging, and dashboarding.
