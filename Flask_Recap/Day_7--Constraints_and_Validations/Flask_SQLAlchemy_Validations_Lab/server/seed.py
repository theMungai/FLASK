from faker import Faker

from models import db, Post, Author
from app import app

fake = Faker()

with app.app_context():
    Post.query.delete()
    Author.query.delete()

    authors = []
    for i in range(25):
        author = Author(
            name = fake.name(),
            phone_number = '1324543333'
        )
        authors.append(author)

    db.session.add_all(authors)

    posts = []
    for i in range(25):
        post = Post(
            title = "Secret banana",
            content = "This is the content Secret" * 50,
            category = "Fiction",
            summary = "Summary Secret"
        )
        posts.append(post)

    db.session.add_all(posts)
    db.session.commit()


