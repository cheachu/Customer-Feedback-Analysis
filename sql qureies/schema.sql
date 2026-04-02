CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name TEXT,
    city TEXT,
    region TEXT,
    industry TEXT,
    signup_date DATE
);

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price NUMERIC,
    cost NUMERIC
);

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    order_date DATE,
    quantity INT,
    price NUMERIC,
    discount_percent NUMERIC,
    status TEXT
);

CREATE TABLE reviews (
    review_id INT PRIMARY KEY,
    order_id INT,
    customer_id INT,
    product_id INT,
    rating INT,
    review_text TEXT,
    review_date DATE,
    sentiment_label TEXT,
    sentiment_score NUMERIC,
    dominant_topic_id INT,
    topic_name TEXT
);