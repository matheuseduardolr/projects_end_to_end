CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_ratings_heatmap` AS

SELECT
    rating_timestamp,
    DATE(rating_timestamp) AS rating_date,

    EXTRACT(YEAR FROM rating_timestamp) AS year,
    EXTRACT(MONTH FROM rating_timestamp) AS month,
    FORMAT_TIMESTAMP('%B', rating_timestamp) AS month_name,

    EXTRACT(DAY FROM rating_timestamp) AS day,
    FORMAT_TIMESTAMP('%A', rating_timestamp) AS day_name,
    EXTRACT(DAYOFWEEK FROM rating_timestamp) AS day_of_week,

    EXTRACT(HOUR FROM rating_timestamp) AS hour_of_day,

    COUNT(*) AS total_ratings
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings`

GROUP BY
    rating_timestamp,
    rating_date,
    year,
    month,
    month_name,
    day,
    day_name,
    hour_of_day

ORDER BY
    rating_date,
    hour_of_day;