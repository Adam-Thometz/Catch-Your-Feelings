\c catch_your_feelings

DROP TABLE IF EXISTS users
CASCADE;
DROP TABLE IF EXISTS recordings
CASCADE;
DROP TABLE IF EXISTS feelings
CASCADE;

CREATE TABLE users
(
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE recordings
(
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  spotify_uri TEXT NOT NULL,
  valence FLOAT NOT NULL,
  energy FLOAT NOT NULL
);

CREATE TABLE library
(
  user_id INTEGER NOT NULL REFERENCES users,
  recording_id INTEGER NOT NULL REFERENCES recordings,
  PRIMARY KEY(user_id, recording_id)
)

CREATE TABLE feelings 
(
  id SERIAL PRIMARY KEY,
  valence TEXT NOT NULL,
  energy TEXT NOT NULL,
  time TIMESTAMP NOT NULL,
  user_id INTEGER NOT NULL REFERENCES users
);