from pymysql import OperationalError
from config import db, Flask, SQLAlchemy

from sqlalchemy import text
import pandas as pd  
import os
import repository as repo

def is_database_initialized(app: Flask, db: SQLAlchemy):
    with app.app_context():
        try:
            return 'Shows' in db.inspect(db.get_engine()).get_table_names()
        except OperationalError:
            return False

def is_database_populated(app: Flask, db: SQLAlchemy):
    with app.app_context():
        with db.session.begin():
            result = db.session.execute(
                text("SELECT COUNT(*) FROM Shows")
            ).scalar()
            return result > 0

def initialize_database(app: Flask, db: SQLAlchemy):
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

def preprocess_dataset(data: pd.DataFrame):
        try:
            # Fill missing string fields with default values
            data['title'] = data['title'].fillna('Unknown Title')
            data['rating'] = data['rating'].fillna('Not Rated')
            data['description'] = data['description'].fillna('No Description Available')

            # Fill missing date fields with None (interpreted as NULL in SQL)
            data['date_added'] = data['date_added'].fillna(pd.NaT).replace({pd.NaT: None})

            data['release_year'] = data['release_year'].fillna(0).astype(int) 

            return data
        
        except Exception as e:
            print(f"Error during dataset preprocessing: {e}")
            raise

def populate_database(app: Flask, db: SQLAlchemy):
    with app.app_context():
        try:
            file_path = os.path.join(os.path.dirname(__file__), '../assets/DisneyPlus.xlsx')
            data = preprocess_dataset(pd.read_excel(file_path))

            for _, row in data.iterrows():

                rating = row["rating"]

                show_id: int = repo.call_create_show(
                    row['title'],
                    int(row['release_year']),
                    row['date_added'],
                    repo.call_create_rating(rating),
                    row['description']
                )

                genres: list = [genre.strip() for genre in row['listed_in'].split(', ')]
                for genre in genres:
                    repo.call_create_listed_in(
                        show_id  = show_id,
                        genre_id = repo.call_create_genre(genre)
                    )

                countries: list = [country.strip() for country in row['country'].split(', ')] if pd.notnull(row['country']) else []
                for country in countries:
                    repo.call_create_streaming_on(
                        show_id    = show_id,
                        country_id = repo.call_create_country(country)
                    )

                persons: set = set()
                if pd.notnull(row['director']):
                    persons.update(row['director'].split(', '))
                if pd.notnull(row['cast']):
                    persons.update(row['cast'].split(', '))
                for person in persons: 
                    repo.call_create_paper(
                        show_id   = show_id,
                        person_id = repo.call_create_person(person),
                        role      = 'Director' if pd.notnull(row['director']) and person in row['director'] else 'Actor'
                    )
                
                repo.call_create_duration(
                    show_id       = show_id,
                    category_id   = repo.call_create_category(row['type']),
                    duration_time = int(row["duration"].split()[0]),
                    unit_id       = repo.call_create_unit(row["duration"].split()[1])
                )

            db.session.commit()
            print("Database populated successfully!")

        except Exception as e:
            print(f"Error occurred during data population: {e}")
