from config import app, db
from database import is_database_initialized, is_database_populated, initialize_database, populate_database
from views import *

if __name__ == "__main__":
    if not is_database_initialized(app, db):
        initialize_database(app, db)
    if not is_database_populated(app, db):
        populate_database(app, db)
    app.run(debug = True)
