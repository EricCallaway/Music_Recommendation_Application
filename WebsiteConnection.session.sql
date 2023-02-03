-- Active: 1636556615537@@127.0.0.1@3306

-- CREATE TABLE user(
--     id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
--     username VARCHAR(255) NOT NULL,
--     password VARCHAR(255) NOT NULL
-- );

-- CREATE TABLE songs(
--     spotify_id VARCHAR(255) NOT NULL PRIMARY KEY,
--     title VARCHAR(255) NOT NULL,
--     artist VARCHAR(255) NOT NULL,
--     spotify_link VARCHAR(255) NOT NULL,
--     genre VARCHAR(255) NOT NULL,
--     energy DECIMAL(3, 3),
--     liveness DECIMAL(4, 4),
--     tempo DECIMAL(4, 3),
--     speechiness DECIMAL(3, 3),
--     acousticness DECIMAL(4, 4),
--     instrumentalness DECIMAL(6, 6),
--     time_signature INT,
--     danceability DECIMAL(3, 3),
--     song_key INT,
--     duration_ms BIGINT,
--     loudness DECIMAL(3, 3),
--     valence DECIMAL(3, 3),
--     mode INT,
--     lyrics TEXT NOT NULL
-- );

-- CREATE TABLE recommended_songs(
--     id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
--     user_id INT NOT NULL,
--     spotify_id VARCHAR(255) NOT NULL
-- );

-- ALTER TABLE recommended_songs 
-- ADD CONSTRAINT recommended_songs_user_id_foreign
-- FOREIGN KEY(user_id) REFERENCES user(id);

-- ALTER TABLE recommended_songs 
-- ADD CONSTRAINT recommended_songs_spotify_id_foreign
-- FOREIGN KEY(spotify_id) REFERENCES songs(spotify_id);

SELECT artist, title FROM songs LIMIT 20;