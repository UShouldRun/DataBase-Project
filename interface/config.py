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

def preprocess_dataset(data):
        try:
            # Fill missing string fields with default values
            data['title'] = data['title'].fillna('Unknown Title')
            data['rating'] = data['rating'].fillna('Not Rated')
            data['description'] = data['description'].fillna('No Description Available')

            # Fill missing date fields with None (interpreted as NULL in SQL)
            data['date_added'] = data['date_added'].fillna(pd.NaT).replace({pd.NaT: None})
            # Porque os anos no dataset veem como 2,016 em vez de 2016 tipo wtf stor 
            data['release_year'] = data['release_year'].fillna(0).astype(int) *1000
            data['release_year'] = data['release_year'].astype(int)

            return data
        
        except Exception as e:
            print(f"Error during dataset preprocessing: {e}")
            raise

        

def populate_database():
    with app.app_context():
        try:
            file_path = os.path.join(os.path.dirname(__file__), '../assets/DisneyPlus.xlsx')
            data = pd.read_excel(file_path)

            data = preprocess_dataset(data)

            for _, row in data.iterrows():
                db.session.execute( 
                    text("""CALL create_show(:title, :release_year, :release_date, :rating, :show_description, @show_id)"""),
                    {
                        'title': row['title'],
                        'release_year': int(row['release_year']),
                        'release_date': row['date_added'],
                        'rating': row['rating'],
                        'show_description': row['description']
                    }
                )
                result= db.session.execute(text("""SELECT @show_id"""))
                show_id = result.fetchone()[0]
                genres = [genre.strip() for genre in row['listed_in'].split(', ')]
                for genre in genres:
                    db.session.execute(
                        text("""CALL create_genre(:genre_name, @genre_id)"""), {'genre_name': genre}
                    )
                    result=db.session.execute(text("""SELECT @genre_id"""))
                    genre_id = result.fetchone()[0]
                    db.session.execute(
                        text("""CALL create_listed_in(:show_id, :genre_id)"""), {
                            'show_id': show_id,
                            'genre_id': genre_id
                        }
                    )
                countries = [country.strip() for country in row['country'].split(', ')] if pd.notnull(row['country']) else []
                for country in countries:
                    db.session.execute(
                        text("""CALL create_country(:country_name, @country_id)"""),{
                            'country_name':country
                        }
                    )
                    result= db.session.execute(text("""SELECT @country_id"""))
                    country_id = result.fetchone()[0]
                    db.session.execute(
                        text("""CALL create_streaming_on(:show_id,:country_id)"""),{
                            'show_id': show_id,
                            'country_id': country_id
                        }
                    )
                persons = []
                if pd.notnull(row['director']):
                    persons.extend(row['director'].split(', '))
                if pd.notnull(row['cast']):
                    persons.extend(row['cast'].split(', '))
                for person in persons:
                    db.session.execute(
                        text("""CALL create_person(:person_name, @person_id)"""), {'person_name': person}
                    )
                    result=db.session.execute(text("""SELECT @person_id"""))
                    person_id = result.fetchone()[0]
                    role='Director' if pd.notnull(row['director']) and person in row['director'] else 'Actor'
                    db.session.execute(
                        text("""CALL create_paper(:show_id,:person_id,:paper_role)"""),{
                            'show_id': show_id,
                            'person_id': person_id,
                            'paper_role': role
                        }
                    )
                
                db.session.execute(
                    text("""CALL create_category(:category_type, @category_id)"""),{
                        'category_type':row['type']
                    }
                )
                result= db.session.execute(text("""SELECT @category_id"""))
                category_id = result.fetchone()[0]
                db.session.execute(
                    text("""CALL create_duration(:show_id, :category_id, :duration_time)"""),{
                        'show_id': show_id,
                        'category_id': category_id,
                        'duration_time': row['duration']
                        
                    }
                )

            db.session.commit()
            print("Database populated successfully!")

        except Exception as e:
            print(f"Error occurred during data population: {e}")