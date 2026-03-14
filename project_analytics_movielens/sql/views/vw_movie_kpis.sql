CREATE OR REPLACE VIEW `${PROJECT_ID}.movielens_views.vw_movie_kpis` AS

SELECT
    COUNT(DISTINCT r.movie_id) AS total_movies_rated,
    COUNT(DISTINCT r.user_id) AS total_users,
    COUNT(*) AS total_ratings,
    AVG(r.rating) AS avg_rating
FROM `${PROJECT_ID}.movielens_analytics.fact_ratings` r;