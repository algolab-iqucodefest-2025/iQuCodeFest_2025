from player_slot_class import PlayerSlot
from card_generator import generate_card

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = [PlayerSlot() for _ in range(4)]

    def points(self):
        pass

    def play_a_turn(self):
        pass