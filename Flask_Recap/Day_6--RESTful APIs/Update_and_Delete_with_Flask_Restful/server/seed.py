from faker import Faker

from models import Newsletter, db
from app import app

with app.app_context():
    Newsletter.query.delete()

    fake = Faker()
    newsletters = []
    for i in range(50):
        newsletter = Newsletter(
            title = fake.text(max_nb_chars=20),
            body = fake.paragraph(nb_sentences=5)
        )
        newsletters.append(newsletter)

    db.session.add_all(newsletters)
    db.session.commit()