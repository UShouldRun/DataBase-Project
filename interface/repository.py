from config import db, Table
from sqlalchemy import text

def call_show_all_actors() -> [str]:
    result = db.session.execute(
        text("CALL show_all_actors()")
    )
    actors_array = [row['actors'] for row in result.mappings()]
    return actors_array

def call_show_all_directors() -> [str]:
    result = db.session.execute(
        text("CALL show_all_directors()")
    )
    directors_array = [row['directors'] for row in result.mappings()]
    return directors_array

def call_show_genre(title: str) -> [str]:
    result = db.session.execute(
        text("CALL show_genre(:title)"), {"title": title}
    )
    genre_array = [row["genres"] for row in result.mappings()]
    return genre_array

def call_show_all_genres() -> [str]:
    result = db.session.execute(
        text("CALL show_all_genres()")
    )
    genre_array = [row["genres"] for row in result.mappings()]
    return genre_array

'''CONFIRMEM A PARTIR DAQUI'''

def call_show_streaming_countries(title: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_streaming_countries(:title)"""), {'title': title}
    )
    return [row["country_name"] for row in result.fetchall()]

def call_show_directors(title: str) -> list[str]:
    result = db.session.execute(
        text("""CALL show_directors(:title)"""), {'title': title}
    )
    return [row["person_name"] for row in result.fetchall()]


def call_show_actors(title: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_directors(:title)"""), {'title': title}
    )
    return [row["person_name"] for row in result.fetchall()]


def call_show_top10_genre(category_type: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_directors(:category_type)"""), {'category_type': category_type}
    )
    return [row["title"] for row in result.fetchall()]


def call_top_actor_by_genre() -> list[dict]:
    result = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [dict(row) for row in result.fetchall()]