# Customer Sentiment and Feedback Analysis

This repository contains a data pipeline for generating synthetic customer transaction and review data, applying sentiment and topic modeling analysis, and loading results into a PostgreSQL database for reporting or BI consumption.

## 📦 Project Structure

- `main.py`: orchestrates the full pipeline by running `synthetic_data.py`, `sentiment_topic_analysis.py`, and `load_csv.py`.
- `synthetic_data.py`: generates synthetic datasets for customers, products, orders, and reviews, and writes CSV files under `data/`.
- `sentiment_topic_analysis.py`: reads `data/reviews.csv`, performs sentiment analysis (VADER), LDA topic modeling, and writes `data/processed_reviews.csv`.
- `load_csv.py`: imports CSV data into PostgreSQL tables using SQLAlchemy.

Data files (in `data/`):
- `customers.csv`
- `products.csv`
- `orders.csv`
- `reviews.csv`
- `processed_reviews.csv`

SQL folder:
- `sql qureies/kpi_quries.sql`
- `sql qureies/schema.sql`

## ⚙️ Requirements

Python packages (install with pip):

```bash
pip install -r requirements.txt
```

- pandas
- numpy
- faker
- sqlalchemy
- psycopg2-binary
- nltk
- spacy
- scikit-learn

## 🛠️ PostgreSQL Setup

1. Ensure PostgreSQL is running locally.
2. Create database:

```bash
psql -U postgres -c "CREATE DATABASE feedback_db;"
```

3. Connection string in `load_csv.py`:

```python
postgresql://postgres:password@localhost:5432/db_name
```

Update credentials if needed.

## 🚀 Run Pipeline

From project root:

```bash
python main.py
```

Pipeline steps:
1. `synthetic_data.py` -> generate synthetic `customers`, `products`, `orders`, `reviews`.
2. `sentiment_topic_analysis.py` -> perform sentiment and LDA topic modeling, save `processed_reviews.csv`.
3. `load_csv.py` -> load all CSVs into PostgreSQL tables `customers`, `products`, `orders`, `reviews`.

## 🔍 What the analysis does

### Sentiment analysis
- Uses NLTK VADER (`SentimentIntensityAnalyzer`).
- Labels reviews as `Positive`, `Neutral`, `Negative`.
- Adds `sentiment_score` and `sentiment_label` to `processed_reviews.csv`.

### Topic modeling
- Uses `CountVectorizer` + `LatentDirichletAllocation`.
- `NUM_TOPICS = 4`.
- Maps topics to:
  - Delivery & Logistics
  - Customer Service
  - Product Quality & Bugs
  - Pricing & Value

## 🧾 Output

- `data/processed_reviews.csv` contains review text, sentiment labels/scores, dominant topic, and mapped topic name.
- Tables in PostgreSQL: `customers`, `products`, `orders`, `reviews`.

## 🧪 Validation

Run these steps after pipeline completes:

```bash
ls data
python -c "import pandas as pd; print(pd.read_csv('data/processed_reviews.csv').head())"
```

## ✨ Optional extensions

- Add a config file for db credentials and synthetic sizes.
- Add unit tests for data generation and NLP functions.
- Add export to dashboard-ready CSV/XLSX.

