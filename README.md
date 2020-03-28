# Data Modeling with Postgres

Fictional music streaming startup Sparkify wants to analyze their data on songs
and user activity, particularly what songs users are listening to. Their data is
currently stored in:
- JSON logs of user activity
- JSON metadata on songs

I create the following to help them out:
- A Postgres database with tables to optimize Sparkify's querying of song play
analysis
- An ETL pipeline to transfer data from the JSON files into Postgres using
Python and SQL.

# How to Use
After installing necessary packages outlined in `requirements.txt`, run the
files in the following order:

1. **create_tables.py:** This module connects to the `sparkifydb` database (or
  creates it if not yet existing), drops any tables if they exist, and creates
  the tables.
2. **etl.py:** This module connects to the `sparkifydb` database, extracts and
processes the log_data and song_data, and loads data into the five tables.

Both the modules above call upon **sql_queries.py** which contains the create,
drop, and insert queries for all five tables.

Lastly, **test.ipynb** can be used to write queries to test each of the tables.
