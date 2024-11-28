from config import app, initialize_database
from views import *

if __name__=="__main__":
    app.run()
    initialize_database()