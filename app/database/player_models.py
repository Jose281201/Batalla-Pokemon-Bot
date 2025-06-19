from app.database import db
import uuid

class Player(db.Model):
    id = db.Column(db.String(36), primary_key = True, default=lambda: str(uuid.uuid4()))
    playername = db.Column(db.String(36), nullable=False)