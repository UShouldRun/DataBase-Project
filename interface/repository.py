from config import db
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Result
Table = Result

# Data Insert Procedure Calls

def call_create_show(title: str, release_year: int, date_added: str, rating_id: int, description: str) -> int:
    show_id: int | None = call_exists_show(title, release_year, date_added, rating_id, description)
    if not show_id:
        db.session.execute(
            text(
                """
                CALL create_show(
                        :title,
                        :release_year,
                        :release_date,
                        :rating_id,
                        :show_description,
                        @show_id
                     )
                """
            ),
            {
                'title':            title,
                'release_year':     release_year,
                'release_date':     date_added,
                'rating_id':        rating_id,
                'show_description': description 
            }
        )
        return call_get_current_show_id()
    return show_id

def call_exists_show(title: str, release_year: int, date_added: str, rating: str, description: str) -> int | None :
    result: Table = db.session.execute(
        text(
            """
            SELECT
                show_id
            FROM Shows
            WHERE Shows.title = :title
            AND Shows.release_year = :release_year
            AND Shows.release_date = :release_date
            AND Shows.rating_id = :rating
            AND Shows.show_description = :show_description
            ;
            """
        ),
        {
            'title':            title,
            'release_year':     release_year,
            'release_date':     date_added,
            'rating':           rating,
            'show_description': description 
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_show_id() -> int:
    return db.session.execute(text("""SELECT @show_id""")).fetchone()[0]

def call_create_rating(rating: str) -> int:
    rating_id: int | None = call_exists_rating(rating)
    if not rating_id:
        db.session.execute(
            text(
                """CALL create_rating(:rating_type, @genre_id)"""),
            {
                'rating_type': rating
            }
        )
        return call_get_current_rating_id()
    return rating_id

def call_exists_rating(rating: str) -> int | None:
    result: Table = db.session.execute(
        text("""SELECT rating_id 
            FROM Rating 
            WHERE Rating.rating_type = :rating"""),
        {
            'rating': rating
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_rating_id() -> int:
    return db.session.execute(text("""SELECT @genre_id""")).fetchone()[0]

def call_create_genre(genre: str) -> int:
    genre_id: int | None = call_exists_genre(genre)
    if not genre_id:
        db.session.execute(
            text(
                """CALL create_genre(:genre_name,@genre_id)"""),
            {
                'genre_name': genre
            }
        )
        return call_get_current_genre_id()
    
    return genre_id

def call_exists_genre(genre: str) -> int | None:
    result: Table = db.session.execute(
        text("""SELECT genre_id 
            FROM Genre
            WHERE Genre.genre_name = :genre"""),
        {
            'genre': genre
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_genre_id() -> int:
    return db.session.execute(text("""SELECT @genre_id""")).fetchone()[0]


def call_create_listed_in(show_id: int, genre_id: int) -> None:
    db.session.execute(
        text(
            """
            CALL create_listed_in(
                    :show_id,
                    :genre_id
                 )
            """
        ),
        {
            'show_id':  show_id,
            'genre_id': genre_id
        }
    )

def call_create_country(country: str) -> int:
    country_id: int | None = call_exists_country(country)
    if not country_id:
        db.session.execute(
            text(
                """
                CALL create_country(
                        :country_name,
                        @country_id
                     )
                """
            ),
            {
                'country_name': country
            }
        )
        return call_get_current_country_id()
    return country_id

def call_exists_country(country: str) -> bool:
    result: Table = db.session.execute(
        text(
            """
            SELECT
                country_id
            FROM Country
            WHERE Country.country_name = :country
            """
        ),
        {
            'country': country
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_country_id() -> int:
    return db.session.execute(text("""SELECT @country_id""")).fetchone()[0]

def call_create_streaming_on(show_id: int, country_id: int) -> None:
    db.session.execute(
        text(
            """
            CALL create_streaming_on(
                    :show_id,
                    :country_id
                 )
            """
        ),
        {
            'show_id':    show_id,
            'country_id': country_id
        }
    )

def call_create_person(person: str) -> int:
    person_id: int | None = call_exists_person(person)
    if not person_id:
        db.session.execute(
            text(
                """
                CALL create_person(
                        :person_name,
                        @person_id
                     )
                """
            ),
            {
                'person_name': person
            }
        )
        return call_get_current_person_id()
    return person_id

def call_exists_person(person: str) -> int | None:
    result: Table = db.session.execute(
        text(
            """
            SELECT
                person_id
            FROM Person
            WHERE Person.person_name = :person
            """
        ),
        {
            'person': person
        }
    ).fetchone()
    assert result is None or len(result) == 1
    return result[0] if result is not None else None

def call_get_current_person_id() -> int:
    return db.session.execute(text("""SELECT @person_id""")).fetchone()[0]

def call_create_paper(show_id: int, person_id: int, role: str) -> None:
    db.session.execute(
        text(
            """
            CALL create_paper(
                    :show_id,
                    :person_id,
                    :paper_role
                 )
            """
        ),
        {
            'show_id':    show_id,
            'person_id':  person_id,
            'paper_role': role
        }
    )

def call_create_category(category: str) -> int:
    category_id: int | None = call_exists_category(category)
    if not category_id:
        db.session.execute(
            text(
                """
                CALL create_category(
                        :category_type,
                        @category_id
                     )
                """
            ),
            {
                'category_type': category
            }
        )
        return call_get_current_category_id()
    return category_id

def call_exists_category(category: str) -> int | None:
    result: Table = db.session.execute(
        text(
            """
            SELECT
                category_id
            FROM Category
            WHERE Category.category_type = :category
            """
        ),
        {
            'category': category
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_category_id() -> int:
    return db.session.execute(text("""SELECT @category_id""")).fetchone()[0]

def call_create_unit(unit: str) -> int:
    unit_id: int | None = call_exists_unit(unit)
    if not unit_id:
        db.session.execute(
            text(
                """
                CALL create_duration_unit(
                        :in_unit_name,
                        @unit_id
                     )
                """
            ),
            {
                'in_unit_name': unit
            }
        )
        return call_get_current_unit_id()
    return unit_id

def call_exists_unit(unit: str) -> int | None:
    result: Table = db.session.execute(
        text(
            """
            SELECT unit_id
            FROM DurationUnit
            WHERE unit_name = :unit_name
            """
        ),
        {
            'unit_name': unit
        }
    ).fetchone()
    return result[0] if result is not None else None

def call_get_current_unit_id() -> int:
    return db.session.execute(text("SELECT @unit_id")).fetchone()[0]

def call_create_duration(show_id: int, category_id: int, duration_time: int, unit_id: int) -> None:
    db.session.execute(
        text(
            """
            CALL create_duration(
                    :show_id,
                    :category_id,
                    :duration_time,
                    :unit_id
            )
            """
        ),
        {
            'show_id': show_id,
            'category_id': category_id,
            'duration_time': duration_time,
            'unit_id': unit_id
        }
    )

# Data Get Procedure Calls

def call_actors_all() -> list[str]:
    result: Table = db.session.execute(
        text("CALL actors_all()")
    )
    return [row['actors'] for row in result.mappings()]

def call_actors(title: str) -> list[str]:
    result: Table = db.session.execute(
        text("""CALL actors(:title)"""),
        {
            'title': title
        }
    )
    return [row["actors"] for row in result.mappings()]

def call_directors_all() -> list[str]:
    result: Table = db.session.execute(
        text("CALL directors_all()")
    )
    return [row['directors'] for row in result.mappings()]

def call_directors(title: str) -> list[str]:
    result: Table = db.session.execute(
        text("""CALL directors(:title)"""),
        {
            'title': title
        }
    )
    return [row["directors"] for row in result.mappings()]

def call_genres_all() -> list[str]:
    result: Table = db.session.execute(
        text("CALL genres_all()")
    )
    return [row["genres"] for row in result.mappings()]

def call_genres(title: str) -> list[str]:
    result: Table = db.session.execute(
        text("CALL genres(:title)"),
        {
            "title": title
        }
    )
    return [row["genres"] for row in result.mappings()]

def call_countries_all() -> list[str]:
    result: Table = db.session.execute(
        text("""CALL countries_all()""")
    )
    return [row["countries"] for row in result.mappings()]

def call_countries(title: str) -> list[str]:
    result: Table = db.session.execute(
        text("""CALL countries(:title)"""),
        {
            'title': title
        }
    )
    return [row["countries"] for row in result.mappings()]

def call_titles_all() -> list[dict]:
    result: Table = db.session.execute(
        text(
            """
            SELECT DISTINCT
                Shows.title AS title,
	            Rating.rating_type AS rating,
                Duration.duration_time AS duration,
                DurationUnit.unit_name as unit,
                Shows.show_description AS description
            FROM Shows
            NATURAL JOIN Duration
            NATURAL JOIN DurationUnit
            NATURAL JOIN Rating
            ORDER BY title, duration
            """
        )
    )
    return [
        {
            "title":       row["title"],
            "rating":      row["rating"],
            "duration": f"{row['duration']} {row['unit']}", 
            "description": row["description"]
        } for row in result.mappings()
    ]

def call_titles_by_genre(genre: str) -> list[dict]:
    result: Table = db.session.execute(
        text("CALL titles_by_genre(:in_genre)"),
        {
            "in_genre": genre
        }
    )
    return [
        {
            "title":       row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "rating":      row["rating"],
            "description": row["description"],
        }
        for row in result.mappings()
    ]
def call_titles_by_country(country: str) -> list[dict]:
    result: Table = db.session.execute(
        text("CALL titles_by_country(:in_country)"),
        {
            "in_country": country
        }
    )
    return [
        {
            "title":       row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "rating":      row["rating"],
            "description": row["description"],
        }
        for row in result.mappings()
    ]

def call_titles_by_rating(rating: str) -> list[dict]:
    result: Table = db.session.execute(
        text("CALL titles_by_rating(:in_rating)"),
        {
            "in_rating":rating
        }
    )
    return [
        {
            "title":       row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "rating":      row["rating"],
            "description": row["description"],
        }
        for row in result.mappings()
    ]

def call_ratings_all() -> list[str]:
    result: Table = db.session.execute(
        text("CALL ratings_all()")
    )
    return [row["ratings"] for row in result.mappings()]
def call_show_within_restrictions(category_type,min_time,max_time)-> list[dict]:
    result: Table = db.session.execute(
        text(
            """
            CALL show_within_restrictions(
                    :in_category_type,
                    :in_min_time,
                    :in_max_time
                 )
            """
        ),
        {
            "in_category_type": category_type,
            "in_min_time":      min_time,
            "in_max_time":      max_time
        }
    )
    return [
        {
            "title":       row["title"],
            "rating":      row["rating"],
            "duration": f"{row['duration']} {row['unit']}",
            "description": row["description"],
        }
        for row in result.mappings()
    ]

def call_top_actor_by_genre() -> list[dict]:
    result: Table = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [
        {
            "genre":       row["genre"],
            "actor":       row["actor"],
            "appearances": row["appearances"]
        }
        for row in result.mappings()
    ]

def call_top_actors() -> list[dict]:
    result: Table = db.session.execute(
        text("""CALL top_actors()""")
    )
    return [
        {
            "name":       row["actors"],
            "appearances": row["appearances"]
        }
        for row in result.mappings()
    ]

def call_titles_top10_genre(category_type: str) -> list[str]:
    result: Table = db.session.execute(
        text(
            """
            CALL titles_top10_genre(
                    :category_type
                 )
            """
        ),
        {
            'category_type': category_type
        }
    )
    return [row["title"] for row in result.mappings()]

