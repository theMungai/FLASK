from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ('-recipes.user', '-_password_hash')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    bio = db.Column(db.String)
    image_url = db.Column(db.String)

    recipes = db.relationship("Recipe", back_populates="user", cascade="all, delete-orphan")

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Password hash cannot be viewed.")


    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    def __repr__(self):
        return f"<User {self.username}, ID={self.id}>"


class Recipe(db.Model, SerializerMixin):
    __tablename__ = "recipes"

    serialize_rules = ('-user.recipes', 'user',)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    instructions = db.Column(db.String)
    minutes_to_complete = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="recipes")

    @validates('title')
    def validate_title(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Title is required.")
        return value

    @validates("instructions")
    def validate_instructions(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Instructions are required.")

        if len(value.strip()) < 50:
            raise ValueError("Instructions must be at least 50 characters.")
        return value

    def __repr__(self):
        return f"<Recipe {self.title}, ID={self.id}>"


