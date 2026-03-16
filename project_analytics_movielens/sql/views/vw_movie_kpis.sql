CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_movie_kpis` AS

SELECT
    r.movie_id,
    m.title,
    m.genres,
    m.release_year,
    COUNT(r.rating) AS total_ratings,
    AVG(r.rating) AS avg_rating,
    STDDEV(r.rating) AS std_rating,
    MIN(r.rating_timestamp) as first_rating,
    MAX(r.rating_timestamp) as last_rating,
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r
JOIN `${PROJECT_ID}.movielens_analytics.dim_movies` m ON r.movie_id = m.movie_id
GROUP BY 1, 2, 3, 4;