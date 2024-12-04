DROP PROCEDURE IF EXISTS show_all_actors;
DROP PROCEDURE IF EXISTS show_streaming_countries;
DROP PROCEDURE IF EXISTS show_genre;

DELIMITER //

CREATE PROCEDURE show_all_actors()
BEGIN 
  SELECT p.person_name
  FROM person p
  NATURAL JOIN paper pap 
  WHERE LOWER(pap.paper_role) = 'actor'
  GROUP BY p.person_name
  ORDER BY TRIM(p.person_name);
END//

CREATE PROCEDURE show_all_directors()
BEGIN 
  SELECT p.person_name
  FROM person p
  NATURAL JOIN paper pap
  WHERE LOWER(pap.paper) = 'director'
  GROUP BY p.person_name
  ORDER BY TRIM(p.person_name);
END//

CREATE PROCEDURE show_all_genres()
BEGIN
  SELECT li.genre 
  FROM listed_in li
  GROUP BY li.genre
  ORDER BY li.genre;
END//

CREATE PROCEDURE show_genre(IN title VARCHAR(100))
BEGIN
  SELECT g.genre_name
  FROM Shows s
  NATURAL JOIN ListedIn li 
  NATURAL JOIN Genre g
  WHERE LOWER(s.title) = LOWER(title) 
  ORDER BY g.genre_name;
END//

CREATE PROCEDURE show_streaming_countries(IN title VARCHAR(100))
BEGIN
  SELECT s.show_id, s.title, c.country_name
  FROM country c 
  NATURAL JOIN streamingOn so
  NATURAL JOIN shows s 
  WHERE LOWER(s.title) = LOWER(title) 
  GROUP BY s.show_id
  ORDER BY s.show_id;
END//

CREATE PROCEDURE show_directors(IN title VARCHAR(100))
BEGIN
  SELECT s.show_id, s.title, p.person_name
  FROM person p
  NATURAL JOIN paper pap
  NATURAL JOIN shows s
  WHERE LOWER(s.title) = LOWER(title) AND LOWER(pap.paper) = 'director' 
  GROUP BY s.show_id
  ORDER BY s.show_id;
END//

CREATE PROCEDURE show_actors(IN title VARCHAR(100))
BEGIN    
  SELECT s.show_id, s.title, p.person_name
  FROM person p
  NATURAL JOIN paper pap
  NATURAL JOIN shows s
  WHERE LOWER(s.title) = LOWER(title) AND LOWER(pap.paper) = 'actor' 
  GROUP BY s.show_id
  ORDER BY s.show_id; 
END//

CREATE PROCEDURE show_films_by_director(IN director VARCHAR(100))
BEGIN
  SELECT p.person_name, s.title
  FROM shows s 
  NATURAL JOIN paper pap
  NATURAL JOIN person p
  WHERE LOWER(pap.paper_role) = 'director' AND LOWER(p.person_name) = LOWER(director)
  GROUP BY p.person_name
  ORDER BY s.title;
END//

CREATE PROCEDURE show_films_by_actor(IN actor VARCHAR(100))
BEGIN
  SELECT p.person_name, s.title
  FROM shows s 
  NATURAL JOIN paper pap
  NATURAL JOIN person p
  WHERE LOWER(pap.paper_role) = 'actor' AND LOWER(p.person_name) = LOWER(actor)
  GROUP BY p.person_name
  ORDER BY s.title;
END//

CREATE PROCEDURE show_genre_count()
BEGIN
  SELECT s.show_id, COUNT(*) AS genre_count
  FROM shows s
  NATURAL JOIN listed_in li
  GROUP BY s.show_id
  ORDER BY genre_count DESC;
END//

CREATE PROCEDURE genre_show_count()
BEGIN
  SELECT genre_id, COUNT(*) AS genre_count
  FROM listed_in
  GROUP BY genre_id
  ORDER BY genre_count;
END//

CREATE PROCEDURE show_yearly_count(IN category_type VARCHAR(10))
BEGIN
  SELECT s.release_year, COUNT(*) AS show_count
  FROM shows s
  NATURAL JOIN duration
  NATURAL JOIN category c
  GROUP BY s.release_year
  HAVING category_type IS NULL OR c.category_type = category_type
  ORDER BY show_count DESC;
END//

CREATE PROCEDURE show_top10_genre(IN category_type VARCHAR(10))
BEGIN
  CALL show_genre_count();
  SELECT s.title
  FROM show_genre_count AS sgc
  NATURAL JOIN shows s
  NATURAL JOIN duration d
  NATURAL JOIN category c
  WHERE category_type IS NULL OR c.category_type = category_type
  LIMIT 10;
END//

CREATE PROCEDURE genre_size_by_country()
BEGIN
  SELECT c.country_name AS Country, g.genre_name AS Genre
  FROM country c
  NATURAL JOIN streaming_on so
  NATURAL JOIN shows s
  NATURAL JOIN listed_in li
  NATURAL JOIN genre g
  GROUP BY Country, Genre
  HAVING COUNT(*) = (
    SELECT MAX(genre_count)
    FROM genre_show_count
    NATURAL JOIN listed_in li
    NATURAL JOIN shows s
    NATURAL JOIN streaming_on so
    GROUP BY so.country_id, genre_id
  );
END//

CREATE PROCEDURE top_actor_per_genre()
BEGIN
  SELECT 
    g.genre_name AS Genre,
    p.person_name AS Actor,
    COUNT(*) AS Appearances
  FROM show_cast sc
  NATURAL JOIN shows s 
  NATURAL JOIN listed_in li 
  NATURAL JOIN genre g  
  JOIN paper pp ON sc.actor_id = pp.person_id AND LOWER(pp.paper) = 'actor'
  NATURAL JOIN person p
  GROUP BY g.genre_name, p.person_name
  HAVING COUNT(*) = (
    SELECT MAX(Appearances)
    FROM (
      SELECT 
        g_inner.genre_name AS Genre,
        sc_inner.actor_id,
        COUNT(*) AS Appearances
      FROM show_cast sc_inner
      NATURAL JOIN shows s_inner 
      NATURAL JOIN listed_in li_inner 
      NATURAL JOIN genre g_inner 
      GROUP BY g_inner.genre_name, sc_inner.actor_id
    ) actor_counts
    WHERE actor_counts.Genre = g.genre_name
  )
  ORDER BY Genre, Appearances DESC;
END//

DELIMITER ;