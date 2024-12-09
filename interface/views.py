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
    filter_applied = request.args.get("filter")=="true"
    actors=[]
    if title:
        actors = [{"name": actor} for actor in call_actors(title.strip())]
    elif filter_applied:
        actors=call_top_actors()
    else:
        actors = [{"name": actor} for actor in call_actors_all()]

    return render_template(
        "actors.html",
        actors =  actors
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
    shows = call_show_all_dataset()
    return render_template("shows.html", shows=shows)

@app.route("/genres", methods=["GET"])
def show_genres():
    title = request.args.get("title")

    return render_template(
        "genres.html",
        genres = call_genres(title.strip()) if title else call_genres_all()
    )
@app.route("/top_actors_by_genre", methods=["GET"])
def top_actors_by_genre():
    try:
        top_actors = call_top_actor_by_genre()
        return render_template(
            "top_actors_by_genre.html",
            actors_by_genre=top_actors
        )
    except Exception as e:
        print(f"Error fetching top actors by genre: {e}")
        return "An error occurred.", 500
    
@app.route("/top_actors_by_country", methods=["GET"])
def top_actors_by_country():
    try:
        top_actors = call_top_actor_by_country()
        return render_template(
            "top_actors_by_country.html",
            actors_by_country=top_actors
        )
    except Exception as e:
        print(f"Error fetching top actors by genre: {e}")
        return "An error occurred.", 500
    
@app.route("/genre_statistics", methods=["GET"])
def genre_statistics():
    try:
        genres_n_percentages = call_genre_percentage()
        return render_template(
            "genre_percentage.html",
            genres_n_percentages=genres_n_percentages
        )
    except Exception as e:
        print(f"Error fetching top actors by genre: {e}")
        return "An error occurred.", 500
    
@app.route("/country_statistics", methods=["GET"])
def country_statistics():
    try:
        countries_n_percentages = call_country_percentage()
        return render_template(
            "country_percentage.html",
            countries_n_percentages=countries_n_percentages
        )
    except Exception as e:
        print(f"Error fetching top actors by genre: {e}")
        return "An error occurred.", 500


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
    elif val == "filter_time":
        category_type = request.args.get("category")
        min_time = request.args.get("min_time")
        max_time = request.args.get("max_time")
        rating = request.args.get("rating")

        min_time = int(min_time) if min_time and min_time.isdigit() else 0
        max_time = int(max_time) if max_time and max_time.isdigit() else 99999

        if category_type == "All":
            titles = call_titles_all()
        else:
            titles = call_show_within_restrictions(category_type, min_time, max_time)

        if rating and rating!="All":
            if rating == "Not":  # Handle "Not Rated" (i give up)
                titles = [title for title in titles if title["rating"] == "Not Rated"]
            else:
                titles = [title for title in titles if title["rating"] == rating]
    else:
        titles = call_titles_all()
        
    return render_template(
        "titles.html",
        titles = titles,
        ratings= call_ratings_all()
    )
@app.route("/search_titles", methods=["GET"])
def search_titles():
    query : str = request.args.get("query") 
    titles=call_titles_by_letters(query)
    return render_template(
        "titles.html",
        titles = titles,
        ratings= call_ratings_all()
    )
@app.route("/year_statistics", methods=["GET"])
def titles_over_time():
    data = call_titles_yearly_count() 
    return render_template(
        "year_statistics.html",
        data = data,
    )