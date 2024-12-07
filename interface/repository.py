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

def call_show_all_titles()->[str]:
    result = db.session.execute(
        text("SELECT title as titles FROM Shows ORDER BY title")
    )
    return [row["titles"] for row in result.mappings()]
'''A PARTIR DAQUI    '''
def call_show_all_shows_by_country() -> list[dict]:
    result = db.session.execute(
        text("CALL show_all_shows_by_country()")
    )
    movies_array = [{"country": row["country"], "movies": row["movies"]} for row in result.mappings()]
    return movies_array

def call_show_all_shows_by_genre() -> list[dict]:
    result = db.session.execute(
        text("CALL show_all_shows_by_genre()")
    )
    movies_array = [{"genre": row["genres"], "movies": row["movies"]} for row in result.mappings()]
    return movies_array
'''---------------------------'''

def call_top_actor_by_genre() -> list[dict]:
    result = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [row["countries"] for row in result.mappings()]

def call_show_all_countries() -> [str]:
    result = db.session.execute(
        text("""CALL show_all_countries()""")
    )
    return [row["countries"] for row in result.mappings()]

def call_show_countries(title: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_countries(:title)"""), {'title': title}
    )
    return [row["countries"] for row in result.mappings()]

def call_show_directors(title: str) -> list[str]:
    result = db.session.execute(
        text("""CALL show_directors(:title)"""), {'title': title}
    )
    return [row["directors"] for row in result.mappings()]


def call_show_actors(title: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_actors(:title)"""), {'title': title}
    )
    return [row["actors"] for row in result.mappings()]

'''CONFIRMEM A PARTIR DAQUI'''
def call_show_top10_genre(category_type: str) -> [str]:
    result = db.session.execute(
        text("""CALL show_directors(:category_type)"""), {'category_type': category_type}
    )
    return [row["title"] for row in result.mappings()]
'''probably delete this'''
def call_top_actor_by_genre() -> list[dict]:
    result = db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
    return [dict(row) for row in result.fetchall()]
