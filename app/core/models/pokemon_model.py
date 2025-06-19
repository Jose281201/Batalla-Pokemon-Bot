"""Modelo de datos del pokemon"""

class Pokemon:
    def __init__(self, pokemon: dict):
        self.pokemon = pokemon
        self.name = self.get_pokemon_name()
        self.atributes = self.get_pokemon_atributes()
    
    def get_pokemon_name(self) -> str:
        name = self.pokemon.get["name"]
        return name
    
    def get_pokemon_atributes(self) -> dict:
        return {
            "hp": self.pokemon.get["hp"],
            "attack": self.pokemon.get["attack"],
            "defense": self.pokemon.get["defense"],
            "speed": self.pokemon.get["speed"],
            "special": self.pokemon.get["special"]
        }
    
    def _get_moves_name(self) -> list:
        moves = self.pokemon.get["moves"]
        return moves

    def get_move(self, moves: dict) -> dict:
        pokemon_moves = self._get_moves_name()

        try:        
            for move in pokemon_moves:
                for move in moves:
                    atributes = {
                        "name": move.get["name"],
                        "type": move.get["type"],
                        "power": move.get["power"]
                    }
        except Exception as e:
            print(f"Error al extraer movimientos de {self.name}: {e}")
        
        return atributes