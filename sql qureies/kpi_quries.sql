SET search_path TO public;

-- ----------------------------
-- 1. OVERALL CSAT (Customer Satisfaction Score)
-- Percentage of 4 and 5 star ratings
-- ----------------------------
SELECT 
    ROUND(
        (COUNT(*) FILTER (WHERE rating >= 4) * 100.0 / COUNT(*))::numeric,
        2
    ) AS csat_percentage,
    
    ROUND(AVG(sentiment_score)::numeric, 4) AS avg_sentiment_score
FROM reviews;

-- ----------------------------
-- 2. SENTIMENT TREND OVER TIME (Monthly)
-- Tracks the target of 15% CSAT improvement
-- ----------------------------
SELECT 
    DATE_TRUNC('month', review_date::timestamp) AS review_month,
    COUNT(*) AS total_reviews,
    ROUND(AVG(sentiment_score)::numeric, 4) AS avg_sentiment_score,
    COUNT(*) FILTER (WHERE sentiment_label = 'Positive') AS positive_reviews,
    COUNT(*) FILTER (WHERE sentiment_label = 'Negative') AS negative_reviews
FROM reviews
GROUP BY review_month
ORDER BY review_month;

-- ----------------------------
-- 3. EMERGING PRODUCT ISSUES (Topic Modeling Aggregation)
-- Identifies the volume of negative feedback by specific topics
-- ----------------------------
SELECT 
    topic_name,
    COUNT(*) AS issue_volume,
    ROUND(AVG(sentiment_score)::numeric, 4) AS avg_sentiment
FROM reviews
WHERE sentiment_label = 'Negative'
GROUP BY topic_name
ORDER BY issue_volume DESC;

-- ----------------------------
-- 4. SENTIMENT BY PRODUCT CATEGORY
-- Joins reviews with products to find the root cause of dissatisfaction
-- ----------------------------
SELECT 
    p.category,
    COUNT(r.review_id) AS total_reviews,
    ROUND(AVG(r.sentiment_score)::numeric, 4) AS category_sentiment,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_star_rating
FROM reviews r
JOIN products p ON r.product_id = p.product_id
GROUP BY p.category
ORDER BY category_sentiment ASC;