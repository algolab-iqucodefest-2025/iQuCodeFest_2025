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



# --- Main Game Loop ---
def main():
    show_states = True  # Show states at start

    while True:
        draw_table_with_states(players, show_states)
        if not show_states:
            draw_center_elements()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    show_states = False  # Hide states after ENTER

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not show_states:  # ✅ Only active after ENTER
                    mx, my = pygame.mouse.get_pos()

                    # Check player cards
                    for rect, player, card_index in card_buttons:
                        if rect.collidepoint((mx, my)):
                            print([player, card_index])

                    # Check center elements
                    for rect, label in center_buttons:
                        if rect.collidepoint((mx, my)):
                            print(label)

        pygame.display.flip()
        clock.tick(60)

# --- Entry Point ---
if __name__ == "__main__":
    main()
