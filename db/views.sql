USE DisneyDB;

DROP PROCEDURE IF EXISTS actors_all;
DROP PROCEDURE IF EXISTS actors;
DROP PROCEDURE IF EXISTS directors_all;
DROP PROCEDURE IF EXISTS directors;
DROP PROCEDURE IF EXISTS genres_all;
DROP PROCEDURE IF EXISTS genres;
DROP PROCEDURE IF EXISTS countries_all;
DROP PROCEDURE IF EXISTS countries;
DROP PROCEDURE IF EXISTS titles_by_director;
DROP PROCEDURE IF EXISTS titles_by_actor;
DROP PROCEDURE IF EXISTS titles_by_country;
DROP PROCEDURE IF EXISTS titles_by_genre;
DROP PROCEDURE IF EXISTS titles_yearly_count;
DROP PROCEDURE IF EXISTS titles_top10_by_genre;
DROP PROCEDURE IF EXISTS top_actor_by_genre;
DROP PROCEDURE IF EXISTS top_actor;

DELIMITER //

CREATE PROCEDURE actors_all()
BEGIN 
  SELECT DISTINCT Person.person_name AS actors
  FROM Person
  NATURAL JOIN Paper
  WHERE LOWER(Paper.paper_role) = 'actor'
  ORDER BY TRIM(Person.person_name);
END//

CREATE PROCEDURE actors(IN title VARCHAR(100))
BEGIN    
  SELECT Person.person_name as actors
  FROM Person
  NATURAL JOIN Paper
  NATURAL JOIN Shows
  WHERE LOWER(Shows.title) = LOWER(title) AND LOWER(Paper.paper_role) = 'actor' 
  GROUP BY Person.person_name
  ORDER BY Person.person_name;
END//

CREATE PROCEDURE directors_all()
BEGIN 
  SELECT DISTINCT Person.person_name AS directors
  FROM Person
  NATURAL JOIN Paper
  WHERE LOWER(Paper.paper_role) = 'director'
  ORDER BY TRIM(Person.person_name);
END//

CREATE PROCEDURE directors(IN title VARCHAR(100))
BEGIN
  SELECT Person.person_name as directors
  FROM Person
  NATURAL JOIN Paper
  NATURAL JOIN Shows
  WHERE LOWER(Shows.title) = LOWER(title) AND LOWER(Paper.paper_role) = 'director'
  GROUP BY Person.person_name
  ORDER BY Person.person_name;
END//

CREATE PROCEDURE genres_all()
BEGIN
  SELECT DISTINCT genre_name AS genres
  FROM Genre
  ORDER BY genre_name;
END//

CREATE PROCEDURE genres(IN title VARCHAR(100))
BEGIN	
  SELECT Genre.genre_name AS genres
  FROM Shows
  NATURAL JOIN ListedIn
  NATURAL JOIN Genre
  WHERE LOWER(Shows.title) = LOWER(title) 
  ORDER BY Genre.genre_name;
END//

CREATE PROCEDURE countries_all()
BEGIN
  SELECT DISTINCT country_name AS countries
  FROM Country
  ORDER BY country_name;
END//

CREATE PROCEDURE countries(IN in_title VARCHAR(100))
BEGIN
	SELECT Country.country_name AS countries
	FROM Country
	NATURAL JOIN StreamingOn
	NATURAL JOIN Shows
	WHERE LOWER(Shows.title) = LOWER(in_title);
END//

CREATE PROCEDURE titles_by_director(IN director VARCHAR(100))
BEGIN
  SELECT Shows.title
  FROM Shows 
  NATURAL JOIN Paper
  NATURAL JOIN Person
  WHERE LOWER(Paper.paper_role) = 'director' AND LOWER(Person.person_name) = LOWER(director)
  GROUP BY Shows.title
  ORDER BY Shows.title;
END//

CREATE PROCEDURE titles_by_actor(IN actor VARCHAR(100))
BEGIN
  SELECT Shows.title
  FROM Shows
  NATURAL JOIN Paper
  NATURAL JOIN Person
  WHERE LOWER(Paper.paper_role) = 'actor' AND LOWER(Person.person_name) = LOWER(actor)
  GROUP BY Shows.title
  ORDER BY Shows.title;
END//

CREATE PROCEDURE titles_by_genre()
BEGIN
  SELECT 
    Genre.genre_name AS genres, 
    GROUP_CONCAT(DISTINCT Shows.title ORDER BY Shows.title SEPARATOR ', ') AS titles
  FROM Shows 
  NATURAL JOIN ListedIn
  NATURAL JOIN Genre 
  GROUP BY Genre.genre_name
  ORDER BY Genre.genre_name;
END//

CREATE PROCEDURE titles_by_country()
BEGIN
  SELECT 
    Country.country_name AS countries,
    GROUP_CONCAT(DISTINCT Shows.title ORDER BY Shows.title SEPARATOR ', ') AS titles
  FROM Shows 
  NATURAL JOIN StreamingOn
  NATURAL JOIN Country
  GROUP BY Country.country_name
  ORDER BY Country.country_name;
END//

CREATE PROCEDURE titles_yearly_count(IN category_type VARCHAR(10))
BEGIN
  SELECT Shows.release_year, COUNT(*) AS show_count
  FROM Shows
  NATURAL JOIN Duration
  NATURAL JOIN Category
  WHERE (category_type IS NULL OR Category.category_type = category_type)
  GROUP BY Shows.release_year
  ORDER BY show_count DESC;
END//

CREATE PROCEDURE titles_top10_by_genre(IN category_type VARCHAR(10))
BEGIN
  SELECT Shows.title
  FROM genres_count
  NATURAL JOIN Shows
  NATURAL JOIN Duration
  NATURAL JOIN Category
  WHERE category_type IS NULL OR Category.category_type = category_type
  LIMIT 10;
END//

CREATE PROCEDURE top_actor_by_genre()
BEGIN
  SELECT 
    Genre.genre_name,
    Person.person_name AS actor,
    pa.appearances
  FROM Person
  JOIN person_appearances_per_genre_per_role pa ON pa.person_id = Person.person_id
  JOIN Genre ON Genre.genre_id = pa.genre_id
  WHERE LOWER(pa.paper_role) = 'actor'
     AND appearances = (
       SELECT MAX(pa_inner.appearances)
       FROM person_appearances_per_genre_per_role pa_inner
       WHERE pa_inner.genre_id = Genre.genre_id
     )
  ORDER BY pa.appearances DESC, Genre.genre_name ASC
  LIMIT 10;
END//

CREATE PROCEDURE top_actor()
BEGIN
  SELECT
    Person.person_name AS actor,
    actor_appearances.appearances
  FROM Person
  NATURAL JOIN actor_appearances
  WHERE actor_appearances.appearances = (
    SELECT MAX(a.appearances)
    FROM actor_appearances a
  )
  GROUP BY actor_appearances.person_id
  ORDER BY actor_appearances.appearances, Person.person_name
  LIMIT 10;
END//

-- Views

CREATE OR REPLACE VIEW genres_count AS
SELECT Shows.show_id, COUNT(*) AS genre_count
FROM Shows
NATURAL JOIN ListedIn
GROUP BY Shows.show_id
ORDER BY genre_count DESC;

CREATE OR REPLACE VIEW genre_show_count AS
SELECT genre_id, COUNT(*) AS genre_count
FROM ListedIn 
GROUP BY genre_id
ORDER BY genre_count DESC;

CREATE OR REPLACE VIEW person_appearances AS
SELECT 
  person_id,
  COUNT(*) AS appearances
FROM Paper
NATURAL JOIN Person
GROUP BY person_id
ORDER BY appearances DESC, person_id;

CREATE OR REPLACE VIEW actor_appearances AS
SELECT 
  person_id,
  COUNT(*) AS appearances
FROM Paper
WHERE paper_role = 'actor'
GROUP BY person_id
ORDER BY appearances DESC, person_id;

CREATE OR REPLACE VIEW person_appearances_per_genre_per_role AS
SELECT 
  ListedIn.genre_id,
  Paper.person_id,
  Paper.paper_role,
  COUNT(*) AS appearances
FROM Paper
NATURAL JOIN Shows
NATURAL JOIN ListedIn
GROUP BY ListedIn.genre_id, Paper.person_id, Paper.paper_role;
