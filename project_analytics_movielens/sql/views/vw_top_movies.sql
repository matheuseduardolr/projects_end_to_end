CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_top_movies` AS

SELECT
    m.title,
    COUNT(r.rating) AS total_ratings,
    AVG(r.rating) AS avg_rating
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r
JOIN `${PROJECT_ID}.movielens_analytics.dim_movies` m
ON r.movie_id = m.movie_id
GROUP BY m.title
HAVING COUNT(r.rating) >= 50
ORDER BY avg_rating DESC;