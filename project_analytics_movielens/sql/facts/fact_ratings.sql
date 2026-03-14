CREATE OR REPLACE TABLE `${PROJECT_ID}.movielens_analytics.fact_ratings` AS

WITH ratings AS (

SELECT
    SAFE_CAST(userId AS INT64) AS user_id,
    SAFE_CAST(movieId AS INT64) AS movie_id,
    SAFE_CAST(rating AS FLOAT64) AS rating,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', tstamp) AS timestamp
FROM `${PROJECT_ID}.movielens_raw.raw_user_rating_history`

UNION ALL

SELECT
    SAFE_CAST(userId AS INT64) AS user_id,
    SAFE_CAST(movieId AS INT64) AS movie_id,
    SAFE_CAST(rating AS FLOAT64) AS rating,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', tstamp) AS timestamp
FROM `${PROJECT_ID}.movielens_raw.raw_ratings_for_additional_users`

)

SELECT *
FROM ratings
WHERE rating IS NOT NULL;