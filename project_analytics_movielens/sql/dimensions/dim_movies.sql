CREATE OR REPLACE TABLE `${PROJECT_ID}.movielens_analytics.dim_movies` AS

SELECT
    SAFE_CAST(movieId AS INT64) AS movie_id,

    REGEXP_EXTRACT(title, r'^(.*)\s\(') AS title,

    SAFE_CAST(
        REGEXP_EXTRACT(title, r'\((\d{4})\)')
        AS INT64
    ) AS release_year,

    genres

FROM `${PROJECT_ID}.movielens_raw.raw_movies`;