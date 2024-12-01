DELIMITER //

CREATE PROCEDURE create_show(
<<<<<<< HEAD
  IN in_title VARCHAR(50),
  IN in_year INT,
  IN in_release_date DATE,
  IN in_rating VARCHAR(30),
  IN in_show_description VARCHAR(500),
  OUT _id INT 
) BEGIN  
  INSERT INTO Shows (title, year, release_date , rating, show_description) 
  VALUES (in_title, in_year, in_release_date, in_rating, in_show_description);
  
  SET _id = LAST_INSERT_id();
END//

CREATE PROCEDURE create_person(
  IN in_person_name VARCHAR(100),
  OUT _id INT
) BEGIN
  INSERT INTO Person(person_name)
  VALUES (in_person_name);
  
  SET _id = LAST_INSERT_id();

END//

CREATE PROCEDURE create_genre(
  IN in_genre_name VARCHAR(50),
  OUT _id INT

) BEGIN
  INSERT INTO Genre (genre_name)
  VALUES (in_genre_name);
  
  SET _id = LAST_INSERT_id();
END//

CREATE PROCEDURE create_country(
  IN in_country_name VARCHAR(30),
  OUT _id INT
) BEGIN
  INSERT INTO Country(country_name)
  VALUES (in_country_name);
  
  SET _id = LAST_INSERT_id();

END//

CREATE PROCEDURE create_category(
  IN in_category_type VARCHAR(10),
  OUT _id INT
) BEGIN
  INSERT INTO Category(category_type)
  VALUES (in_category_type);
  
  SET _id = LAST_INSERT_id();
END//

CREATE PROCEDURE create_paper(
  IN in_show_id INT,
  IN in_person_id INT,
  IN in_paper_role VARCHAR(10)
) BEGIN
  INSERT INTO Paper(show_id, person_id, paper_role)
  VALUES (in_show_id, in_person_id, in_paper_role);
END//

CREATE PROCEDURE create_listedin(
  IN in_show_id INT,
  IN in_genre_id INT
) BEGIN
  INSERT INTO ListedIn(show_id, genre_id)
  VALUES (in_show_id, in_genre_id);
END//

CREATE PROCEDURE create_streaming_on(
  IN in_show_id INT,
  IN in_country_id INT
) BEGIN
  INSERT INTO StreamingOn(show_id, country_id)
  VALUES (in_show_id, in_country_id);
END//

CREATE PROCEDURE create_duration(
  IN in_show_id INT,
  IN in_category_id INT,
  IN in_duration INT
) BEGIN
  INSERT INTO Duration(show_id, category_id, duration)
  VALUES (in_show_id, in_category_id, in_duration);
=======
  IN title VARCHAR(100),
  IN release_year INT,
  IN release_date_date DATE,
  IN rating VARCHAR(30),
  IN show_description VARCHAR(500)
) BEGIN  
  INSERT INTO shows(title, release_year, release_date, rating, show_description)
  VALUES (title, release_year, release_date, rating, show_description);
END//

CREATE PROCEDURE create_person(
  IN person_name VARCHAR(100)
) BEGIN
  INSERT INTO person(person_name)
  VALUES (person_name);
END//

CREATE PROCEDURE create_genre(
  IN genre VARCHAR(50)
) BEGIN
  INSERT INTO genre(genre)
  VALUES (genre);
END//

CREATE PROCEDURE create_country(
  IN country VARCHAR(30)
) BEGIN
  INSERT INTO country(country)
  VALUES (country);
END//

CREATE PROCEDURE create_category(
  IN category_type VARCHAR(10)
) BEGIN
  INSERT INTO category(category_type)
  VALUES (category_type);
END//

CREATE PROCEDURE create_paper(
  IN show_id INT,
  IN person_id INT,
  IN paper_role VARCHAR(10)
) BEGIN
  INSERT INTO Paper(show_id, person_id, paper_role)
  VALUES (show_id, person_id, paper_role);
END//

CREATE PROCEDURE create_listed_in(
  IN show_id INT,
  IN genre_id INT
) BEGIN
  INSERT INTO listed_in(show_id, genre_id)
  VALUES (show_id, genre_id);
END//

CREATE PROCEDURE create_streaming_on(
  IN show_id INT,
  IN country_id INT
) BEGIN
  INSERT INTO streaming_on(show_id, country_id)
  VALUES (show_id, country_id);
END//

CREATE PROCEDURE create_duration(
  IN show_id INT,
  IN category_id INT,
  IN duration_time INT
) BEGIN
  INSERT INTO duration(show_id, category_id, duration_time)
  VALUES (show_id, category_id, duration_time);
>>>>>>> 187ddfe4c40b1d6fafe08d0b0ad8a30cfbf32dd0
END//

DELIMITER ;
