# Criando EXTERNAL TABLE
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_movies`
(
  movieID STRING,
  title STRING,
  genres STRING,
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/movies.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);

# raw_user_rating_history
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_user_rating_history`
(
  userId STRING,
  movieId STRING,
  rating STRING,
  timestamp STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/user_rating_history.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);

# raw_ratings_for_additional_users
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_ratings_for_additional_users`
(
  userId STRING,
  movieId STRING,
  rating STRING,
  timestamp STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/ratings_for_additional_users.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);

# raw_belief_data
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_belief_data`
(
  userId STRING,
  movieId STRING,
  isSeen STRING,
  watchDate STRING,
  userElicitRating STRING,
  userPredictRating STRING,
  userCertainty STRING,
  tstamp STRING,
  month_idx STRING,
  source STRING,
  systemPredictRating STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/belief_data.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);

# raw_movie_elicitation_set
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_movie_elicitation_set`
(
  movieId STRING,
  month_idx STRING,
  source STRING,
  tstamp STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/movie_elicitation_set.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);

# raw_recommendation_history
CREATE OR REPLACE EXTERNAL TABLE `prejeto-desafios.raw.raw_recommendation_history`
(
  userId STRING,
  tstamp STRING,
  movieId STRING,
  predictedRating STRING
)
OPTIONS (
  format = 'CSV',
  uris = ['gs://src-desafio01/bronze/recommendation_history.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE,
  allow_jagged_rows = TRUE
);


--$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\luanr\OneDrive\python_estudos_aleatorios\desafios\Desafio01_BigQueryMetabase\gbq.json"

# Imagem Docker do metabase
docker run -d -p 3000:3000 --name metabase metabase/metabase

# http://localhost:3000

# docker start metabase
# docker stop metabase
# docker ps

# L ano metabse vai ser necessário colocar o gbq.json
