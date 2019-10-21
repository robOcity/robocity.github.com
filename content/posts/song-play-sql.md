Title: Data Modeling with PostgreSQL
Slug: data-modeling-with-postgresql
Date: 2019-07-22
Category: Data Engineering
Tags: SQL, Data Modeling, PostgreSQL, postgres, query, table, primary key, relational, database
Author: Rob Osterburg
Summary: See how to extract data from CSV files, transform it, and load it into PostgreSQL.  Learn how to extract log data from CSV files using pandas, transform it with SQL and python, and then load it into a star-scheme perfect for aggregations and analytics.  

Have you ever wondered how to take raw log files and transform them into a relational database?  With this [repository](https://github.com/robOcity/song-play), I will show you how to do it using [pandas](https://pandas.pydata.org/), [Postgres](https://www.postgresql.org/) and  [pscopg2](http://initd.org/psycopg/) in [Python](https://www.python.org/).  You will learn to read log files into a tabular panda's dataframe, use SQL to create a star-scheme perfect for doing aggregations and analytics in python.

## Purpose

Sparkify -- a fictitious startup -- wants to analyze the data they have been collecting on songs and user activity form their new music streaming app.  Understanding what songs are users are listening to is of particular interest. Their data is stored in JSON logs files and needs to be analyzed to figure this out.  They want to create a database optimized to analyze the user's listening behavior. To perform this analysis routinely, they need a database schema and an extract-transform-and-load (ETL) pipeline.

## Design

What songs are popular with subscribers?  To answer this question, I need to restructure the Sparkify log files into a relational database allowing it to be quantified using SQL queries.  Log files of subscriber activities are gathered using Sparkify's online transactional processing (OLTP) system optimized for fast writes.  Think log files.  To profit from the analysis of user data, the larger the data volume, the better.  Analyzing this data is the realm of data warehouses that ingest and restructure transactional data for analysis.  Star schemas simplify analytic queries by restructuring and normalizing the data.  Think of tables of data where each row has a unique identifier or primary key.  Known as the second-normal-form, tables of this kind are common in data warehouses.  The idea of star schema is simple, one central fact table that is related to dimension tables by their primary keys.  Star schemas are standard in data warehouses -- a typical example of an online analytical processing system (OLAP).

## Files Descriptions

1. `data` directory - Holds the song data and the log data.

2. `create_tables.py` - Uses `sql_queries.py` to delete and re-create the database and all its tables.  After running this function, the database is ready for data is ready for importing.

3. `environment.yml` - The Python packages required to run this application.

4. `etl_prototype.py` - This is a prototype for the data processing pipeline that loads data from one song and one log data file.
 
5. `etl.ipynb` - Exported from `etl.py` using tooling provided by the [Python Plugin](https://code.visualstudio.com/docs/languages/python) for [Visual Studio Code](https://code.visualstudio.com/).

6. `sql_queries.py` - Creates, inserts, and drops the tables that implement the star schema.

7. `test.ipynb` - Tests whether all the data is present in the resulting database tables.

## Running

1. Install: Download this project from Github [https://github.com/robOcity/song_play](https://github.com/robOcity/song_play) by running `git clone https://github.com/robOcity/song_play`.

2. Configure: Configure your Python environment by running `conda env create -f environment.yml`.  Regrettable, if you are using `pip` you can't get there from here.  In other words, `conda` does not support creating a `requirments.txt` file directly.

3. Run:  
   1. Start and configure your Postgres database (not covered here)
   2. Change directories into the `song_play` directory
   3. Run `python create_tables.py` 
   4. Run `python etl.py`  
   
## Implementation

PostgreSQL tables are managed using SQL statements that are executed using the Python psycopg2 package creating dimensional tables that comprise a star-schema.  Data files are read using the pandas `read_json` function that returns a dataframe.  Columns and rows from the dataframe are selected and output as tuples for insertion into the database tables.  Connections to the database are managed by psycopg2, as is the cursor object used to interact with the database.  


### ETL Pipeline Prototype

 Establish the data processing workflow using a small subset of the data.


```python
import os
import glob
import psycopg2
import pandas as pd
import numpy as np
from pathlib import Path
from sql_queries import *

```

### Connect to Postgres Database

 After connecting to the database and getting a cursor object, then drop and recreate all tables.


```python
conn = psycopg2.connect(
    "host=127.0.0.1 dbname=sparkifydb user=student password=student"
)
conn.set_session(autocommit=True)
cur = conn.cursor()
for sql_cmd in drop_table_queries + create_table_queries:
    cur.execute(sql_cmd)

```

### Find data files for processing

 Use `os.walk` to find all `*.json` files under the `filepath` directory.


```python
# Let's apply the DRY principle and write a function to load our
# data.


def get_files(filepath):
    """Return all JSON files under filepath as a list"""
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    return all_files


```

### #1: `song` Table

#### #Extract Data for Song Table

Run these commands to process the `song_data` by reading in a subset of the [Million Song Dataset](http://millionsongdataset.com/) and extracting the data from the JSON files using pandas.


```python
song_root_dir = Path().cwd() / "data" / "song_data"
song_files = get_files(song_root_dir)
filepath = song_files[0]
df = pd.read_json(filepath, lines=True)

```

##### Insert Data into the Song Table

 - Method 1: select columns and return as a tuple, knowing that there is one song per dataframe and results in __year as typye np.int64 and duration as type np.float64__.  Pandas is implemented using numpy, and numpy (abbreviated np) data types are common.


```python
song_data = next(
    df[["song_id", "title", "artist_id", "year", "duration"]].itertuples(
        index=False, name=None
    )
)

```

 - Method 2: Select columns, select first row, get values as numpy array, and convert to a list that results in __year as type int and duration as type float__.  But inserting numpy numeric types into the database using psycopg2 causes errors, so I convert them to Python types first.  This type conversion occurs because it is behavior of [numpy.ndarray.tolist](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.tolist.html#numpy.ndarray.tolist) upon which [pandas.Series.tolist](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.tolist.html) is based.  Mystery solved!


```python
# Select and insert data into the songs table
song_df = df[["song_id", "title", "artist_id",
              "year", "duration"]]
song_df.head()

```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>song_id</th>
      <th>title</th>
      <th>artist_id</th>
      <th>year</th>
      <th>duration</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>SONHOTT12A8C13493C</td>
      <td>Something Girls</td>
      <td>AR7G5I41187FB4CE6C</td>
      <td>1982</td>
      <td>233.40363</td>
    </tr>
  </tbody>
</table>
</div>


```python
song_data = song_df.values[0].tolist()
song_data = [x if x else None for x in song_data]
cur.execute(song_table_insert, song_data)

```

### #2: `artists` Table

##### Extract Data for Artist Table

 Extract the data and insert it into the artist table.


```python
artist_df = (
    df[
        [
            "artist_id",
            "artist_name",
            "artist_location",
            "artist_latitude",
            "artist_longitude",
        ]
    ]
)
artist_df.head()

```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>artist_id</th>
      <th>artist_name</th>
      <th>artist_location</th>
      <th>artist_latitude</th>
      <th>artist_longitude</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AR7G5I41187FB4CE6C</td>
      <td>Adam Ant</td>
      <td>London, England</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
artist_data = artist_df.values[0].tolist()
cur.execute(artist_table_insert, artist_data)

```

## Process `log_data`

 Now let's add the subscriber activity data to see which songs are popular.


```python
log_data_root = Path().cwd() / "data" / "log_data"
log_files = get_files(log_data_root)
# just read first file to test functionality
filepath = log_files[0]
df = pd.read_json(filepath, lines=True)

```

### #3: `time` Table

##### Extract and Insert Data into Time Table

 Find what songs users are choosing by just considering `NextSong` records.  Then convert the `ts` timestamp column to datetime and extract columns for an hour, day, week of the year, month, year, and weekday (see: [Accessors](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#time-series-related) [dt Accessor](https://pandas.pydata.org/pandas-docs/stable/reference/series.html#api-series-dt) that allows datetime properties to be easily accessed).


```python
df = df.assign(ts=pd.to_datetime(df.ts, unit="ms"))
df = df.loc[df.page.isin(["NextSong"])]
df = df.assign(timestamp=pd.to_datetime(df.ts, unit="ms"))
df.timestamp = df.timestamp.dt.tz_localize("UTC")

```


```python
time_df = pd.DataFrame(
    {
        "timestamp": df.timestamp,
        "hour": df.timestamp.dt.hour,
        "day": df.timestamp.dt.day,
        "week_of_year": df.timestamp.dt.week,
        "month": df.timestamp.dt.month,
        "year": df.timestamp.dt.year,
        "weekday": df.timestamp.dt.weekday,
    }
)
# Here we want native pandas datatypes, so I'll user iterrows.
for i, row in time_df.iterrows():
    cur.execute(time_table_insert, list(row))

```


```python
time_df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>timestamp</th>
      <th>hour</th>
      <th>day</th>
      <th>week_of_year</th>
      <th>month</th>
      <th>year</th>
      <th>weekday</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2018-11-11 02:33:56.796000+00:00</td>
      <td>2</td>
      <td>11</td>
      <td>45</td>
      <td>11</td>
      <td>2018</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2018-11-11 02:36:10.796000+00:00</td>
      <td>2</td>
      <td>11</td>
      <td>45</td>
      <td>11</td>
      <td>2018</td>
      <td>6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2018-11-11 02:40:34.796000+00:00</td>
      <td>2</td>
      <td>11</td>
      <td>45</td>
      <td>11</td>
      <td>2018</td>
      <td>6</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2018-11-11 04:36:13.796000+00:00</td>
      <td>4</td>
      <td>11</td>
      <td>45</td>
      <td>11</td>
      <td>2018</td>
      <td>6</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2018-11-11 04:36:46.796000+00:00</td>
      <td>4</td>
      <td>11</td>
      <td>45</td>
      <td>11</td>
      <td>2018</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



### #4: `users` Table

##### Extract and Insert Data into Users Table

 Every time a user plays a song, they appear in the log file, so naturally, there are duplicate userId entries.  Here we remove them to create a normalized user table.


```python
user_df = df[["userId", "firstName", "lastName", "gender", "level"]]
user_df = user_df.drop_duplicates(subset="userId", keep="last")
user_df.head()

```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>userId</th>
      <th>firstName</th>
      <th>lastName</th>
      <th>gender</th>
      <th>level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2</th>
      <td>69</td>
      <td>Anabelle</td>
      <td>Simpson</td>
      <td>F</td>
      <td>free</td>
    </tr>
    <tr>
      <th>4</th>
      <td>32</td>
      <td>Lily</td>
      <td>Burns</td>
      <td>F</td>
      <td>free</td>
    </tr>
    <tr>
      <th>5</th>
      <td>75</td>
      <td>Joseph</td>
      <td>Gutierrez</td>
      <td>M</td>
      <td>free</td>
    </tr>
    <tr>
      <th>10</th>
      <td>92</td>
      <td>Ryann</td>
      <td>Smith</td>
      <td>F</td>
      <td>free</td>
    </tr>
    <tr>
      <th>25</th>
      <td>49</td>
      <td>Chloe</td>
      <td>Cuevas</td>
      <td>F</td>
      <td>free</td>
    </tr>
  </tbody>
</table>
</div>


```python
for i, row in user_df.iterrows():
    cur.execute(user_table_insert, row)

```

### #5: `songplays` Table

##### Extract and Insert Data and Songplays Table

To look up a song or an artist using the primary key that uniquely identifies it.  The log files only have the name of the song and artist.  So, I need to do a reverse lookup up to get identifiers.

 ```sql
 SELECT s.song_id, a.artist_id FROM dim_song s
 JOIN dim_artist a ON s.artist_id = a.artist_id
 WHERE s.title = %s AND a.name = %s AND s.duration = %s;
 ```

 Iterating over the rows of the dataframe holding the log data.  First, I extract the find the unique identifiers.  Next, I combine them with other data from the log data to insert the user's songplay activity into the `song_play` table.


```python
for index, row in df.iterrows():

    # get songid and artistid from song and artist tables
    cur.execute(song_select, (row.song, row.artist, row.length))
    results = cur.fetchone()

    if results:
        songid, artistid = results
    else:
        songid, artistid = None, None

    # insert songplay record
    songplay_data = (
        row.userId,
        songid,
        artistid,
        row.sessionId,
        row.ts,
        row.level,
        row.location,
        row.userAgent,
    )
    cur.execute(songplay_table_insert, songplay_data)

```

### Close Connection to Sparkify Database

```python
conn.close()

```


## References

1. [Million Song Dataset - FAQ with fields and data types](http://millionsongdataset.com/faq/) - Lists the fields and data-types used in the [Million Song Dataset](http://millionsongdataset.com/).

2. [Converting from Unix Timestamp to PostgreSQL Timestamp or Date](http://www.postgresonline.com/journal/archives/3-Converting-from-Unix-Timestamp-to-PostgreSQL-Timestamp-or-Date.html) - Explans how to go from Unix epoch time to a PostgreSQL timestamp value.

3. [PostgreSQL Keyword List](https://www.postgresql.org/docs/current/sql-keywords-appendix.html) - Note: _USER_ is a reserved keyword in Postgres and cannot be used as a table name.

4. [Psycopg2 - Fast execution helpers](http://initd.org/psycopg/docs/extras.html#fast-execution-helpers) - How to use the `executemany()` method to insert many rows into a table, at once.

5. [Using PostgreSQL SERIAL To Create Auto-increment Column](http://www.postgresqltutorial.com/postgresql-serial/) - How to create a primary key that increments automatically.

6. [How to insert current_timestamp into Postgres via python](https://stackoverflow.com/questions/6018214/how-to-insert-current-timestamp-into-postgres-via-python) - Explains how to easily insert timestamps into PostgreSQL by converting them to datetime objects in Python and then letting [pscopg2](http://initd.org/psycopg/) handle the rest. 

7. [Pandas convert dataframe to an array of tuples](https://stackoverflow.com/questions/9758450/pandas-convert-dataframe-to-array-of-tuples) - Examples and explanation of how to convert rows of [pandas](https://pandas.pydata.org/) dataframe into tuples for insertion into the database.  

8. [Psycopg2 Extras - Fast execution helpers](http://initd.org/psycopg/docs/extras.html?highlight=executemany) - Explanation and examples of how to insert many records into a table in one transaction using psycopg2's `executemany()` method.  

9. [How to UPSERT (MERGE, INSERT … ON DUPLICATE UPDATE) in PostgreSQL?](https://stackoverflow.com/questions/17267417/how-to-upsert-merge-insert-on-duplicate-update-in-postgresql?noredirect=1&lq=1) - How to handle duplicate primary keys in PostgreSQL INSERT statements informally called `upsert`.  