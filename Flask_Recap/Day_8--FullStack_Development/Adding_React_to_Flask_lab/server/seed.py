from faker import Faker
from random import choice as rc

from models import Movie, db
from app import app

fake = Faker()

def seed():
    Movie.query.delete()

    movies = []
    for i in range(50):
        movie = Movie(
            title= fake.sentence(nb_words=4).title()
        )
        movies.append(movie)

    db.session.add_all(movies)
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        seed()