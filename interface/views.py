from main import app
from flask import render_template, request 
from repository import  *
# routes
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/actors",methods=["GET"])
def show_all_actors():
    title = request.args.get("title")
    if title:
        actors=call_show_actors(title.strip())
    else:
        actors=call_show_all_actors()
    
    return render_template("actors.html", actors=actors)

@app.route("/directors")
def show_all_directors():
    title = request.args.get("title")
    if title:
        directors=call_show_directors(title.strip())
    else:
        directors=call_show_all_directors()
    
    return render_template("directors.html", directors=directors)

@app.route("/shows")
def show_all_shows():
    shows = [
    {
        "type": "Movie",
        "title": "As aventuras da cadeira de base de dados",
        "directors": ["João", "Henrique"],
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
        "directors": ["Rogério"],
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

@app.route("/genres", methods=["GET"])
def show_genres():
    title = request.args.get("title")

    if title:
        genres = call_show_genre(title.strip())
    else:
        genres = call_show_all_genres()

    return render_template("genres.html", genres=genres)

@app.route("/countries", methods=["GET"])
def show_countries():
    title = request.args.get("title")

    if title:
        countries = call_show_countries(title.strip())
    else:
        countries = call_show_all_countries()

    return render_template("countries.html", countries=countries)
