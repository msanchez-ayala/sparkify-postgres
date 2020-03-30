import os
import glob
import psycopg2
import pandas as pd
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
    # Extract song file
    df = pd.read_json(filepath, lines = True)

    # Transform
    # Slice df, extract values (tuple), access just the array, convert to list
    song_columns = ['song_id', 'title','artist_id', 'year', 'duration']
    song_data = list(df[song_columns].values[0])

    # Load song data
    cur.execute(song_table_insert, song_data)

    # Slice df, extract values, etc...
    artist_columns = ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artist_data = list(df[artist_columns].values[0])

    # Load artist data
    cur.execute(artist_table_insert, artist_data)


def prep_log_data(filepath):
    """
    Returns
    -------
    df: A dataframe that is a subset of the log data with the timestamp column
        converted to datetime.

    Parameters
    ----------
    filepath: a string of the filepath to a log data JSON file.
    """
    # open log file
    df = pd.read_json(filepath, lines = True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df.ts, unit = 'ms')

    return df


def transform_time_data(df):
    """
    Returns
    -------
    time_df: DataFrame of transformed log data for insertion into the time
        table.

    Parameters
    ----------
    df: The DataFrame that is returned from prep_log_data().
    """
    # Isolate relevant features and combine into dict
    time_data = (
        df.ts, df.ts.dt.hour, df.ts.dt.day, df.ts.dt.week,
        df.ts.dt.month, df.ts.dt.year, df.ts.dt.weekday
    )
    column_labels = (
        'timestamp', 'hour', 'day', 'week_of_year',
        'month', 'year', 'weekday'
    )
    data = dict(zip(column_labels, time_data))

    # Create time df
    time_df = pd.DataFrame(data)

    return time_df


def transform_user_data(df):
    """
    Returns
    -------
    time_df: DataFrame of transformed log data for insertion into the users
        table.

    Parameters
    ----------
    df: The DataFrame that is returned from prep_log_data().
    """

    # Slice df and drop duplicates
    user_columns = ['userId', 'firstName', 'lastName', 'gender', 'level']
    user_df = df[user_columns]
    user_df.drop_duplicates(subset=None, keep='first', inplace=True)
    return user_df


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
    # Transform data
    df = prep_log_data(filepath)
    time_df = transform_time_data(df)
    user_df = transform_user_data(df)

    # Load time data
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Load user data
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Transform/load songplay data
    for index, row in df.iterrows():

        # get song_id and artist_id from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            song_id, artist_id = results
        else:
            song_id, artist_id = None, None

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
        # Load songplay data
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Performs ETL for either the song data or log data.

    Parameters
    ----------
    cur, conn: cursor and connection to sparkifydb
    filepath: string containing the filepath to either the song_data or log_data
        directory.
    func: function that performs ETL on the given set of files (either song or
        log data).
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and perform ETL
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    Bundles all ETL. Connects to sparkifydb, performs ETL on song data and then
    log data. Closes the connection to sparkifydb.
    """
    conn = psycopg2.connect(
        host = '127.0.0.1',
        dbname = 'sparkifydb',
        user = 'student',
        password = 'student',
        port = '5555'
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
