import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    Returns
    -------
    psycopg2 cursor and connection objects.

    A connection is established with the default database. sparkifydb is dropped
    if it exists, and is then created. The connection to the default database is
    closed, and a new connection is establised with sparkifydb.
    """

    # connect to default database
    conn = psycopg2.connect(
        host = '127.0.0.1',
        dbname = 'studentdb',
        user = 'student',
        password = 'student',
        port = '5555'
    )
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(
        host = '127.0.0.1',
        dbname = 'sparkifydb',
        user = 'student',
        password = 'student',
        port = '5555'
    )
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    All five tables in sparkifydb are dropped as specified by the queries in
    sql_queries.py.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    All tables in sparkifydb are created as specified by the queries in
    sql_queries.py.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Bundles up the script: creates db and opens connection, drops all tables
    that exist, creates all five tables, and then closes the connection to the
    database.
    """
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
