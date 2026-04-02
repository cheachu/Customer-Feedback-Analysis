import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker("en_IN")

NUM_CUSTOMERS = 75000
NUM_PRODUCTS = 200
NUM_ORDERS = 100000
NUM_REVIEWS = 60000

industries = [
    "Technology",
    "Finance",
    "Healthcare",
    "Retail",
    "Education",
    "Manufacturing",
]
regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Software", "Office", "Accessories"]
order_statuses = ["Completed", "Returned", "Cancelled"]

# Sample feedback templates to ensure LDA has distinct topics to find
positive_phrases = [
    "Amazing quality and fast delivery.",
    "The product works exactly as advertised.",
    "Customer service was very helpful.",
    "Highly recommend this to everyone.",
    "Great value for the money.",
    "Exceeded my expectations.",
]
negative_phrases = [
    "The battery life is terrible.",
    "Software keeps crashing and is buggy.",
    "Delivery was delayed by a week.",
    "Customer support was unresponsive.",
    "Product arrived damaged.",
    "Too expensive for what it offers, completely broken.",
]
neutral_phrases = [
    "It is okay, does the job.",
    "Average product, nothing special.",
    "Decent, but could be improved.",
    "Standard quality, as expected.",
]

print("Generating Customers...")
customers = [
    {
        "customer_id": i,
        "name": fake.name(),
        "city": fake.city(),
        "region": random.choice(regions),
        "industry": random.choice(industries),
        "signup_date": fake.date_between(start_date="-3y", end_date="today"),
    }
    for i in range(1, NUM_CUSTOMERS + 1)
]
customers_df = pd.DataFrame(customers)

print("Generating Products...")
products = []
for i in range(1, NUM_PRODUCTS + 1):
    price = random.randint(20, 800)
    products.append(
        {
            "product_id": i,
            "product_name": f"Product_{i}",
            "category": random.choice(categories),
            "price": price,
            "cost": round(price * random.uniform(0.4, 0.7), 2),
        }
    )
products_df = pd.DataFrame(products)

print("Generating Orders...")
orders = []
for i in range(1, NUM_ORDERS + 1):
    prod = random.choice(products)
    qty = np.random.choice([1, 2, 3, 4], p=[0.5, 0.3, 0.15, 0.05])
    orders.append(
        {
            "order_id": i,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "product_id": prod["product_id"],
            "order_date": fake.date_between(start_date="-2y", end_date="today"),
            "quantity": qty,
            "price": prod["price"],
            "discount_percent": random.choice([0, 0, 0, 5, 10, 15]),
            "status": random.choices(order_statuses, weights=[0.9, 0.07, 0.03])[0],
        }
    )
orders_df = pd.DataFrame(orders)

print("Generating Reviews (Unstructured Data)...")
reviews = []
# Select a random subset of orders to have reviews
reviewed_orders = orders_df.sample(n=NUM_REVIEWS, random_state=42)

for index, row in reviewed_orders.iterrows():
    # Simulate a realistic distribution of ratings
    rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.1, 0.2, 0.3, 0.3])

    if rating >= 4:
        text = random.choice(positive_phrases) + " " + fake.sentence()
    elif rating == 3:
        text = random.choice(neutral_phrases) + " " + fake.sentence()
    else:
        text = random.choice(negative_phrases) + " " + fake.sentence()

    reviews.append(
        {
            "review_id": len(reviews) + 1,
            "order_id": row["order_id"],
            "customer_id": row["customer_id"],
            "product_id": row["product_id"],
            "rating": rating,
            "review_text": text,
            "review_date": fake.date_between(
                start_date=row["order_date"], end_date="today"
            ),
        }
    )

reviews_df = pd.DataFrame(reviews)

os.makedirs("data", exist_ok=True)
customers_df.to_csv("data/customers.csv", index=False)
products_df.to_csv("data/products.csv", index=False)
orders_df.to_csv("data/orders.csv", index=False)
reviews_df.to_csv("data/reviews.csv", index=False)

print("Synthetic dataset generated successfully with unstructured feedback!")
