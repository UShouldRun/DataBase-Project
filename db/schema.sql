CREATE DATABASE IF NOT EXISTS DisneyDB;
USE DisneyDB;

CREATE TABLE IF NOT EXISTS shows (
  show_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  release_year INT NOT NULL,
  release_date DATE,
  rating VARCHAR(30),
  show_description VARCHAR(500) NOT NULL
);

CREATE TABLE IF NOT EXISTS person (
  person_id INT AUTO_INCREMENT PRIMARY KEY,
  person_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS genre (
  genre_id INT AUTO_INCREMENT PRIMARY KEY,
  genre_name VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS country (
  country_id INT AUTO_INCREMENT PRIMARY KEY,
  country_name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS paper (
  show_id INT NOT NULL,
  person_id INT,
  paper_role VARCHAR(10) NOT NULL,
  PRIMARY KEY (show_id, person_id),
  FOREIGN KEY (show_id)   REFERENCES shows(show_id),
  FOREIGN KEY (person_id) REFERENCES person(person_id)
);

CREATE TABLE IF NOT EXISTS category (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_type VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS streaming_on (
  show_id INT NOT NULL,
  country_id INT,
  PRIMARY KEY (show_id, country_id),
  FOREIGN KEY (show_id)    REFERENCES shows(show_id),
  FOREIGN KEY (country_id) REFERENCES country(country_id)
);

CREATE TABLE IF NOT EXISTS listed_in (
  show_id INT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY (show_id, genre_id),
  FOREIGN KEY (show_id)  REFERENCES shows(show_id),
  FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
);

CREATE TABLE IF NOT EXISTS duration (
  show_id INT,
  category_id INT,
  duration_time INT,
  PRIMARY KEY (show_id, category_id),
  FOREIGN KEY (show_id)     REFERENCES shows(show_id),
  FOREIGN KEY (category_id) REFERENCES category(category_id)
);
