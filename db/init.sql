CREATE TABLE IF NOT EXISTS Cities (city_id integer PRIMARY KEY, city text);
CREATE TABLE IF NOT EXISTS Regions (region_id integer PRIMARY KEY, region text);
CREATE TABLE IF NOT EXISTS Users (
    user_id integer PRIMARY KEY,
    fName text ,
    lName text,
    mName text,
    email text,
    phone text,
    city_id integer,
    region_id integer
);
CREATE TABLE IF NOT EXISTS Comments (
    comment_id INTEGER PRIMARY KEY,
    users_id integer,
    date_time,
    comment text);

select name from sqlite_master;