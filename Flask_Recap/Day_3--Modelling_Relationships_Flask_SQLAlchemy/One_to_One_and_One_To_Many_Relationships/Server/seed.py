from faker import Faker
from models import db, Employee, Review, Onboarding
from app import  app
import datetime

with app.app_context():
    Employee.query.delete()
    Review.query.delete()
    Onboarding.query.delete()

    fake = Faker()

    employee1 = Employee(name = fake.name(), hire_date=datetime.datetime(2022, 5, 18))
    employee2 = Employee(name = fake.name(), hire_date=datetime.datetime(2020,8, 12))

    db.session.add_all([employee1,employee2])
    db.session.commit()

    # one-to-many relationship between Employee and Review
    employee1_2023 = Review(year=2023, summary="Great web developer!", employee=employee1)
    employee2_2021 = Review(year=2021, summary="Good coding skills, often late to work", employee=employee2)
    employee2_2022 = Review(year=2022, summary="Strong coding skills, takes long lunches", employee=employee2)
    employee2_2023 = Review(year=2023, summary="Awesome coding skills, dedicated worker", employee=employee2)

    db.session.add_all([employee1_2023, employee2_2021,employee2_2022,employee2_2023])
    db.session.commit()

    # one_to_one relationship between Employee and Onboarding
    employee1_onboarding = Onboarding(orientation=datetime.datetime(2023, 3, 7), employee = employee1)
    employee2_onboarding = Onboarding(orientation=datetime.datetime(2020,1,20,14,31), forms_complete=True,employee=employee2 )

    db.session.add_all([employee1_onboarding, employee2_onboarding])
    db.session.commit()



