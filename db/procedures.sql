DELIMITER //

CREATE PROCEDURE create_show(
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
END//

DELIMITER ;
