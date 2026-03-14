CREATE OR REPLACE TABLE `${PROJECT_ID}.movielens_analytics.fact_ratings` AS

WITH ratings AS (

SELECT
    SAFE_CAST(NULLIF(TRIM(userId), '') AS INT64) AS user_id,
    SAFE_CAST(NULLIF(TRIM(movieId), '') AS INT64) AS movie_id,
    SAFE_CAST(NULLIF(TRIM(rating), '') AS FLOAT64) AS rating,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', NULLIF(TRIM(tstamp), '')) AS rating_timestamp
FROM `${PROJECT_ID}.movielens_raw.raw_user_rating_history`

UNION ALL

SELECT
    SAFE_CAST(NULLIF(TRIM(userId), '') AS INT64) AS user_id,
    SAFE_CAST(NULLIF(TRIM(movieId), '') AS INT64) AS movie_id,
    SAFE_CAST(NULLIF(TRIM(rating), '') AS FLOAT64) AS rating,
    PARSE_TIMESTAMP('%Y-%m-%d %H:%M:%S', NULLIF(TRIM(tstamp), '')) AS rating_timestamp
FROM `${PROJECT_ID}.movielens_raw.raw_ratings_for_additional_users`

)

SELECT
    user_id,
    movie_id,
    rating,
    rating_timestamp,
    DATE(rating_timestamp) AS rating_date
FROM ratings
WHERE
    user_id IS NOT NULL
    AND movie_id IS NOT NULL
    AND rating IS NOT NULL
    AND rating_timestamp IS NOT NULL;