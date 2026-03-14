CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_user_activity` AS

SELECT
    user_id,
    COUNT(*) AS total_ratings,
    AVG(rating) AS avg_rating,
    MIN(rating_timestamp) AS first_rating,
    MAX(rating_timestamp) AS last_rating
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings`
GROUP BY user_id;