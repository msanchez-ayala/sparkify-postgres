# Data Modeling with Postgres

Fictional music streaming startup Sparkify wants to analyze their streaming data
on songs and user activity, particularly what songs users are listening to.
Their data is initially stored in JSON logs of user activity and JSON metadata
of songs.

I create the following to help them out:
- A Postgres database with with a star schema that optimizes Sparkify's querying
of song play analysis.
- An ETL pipeline to transfer data from the JSON files into Postgres using
Python and SQL.

**NOTE:** This code runs in a docker container as outlined at the bottom of this  
README. The default connections specified in all python modules and the two
Jupyter notebooks (namely the fact that ports have been set to 5555) will not
allow you to connect to a locally hosted postgres instance. See instructions at
the bottom of this README to run in a container.

If you want to run it locally instead, just comment out the port assignments and
the default of 5432 will be used.

## Database Schema

![](sparkifydb_erd.jpeg?raw=true)

This star schema is comprised of one fact table, songplays, and four dimension
tables.

## Repo Organization
 The database can be created and filled by running scripts in the following
 order:
1. **create_tables.py:** This module connects to the `sparkifydb` database
(or creates it if doesn't exist), drops any tables if they exist, and creates
all five tables.
2. **etl.py:** This module connects to the `sparkifydb` database, extracts and
processes the log_data and song_data, and loads data into the five tables.

The last module, **sql_queries.py** contains all of the SQL queries used for both
read and write queries called from **create_tables.py** and **etl.py**.

**test.ipynb** can be used to write queries to test each of the tables.

## Sample Queries
Most common user locations

```
SELECT
  location,
  COUNT(location)
FROM
  songplays
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT 10
```

Breakdown of user demographic

```
SELECT
  gender,
  COUNT(gender)
FROM
  users
GROUP BY
  1
 ```

Most common hour of the day to stream music

```
SELECT
  hour,
  COUNT(hour)
FROM
  time
GROUP BY
  1
ORDER BY
  2 DESC
LIMIT 5
```

## How to Use - Docker

Clone this repo to your desired directory and install [docker](https://docs.docker.com/). Create an account if you haven't already.

Login to your account via the terminal (or Docker Desktop)

```
docker login docker.io
```
Pull the docker image I've created for this project.
```
docker pull msanchezayala/sparkify-postgres-image
```
Run the container
```
docker run -d --name CONTAINER_NAME -p 5555:5432 msanchezayala/sparkify-postgres-image
```
where `CONTAINER_NAME` can be whatever alias you want to use to reference this
container.

Now you're able to run the scripts in the order specified above. All of the
connections specify a port of 5555, so you will automatically connect to the
container's PostgreSQL instance.

Once you're done and want to close out
```
docker stop CONTAINER_NAME
docker rm CONTAINER_NAME
```
## Acknowledgements
- **Dockerfile**, **init.sql**, and these instructions above are attributed to the
work of [Ken H](https://github.com/kenhanscombe), whose examples I've followed
to containerize my project.
- The erd diagram was created using [Lucidchart](lucidchart.com)
