from app.database import db
import uuid


class Pokemons(db.Model):
    id = db.Column(db.String(36),
    primary_key = True, 
    default=lambda: str(uuid.uuid4()))

    name = db.Column(db.String(18),
    unique = True,
    nullable = False)

    type1 = db.Column(db.String(10))

    type2 = db.Column(db.String(10))

    hp = db.Column(db.String(8))

    attack = db.Column(db.String(10))

    defense = db.Column(db.String(10))
    
    speed = db.Column(db.String(10))

    special = db.Column(db.String(10))

    moves = db.Column(db.String(200))