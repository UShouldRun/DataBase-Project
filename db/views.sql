USE DisneyDB;

DROP PROCEDURE IF EXISTS actors_all;
DROP PROCEDURE IF EXISTS actors;
DROP PROCEDURE IF EXISTS directors_all;
DROP PROCEDURE IF EXISTS directors;
DROP PROCEDURE IF EXISTS genres_all;
DROP PROCEDURE IF EXISTS genres;
DROP PROCEDURE IF EXISTS countries_all;
DROP PROCEDURE IF EXISTS countries;
DROP PROCEDURE IF EXISTS ratings_all;
DROP PROCEDURE IF EXISTS titles_by_director;
DROP PROCEDURE IF EXISTS titles_by_actor;
DROP PROCEDURE IF EXISTS titles_by_country;
DROP PROCEDURE IF EXISTS titles_by_genre;
DROP PROCEDURE IF EXISTS titles_by_rating;
DROP PROCEDURE IF EXISTS show_within_restrictions;
DROP PROCEDURE IF EXISTS top_actors;
DROP PROCEDURE IF EXISTS top_actor_by_genre;
DROP PROCEDURE IF EXISTS genre_percentage;
DROP PROCEDURE IF EXISTS titles_by_letters;
-- not yet implemented
DROP PROCEDURE IF EXISTS titles_yearly_count;
DROP PROCEDURE IF EXISTS titles_top10_by_genre;
DROP PROCEDURE IF EXISTS show_within_decade;


DELIMITER //

CREATE PROCEDURE actors_all()
BEGIN 
  SELECT DISTINCT Person.person_name AS actors
  FROM Person
  NATURAL JOIN Paper
  WHERE LOWER(Paper.paper_role) = 'actor'
  ORDER BY
    CASE
      WHEN LEFT(TRIM(Person.person_name), 1) REGEXP '[a-zA-Z]' THEN LOWER(TRIM(Person.person_name))
      ELSE CONCAT('zzz_', LOWER(TRIM(Person.person_name))) 
    END;
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
  SELECT DISTINCT Genre.genre_name AS genres
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

CREATE PROCEDURE ratings_all()
BEGIN 
	SELECT rating_type AS ratings
	FROM Rating;
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
  SELECT DISTINCT
	Shows.title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows 
  NATURAL JOIN Paper
  NATURAL JOIN Person
  NATURAL JOIN Rating
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  WHERE LOWER(Paper.paper_role) = 'director' AND LOWER(Person.person_name) = LOWER(director)
  ORDER BY Shows.title;
END//

CREATE PROCEDURE titles_by_actor(IN actor VARCHAR(100))
BEGIN
  SELECT DISTINCT 
    Shows.title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows
  NATURAL JOIN Paper
  NATURAL JOIN Person
  NATURAL JOIN Rating
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  WHERE LOWER(Paper.paper_role) = 'actor' AND LOWER(Person.person_name) = LOWER(actor)
  ORDER BY Shows.title;
END//

CREATE PROCEDURE titles_by_genre(IN in_genre VARCHAR(50))
BEGIN
  SELECT DISTINCT
    Genre.genre_name AS genre,
    Shows.title AS title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows 
  NATURAL JOIN ListedIn
  NATURAL JOIN Genre 
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  NATURAL JOIN Rating
  WHERE Genre.genre_name = in_genre
  ORDER BY Shows.title;
END//

CREATE PROCEDURE titles_by_country(IN in_country VARCHAR(50))
BEGIN
  SELECT DISTINCT
    Country.country_name AS country,
    Shows.title AS title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows 
  NATURAL JOIN StreamingOn
  NATURAL JOIN Country
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  NATURAL JOIN Rating
  WHERE Country.country_name = in_country
  ORDER BY Shows.title;
END//


CREATE PROCEDURE titles_by_rating(IN in_rating VARCHAR(30))
BEGIN
  SELECT DISTINCT
    Shows.title AS title,
	Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows 
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  NATURAL JOIN Rating
  WHERE Rating.rating_type = in_rating
  ORDER BY Shows.title;
END//

-- OPERAÇÕES PARA UMA DETERMINADA DURAÇÃO

CREATE PROCEDURE show_within_restrictions(IN in_category_type VARCHAR(50), IN in_min_time INT, IN in_max_time INT)
BEGIN
  SELECT DISTINCT
    Shows.title AS title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  NATURAL JOIN Category
  NATURAL JOIN Rating
  WHERE Duration.duration_time BETWEEN in_min_time AND in_max_time AND Category.category_type = in_category_type
  ORDER BY Duration.duration_time DESC;
END//

CREATE PROCEDURE show_within_decade(IN in_min_year INT, IN in_max_year INT)
BEGIN
  SELECT 
    Shows.title AS title,
    Shows.rating AS rating,
    Shows.release_date AS date,
    Shows.show_description AS description
  FROM Shows
  WHERE Shows.release_year BETWEEN in_min_year AND in_max_year
  ORDER BY Shows.release_year DESC;
END//

CREATE PROCEDURE titles_yearly_count()
BEGIN
  SELECT Shows.release_year, COUNT(*) AS show_count
  FROM Shows
  NATURAL JOIN Duration
  NATURAL JOIN Category
  GROUP BY Shows.release_year
  ORDER BY show_count ASC;
END//

-- PERCENTAGENS

CREATE PROCEDURE genre_percentage()
BEGIN
  SELECT 
    genre.genre_name AS genre,
    COUNT(Shows.title) AS nr_of_titles,
    ROUND((COUNT(Shows.title) * 100.0 / (SELECT COUNT(*) FROM Shows)), 2) AS percentage
  FROM Shows
  NATURAL JOIN listedin
  NATURAL JOIN genre
  GROUP BY genre.genre_name
  ORDER BY genre.genre_name ASC;
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
	WITH RankedActors AS (
	  SELECT 
		Genre.genre_name AS genre,
		Person.person_name AS actor,
		pa.appearances,
		ROW_NUMBER() OVER (PARTITION BY pa.genre_id ORDER BY pa.appearances DESC) AS ranking
	  FROM person_appearances_per_genre_per_role pa
	  JOIN Person ON pa.person_id = Person.person_id
	  JOIN Genre ON Genre.genre_id = pa.genre_id
	  WHERE LOWER(pa.paper_role) = 'actor'
	)
	SELECT genre, actor, appearances
	FROM RankedActors
	WHERE ranking = 1
	ORDER BY genre ASC;
END//

CREATE PROCEDURE top_actors()
BEGIN
	SELECT
	  Person.person_name AS actors,
	  actor_appearances.appearances
	FROM Person
	JOIN actor_appearances ON Person.person_id = actor_appearances.person_id
	JOIN Paper ON Person.person_id = Paper.person_id
	WHERE Paper.paper_role = "actor"
	GROUP BY Person.person_id
	ORDER BY actor_appearances.appearances DESC, Person.person_name ASC;
END//

CREATE PROCEDURE titles_by_letters(IN in_letters VARCHAR(30))
BEGIN
  SELECT DISTINCT
    Shows.title AS title,
    Rating.rating_type AS rating,
    Duration.duration_time AS duration,
    DurationUnit.unit_name AS unit,
    Shows.show_description AS description
  FROM Shows
  NATURAL JOIN Duration
  NATURAL JOIN DurationUnit
  NATURAL JOIN Category
  NATURAL JOIN Rating
  WHERE LOWER(Shows.title) LIKE CONCAT(LOWER(in_letters), '%');
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
  person.person_id,
  person.person_name,
  COUNT(paper.show_id) AS appearances
FROM Paper
JOIN Person ON Paper.person_id = Person.person_id
GROUP BY person.person_id, person.person_name
ORDER BY appearances DESC, person.person_id;

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
