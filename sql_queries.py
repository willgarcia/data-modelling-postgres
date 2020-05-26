# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays
( songplay_id SERIAL PRIMARY KEY,
  start_time TIME NOT NULL,
  user_id  integer REFERENCES users(user_id),
  level varchar,
  song_id varchar REFERENCES songs(song_id),
  session_id integer,
  location TEXT,
  user_agent varchar,
  artist_id varchar REFERENCES artists(artist_id)
);        
""")

user_table_create = ("""
CREATE TABLE users
( user_id integer CONSTRAINT user_id_pk PRIMARY KEY,
  first_name varchar,
  last_name varchar,
  gender char(1),
  level varchar
);
""")

song_table_create = ("""
CREATE TABLE songs
( song_id varchar CONSTRAINT song_id_pk PRIMARY KEY,
  title TEXT,
  artist_id varchar REFERENCES artists(artist_id),
  year INTEGER NOT NULL,
  duration FLOAT8
);
""")

artist_table_create = ("""
CREATE TABLE artists
( artist_id varchar CONSTRAINT artist_id_pk PRIMARY KEY,
  name varchar,
  location TEXT,
  latitude FLOAT8 NULL,
  longitude FLOAT8 NULL
);
""")

time_table_create = ("""
CREATE TABLE time
( start_time TIME PRIMARY KEY,
  hour INTEGER NOT NULL,
  day INTEGER NOT NULL,
  week INTEGER NOT NULL,
  month INTEGER NOT NULL, 
  year INTEGER NOT NULL,
  weekday INTEGER NOT NULL
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, session_id, location, user_agent, artist_id)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level=EXCLUDED.level
""")

song_table_insert = ("""
ALTER TABLE songs DISABLE TRIGGER ALL;
INSERT INTO songs (song_id, title, artist_id, year, duration) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING;
ALTER TABLE songs DISABLE TRIGGER ALL;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) 
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id)
DO NOTHING;
""")

artist_select = "SELECT * FROM artists"

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time)
DO NOTHING;
""")

# SELECTS

time_select_all = ("""SELECT COUNT(*) FROM time""")

artist_select_all = ("""SELECT * FROM artists""")

song_select_all = ("""SELECT * FROM songs""")

song_select = ("""
SELECT songs.song_id, songs.artist_id
FROM songs
JOIN artists 
    ON songs.artist_id = artists.artist_id
WHERE 
    songs.title = %s
    AND artists.name = %s
    AND songs.duration = %s;
""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]