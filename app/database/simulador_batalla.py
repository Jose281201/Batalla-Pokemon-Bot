import random
import time
import copy


#Clase que representa un Pokemon con todos sus atributos y movimientos
class Pokemon:
    def __init__(self,name,type1,type2,hp,attack,defense,speed,moves):
        # Atributos básicos del Pokémon
        self.name = name          # Nombre del Pokémon
        self.type1 = type1        # Tipo primario (fuego, agua, planta, etc.)
        self.type2 = type2        # Tipo secundario (puede ser None)
        self.hp_max = int(hp)     # Puntos de salud máximos
        self.hp_current = int(hp) # Puntos de salud actuales
        self.attack = int(attack) # Puntos de ataque
        self.defense = int(defense) # Puntos de defensa
        self.speed = int(speed)   # Velocidad (determina orden de ataque)
        self.moves = moves        # Lista de movimientos: (nombre, poder, tipo, precisión)
    
    # Método para que el Pokémon realice un ataque
    def attack_move(self, opponent, move_idx):
        # Verificar si el movimiento existe
        if move_idx >= len(self.moves):
            print(f"{self.name} doesn't know that move!")
            return False
        
        # Extraer detalles del movimiento
        move_name, power, move_type, accuracy = self.moves[move_idx]
        print(f"{self.name} uses {move_name}!")
        
        # Verificar si el ataque acierta
        if random.randint(1, 100) > accuracy:
            print("The attack missed!")
            return False
        
        # Calcular efectividad del movimiento contra los tipos del oponente
        effectiveness = self.calculate_effectiveness(move_type, opponent.type1, opponent.type2)
        
        # Fórmula simplificada de daño
        damage = max(1, (self.attack + power - opponent.defense) // 2)
        total_damage = int(damage * effectiveness)
        
        # Aplicar el daño al oponente
        opponent.hp_current -= total_damage
        opponent.hp_current = max(0, opponent.hp_current)
        
        # Mostrar resultados del ataque
        print(f"It does {total_damage} damage!")
        if effectiveness > 1:
            print("It's super effective!")
        elif effectiveness < 1:
            print("It's not very effective...")
        
        # Devolver si el oponente fue debilitado
        return opponent.hp_current <= 0
    
    # Método para calcular la efectividad de un tipo contra otro
    def calculate_effectiveness(self, move_type, opponent_type1, opponent_type2=None):
        # Tabla de efectividad de tipos (simplificada)
        effectiveness_chart = {
            'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'electric': 1, 'ground': 1, 'flying': 1, 'dragon': 0.5},
            'water': {'fire': 2, 'water': 0.5, 'grass': 0.5, 'electric': 1, 'ground': 2, 'flying': 1, 'dragon': 0.5},
            'grass': {'fire': 0.5, 'water': 2, 'grass': 0.5, 'electric': 1, 'ground': 2, 'flying': 0.5, 'dragon': 0.5},
            'electric': {'fire': 1, 'water': 2, 'grass': 0.5, 'electric': 0.5, 'ground': 0, 'flying': 2, 'dragon': 0.5},
            'ground': {'fire': 2, 'water': 1, 'grass': 0.5, 'electric': 2, 'ground': 1, 'flying': 0, 'dragon': 1},
            'flying': {'fire': 1, 'water': 1, 'grass': 2, 'electric': 0.5, 'ground': 1, 'flying': 1, 'dragon': 1},
            'dragon': {'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'ground': 1, 'flying': 1, 'dragon': 2},
            'normal': {'fire': 1, 'water': 1, 'grass': 1, 'electric': 1, 'ground': 1, 'flying': 1, 'dragon': 1}
        }
        
        # Calcular efectividad contra el tipo primario
        effectiveness = effectiveness_chart.get(move_type, {}).get(opponent_type1, 1)
        
        # Calcular efectividad contra el tipo secundario (si existe)
        if opponent_type2:
            effectiveness *= effectiveness_chart.get(move_type, {}).get(opponent_type2, 1)

        
        return effectiveness
    
    # Método para verificar si el Pokémon está debilitado
    def is_fainted(self):
        return self.hp_current <= 0
    
    # Representación en string del Pokémon
    def str(self):
        return f"{self.name}: HP {self.hp_current}/{self.hp_max}"

# Clase que representa un Entrenador Pokémon
class Trainer:
    def init(self, name, pokemon_team):
        self.name = name                # Nombre del entrenador
        self.pokemon_team = pokemon_team # Lista de Pokémon en el equipo
        self.current_pokemon = 0       # Índice del Pokémon actual
    
    # Obtener el Pokémon actualmente en batalla
    def get_active_pokemon(self):
        if self.current_pokemon < len(self.pokemon_team):
            return self.pokemon_team[self.current_pokemon]
        return None
    
    # Método para cambiar de Pokémon
    def switch_pokemon(self, new_idx):
        # Verificar que el nuevo Pokémon existe y no está debilitado
        if new_idx < len(self.pokemon_team) and not self.pokemon_team[new_idx].is_fainted():
            if new_idx != self.current_pokemon:
                print(f"{self.name} withdraws {self.get_active_pokemon().name}!")
                self.current_pokemon = new_idx
                print(f"{self.name} sends out {self.get_active_pokemon().name}!")
                return True
        return False
    
    # Verificar si todos los Pokémon del equipo están debilitados
    def all_fainted(self):
        return all(p.is_fainted() for p in self.pokemon_team)
    
    # Representación en string del entrenador
    def str(self):
        return f"{self.name}'s Team: {', '.join(f'{p.name} ({p.hp_current}/{p.hp_max})' for p in self.pokemon_team)}"

# Función para mostrar el menú de movimientos de un Pokémon
def show_move_menu(pokemon):
    print(f"{pokemon.name}'s moves:")
    # Mostrar todos los movimientos disponibles con sus stats
    for i, (name, power, move_type, accuracy) in enumerate(pokemon.moves):
        print(f"{i+1}. {name} ({move_type}, power: {power}, accuracy: {accuracy}%)")

# Función para determinar qué Pokémon ataca primero (basado en velocidad)
def determine_first_turn(pokemon1, pokemon2):
    if pokemon1.speed > pokemon2.speed:
        return 1
    elif pokemon2.speed > pokemon1.speed:
        return 2
    else:
        return random.randint(1, 2)  # En caso de empate, aleatorio

# Función principal que maneja la batalla entre dos entrenadores
def pokemon_battle(trainer1, trainer2):
    print(f"Pokémon battle between {trainer1.name} and {trainer2.name} begins!")
    
    turn = 0
    # Bucle principal de la batalla (por turnos)
    while not trainer1.all_fainted() and not trainer2.all_fainted():
        turn += 1
        print(f"\n--- Turn {turn} ---")
        
        # Mostrar estado actual de los Pokémon en batalla
        print(f"\n{trainer1.name}: {trainer1.get_active_pokemon()}")
        print(f"{trainer2.name}: {trainer2.get_active_pokemon()}")
        
        # Determinar orden de ataque (en el primer turno por velocidad)
        if turn == 1:
            first_turn = determine_first_turn(trainer1.get_active_pokemon(), trainer2.get_active_pokemon())
            if first_turn == 1:
                print(f"\n{trainer1.get_active_pokemon().name} is faster and moves first!")
            else:
                print(f"\n{trainer2.get_active_pokemon().name} is faster and moves first!")
        else:
            # En turnos siguientes alterna el orden
            first_turn = 2 if (turn % 2 == 0) else 1
        
        # Ejecutar los turnos en el orden determinado
        for trainer in [trainer1 if first_turn == 1 else trainer2, 
                       trainer2 if first_turn == 1 else trainer1]:
            
            # Saltar si el Pokémon actual está debilitado
            if trainer.get_active_pokemon().is_fainted():
                continue
                
            # Mostrar menú de movimientos
            print(f"\n{trainer.name}'s turn:")
            pokemon = trainer.get_active_pokemon()
            show_move_menu(pokemon)
            
            # Seleccionar movimiento aleatorio (en versión real sería input del usuario)
            move_idx = random.randint(0, len(pokemon.moves)-1)
            
            # Determinar oponente
            opponent = trainer2 if trainer == trainer1 else trainer1
            
            # Atacar si el oponente tiene Pokémon activo
            if not opponent.get_active_pokemon().is_fainted():
                opponent_fainted = pokemon.attack_move(opponent.get_active_pokemon(), move_idx)
                
                # Manejar Pokémon debilitado
                if opponent_fainted:
                    print(f"{opponent.get_active_pokemon().name} fainted!")
                    # Buscar siguiente Pokémon disponible
                    for i in range(len(opponent.pokemon_team)):
                        if not opponent.pokemon_team[i].is_fainted():
                            opponent.current_pokemon = i
                            print(f"{opponent.name} sends out {opponent.get_active_pokemon().name}!")
                            break
            
            # Terminar batalla si el oponente no tiene Pokémon disponibles
            if opponent.all_fainted():
                break
            
            # Pequeña pausa entre turnos
            time.sleep(1)
    
    # Mostrar resultado final de la batalla
    if trainer1.all_fainted():
        print(f"\n{trainer2.name} wins the battle!")
    else:
        print(f"\n{trainer1.name} wins the battle!")

# Ejemplo de creación de Pokémon con sus stats
charizard = Pokemon("Charizard", "fire", "flying", 180, 120, 85, 100, 
                   [("Flamethrower", 90, "fire", 85), ("Dragon Claw", 80, "dragon", 100), 
                    ("Aerial Ace", 75, "flying", 95), ("Earthquake", 100, "ground", 100)])

blastoise = Pokemon("Blastoise", "water", None, 190, 85, 130, 78,
                   [("Hydro Pump", 110, "water", 80), ("Skull Bash", 80, "normal", 90),
                    ("Water Gun", 40, "water", 100), ("Rapid Spin", 50, "normal", 100)])

# Creación de equipos y entrenadores
team1 = [charizard, blastoise]  # Equipo del primer entrenador
team2 = [copy.deepcopy(blastoise),copy.deepcopy(charizard)]  # Equipo del segundo entrenador

trainer1 = Trainer("Ash", team1)
trainer2 = Trainer("Gary", team2)

# Iniciar la batalla
pokemon_battle(trainer1, trainer2)