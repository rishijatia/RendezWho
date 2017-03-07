

CREATE TABLE User(
name varchar(30),
userID int PRIMARY KEY,
password varchar(10),
requests int,
email varchar(20)
);

CREATE TABLE ScheduleEntry(
  entryID int PRIMARY KEY,
  activity varchar(20),
  entrytime char(5),
  entrydate char(10)
);

CREATE TABLE Loction(
  coordinate int PRIMARY KEY,
  name varchar(20)
);

CREATE TABLE Meeting(
  meetingID int PRIMARY KEY,
  meetingTime char(5),
  meetingDate char(10),
  meetingPrivacy boolean
);
