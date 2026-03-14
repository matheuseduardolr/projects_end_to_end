CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_genre_performance` AS

SELECT
    genre,
    COUNT(*) AS total_ratings,
    AVG(r.rating) AS avg_rating
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r
JOIN `${PROJECT_ID}.movielens_analytics.dim_movies` m
ON r.movie_id = m.movie_id,
UNNEST(SPLIT(m.genres, '|')) AS genre
GROUP BY genre
ORDER BY avg_rating DESC;