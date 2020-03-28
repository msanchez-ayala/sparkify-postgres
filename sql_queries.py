# DROP TABLES

songplay_table_drop = ""
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
""")

user_table_create = """
    CREATE TABLE IF NOT EXISTS
      users (
        user_id int UNIQUE PRIMARY KEY,
        first_name text,
        last_name text,
        gender text,
        level text
      )
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS
      songs (
        song_id varchar UNIQUE PRIMARY KEY,
        title varchar,
        artist_id varchar,
        year int,
        duration decimal
      )
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS
      artists (
        artist_id varchar UNIQUE PRIMARY KEY,
        name varchar,
        location varchar,
        latitude decimal,
        longitude decimal
      )
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS
      time (
        timestamp timestamp UNIQUE PRIMARY KEY,
        hour int,
        day int,
        week_of_year int,
        month int,
        year int,
        weekday int
      )
"""

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = """
    INSERT INTO
      users (
        user_id,
        first_name,
        last_name,
        gender,
        level
      )
    VALUES
      (%s, %s, %s, %s, %s)
"""

song_table_insert = """
    INSERT INTO
      songs (
        song_id,
        title,
        artist_id,
        year,
        duration
      )
    VALUES
      (%s, %s, %s, %s, %s)
"""

artist_table_insert = """
    INSERT INTO
      artists (
        artist_id,
        name,
        location,
        latitude,
        longitude
      )
    VALUES
      (%s, %s, %s, %s, %s)
"""


time_table_insert = """
    INSERT INTO
      time (
        timestamp,
        hour,
        day,
        week_of_year,
        month,
        year,
        weekday
      )
    VALUES
      (%s, %s, %s, %s,
       %s, %s, %s)
"""

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create] #[songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop, time_table_drop] #[songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
