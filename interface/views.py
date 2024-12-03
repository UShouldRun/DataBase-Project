from main import app
from flask import render_template

# routes
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/actors")
def show_all_actors():
    actors = [
        {"ActorId": 1, "Name": "João"},
        {"ActorId": 2, "Name": "Rossi"},
        {"ActorId": 3, "Name": "Alex"},
        {"ActorId": 4, "Name": "Henrique"}
    ]
    return render_template("actors.html", actors=actors)

@app.route("/shows")
def show_all_shows():
    shows = [
    {
        "type": "Movie",
        "title": "As aventuras da cadeira de base de dados",
        "director": ["João", "Henrique"],
        "cast": ["João", "Henrique", "Rossi", "Alex"],
        "country": ["Portugal"],
        "release_year": [2024],
        "rating": "TOP G",
        "duration": "1 mês",
        "listed_in": ["Comedy", "Dramatic"],
        "description": ["4 jovens tentam desesperadamente acabar uma app para a faculdade"],
    },
    {
        "type": "Movie",
        "title": "O comuna tirano",
        "director": ["Rogério"],
        "cast": ["Rogério"],
        "country": ["Portugal"],
        "release_year": [2024],
        "rating": "Salvem me",
        "duration": "2 semestres",
        "listed_in": ["Comedy", "Dramatic","Terror"],
        "description": ["O comuna tirano dá-nos aulas de estruturas de dados e modelos de computação"],
    }
    ]
    return render_template("shows.html", shows=shows)
