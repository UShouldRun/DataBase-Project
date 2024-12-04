DELIMITER //

CREATE PROCEDURE create_show(
  IN in_title VARCHAR(100),
  IN in_release_year INT,
  IN in_release_date DATE,
  IN in_rating VARCHAR(30),
  IN in_show_description VARCHAR(500),
  OUT _id INT 
) BEGIN  
  INSERT INTO Shows (title, release_year, release_date , rating, show_description) 
  VALUES (in_title, in_release_year, in_release_date, in_rating, in_show_description);
  
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

CREATE PROCEDURE create_listed_in(
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

CREATE PROCEDURE create_duration_unit(
  IN in_unit_name VARCHAR(15),
  OUT _id INT
) BEGIN
  INSERT INTO DurationUnit(unit_name)
  VALUES (in_unit_name);
  
  SET _id = LAST_INSERT_id();

END//

CREATE PROCEDURE create_duration(
  IN in_show_id INT,
  IN in_category_id INT,
  IN in_duration_time INT,
  IN in_unit_id INT
) BEGIN
  INSERT INTO Duration(show_id, category_id, duration_time, unit_id)
  VALUES (in_show_id, in_category_id, in_duration_time, in_unit_id);
END//

DELIMITER ;
