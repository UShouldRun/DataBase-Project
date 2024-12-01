from config import app, initialize_database, populate_database
from views import *

<<<<<<< HEAD
if __name__=="__main__":
    
    initialize_database()
    populate_database()
    app.run(debug=True)
=======
if __name__ == "__main__":
    app.run()
    initialize_database()
>>>>>>> 187ddfe4c40b1d6fafe08d0b0ad8a30cfbf32dd0
