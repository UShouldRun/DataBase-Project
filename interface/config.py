from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

# Change password and username based on your connection details
# root and admin are default and should (ARE) be kept private in an .env file
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:3306/DisneyDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def initialize_database():
    with app.app_context():
        # Execute schema file to start all tables
        with open('schema.sql', 'r') as file:
            sql_script = file.read()
        db.session.execute(sql_script)
        db.session.commit()
        print("Database initialized successfully!")


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
