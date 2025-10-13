from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = "hero_powers"

    serialize_rules = ("-hero.hero_powers", "-power.hero.powers")

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey("heroes.id"))
    power_id = db.Column(db.Integer, db.ForeignKey("powers.id"))

    hero = db.relationship("Hero", back_populates="hero_powers")
    power = db.relationship("Power", back_populates="hero_powers")

    @validates('strength')
    def validate_strength(self, key, value):
        allowed_values = ["Strong", "Weak", "Average"]

        if value not in allowed_values:
            raise ValueError(f"Strength must be one of {allowed_values}")
        return value

    def __repr__(self):
        return f'<HeroPower {self.id}, {self.strength}>'


class Hero(db.Model,SerializerMixin):
    __tablename__ = "heroes"

    serialize_rules = ("-hero_powers.hero",)

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    hero_powers = db.relationship("HeroPower", back_populates="hero")

    def __repr__(self):
        return f'<Hero {self.id}, {self.name}, {self.super_name}>'



class Power(db.Model, SerializerMixin):
    __tablename__ = "powers"

    serialize_rules = ("-hero_powers.power",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    hero_powers = db.relationship("HeroPower", back_populates="power")

    @validates('description')
    def validate_description(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Description must be present")
        if len(value.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def __repr__(self):
        return f'<Power {self.id}, {self.name}, {self.description}>'