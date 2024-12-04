from config import db, Table
from sqlalchemy import text

def call_show_all_actors() -> [str]:
    result = db.session.execute(
        text("CALL show_all_actors()")
    )
    actors_array = [row['person_name'] for row in result.mappings()]
    return actors_array
def call_show_all_directors() -> [str]:
    result = db.session.execute(
        text("CALL show_all_directors()")
    )
    directors_array = [row['person_name'] for row in result.mappings()]
    return directors_array
'''
def call_show_genre(title: str) -> Table:
    return db.session.execute(
        text("""CALL show_genre(:title)"""), { 'title': title }
    )
    return table

def call_show_streaming_countries(title: str) -> Table:
    return db.session.execute(
        text("""CALL show_streaming_countries(:title)"""), { 'title': title }
    )

def call_show_directors(title: str) -> Table:
    return db.session.execute(
        text("""CALL show_directors(:title)"""), { 'title': title }
    )

def call_show_actors():
    result = db.session.execute(
        text("CALL show_actors()")
    )
    actors_array = [dict(row) for row in result.fetchall()]
    return actors_array

def call_show_top10_genre(category_type: str) -> Table:
   return db.session.execute(
        text("""CALL show_yearly_count(:category_type)"""), { 'category_type': category_type }
    ) 

def call_genre_show_count() -> Table:
    return db.session.execute(
        text("""CALL genre_size_by_country()""")
    )

def call_top_actor_by_genre() -> Table:
    return db.session.execute(
        text("""CALL top_actor_by_genre()""")
    )
'''