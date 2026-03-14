CREATE OR REPLACE TABLE `${PROJECT_ID}.movielens_analytics.dim_movies` AS

SELECT
    SAFE_CAST(movieId AS INT64) AS movie_id,

    COALESCE(
        REGEXP_EXTRACT(title, r'^(.*)\s\(\d{4}\)$'),
        title
    ) AS title,

    SAFE_CAST(
        REGEXP_EXTRACT(title, r'\((\d{4})\)')
        AS INT64
    ) AS release_year,

    NULLIF(TRIM(genres), '') AS genres

FROM `${PROJECT_ID}.movielens_raw.raw_movies`
WHERE movieId IS NOT NULL;