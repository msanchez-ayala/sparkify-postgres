# Data Modeling with Postgres

Fictional music streaming startup Sparkify wants to analyze their data on songs and user activity, particularly what songs users are listening to. Their data is currently stored in:
- JSON logs of user activity
- JSON metadata on songs

I create the following to help them out:
- A Postgres database with tables to optimize Sparkify's querying of song play analysis
- An ETL pipeline to transfer data from the JSON files into Postgres using Python and SQL.
