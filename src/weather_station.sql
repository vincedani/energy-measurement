CREATE TABLE Measurements (
 ID integer NOT NULL PRIMARY KEY AUTOINCREMENT,
 TimeStamp text NOT NULL, -- SQLite3 does not have DateTime type
 Temperature real NOT NULL,
 Humidity real NOT NULL,
 Pressure real NOT NULL,
 UNIQUE(TimeStamp)
);
