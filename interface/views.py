from main import app
from flask import render_template

# routes
@app.route("/")
def homepage():
    return render_template("homepage.html", author="João")

@app.route("/fpage")
def fpage():
    return "This is the first page"