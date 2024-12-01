from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
from dotenv import load_dotenv
import pandas as pd  
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:3306/DisneyDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def initialize_database():
    with app.app_context():
        try:
            schema_path = os.path.join(os.path.dirname(__file__), '../db/schema.sql')       
            with open(schema_path, 'r') as file:
                sql_script = file.read()
            for statement in sql_script.split(';'):
                if statement.strip():
                    db.session.execute(text(statement))
            
            db.session.commit()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error occurred during database initialization: {e}")
def populate_database():
    with app.app_context():
        try:
            file_path = os.path.join(os.path.dirname(__file__), '../assets/DisneyPlus.xlsx')
            data = pd.read_excel(file_path)

            # Populate Shows table
            shows = data[['title', 'release_year', 'date_added', 'rating', 'description']].copy()
            shows.rename(columns={'release_year': 'year', 'date_added': 'release_date','description':'show_description'}, inplace=True)
            shows.to_sql('Shows', con=db.engine, if_exists='append', index=False)

            # Populate Genre table
            genres = data['listed_in'].str.split(', ').explode().drop_duplicates().reset_index(drop=True)
            genres_df = pd.DataFrame({'genre_name': genres})  # Updated column name
            genres_df.to_sql('Genre', con=db.engine, if_exists='append', index=False)

            # Populate Country table
            countries = data['country'].str.split(', ').explode().drop_duplicates().reset_index(drop=True)
            countries_df = pd.DataFrame({'country_name': countries})  # Updated column name
            countries_df.to_sql('Country', con=db.engine, if_exists='append', index=False)

            # Populate Person table (Director and Cast)
            persons = pd.concat([ 
                data['director'].str.split(', ').explode(), 
                data['cast'].str.split(', ').explode() 
            ]).dropna().drop_duplicates().reset_index(drop=True)
            persons_df = pd.DataFrame({'person_name': persons})  # Updated column name
            persons_df.to_sql('Person', con=db.engine, if_exists='append', index=False)

            # Populate Paper table (mapping people to their roles in shows)
            for index, row in data.iterrows():
                show_id = row['show_id']  # Assuming show_id is available
                directors = row['director'].split(', ') if pd.notnull(row['director']) else []
                cast = row['cast'].split(', ') if pd.notnull(row['cast']) else []
                all_persons = directors + cast
                for person_name in all_persons:
                    # Insert into Paper table (assuming 'role' or 'paper_role' as a generic role for now)
                    role = 'Actor' if person_name in cast else 'Director'  # Or you can use a more detailed mapping
                    person = db.session.execute(
                        text("SELECT person_id FROM Person WHERE person_name = :person_name"),
                        {"person_name": person_name}
                    ).fetchone()
                    if person:
                        person_id = person[0]
                        db.session.execute(
                            text("INSERT INTO Paper (show_id, person_id, paper_role) VALUES (:show_id, :person_id, :role)"),
                            {"show_id": show_id, "person_id": person_id, "role": role}
                        )
            db.session.commit()

            print("Database populated successfully!")

        except Exception as e:
            print(f"Error occurred during data population: {e}")