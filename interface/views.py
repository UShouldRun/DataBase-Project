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
        genres = call_genres(title.strip) if title else call_genres_all()
    )

@app.route("/countries", methods=["GET"])
def show_countries():
    title = request.args.get("title")
    return render_template(
        "countries.html",
        countries = call_countries(title.strip) if title else call_countries_all()
    )

@app.route("/titles", methods=["GET"])
def show_titles():
    val = request.args.get("val") 
    
    titles = []
    if val == "genre":
        genre = request.args.get("genre") 
        all_titles = call_titles_by_genre()
        print(all_titles)
        for item in all_titles:
            if item["genre"].lower() == genre.lower():
                titles = item["titles"].split(", ")  
                break
    elif val == "countries":
        countries = request.args.get("countries") 
        all_titles = call_titles_by_countries()  
        for item in all_titles:
            if item["countries"].lower() == countries.lower():
                titles = item["titles"].split(", ")  
                break
    else:
        titles = call_titles_all() 

    return render_template(
        "titles.html",
        titles = titles
    )
