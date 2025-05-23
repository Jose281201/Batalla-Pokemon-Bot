from app.database import db
import uuid


class Pokemons(db.Model):
    id = db.Column(db.String(36),
    primary_key = True, 
    default=lambda: str(uuid.uuid4()))

    name = db.Column(db.String(18),
    unique = True,
    nullable = False)