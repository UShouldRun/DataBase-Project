from main import app
from flask import render_template, request 
from repository import  *
# routes
@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/actors")
def show_all_actors():
    all_actors = call_show_all_actors()

    cast_filter = request.args.get('cast')

    # Filter actors if a cast filter is provided
    if cast_filter:
        cast_list = cast_filter.split(',') 
        actors = [actor for actor in all_actors if actor["Name"] in cast_list]
    else:
        actors = all_actors 
    return render_template("actors.html", actors=actors)

@app.route("/directors")
def show_all_directors():
    all_directors = call_show_all_directors()

    cast_filter = request.args.get('cast')

    # Filter cirectors if a cast filter is provided
    if cast_filter:
        cast_list = cast_filter.split(',') 
        directors = [director for director in all_directors if director["Name"] in cast_list]
    else:
        directors = all_directors
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
