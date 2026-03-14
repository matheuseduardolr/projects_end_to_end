CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_scatter_popularity_vs_quality` AS

SELECT
    m.movie_id,
    m.title,
    COUNT(r.rating) AS popularity,
    AVG(r.rating) AS quality
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r
JOIN `${PROJECT_ID}.movielens_analytics.dim_movies` m
ON r.movie_id = m.movie_id
GROUP BY m.movie_id, m.title
HAVING COUNT(r.rating) >= 50;