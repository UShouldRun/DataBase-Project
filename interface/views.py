from main import app
from flask import render_template, request 
from repository import  *

# routes
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/actors", methods=["GET"])
def show_all_actors():
    title = request.args.get("title")
    return render_template(
        "actors.html",
        actors = call_actors(title.strip()) if title else call_actors_all()
    )

@app.route("/directors")
def show_all_directors():
    title = request.args.get("title")
    return render_template(
        "directors.html",
        directors = call_directors(title.strip()) if title else call_directors_all()
    )

@app.route("/shows")
def show_all_shows():
    shows = [
        {
            "type": "Movie",
            "title": "As aventuras da cadeira de base de dados",
            "directors": ["João", "Henrique"],
            "cast": ["João", "Henrique", "Rossi", "Alex"],
            "countries": ["Portugal"],
            "release_year": [2024],
            "rating": "TOP G",
            "duration": "1 mês",
            "listed_in": ["Comedy", "Dramatic"],
            "description": ["4 jovens tentam desesperadamente acabar uma app para a faculdade"],
        },
    ]
    return render_template("shows.html", shows=shows)

@app.route("/genres", methods=["GET"])
def show_genres():
    title = request.args.get("title")
    return render_template(
        "genres.html",
        genres = call_genres(title.strip()) if title else call_genres_all()
    )

@app.route("/countries", methods=["GET"])
def show_countries():
    title = request.args.get("title")
    return render_template(
        "countries.html",
        countries = call_countries(title.strip()) if title else call_countries_all()
    )

@app.route("/titles", methods=["GET"])
def show_titles():
    val = request.args.get("val") 
    
    titles = []
    if val == "genre":
        genre = request.args.get("genre") 
        if genre:
            titles = call_titles_by_genre(genre)
    elif val == "country":
        country = request.args.get("country") 
        if country:
            titles = call_titles_by_country(country)
    elif val=="filter":
        category_type = request.args.get("category")
        if category_type=="All":
                return render_template(
                "titles.html",
                titles = call_titles_all()
            )
        min_time = request.args.get("min_time")
        max_time = request.args.get("max_time")

        min_time = int(min_time) if min_time and min_time.isdigit() else 0
        max_time = int(max_time) if max_time and max_time.isdigit() else 99999

        titles=call_show_within_restrictions(category_type,min_time, max_time)
    else:
        titles = call_titles_all() 

    return render_template(
        "titles.html",
        titles = titles
    )
