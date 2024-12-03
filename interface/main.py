from config import app, initialize_database, populate_database
from views import *

if __name__=="__main__":
    # use these two functions when you first initialize the database and then its not necessary anymore 
    #initialize_database()
    #populate_database()
    app.run(debug=True)
