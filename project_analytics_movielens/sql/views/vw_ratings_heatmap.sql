CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_ratings_heatmap` AS

SELECT
    EXTRACT(DAYOFWEEK FROM rating_timestamp) AS day_of_week,
    EXTRACT(HOUR FROM rating_timestamp) AS hour_of_day,
    COUNT(*) AS total_ratings
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings`
GROUP BY day_of_week, hour_of_day
ORDER BY day_of_week, hour_of_day;