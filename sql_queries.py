import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS song;"
artist_table_drop = "DROP TABLE IF EXISTS artist;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE staging_events(
artist VARCHAR(MAX),
auth VARCHAR(MAX),
firstName VARCHAR(MAX),
gender VARCHAR(MAX),
itemInSession BIGINT,
lastName VARCHAR(MAX),
length VARCHAR(MAX),
level VARCHAR,
location VARCHAR,
method VARCHAR,
page VARCHAR,
registration VARCHAR,
sessionId BIGINT,
song VARCHAR,
status BIGINT,
ts BIGINT,
userAgent VARCHAR,
userId BIGINT)
""")

staging_songs_table_create = ("""CREATE TABLE staging_songs(
artist_id VARCHAR,
artist_latitude FLOAT, 
artist_location VARCHAR(MAX),
artist_longitude FLOAT,  
artist_name VARCHAR(MAX), 
duration FLOAT,
song_id VARCHAR, 
title VARCHAR(MAX),
num_songs BIGINT, 
year BIGINT
)
""")

#songplay_id is being autoincremented here 
songplay_table_create = ("""CREATE TABLE songplay (
songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY NOT NULL, 
start_time TIME,
user_id BIGINT,
level VARCHAR, 
song_id VARCHAR,
artist_id VARCHAR,
session_id BIGINT,
location VARCHAR, 
user_agent VARCHAR
)
""")

user_table_create = (""" CREATE TABLE users(
user_id INT PRIMARY KEY NOT NULL,
first_name VARCHAR, 
last_name VARCHAR,
gender VARCHAR,
level VARCHAR
)
""")

song_table_create = (""" CREATE TABLE song(
song_id VARCHAR PRIMARY KEY NOT NULL,
title VARCHAR,
artist_id VARCHAR,
year INT,
duration FLOAT
)
""")

artist_table_create = (""" CREATE TABLE artist(
artist_id VARCHAR PRIMARY KEY NOT NULL,
name VARCHAR,
location VARCHAR,
latitude FLOAT,
longitude FLOAT
)
""")

time_table_create = (""" CREATE TABLE time(
start_time TIME, 
hour BIGINT,
day BIGINT,
week BIGINT,
month BIGINT,
year BIGINT, 
weekday BIGINT
)
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events
FROM {}
iam_role {}
FORMAT AS json {};
""").format(config['S3']['LOG_DATA'], config['IAM_ROLE']['ARN'], config['S3']['LOG_JSONPATH'])

staging_songs_copy = ("""
COPY staging_songs 
FROM {} 
iam_role {}
FORMAT AS JSON 'auto'
REGION 'us-west-2';
""").format(config['S3']['SONG_DATA'], config['IAM_ROLE']['ARN']) 

# FINAL TABLES

songplay_table_insert = (""" 
INSERT INTO songplay (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 

with main as (SELECT
cast(TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' as time) AS start_time,
se.userId as user_id, 
se.level, 
ss.song_id, 
ss.artist_id, 
se.sessionId as session_id,
se.location, 
se.userAgent as user_agent, 
row_number() over (partition by 
cast(TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' as time), 
se.userId,
se.level, 
ss.song_id, 
ss.artist_id, 
se.sessionId,
se.location, 
se.userAgent) as rn 
                  
FROM staging_events se LEFT JOIN staging_songs ss on lower(se.artist) = lower(ss.artist_name) 

WHERE 
lower(se.page) = 'nextsong'
)

select 
start_time,
user_id, 
level, 
song_id, 
artist_id, 
session_id,
location, 
user_agent
from main 
where rn = 1 
""")

user_table_insert = (""" 
INSERT INTO users (user_id, first_name, last_name, gender, level) 

SELECT
distinct se.userId as user_id,
se.firstName as first_name,
se.lastName as last_name, 
se.gender,
se.level 

FROM 
staging_events se

WHERE
se.userid is not null 
""")

song_table_insert = (""" 
INSERT INTO song (song_id, title, artist_id, year, duration) 

SELECT 
distinct ss.song_id, 
ss.title,
ss.artist_id,
ss.year,
ss.duration

FROM 
staging_songs ss

WHERE
ss.song_id is not null
""")

artist_table_insert = (""" 
INSERT INTO artist (artist_id, name, location, latitude, longitude) 

SELECT
distinct ss.artist_id, 
ss.artist_name as name, 
ss.artist_location as location,
ss.artist_latitude as latitude,
ss.artist_longitude as longitude

FROM 
staging_songs ss

WHERE
ss.artist_id is not null
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) 
with main as(SELECT 
cast(TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as timestamp) AS start_timestamp
FROM staging_events
WHERE
cast(TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as timestamp) 
is not null      
)
SELECT
distinct cast(start_timestamp as time) as start_time,
extract(hour FROM start_timestamp) as hour, 
extract(day from start_timestamp) as day,
extract(week from start_timestamp) as week,
extract(month from start_timestamp) as month, 
extract(year from start_timestamp) as year,
extract(weekday from start_timestamp) as weekday

FROM main 

""")
# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
