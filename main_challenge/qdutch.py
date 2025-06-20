import pygame
import sys

# --- Initialization ---
pygame.init()

# --- Constants ---
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 60, 90
CARD_SPACING = 20
BG_COLOR = (34, 139, 34)      # Green table
BG_CARD_COLOR = (34, 100, 34)  # Light green for cards
CARD_COLOR = (255, 255, 255)
TEXT_COLOR = (0, 0, 0)

# --- Pygame Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top View Table Game")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

# --- Data Classes ---
class Slot:
    def __init__(self, state):
        self.state = state

class Player:
    def __init__(self, name, states):
        self.name = name
        self.hand = [Slot(s) for s in states]

# --- Test Players ---
players = [
    Player("Bottom", [0, 6, 0, 0]),
    Player("Top",    [4, 3, 0, 0]),
    Player("Left",   [2, 5, 0, 0]),
    Player("Right",  [7, 4, 0, 0]),
]

# --- Global Card Buttons ---
card_buttons = []

center_buttons = []


# --- Drawing Functions ---
def draw_card(x, y, text, rotation, player, card_index):
    # Create a transparent card surface
    card_surf = pygame.Surface((CARD_WIDTH, CARD_HEIGHT), pygame.SRCALPHA)
    card_surf.fill(CARD_COLOR)
    pygame.draw.rect(card_surf, TEXT_COLOR, card_surf.get_rect(), 2)

    # Render text onto the card surface
    if text:
        label = font.render(text, True, TEXT_COLOR)
        label_rect = label.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2))
        card_surf.blit(label, label_rect)

    # Rotate entire surface (card + text)
    rotated_surf = pygame.transform.rotate(card_surf, rotation)
    rect = rotated_surf.get_rect(center=(x, y))

    # Draw to main screen
    screen.blit(rotated_surf, rect.topleft)

    # Store clickable area
    card_buttons.append((rect, player, card_index))


def draw_table_with_states(players, show_states):
    screen.fill(BG_COLOR)
    card_buttons.clear()

    def get_card_text(player_index, card_index):
        if show_states and card_index < 2:
            return str(players[player_index].hand[card_index].state)
        return ""

    # Player 1
    for i in range(4):
        x = WIDTH // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        y = HEIGHT - CARD_HEIGHT - 40
        draw_card(x, y, get_card_text(0, i), 0, 0, i)

    # Player 3
    for i in range(4):
        x = WIDTH // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        y = 40 + CARD_HEIGHT // 2
        draw_card(x, y, get_card_text(1, i), 180, 2, i)

    # Player 2
    for i in range(4):
        x = 40 + CARD_HEIGHT // 2
        y = HEIGHT // 2 - 1.5 * (CARD_WIDTH + CARD_SPACING) + i * (CARD_WIDTH + CARD_SPACING)
        draw_card(x, y, get_card_text(2, i), 90, 1, i)

    # Right (index 3) - reversed
    for i in range(4):
        x = WIDTH - 40 - CARD_HEIGHT // 2
        y = HEIGHT // 2 + 1.5 * (CARD_WIDTH + CARD_SPACING) - i * (CARD_WIDTH + CARD_SPACING)
        draw_card(x, y, get_card_text(3, i), 270, 3, i)

def draw_center_elements():
    center_buttons.clear()

    center_x, center_y = WIDTH // 2, HEIGHT // 2

    # Dutch button
    dutch_rect = pygame.Rect(center_x - 160, center_y - 25, 100, 50)
    pygame.draw.rect(screen, (255, 125, 25), dutch_rect)
    dutch_text = font.render("Dutch", True, TEXT_COLOR)
    screen.blit(dutch_text, dutch_text.get_rect(center=dutch_rect.center))
    center_buttons.append((dutch_rect, "Dutch"))

    # Deck
    deck_rect = pygame.Rect(center_x - CARD_WIDTH // 2, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, (180, 180, 180), deck_rect)
    deck_text = font.render("Deck", True, TEXT_COLOR)
    screen.blit(deck_text, deck_text.get_rect(center=deck_rect.center))
    center_buttons.append((deck_rect, "deck"))

    # Cards (no text on these two)
    card1_rect = pygame.Rect(center_x + 70, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, BG_CARD_COLOR, card1_rect)
    center_buttons.append((card1_rect, "card 1"))

    card2_rect = pygame.Rect(center_x + 140, center_y - CARD_HEIGHT // 2, CARD_WIDTH, CARD_HEIGHT)
    pygame.draw.rect(screen, BG_CARD_COLOR, card2_rect)
    center_buttons.append((card2_rect, "card 2"))

def draw_player_labels(show_states, current_player_no):
    label_font = pygame.font.SysFont(None, 28)

    player_positions = {
        0: (WIDTH // 2, HEIGHT - 50),              # Bottom
        1: (175, HEIGHT // 2 - 25),                      # Left
        2: (WIDTH // 2, 20),                       # Top
        3: (WIDTH - 125, HEIGHT // 2 - 25),              # Right
    }

    for i in range(4):
        if show_states or i == current_player_no:
            label = label_font.render(f"Player {i + 1}", True, (255, 255, 255))
            pos = player_positions[i]

            # Center horizontally or vertically based on side
            if i == 0 or i == 2:  # Bottom or top
                label_rect = label.get_rect(center=pos)
            else:  # Left or right
                label_rect = label.get_rect(center=pos)
                label = pygame.transform.rotate(label, 270/i)

            screen.blit(label, label_rect)

def draw_start_message():
    msg_font = pygame.font.SysFont(None, 36)
    message = "Press Enter to Start"
    text = msg_font.render(message, True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, rect)

# --- Main Game Loop ---
def main():
    turn_no = 0
    player_no = 0
    show_states = True              # Only True at game start
    showed_initial_states = False  # Track if states were shown once
    dutch_call = False
    player_dutch = None
    dutch_turn = None
    drew_from_deck = False
    selected_card = None
    can_click_player_cards = False
    player_done = False

    while True:
        # End condition if Dutch was called on a previous turn
        if dutch_turn is not None and turn_no == dutch_turn + 1 and player_no == player_dutch:
            print("The game has ended.")
            break

        draw_table_with_states(players, show_states)
        if not show_states:
            draw_center_elements()
        else:
            draw_start_message()  # Show message only when states are shown

        draw_player_labels(show_states, player_no)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not showed_initial_states:
                    show_states = False
                    showed_initial_states = True  # Only allow this once

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not show_states:
                    mx, my = pygame.mouse.get_pos()

                    # Center buttons
                    for rect, label in center_buttons:
                        if rect.collidepoint((mx, my)):

                            # Dutch button only if no one has called it yet
                            if not drew_from_deck and not dutch_call:
                                if label == "Dutch":
                                    print("Dutch button clicked")
                                    dutch_call = True
                                    player_dutch = player_no
                                    dutch_turn = turn_no
                                    player_done = True
                                    break  # End this player's turn

                            # Allow deck click if Dutch was not chosen
                            if not drew_from_deck and label == "deck":
                                print("Deck clicked")
                                drew_from_deck = True

                            # Then choose card 1 or 2
                            elif drew_from_deck and not selected_card:
                                if label == "card 1":
                                    print("Card 1 clicked")
                                    selected_card = "card 1"
                                    can_click_player_cards = True
                                elif label == "card 2":
                                    print("Card 2 clicked")
                                    selected_card = "card 2"
                                    can_click_player_cards = True

                    # Player card interaction
                    if can_click_player_cards:
                        for rect, player, card_index in card_buttons:
                            if rect.collidepoint((mx, my)):
                                print([player, card_index])
                                player_done = True
                                break

        # Turn ends
        if player_done:
            player_no = (player_no + 1) % 4
            if player_no == 0:
                turn_no += 1

            # Reset per-turn state
            drew_from_deck = False
            selected_card = None
            can_click_player_cards = False
            player_done = False

        pygame.display.flip()
        clock.tick(60)


# --- Entry Point ---
if __name__ == "__main__":
    main()
