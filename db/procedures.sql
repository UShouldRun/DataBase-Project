DELIMITER //

CREATE PROCEDURE create_show(
  IN title VARCHAR(50),
  IN year INT,
  IN show_date DATE,
  IN rating VARCHAR(30),
  IN description VARCHAR(500)
) BEGIN  
  INSERT INTO Shows (title, year, date, rating, description)
  VALUES (title, year, show_date, rating, description);
END//

CREATE PROCEDURE create_person(
  IN name VARCHAR(100)
) BEGIN
  INSERT INTO Person(name)
  VALUES (name);
END//

CREATE PROCEDURE create_genre(
  IN name VARCHAR(50)
) BEGIN
  INSERT INTO Genre (name)
  VALUES (name);
END//

CREATE PROCEDURE create_country(
  IN name VARCHAR(30)
) BEGIN
  INSERT INTO Country(name)
  VALUES (name);
END//

CREATE PROCEDURE create_category(
  IN type VARCHAR(10)
) BEGIN
  INSERT INTO Category(type)
  VALUES (type);
END//

CREATE PROCEDURE create_paper(
  IN showID INT,
  IN personID INT,
  IN paper VARCHAR(10)
) BEGIN
  INSERT INTO Paper(showID, personID, paper)
  VALUES (showID, personID, paper);
END//

CREATE PROCEDURE create_listedin(
  IN showID INT,
  IN genreID INT
) BEGIN
  INSERT INTO ListedIn(showID, genreID)
  VALUES (showID, genreID);
END//

CREATE PROCEDURE create_streaming_on(
  IN showID INT,
  IN countryID INT
) BEGIN
  INSERT INTO StreamingOn(showID, countryID)
  VALUES (showID, countryID);
END//

CREATE PROCEDURE create_duration(
  IN showID INT,
  IN categoryID INT,
  IN delta_time INT
) BEGIN
  INSERT INTO Duration(showID, categoryID, time)
  VALUES (showID, categoryID, delta_time);
END//

DELIMITER ;
