# Sparkify

*Project summary*

The `Sparkify` ETL pipeline loads songs' information and data related to its usage into a postgres database for further analysis on what users listen to.


*Analytical goals*

The insights that can be produced from this data will show which artists and songs users listen to, for how long, and on which day of the week.

After conducting a more advanced analysis on the data, business analysts / product owners / marketing team members of the `Sparkify` organisation should:

* have a better understanding on which popular artists to promote
* which day of the week is preferred by the customers - which again can be used to promote special prices, events and improve communication with users
* what are some of the new features to develop to improve user experience
* which parts of the songs are the most played which will help to improve scaling of our music streaming infrastructure
* how to drive more users to the platform in relation to popular trends!

This ETL pipeline will also be improved in the future with further reporting and automation capabilities based on regular updates from customer data sourced via our production systems.

## Datastore

### Creation (required)

To create the database, run the script `create_tables.py`.

Two possible options:
- From the console: `python create_tables.py`
- From within the `etl.ipynb` notebook: `%run -i 'create_tables.py'`

The script should run without errors, and successfully connect to the Sparkify database.

The script is idempotent and will drop any tables if they exist, and then create the necessary tables. 

The queries used by `create_tables.py` to make DDL changes are defined in `sql_queries.py` as SQL statements.

### Design choices

The database schema uses a STAR schema with a fact tables and multiple dimensional tables. 

This type of design is appropriate for most BI reporting tools and optimise for performant reads / searches through the fact table.

The fact table has an auto-increment (SERIAL) on the primary key as a composite key only on not nullable external foreign keys does not make sense as of today.

On some of the dimensional tables, PKs enable the use of postgres UPSERTs - a method that helps to decide what to update in case of conflicts (duplicate entries breaking the PK unicity) created by the ETL pipeline. 

In the event of duplicated records, we've decided here to not update the original row as there's no real use case today for keeping track of historical changes or to get the most up to date information. This may vary in the future.

The field types might not yet be ideal but try to preserve time format, float precision, reduce disk space / optimise for future text search while preserving full text length.

## ETL pipeline

The ETL pipeline loads the song and user data from the `data` folder.

To run it from the console, run  `python etl.py`.

The script connects to the Sparkify database, extracts and processes the log_data and song_data, and loads data into the five tables.

Since the data is a subset of a much larger dataset, the solution dataset has only 1 row with values containing ID for both songid and artistid. The following SQL query in `test.ipynb` shows a count equal to 1: `%sql SELECT COUNT(*) FROM songplays WHERE song_id != 'None' and artist_id != 'None'`

### Design choices

The ETL pipeline consists in multiple python methods that work with their own data sources, whether it's a log file or song file.

This guarantees separation of concerns and make our code more maintainable.

See method docstring in `etl.py` for further information on the API.