DELIMITER //

CREATE PROCEDURE show_genre(IN title VARCHAR(100))
BEGIN
  -- Mostrar o género dos filmes
  SELECT s.show_id, s.title, li.genre
  FROM listed_in li
  NATURAL JOIN shows s
  WHERE LOWER(s.title) = LOWER(title) 
  GROUP BY s.show_id
  ORDER BY s.show_id; 
END//

CREATE PROCEDURE show_streaming_countries(IN title VARCHAR(100))
BEGIN
  -- Mostrar os países onde o filme está em stream
  SELECT s.show_id, s.title, c.name
  FROM country c 
  NATURAL JOIN streaming_on so
  NATURAL JOIN shows s 
  WHERE LOWER(s.title) = LOWER(title) 
  GROUP BY s.show_id
  ORDER BY s.show_id;
END//

CREATE PROCEDURE show_directors(IN title VARCHAR(100))
BEGIN
  -- Mostrar os diretores do filme
  SELECT s.show_id, s.title, p.name
  FROM person
  NATURAL JOIN paper p
  NATURAL JOIN shows s
  WHERE LOWER(s.title) = LOWER(title) AND LOWER(p.paper) = 'director' 
  GROUP BY s.show_id
  ORDER BY s.show_id;
END//

CREATE PROCEDURE show_actors(IN title VARCHAR(100))
BEGIN    
  -- Mostrar os atores do filme
  SELECT s.show_id, s.title, p.name
  FROM person
  NATURAL JOIN paper p
  NATURAL JOIN shows s
  WHERE LOWER(s.title) = LOWER(title) AND LOWER(p.paper) = 'actor' 
  GROUP BY s.show_id
  ORDER BY s.show_id; 
END//

CREATE PROCEDURE show_genre_count()
BEGIN
  SELECT s.show_id, COUNT(*) AS genre_count
  FROM shows s
  NATURAL JOIN listed_in li
  GROUP BY s.show_id
  ORDER BY genre_count DESC;
END//

CREATE PROCEDURE show_top10_genre(IN category_type VARCHAR(10))
BEGIN
  SELECT s.title
  FROM show_genre_count() sgc
  NATURAL JOIN show s
  NATURAL JOIN duration d
  NATURAL JOIN category c
  WHERE category_type IS NULL OR c.category_type = category_type
  LIMIT 10;
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

CREATE PROCEDURE genre_show_count()
BEGIN
  SELECT genre_id, COUNT(*) AS genre_count
  FROM listed_in
  GROUP BY genre_id
  ORDER BY genre_count;
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
    FROM genre_show_count()
    NATURAL JOIN listed_in li
    NATURAL JOIN shows s
    NATURAL JOIN streaming_on so
    GROUP BY so.country_id, genre_id
  )
  ;
END//

DELIMITER ;
