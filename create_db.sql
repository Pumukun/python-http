Pragma foreign_keys=on;

DROP TABLE if exists Users;

CREATE TABLE Users (
    User_ID INTEGER NOT NULL Primary key, 
    User_Name VARCHAR,
    User_Password VARCHAR
);

