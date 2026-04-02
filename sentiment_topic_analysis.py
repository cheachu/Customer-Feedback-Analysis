import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import re

# Download required NLTK data
nltk.download('vader_lexicon', quiet=True)

print("Loading reviews data...")
reviews_df = pd.read_csv("data/reviews.csv")

# 1. SENTIMENT ANALYSIS
print("Performing Sentiment Analysis...")
sia = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if pd.isna(text):
        return "Neutral", 0.0
    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

# Apply sentiment analysis
sentiment_results = reviews_df['review_text'].apply(get_sentiment)
reviews_df['sentiment_label'] = [res[0] for res in sentiment_results]
reviews_df['sentiment_score'] = [res[1] for res in sentiment_results]

# 2. TOPIC MODELING (LDA) to identify emerging issues
print("Performing LDA Topic Modeling...")

# Basic text cleaning function
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return text

cleaned_reviews = reviews_df['review_text'].apply(clean_text)

# Vectorize text (ignoring common stop words)
vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
dtm = vectorizer.fit_transform(cleaned_reviews)

# Run LDA
NUM_TOPICS = 4
lda = LatentDirichletAllocation(n_components=NUM_TOPICS, random_state=42)
lda.fit(dtm)

# Assign the dominant topic to each review
topic_results = lda.transform(dtm)
reviews_df['dominant_topic_id'] = topic_results.argmax(axis=1)

# Map topic IDs to readable names based on our synthetic data generation patterns
topic_mapping = {
    0: "Delivery & Logistics",
    1: "Customer Service",
    2: "Product Quality & Bugs",
    3: "Pricing & Value"
}
reviews_df['topic_name'] = reviews_df['dominant_topic_id'].map(topic_mapping)

# Save processed data for SQL/PowerBI
reviews_df.to_csv("data/processed_reviews.csv", index=False)
print("NLP Processing complete. Saved to data/processed_reviews.csv")