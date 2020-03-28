import os
import glob
import psycopg2
import pandas as pd
import config
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Given a cursor and a filepath to a song data JSON file, this function
    extracts the raw data and loads only relevant columns into two tables within
    postgres db, sparkifydb. The two tables are songs and artists.

    Parameters
    ----------
    cur: psycopg2 cursor object associated with current connection.
    filepath: string with the filepath pointing to the song JSON file.
    """
    # open song file
    df = pd.read_json(filepath, lines = True)

    # Slice df, extract values (tuple), access just the array, convert to list
    song_columns = ['song_id', 'title','artist_id', 'year', 'duration']
    song_data = list(df[song_columns].values[0])

    # Insert song record
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_columns = ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artist_data = list(df[artist_columns].values[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Given a cursor and a filepath to a log data JSON file, this function
    extracts the raw data and loads only relevant columns into three tables
    within postgres db, sparkifydb. The three tables are time, users, and
    songplays.

    Parameters
    ----------
    cur: psycopg2 cursor object associated with current connection.
    filepath: string with the filepath pointing to the log data JSON file.
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df.ts, unit = 'ms')

    # Isolate relevant features and combine into dict
    time_data = (df.ts, df.ts.dt.hour, df.ts.dt.day, df.ts.dt.week, df.ts.dt.month, df.ts.dt.year, df.ts.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    data = dict(zip(column_labels, time_data))

    # Load into time df and insert into db
    time_df = pd.DataFrame(data)
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Load user df, drop duplicate users
    user_columns = ['userId', 'firstName', 'lastName', 'gender', 'level']
    user_df = df[user_columns]
    user_df.drop_duplicates(subset=None, keep='first', inplace=True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get song_id and artist_id from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

        # insert songplay record
        songplay_data = (
            row.ts,
            row.userId,
            row.level,
            song_id,
            artist_id,
            row.sessionId,
            row.location,
            row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect(f"host=127.0.0.1 dbname=sparkifydb user={config.user} password={config.password}")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
