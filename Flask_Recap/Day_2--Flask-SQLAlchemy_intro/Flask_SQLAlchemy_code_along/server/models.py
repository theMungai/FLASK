# models.py

# Flask-SQLAlchemy performs object-relational mapping between the model class and an associated database table.

# Flask-Migrate uses changes to the model class to evolve a database schema.

# Migration is a set of SQL statements that tells a database how to move from an old schema to a new one.

# Defining a model with Flask-SQLAlchemy requires a Python class with four key traits:
#
# Inheritance from the db.Model class.
# A __tablename__ class attribute.
# One or more class attributes assigned to the type db.Column.
# One class attribute specified to be the table's primary key.

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# contains definitions of tables and associated schema constructs
metadata = MetaData()

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# define a model class by inheriting from db.Model
class Pet(db.Model):
    __tablename = "pets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    species = db.Column(db.String(120), nullable=False)