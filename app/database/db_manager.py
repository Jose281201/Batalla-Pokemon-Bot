from typing import Union, List

from database.db_config import db
from database.pokemon_models import Pokemons
from database.player_models import Player

class DatabaseManager:
    def __init__(self):
        self.session = db.session

    def _commit_or_rollback(self):
        """Método de commit"""
        try:
            self.session.commit()
            return True
        
        except Exception as e:
            self.session.rollback()
            return str(e)
    
    def create_player(self, player_name: str)-> Union[bool, str]:
        """Método para guardar un player en la base de datos"""

        player = Player(player_name)
        self.session.add(player)

        return self._commit_or_rollback()
    
    def delete_player(self, player_id: str) -> Union[bool, str]:
        """Método para eliminar player de la base de datos"""

        player = Player.query.filter_by(id=player_id)
        self.session.delete(player)

        return self._commit_or_rollback()
        