CREATE DATABASE IF NOT EXISTS DisneyDB;
USE DisneyDB;

CREATE TABLE IF NOT EXISTS Shows (
  show_id          INT AUTO_INCREMENT PRIMARY KEY,
  title            VARCHAR(100) NOT NULL,
  release_year     INT NOT NULL,	
  release_date     DATE,
  rating           VARCHAR(30),
  show_description VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS Person (
  person_id   INT AUTO_INCREMENT PRIMARY KEY,
  person_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Genre (
  genre_id   INT AUTO_INCREMENT PRIMARY KEY,
  genre_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Country (
  country_id   INT AUTO_INCREMENT PRIMARY KEY,
  country_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS Paper (
  show_id    INT NOT NULL,
  person_id  INT,	
  paper_role VARCHAR(10) NOT NULL,
  PRIMARY KEY (show_id, person_id, paper_role),
  FOREIGN KEY (show_id)   REFERENCES Shows(show_id),
  FOREIGN KEY (person_id) REFERENCES Person(person_id)
);

CREATE TABLE IF NOT EXISTS Category (
  category_id   INT AUTO_INCREMENT PRIMARY KEY,
  category_type VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS StreamingOn (
  show_id    INT NOT NULL,
  country_id INT,
  PRIMARY KEY (show_id, country_id),
  FOREIGN KEY (show_id) REFERENCES Shows(show_id),
  FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

CREATE TABLE IF NOT EXISTS ListedIn (
  show_id  INT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY (show_id, genre_id),
  FOREIGN KEY (show_id)  REFERENCES Shows(show_id),
  FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);

CREATE TABLE IF NOT EXISTS DurationUnit (
  unit_id   INT AUTO_INCREMENT PRIMARY KEY,
  unit_name VARCHAR(15) NOT NULL UNIQUE
); 

CREATE TABLE IF NOT EXISTS Duration (
  show_id       INT,
  category_id   INT,
  duration_time INT,
  unit_id       INT,
  PRIMARY KEY (show_id, category_id, unit_id),
  FOREIGN KEY (show_id)     REFERENCES Shows(show_id),
  FOREIGN KEY (category_id) REFERENCES Category(category_id),
  FOREIGN KEY (unit_id) REFERENCES DurationUnit(unit_id)
);

