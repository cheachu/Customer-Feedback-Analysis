import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection
engine = create_engine("postgresql://postgres:123@localhost:5432/feedback_db")

# Load CSVs
print("Loading base tables...")
pd.read_csv("data/customers.csv").to_sql("customers", engine, if_exists="replace", index=False)
pd.read_csv("data/products.csv").to_sql("products", engine, if_exists="replace", index=False)
pd.read_csv("data/orders.csv").to_sql("orders", engine, if_exists="replace", index=False)
print("Loading processed reviews...")
try:
    pd.read_csv("data/processed_reviews.csv").to_sql("reviews", engine, if_exists="replace", index=False)
    print("All CSV files loaded into SQL database!")
except FileNotFoundError:
    print("Error: processed_reviews.csv not found. Please run sentiment_topic_analysis.py first.")