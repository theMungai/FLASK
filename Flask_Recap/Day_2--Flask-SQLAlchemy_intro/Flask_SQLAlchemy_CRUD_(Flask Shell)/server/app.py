from flask import Flask
from flask_migrate import Migrate

from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

migrate = Migrate(app, db)

if __name__ == "__main__":
    app.run(port=5555, debug=True)

# Persisting an object to the database requires a database session.
# Database session is an object that manages database transaction.

# TRANSACTION  -> is a sequence of SQL statements that are processed as an atomic unit.

# use get() if you want to access a certain row by its primary key.

# importing func from sqlalchemy, gives us access to common SQL operations through functions like sum() and count()

# func.count()

# When calling these functions, we invoke QUERY function on the session, rather than accessing the query attribute inherited from db.Model




