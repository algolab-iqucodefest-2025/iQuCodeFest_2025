import pygame
from card_generator import generate_card


class QDutch:
    def __init__(self, nb_players):
        self.players = list()
        self.dutch_called = False
        self.dutch_turn = None
        self.nb_players = nb_players

    def init_game(self):
        pass

    def end_game(self):
        pass

    def player_turn(self, player_no, turn_no):
        if self.dutch_called:
            if turn_no == self.dutch_turn:
                self.end_game()
                return  
        Dutch = self.get_player_dutch(player_no)
        if Dutch:
            self.dutch_called = True
            self.dutch_turn = turn_no + 1
            return
        else:
            card1 = generate_card()
            card2 = generate_card()

            selected_card = self.get_player_choice(player_no, card1, card2)

            if selected_card.type == "Operator":
                selected_slot, tgt_player = self.get_player_slot("Operator")
                self.players[tgt_player].apply_operator(selected_card.data, selected_slot)
            elif selected_card.type == "State":
                selected_slot, tgt_player = self.get_player_slot("State", player_no)
                self.players[tgt_player].set_state(selected_card.data, selected_slot)
            elif selected_card.type == "Measurement":
                selected_slot, tgt_player = self.get_player_slot("Measurement")
                self.players[tgt_player].measure(selected_card.data, selected_slot)
            else:
                pass

