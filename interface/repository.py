from config import db

def call_show_genre(title):
    db.session.execute("CALL show_genre(title)")
    