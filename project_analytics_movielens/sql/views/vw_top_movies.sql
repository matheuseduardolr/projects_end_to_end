CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_top_movies` AS

SELECT
    m.movie_id,
    m.title,
    m.genres,
    m.release_year,
    COUNT(r.rating) AS total_ratings,
    AVG(r.rating) AS avg_rating
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r
JOIN `${PROJECT_ID}.movielens_analytics.dim_movies` m 
    ON r.movie_id = m.movie_id

GROUP BY
    m.movie_id,
    m.title,
    m.genres,
    m.release_year

HAVING
    COUNT(r.rating) >= 20
    AND AVG(r.rating) BETWEEN 0 AND 5

ORDER BY
    avg_rating DESC,
    total_ratings DESC

LIMIT 10;