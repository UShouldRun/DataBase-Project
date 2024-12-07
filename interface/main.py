from config import app, initialize_database, populate_database
from views import *

if __name__ == "__main__":
    # initialize_database()
    # populate_database()
    app.run(debug=True)
