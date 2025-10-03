from faker import Faker
from random import choice as rc

from models import Zookeeper, Enclosure, Animal, db
from app import app

fake =Faker()

with app.app_context():
    Zookeeper.query.delete()
    Enclosure.query.delete()
    Animal.query.delete()

    zookeepers = []
    for n in range(25):
        zk = Zookeeper(name=fake.name(),birthday=fake.date_between(
            start_date='-70y', end_date='-18y'))
        zookeepers.append(zk)

    db.session.add_all(zookeepers)


    enclosures = []
    environments = ['Desert', 'Pond', 'Ocean', 'Field', 'Trees', 'Cage', 'Cave']

    for n in range(25):
        e = Enclosure(environment=rc(environments), open_to_visitors=rc([True, False]))
        enclosures.append(e)

    db.session.add_all(enclosures)


    animals = []
    species = ['Lion', 'Tiger', 'Bear', 'Hippo', 'Rhino', 'Elephant', 'Ostrich', 'Snake', 'Monkey']

    for n in range(200):
        name = fake.name()
        while name in [a.name for a in animals]:
            name = fake.first_name()
        a = Animal(name=name, species=rc(species))
        a.zookeeper = rc(zookeepers)
        a.enclosure = rc(enclosures)
        animals.append(a)

    db.session.add_all(animals)
    db.session.commit()

