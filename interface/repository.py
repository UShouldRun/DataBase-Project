from config import db, Table
from sqlalchemy import text

def call_actors_all() -> list[str]:
    result: Table = db.session.execute(
        text("CALL actors_all()")
    )
    return [row['actors'] for row in result.mappings()]

def call_actors(title: str) -> list[str]:
    result: Table = db.session.execute(
        text("""CALL actors(:title)"""),
        { 'title': title }
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
        { 'title': title }
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
        { "title": title }
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
        { 'title': title }
    )
    return [row["countries"] for row in result.mappings()]

def call_titles_all() -> list[dict]:
    result = db.session.execute(
        text(
            """
            SELECT DISTINCT
                Shows.title AS title,
                Duration.duration_time AS duration,
                DurationUnit.unit_name as unit,
                Shows.show_description AS description
            FROM Shows
            NATURAL JOIN Duration
            NATURAL JOIN DurationUnit
            ORDER BY title, duration
            """
        )
    )
    return [
        {
            "title":       row["title"],
            "duration": f"{row['duration']} {row['unit']}", 
            "description": row["description"]
        } for row in result.mappings()
    ]

def call_titles_by_genre(genre: str) -> list[dict]:
    result = db.session.execute(
        text("CALL titles_by_genre(:in_genre)"),
        {"in_genre": genre}
    )
    return [
        {
            "title": row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "description": row["description"],
        }
        for row in result.mappings()
    ]
def call_titles_by_country(country: str) -> list[dict]:
    result = db.session.execute(
        text("CALL titles_by_country(:in_country)"),{"in_country":country}
    )
    return [
        {
            "title": row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "description": row["description"],
        }
        for row in result.mappings()
    ]

def call_show_within_restrictions(category_type,min_time,max_time)-> list[dict]:
    result = db.session.execute(
        text("CALL show_within_restrictions(:in_category_type, :in_min_time, :in_max_time)"),
        {
            "in_category_type":category_type,
            "in_min_time":min_time,
            "in_max_time":max_time
        }
    )
    return [
        {
            "title": row["title"],
            "duration": f"{row['duration']} {row['unit']}",
            "description": row["description"],
        }
        for row in result.mappings()
    ]

def call_top_actor_by_genre() -> list[dict]:
    result: Table = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [row["countries"] for row in result.mappings()]

def call_titles_top10_genre(category_type: str) -> list[str]:
    result: Table = db.session.execute(
        text("""CALL titles_top10_genre(:category_type)"""),
        { 'category_type': category_type }
    )
    return [row["title"] for row in result.mappings()]

def call_top_actor_by_genre() -> list[dict]:
    result: Table = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [dict(row) for row in result.fetchall()]
